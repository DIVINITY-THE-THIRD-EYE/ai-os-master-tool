from dataclasses import dataclass


@dataclass
class PersistenceConfig:
    memory_cache: bool = True
    flush_mode: str = "workflow_end"
    checkpoint_mode: str = "write_count"
    checkpoint_interval: int = 100
    backup_retention: int = 20
    optimize_after_flush: bool = True
    integrity_check: str = "startup"
    journal_enabled: bool = True
    snapshots_enabled: bool = True
    metrics_enabled: bool = True
    event_bus_enabled: bool = True
