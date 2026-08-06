import logging
import os
import sqlite3
import time
import uuid
from typing import Optional

from .config import PersistenceConfig
from .event_bus import EventBus
from .events import (
    BackupCompletedEvent,
    BackupFailedEvent,
    BackupStartedEvent,
    BeforeBackupEvent,
    BeforeFlushEvent,
    FlushCompletedEvent,
    FlushFailedEvent,
    FlushSkippedEvent,
    FlushStartedEvent,
    JournalCommittedEvent,
)
from .interfaces.backup import IBackupManager
from .interfaces.health import IHealthMonitor
from .interfaces.journal import IJournalManager
from .interfaces.metrics import IMetricsManager

logger = logging.getLogger("ai_os.persistence_coordinator")


class PersistenceCoordinator:
    """Stateless internal coordinator orchestrating the deterministic persistence pipeline."""

    def __init__(
        self, db_path: str, is_supabase: bool, enable_vram_image: bool, config: PersistenceConfig, event_bus: EventBus
    ):
        self.db_path = db_path
        self._is_supabase = is_supabase
        self.enable_vram_image = enable_vram_image
        self.config = config
        self.event_bus = event_bus

    def orchestrate_flush(
        self,
        vram_conn: Optional[sqlite3.Connection],
        current_image_version: int,
        is_dirty: bool,
        workflow_id: Optional[str],
        journal_manager: IJournalManager,
        backup_manager: IBackupManager,
        metrics: IMetricsManager,
        health_monitor: IHealthMonitor,
    ) -> int:
        """
        Executes the deterministic coordinator pipeline.
        Acquire Lock (assumed held by StateManager) -> Journal Begin (happened in log_operation) ->
        Backup Decision -> Checkpoint Decision -> Atomic Flush -> Optimize -> Journal Commit ->
        Metrics Update -> Health Update -> Publish Events -> Release Lock.
        """
        correlation_id = str(uuid.uuid4())

        if not is_dirty:
            if not self._is_supabase and self.enable_vram_image:
                self.event_bus.publish(
                    FlushSkippedEvent(correlation_id=correlation_id, reason="CLEAN_DATABASE", workflow_id=workflow_id)
                )
            return current_image_version

        if not self._is_supabase and self.enable_vram_image and vram_conn:
            self.event_bus.publish(
                BeforeFlushEvent(
                    correlation_id=correlation_id, image_version=current_image_version, workflow_id=workflow_id
                )
            )

            start_time = time.perf_counter()
            temp_db_path = f"{self.db_path}.tmp"

            try:
                rows_changed = vram_conn.total_changes
            except Exception:
                rows_changed = 0

            new_image_version = current_image_version + 1

            self.event_bus.publish(
                FlushStartedEvent(
                    correlation_id=correlation_id, image_version=new_image_version, workflow_id=workflow_id
                )
            )

            try:
                # VRAM update
                vram_conn.execute(
                    "INSERT OR REPLACE INTO system_metadata (key, value) VALUES (?, ?)",
                    ("image_version", str(new_image_version)),
                )
                vram_conn.commit()

                # Temp copy
                temp_conn = sqlite3.connect(temp_db_path)
                vram_conn.backup(temp_conn)
                temp_conn.close()

                # Backup Decision
                self.event_bus.publish(BeforeBackupEvent(correlation_id=correlation_id, workflow_id=workflow_id))
                self.event_bus.publish(BackupStartedEvent(correlation_id=correlation_id, workflow_id=workflow_id))
                try:
                    backup_path = backup_manager.create_backup()
                    if backup_path:
                        self.event_bus.publish(
                            BackupCompletedEvent(
                                correlation_id=correlation_id, backup_path=backup_path, workflow_id=workflow_id
                            )
                        )
                except Exception as e:
                    self.event_bus.publish(
                        BackupFailedEvent(correlation_id=correlation_id, error=str(e), workflow_id=workflow_id)
                    )

                # Atomic Flush
                if os.path.exists(temp_db_path):
                    for attempt in range(5):
                        try:
                            os.replace(temp_db_path, self.db_path)
                            break
                        except (PermissionError, OSError):
                            if attempt == 4:
                                raise
                            time.sleep(0.1 * (2**attempt))

                # Optimize
                if self.config.optimize_after_flush:
                    try:
                        maint_conn = sqlite3.connect(self.db_path)
                        maint_conn.execute("PRAGMA optimize;")
                        maint_conn.close()
                    except Exception as e:
                        logger.warning(f"Maintenance PRAGMA optimize failed: {e}")

                # Journal Commit
                seq = getattr(journal_manager, "_seq", 0)  # Safe fallback if protocol varies
                journal_manager.mark_committed(seq)
                self.event_bus.publish(
                    JournalCommittedEvent(correlation_id=correlation_id, sequence_no=seq, workflow_id=workflow_id)
                )

                # Metrics Update
                duration_ms = (time.perf_counter() - start_time) * 1000
                metrics.record_flush(duration_ms, success=True)

                # Health Update (implied, the next status() call queries it)

                # Publish Events
                self.event_bus.publish(
                    FlushCompletedEvent(
                        correlation_id=correlation_id,
                        image_version=new_image_version,
                        duration_ms=duration_ms,
                        rows_changed=rows_changed,
                        workflow_id=workflow_id,
                    )
                )

                return new_image_version

            except Exception as e:
                logger.error(f"Failed to flush VRAM image atomically: {e}")
                metrics.record_flush(0, success=False)
                self.event_bus.publish(
                    FlushFailedEvent(correlation_id=correlation_id, error=str(e), workflow_id=workflow_id)
                )
                if os.path.exists(temp_db_path):
                    try:
                        os.remove(temp_db_path)
                    except OSError:
                        pass
                raise

        return current_image_version
