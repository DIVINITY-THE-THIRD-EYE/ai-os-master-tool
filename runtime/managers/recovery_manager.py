import logging
import os
import shutil
import sqlite3
import time

logger = logging.getLogger(__name__)


class RecoveryManager:
    """Handles startup self-healing and disaster recovery."""

    def __init__(self, db_path: str, backups_dir: str):
        self.db_path = db_path
        self.backups_dir = backups_dir

    def heal(self) -> bool:
        """Validates DB integrity and restores from backup if necessary. Returns True if DB is ready."""
        if not os.path.exists(self.db_path):
            return True  # Let StateManager initialize it

        try:
            conn = sqlite3.connect(self.db_path)
            result = conn.execute("PRAGMA integrity_check").fetchone()
            conn.close()

            if result and result[0].lower() != "ok":
                logger.warning(f"Database corruption detected: {result[0]}. Attempting self-healing...")
                return self._restore_from_backup()
            return True
        except sqlite3.DatabaseError as e:
            logger.warning(f"Database corruption detected ({e}). Attempting self-healing...")
            return self._restore_from_backup()

    def _restore_from_backup(self) -> bool:
        corrupted_path = self.db_path + f".corrupted_{int(time.time())}"
        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, corrupted_path)

        backups = sorted([f for f in os.listdir(self.backups_dir) if f.endswith(".db")])
        if not backups:
            logger.error("No backups available for self-healing! Database may be permanently corrupted.")
            return False

        latest_backup = os.path.join(self.backups_dir, backups[-1])
        logger.info(f"Restoring from backup: {latest_backup}")
        shutil.copy2(latest_backup, self.db_path)
        logger.info("Self-healing complete.")
        return True
