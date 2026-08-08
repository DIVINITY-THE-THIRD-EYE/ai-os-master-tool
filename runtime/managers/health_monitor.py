import logging
import os
import sqlite3
import time
from typing import Any, Dict

logger = logging.getLogger("ai_os.health_monitor")


class HealthMonitor:
    """Monitors the health of the AI OS persistence subsystem."""

    def __init__(self, db_path: str, backups_dir: str):
        self.db_path = db_path
        self.backups_dir = backups_dir

    def get_health_status(self, state_manager: Any = None) -> Dict[str, Any]:
        """Runs diagnostics and returns health status."""
        status = {
            "database_integrity": "UNKNOWN",
            "journal_status": "OK",
            "backup_age_seconds": -1,
            "backup_count": 0,
            "snapshot_count": 0,
            "db_size_bytes": 0,
            "vram_size_bytes": 0,
            "status": "HEALTHY",
        }

        # Check DB
        if os.path.exists(self.db_path):
            status["db_size_bytes"] = os.path.getsize(self.db_path)
            try:
                conn = sqlite3.connect(self.db_path)
                res = conn.execute("PRAGMA integrity_check").fetchone()
                status["database_integrity"] = "PASS" if (res and res[0].lower() == "ok") else "FAIL"
                conn.close()
            except sqlite3.Error as e:
                logger.error(f"Database integrity check failed with SQLite error: {e}")
                status["database_integrity"] = "ERROR"
                status["status"] = "UNHEALTHY"

            if status["database_integrity"] not in ["PASS", "UNKNOWN"]:
                status["status"] = "UNHEALTHY"

        # Check Backups
        if os.path.exists(self.backups_dir):
            backups = sorted([f for f in os.listdir(self.backups_dir) if f.endswith(".db")])
            status["backup_count"] = len(backups)
            if backups:
                latest_backup = os.path.join(self.backups_dir, backups[-1])
                status["backup_age_seconds"] = time.time() - os.path.getmtime(latest_backup)
                if status["backup_age_seconds"] > 86400:  # 24 hours
                    if status["status"] == "HEALTHY":
                        status["status"] = "DEGRADED"

        # Add VRAM metrics if available
        if state_manager and getattr(state_manager, "_vram_conn", None):
            try:
                vram_pages = state_manager._vram_conn.execute("PRAGMA page_count").fetchone()[0]
                page_size = state_manager._vram_conn.execute("PRAGMA page_size").fetchone()[0]
                status["vram_size_bytes"] = vram_pages * page_size
            except sqlite3.Error as e:
                logger.warning(f"Failed to fetch VRAM metrics from SQLite: {e}")

        return status
