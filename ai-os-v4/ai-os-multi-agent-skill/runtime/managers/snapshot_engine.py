import os
import shutil
import time
from typing import Any


class SnapshotEngine:
    """Manages explicit VRAM snapshots."""

    def __init__(self, snapshots_dir: str, state_manager: Any):
        self.snapshots_dir = snapshots_dir
        self.state_manager = state_manager
        os.makedirs(self.snapshots_dir, exist_ok=True)

    def create_snapshot(self, name: str, description: str = "") -> str:
        """Creates a snapshot of the current VRAM image."""
        snapshot_id = f"snap_{int(time.time())}"
        path = os.path.join(self.snapshots_dir, f"{snapshot_id}.db")

        # Flush VRAM to physical disk first to ensure snapshot is up to date
        if hasattr(self.state_manager, "flush_image_to_disk"):
            self.state_manager.flush_image_to_disk()

        # Copy the physical db to the snapshot dir
        if os.path.exists(self.state_manager.db_path):
            shutil.copy2(self.state_manager.db_path, path)

        return snapshot_id
