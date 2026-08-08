import json
import sqlite3
import threading
import time
from typing import Any, Dict


class JournalManager:
    """Manages Write-Ahead Log (WAL) and Event Logging for the persistence layer."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._lock = threading.RLock()
        self._seq = 0
        self._memory_conn = sqlite3.connect(":memory:", check_same_thread=False) if db_path == ":memory:" else None
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._memory_conn:
            return self._memory_conn
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._lock:
            # Connect to physical db to init journal if it doesn't exist
            conn = self._get_conn()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sequence_no INTEGER NOT NULL,
                    timestamp REAL NOT NULL,
                    workflow_id TEXT,
                    transaction_id TEXT,
                    operation TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT,
                    payload_json TEXT NOT NULL,
                    checksum TEXT,
                    status TEXT NOT NULL
                )
            """)
            conn.commit()

            # Load max seq
            res = conn.execute("SELECT MAX(sequence_no) FROM journal_entries").fetchone()
            if res and res[0] is not None:
                self._seq = res[0]
            if not self._memory_conn:
                conn.close()

    def log_operation(
        self, operation: str, entity_type: str, entity_id: str, payload: Dict[str, Any], workflow_id: str = None
    ) -> int:
        with self._lock:
            self._seq += 1
            # Connect and fsync journal
            conn = self._get_conn()
            conn.execute(
                """
                INSERT INTO journal_entries (sequence_no, timestamp, workflow_id, operation, entity_type, entity_id, payload_json, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self._seq,
                    time.time(),
                    workflow_id,
                    operation,
                    entity_type,
                    entity_id,
                    json.dumps(payload),
                    "PENDING",
                ),
            )
            conn.commit()
            if not self._memory_conn:
                conn.close()
            return self._seq

    def mark_committed(self, sequence_no_up_to: int):
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                "UPDATE journal_entries SET status = 'COMMITTED' WHERE sequence_no <= ? AND status = 'PENDING'",
                (sequence_no_up_to,),
            )
            conn.commit()
            if not self._memory_conn:
                conn.close()
