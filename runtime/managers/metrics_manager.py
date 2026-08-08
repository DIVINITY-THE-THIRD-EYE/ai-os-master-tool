import threading
import time
from typing import Any, Dict


class MetricsCollector:
    """Collects runtime telemetry for the AI OS persistence subsystem."""

    def __init__(self):
        self._metrics = {
            "total_reads": 0,
            "total_writes": 0,
            "flush_count": 0,
            "flush_failures": 0,
            "average_flush_ms": 0.0,
            "backup_count": 0,
            "restore_count": 0,
            "checkpoint_count": 0,
            "journal_entries": 0,
            "snapshot_count": 0,
            "db_size": 0,
            "vram_size": 0,
            "memory_usage": 0,
            "cpu_usage": 0,
            "uptime_seconds": 0,
        }
        self._lock = threading.RLock()
        self._start_time = time.time()

    def record_flush(self, duration_ms: float, success: bool = True):
        with self._lock:
            self._metrics["flush_count"] += 1
            if not success:
                self._metrics["flush_failures"] += 1

            # Running average
            n = self._metrics["flush_count"]
            old_avg = self._metrics["average_flush_ms"]
            self._metrics["average_flush_ms"] = old_avg + (duration_ms - old_avg) / n

    def increment(self, metric_name: str, amount: int = 1):
        with self._lock:
            if metric_name in self._metrics:
                self._metrics[metric_name] += amount

    def set_gauge(self, metric_name: str, value: float):
        with self._lock:
            if metric_name in self._metrics:
                self._metrics[metric_name] = value

    def get_metrics(self) -> Dict[str, Any]:
        with self._lock:
            self._metrics["uptime_seconds"] = time.time() - self._start_time
            return dict(self._metrics)
