"""
AI OS State Manager — system state persistence and recovery service.
Acts as a Facade orchestrating injected enterprise managers behind a strict API.
"""

import json
import logging
import sqlite3
import threading
import time
from typing import Any, Dict, List, Optional

from .event_bus import EventBus
from .interfaces.backup import IBackupManager
from .interfaces.checkpoint import ICheckpointManager
from .interfaces.coordinator import IPersistenceCoordinator
from .interfaces.health import IHealthMonitor
from .interfaces.journal import IJournalManager
from .interfaces.metrics import IMetricsManager
from .interfaces.recovery import IRecoveryManager
from .interfaces.snapshot import ISnapshotEngine

logger = logging.getLogger("ai_os.state_manager")


class StateManager:
    """
    ACID-compliant State Manager Façade.
    Exposes a constrained, high-level API while delegating orchestration to the PersistenceCoordinator.
    """

    def __init__(
        self,
        db_path: str,
        is_supabase: bool,
        enable_vram_image: bool,
        persistence_coordinator: IPersistenceCoordinator,
        checkpoint_manager: ICheckpointManager,
        journal_manager: IJournalManager,
        metrics: IMetricsManager,
        health_monitor: IHealthMonitor,
        snapshot_engine: ISnapshotEngine,
        backup_manager: IBackupManager,
        recovery_manager: IRecoveryManager,
        event_bus: EventBus,
    ):

        self.db_path = db_path
        self._is_supabase = is_supabase
        self.enable_vram_image = enable_vram_image
        self._is_memory = (self.db_path == ":memory:") and not self._is_supabase

        self.coordinator = persistence_coordinator
        self.checkpoint_manager = checkpoint_manager
        self.journal_manager = journal_manager
        self.metrics = metrics
        self.health_monitor = health_monitor
        self.snapshot_engine = snapshot_engine
        self.backup_manager = backup_manager
        self.recovery_manager = recovery_manager
        self.event_bus = event_bus

        self._disk_conn = None
        self._vram_conn = None
        self._is_dirty = False
        self._image_version = 0
        self._db_lock = threading.RLock()

        self.initialize()

    def initialize(self) -> None:
        """Initialize database connections and recover state if needed."""
        if not self._is_supabase:
            # Automatic startup self-healing
            if not self._is_memory and not self.recovery_manager.heal():
                logger.error("Startup self-healing failed. Proceeding with risk.")

            if self._is_memory:
                self._vram_conn = sqlite3.connect(":memory:", check_same_thread=False)
                self._vram_conn.row_factory = sqlite3.Row
            else:
                self._disk_conn = sqlite3.connect(self.db_path, check_same_thread=False)
                self._disk_conn.row_factory = sqlite3.Row
                if self.enable_vram_image:
                    self._vram_conn = sqlite3.connect(":memory:", check_same_thread=False)
                    self._vram_conn.row_factory = sqlite3.Row
                    self._disk_conn.backup(self._vram_conn)

        self._init_db()

        with self._get_connection() as conn:
            row = conn.execute("SELECT value FROM system_metadata WHERE key = 'image_version'").fetchone()
            if row:
                self._image_version = int(row["value"])

    def shutdown(self) -> None:
        """Gracefully shutdown and flush all state."""
        self.flush()
        if self._vram_conn:
            self._vram_conn.close()
        if self._disk_conn:
            self._disk_conn.close()

    def _get_connection(self) -> Any:
        if self._vram_conn and self.enable_vram_image:
            return self._vram_conn
        if self._disk_conn:
            return self._disk_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS agents (agent_id TEXT PRIMARY KEY, name TEXT NOT NULL, version TEXT NOT NULL, status TEXT NOT NULL, capabilities TEXT NOT NULL, record_json TEXT NOT NULL, updated_at REAL NOT NULL)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS workflows (workflow_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, trace_id TEXT NOT NULL, status TEXT NOT NULL, steps_completed INTEGER NOT NULL, steps_failed INTEGER NOT NULL, result_json TEXT NOT NULL, updated_at REAL NOT NULL)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS checkpoints (workflow_id TEXT NOT NULL, step_id TEXT NOT NULL, output_json TEXT NOT NULL, created_at REAL NOT NULL, PRIMARY KEY (workflow_id, step_id))"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, agent_id TEXT NOT NULL, task_id TEXT NOT NULL, payload_json TEXT NOT NULL, created_at REAL NOT NULL)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS knowledge_nodes (node_id TEXT PRIMARY KEY, label TEXT NOT NULL, node_type TEXT NOT NULL, attributes_json TEXT NOT NULL, updated_at REAL NOT NULL)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS knowledge_edges (id INTEGER PRIMARY KEY AUTOINCREMENT, source_id TEXT NOT NULL, target_id TEXT NOT NULL, relation TEXT NOT NULL, weight REAL NOT NULL, created_at REAL NOT NULL, UNIQUE(source_id, target_id, relation))"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS experiences (id INTEGER PRIMARY KEY AUTOINCREMENT, task_type TEXT NOT NULL, outcome TEXT NOT NULL, lesson TEXT NOT NULL, metadata_json TEXT NOT NULL, recorded_at REAL NOT NULL)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS persistent_memory (memory_key TEXT PRIMARY KEY, value_json TEXT NOT NULL, tags_json TEXT NOT NULL, updated_at REAL NOT NULL)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS vram_sync_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, operation TEXT NOT NULL, details TEXT NOT NULL, timestamp REAL NOT NULL, image_version INTEGER, duration_ms REAL, db_size_bytes INTEGER, status TEXT)"
            )
            cursor.execute("CREATE TABLE IF NOT EXISTS system_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            conn.commit()

    def flush(self, workflow_id: Optional[str] = None) -> None:
        """Delegate flush orchestration to PersistenceCoordinator."""
        with self._db_lock:
            self._image_version = self.coordinator.orchestrate_flush(
                vram_conn=self._vram_conn,
                current_image_version=self._image_version,
                is_dirty=self._is_dirty,
                workflow_id=workflow_id,
                journal_manager=self.journal_manager,
                backup_manager=self.backup_manager,
                metrics=self.metrics,
                health_monitor=self.health_monitor,
            )
            self._is_dirty = False

    def status(self) -> Dict[str, Any]:
        """Diagnostic API returning full internal telemetry state."""
        status = self.health_monitor.get_health_status(self)
        status["image_version"] = self._image_version
        status["is_dirty"] = self._is_dirty
        status.update(self.metrics.get_metrics())
        return status

    def _mark_dirty(self, workflow_id: Optional[str] = None):
        self._is_dirty = True
        self.metrics.increment("total_writes")
        self.checkpoint_manager.record_write()
        if self.checkpoint_manager.should_checkpoint():
            self.flush(workflow_id)
            self.checkpoint_manager.record_checkpoint()

    def transaction(
        self,
        operation: str,
        table: str,
        entity_id: str,
        payload: dict,
        workflow_id: Optional[str] = None,
        sql: str = "",
        params: tuple = (),
    ) -> None:
        """Universal write method for simple UPSERTs to consolidate duplication."""
        with self._db_lock:
            self.journal_manager.log_operation(operation, table, entity_id, payload, workflow_id)
            with self._get_connection() as conn:
                conn.execute(sql, params)
                conn.commit()
            self._mark_dirty(workflow_id)

    # ---------------------------------------------------------------------------
    # Public API mapped to legacy signatures for backwards compatibility
    # ---------------------------------------------------------------------------

    def save_agent(
        self, agent_id: str, name: str, version: str, status: str, capabilities: List[str], record_json: dict
    ) -> None:
        payload = {
            "name": name,
            "version": version,
            "status": status,
            "capabilities": capabilities,
            "record_json": record_json,
        }
        sql = "INSERT INTO agents (agent_id, name, version, status, capabilities, record_json, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(agent_id) DO UPDATE SET name=excluded.name, version=excluded.version, status=excluded.status, capabilities=excluded.capabilities, record_json=excluded.record_json, updated_at=excluded.updated_at"
        params = (agent_id, name, version, status, json.dumps(capabilities), json.dumps(record_json), time.time())
        self.transaction("UPSERT", "agents", agent_id, payload, sql=sql, params=params)

    def get_agent(self, agent_id: str) -> Optional[dict]:
        self.metrics.increment("total_reads")
        with self._get_connection() as conn:
            row = conn.execute("SELECT record_json FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()
            if row:
                return json.loads(row["record_json"])
        return None

    def list_agents(self) -> List[dict]:
        self.metrics.increment("total_reads")
        with self._get_connection() as conn:
            rows = conn.execute("SELECT record_json FROM agents").fetchall()
            return [json.loads(r["record_json"]) for r in rows]

    def save_workflow(
        self,
        workflow_id: str,
        task_id: str,
        trace_id: str,
        status: str,
        steps_completed: int,
        steps_failed: int,
        result_json: dict,
    ) -> None:
        payload = {
            "task_id": task_id,
            "trace_id": trace_id,
            "status": status,
            "steps_completed": steps_completed,
            "steps_failed": steps_failed,
            "result_json": result_json,
        }
        sql = "INSERT INTO workflows (workflow_id, task_id, trace_id, status, steps_completed, steps_failed, result_json, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(workflow_id) DO UPDATE SET status=excluded.status, steps_completed=excluded.steps_completed, steps_failed=excluded.steps_failed, result_json=excluded.result_json, updated_at=excluded.updated_at"
        params = (
            workflow_id,
            task_id,
            trace_id,
            status,
            steps_completed,
            steps_failed,
            json.dumps(result_json),
            time.time(),
        )
        self.transaction("UPSERT", "workflows", workflow_id, payload, workflow_id, sql, params)

    def save_checkpoint(self, workflow_id: str, step_id: str, output: dict) -> None:
        payload = {"step_id": step_id, "output": output}
        sql = "INSERT INTO checkpoints (workflow_id, step_id, output_json, created_at) VALUES (?, ?, ?, ?) ON CONFLICT(workflow_id, step_id) DO UPDATE SET output_json=excluded.output_json, created_at=excluded.created_at"
        params = (workflow_id, step_id, json.dumps(output), time.time())
        self.transaction("UPSERT", "checkpoints", f"{workflow_id}_{step_id}", payload, workflow_id, sql, params)

    def get_checkpoints(self, workflow_id: str) -> Dict[str, dict]:
        self.metrics.increment("total_reads")
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT step_id, output_json FROM checkpoints WHERE workflow_id = ?", (workflow_id,)
            ).fetchall()
            return {r["step_id"]: json.loads(r["output_json"]) for r in rows}

    def save_event(self, event_id: str, event_type: str, agent_id: str, task_id: str, payload: dict) -> None:
        log_payload = {"event_type": event_type, "agent_id": agent_id, "task_id": task_id, "payload": payload}
        sql = "INSERT INTO events (event_id, event_type, agent_id, task_id, payload_json, created_at) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(event_id) DO NOTHING"
        params = (event_id, event_type, agent_id, task_id, json.dumps(payload), time.time())
        self.transaction("INSERT", "events", event_id, log_payload, sql=sql, params=params)

    def query_events(self, topic: Optional[str] = None, task_id: Optional[str] = None) -> List[dict]:
        self.metrics.increment("total_reads")
        query = "SELECT event_id, event_type, agent_id, task_id, payload_json, created_at FROM events WHERE 1=1"
        params = []
        if topic:
            query += " AND event_type = ?"
            params.append(topic)
        if task_id:
            query += " AND task_id = ?"
            params.append(task_id)
        query += " ORDER BY created_at ASC"

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                {
                    "event_id": r["event_id"],
                    "event_type": r["event_type"],
                    "agent_id": r["agent_id"],
                    "task_id": r["task_id"],
                    "payload": json.loads(r["payload_json"]),
                    "created_at": r["created_at"],
                }
                for r in rows
            ]

    def save_knowledge_node(self, node_id: str, label: str, node_type: str, attributes: dict) -> None:
        payload = {"label": label, "node_type": node_type, "attributes": attributes}
        sql = "INSERT INTO knowledge_nodes (node_id, label, node_type, attributes_json, updated_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT(node_id) DO UPDATE SET label=excluded.label, node_type=excluded.node_type, attributes_json=excluded.attributes_json, updated_at=excluded.updated_at"
        params = (node_id, label, node_type, json.dumps(attributes), time.time())
        self.transaction("UPSERT", "knowledge_nodes", node_id, payload, sql=sql, params=params)

    def save_knowledge_edge(self, source_id: str, target_id: str, relation: str, weight: float) -> None:
        payload = {"source_id": source_id, "target_id": target_id, "relation": relation, "weight": weight}
        sql = "INSERT INTO knowledge_edges (source_id, target_id, relation, weight, created_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT(source_id, target_id, relation) DO UPDATE SET weight=excluded.weight"
        params = (source_id, target_id, relation, weight, time.time())
        self.transaction(
            "UPSERT", "knowledge_edges", f"{source_id}_{target_id}_{relation}", payload, sql=sql, params=params
        )

    def get_related_nodes(self, node_id: str, relation: Optional[str] = None) -> List[dict]:
        self.metrics.increment("total_reads")
        query = "SELECT n.node_id, n.label, n.node_type, n.attributes_json FROM knowledge_nodes n JOIN knowledge_edges e ON n.node_id = e.target_id WHERE e.source_id = ?"
        params = [node_id]
        if relation:
            query += " AND e.relation = ?"
            params.append(relation)

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                {
                    "node_id": r["node_id"],
                    "label": r["label"],
                    "node_type": r["node_type"],
                    "attributes": json.loads(r["attributes_json"]),
                }
                for r in rows
            ]

    def save_experience(self, task_type: str, outcome: str, lesson: str, metadata: dict) -> None:
        payload = {"task_type": task_type, "outcome": outcome, "lesson": lesson, "metadata": metadata}
        sql = "INSERT INTO experiences (task_type, outcome, lesson, metadata_json, recorded_at) VALUES (?, ?, ?, ?, ?)"
        params = (task_type, outcome, lesson, json.dumps(metadata), time.time())
        self.transaction("INSERT", "experiences", task_type, payload, sql=sql, params=params)

    def get_experiences(self, task_type: Optional[str] = None) -> List[dict]:
        self.metrics.increment("total_reads")
        query = "SELECT task_type, outcome, lesson, metadata_json, recorded_at FROM experiences WHERE 1=1"
        params = []
        if task_type:
            query += " AND task_type = ?"
            params.append(task_type)

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                {
                    "task_type": r["task_type"],
                    "outcome": r["outcome"],
                    "lesson": r["lesson"],
                    "metadata": json.loads(r["metadata_json"]),
                    "recorded_at": r["recorded_at"],
                }
                for r in rows
            ]

    def save_persistent_memory(self, key: str, value: Any, tags: List[str]) -> None:
        payload = {"value": value, "tags": tags}
        sql = "INSERT INTO persistent_memory (memory_key, value_json, tags_json, updated_at) VALUES (?, ?, ?, ?) ON CONFLICT(memory_key) DO UPDATE SET value_json=excluded.value_json, tags_json=excluded.tags_json, updated_at=excluded.updated_at"
        params = (key, json.dumps(value), json.dumps(tags), time.time())
        self.transaction("UPSERT", "persistent_memory", key, payload, sql=sql, params=params)

    def get_persistent_memory(self, key: str) -> Optional[dict]:
        self.metrics.increment("total_reads")
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT value_json, tags_json FROM persistent_memory WHERE memory_key = ?", (key,)
            ).fetchone()
            if row:
                return {"value": json.loads(row["value_json"]), "tags": json.loads(row["tags_json"])}
            return None

    def list_persistent_memory(self) -> Dict[str, dict]:
        self.metrics.increment("total_reads")
        with self._get_connection() as conn:
            rows = conn.execute("SELECT memory_key, value_json, tags_json FROM persistent_memory").fetchall()
            return {
                r["memory_key"]: {"value": json.loads(r["value_json"]), "tags": json.loads(r["tags_json"])}
                for r in rows
            }

    def snapshot(self) -> Dict[str, Any]:
        """Expose explicit snapshot generation."""
        self.metrics.increment("total_reads")
        # In a real app this would use snapshot_engine.create_snapshot()
        # but for compatibility returning raw dict for now.
        with self._get_connection() as conn:
            agents = [dict(r) for r in conn.execute("SELECT * FROM agents").fetchall()]
            workflows = [dict(r) for r in conn.execute("SELECT * FROM workflows").fetchall()]
            checkpoints = [dict(r) for r in conn.execute("SELECT * FROM checkpoints").fetchall()]
            events = [dict(r) for r in conn.execute("SELECT * FROM events").fetchall()]
            return {
                "snapshot_timestamp": time.time(),
                "agents": agents,
                "workflows": workflows,
                "checkpoints": checkpoints,
                "events": events,
            }
