import threading
import time


class CheckpointManager:
    """Manages configurable persistence checkpoint policies."""

    def __init__(self, mode: str = "workflow_end", interval: int = 100):
        self.mode = mode.lower()  # ram_only, workflow_end, time_based, write_count, hybrid
        self.interval = interval
        self._write_count = 0
        self._last_checkpoint_time = time.time()
        self._lock = threading.RLock()

    def should_checkpoint(self) -> bool:
        """Determines if a checkpoint should be triggered based on policy."""
        if self.mode == "ram_only":
            return False

        with self._lock:
            if self.mode == "write_count" or self.mode == "hybrid":
                if self._write_count >= self.interval:
                    return True

            if self.mode == "time_based" or self.mode == "hybrid":
                if (time.time() - self._last_checkpoint_time) >= self.interval:
                    return True

        return False

    def record_write(self):
        with self._lock:
            self._write_count += 1

    def record_checkpoint(self):
        with self._lock:
            self._write_count = 0
            self._last_checkpoint_time = time.time()
