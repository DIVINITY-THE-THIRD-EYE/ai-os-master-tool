import datetime
import logging
import os
import shutil

logger = logging.getLogger(__name__)


class BackupManager:
    """Manages rolling backups, retention policies, and restoration."""

    def __init__(self, db_path: str, backups_dir: str, retention_count: int = 20):
        self.db_path = db_path
        self.backups_dir = backups_dir
        self.retention_count = retention_count
        os.makedirs(self.backups_dir, exist_ok=True)

    def create_backup(self) -> str:
        if not os.path.exists(self.db_path):
            return ""

        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_path = os.path.join(self.backups_dir, f"{timestamp_str}.db")
        shutil.copy2(self.db_path, backup_path)

        self.prune_old_backups()
        return backup_path

    def prune_old_backups(self):
        backups = sorted([f for f in os.listdir(self.backups_dir) if f.endswith(".db")])
        if len(backups) > self.retention_count:
            for old_backup in backups[: -self.retention_count]:
                try:
                    os.remove(os.path.join(self.backups_dir, old_backup))
                except OSError:
                    pass
