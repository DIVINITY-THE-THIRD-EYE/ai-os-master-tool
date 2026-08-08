import os

from .config import PersistenceConfig
from .event_bus import EventBus
from .managers.backup_manager import BackupManager
from .managers.checkpoint_manager import CheckpointManager
from .managers.health_monitor import HealthMonitor
from .managers.journal_manager import JournalManager
from .managers.metrics_manager import MetricsCollector
from .managers.recovery_manager import RecoveryManager
from .managers.snapshot_engine import SnapshotEngine
from .persistence_coordinator import PersistenceCoordinator
from .state_manager import StateManager


def bootstrap_persistence(
    db_path: str = None, is_supabase: bool = False, enable_vram_image: bool = True, event_bus: EventBus = None
) -> StateManager:
    """Composition Root for Persistence subsystem."""
    if db_path is None:
        db_path = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "local_os_state.db"))

    if event_bus is None:
        event_bus = EventBus()

    backups_dir = os.path.join(os.path.dirname(db_path), "backups")
    snapshots_dir = os.path.join(os.path.dirname(db_path), "snapshots")

    config = PersistenceConfig()
    metrics = MetricsCollector()
    health = HealthMonitor(db_path, backups_dir)
    checkpoint = CheckpointManager(config.checkpoint_mode, config.checkpoint_interval)
    journal = JournalManager(db_path)
    backup = BackupManager(db_path, backups_dir, config.backup_retention)
    recovery = RecoveryManager(db_path, backups_dir)
    snapshot = SnapshotEngine(snapshots_dir, None)

    coordinator = PersistenceCoordinator(db_path, is_supabase, enable_vram_image, config, event_bus)

    state_manager = StateManager(
        db_path=db_path,
        is_supabase=is_supabase,
        enable_vram_image=enable_vram_image,
        persistence_coordinator=coordinator,
        checkpoint_manager=checkpoint,
        journal_manager=journal,
        metrics=metrics,
        health_monitor=health,
        snapshot_engine=snapshot,
        backup_manager=backup,
        recovery_manager=recovery,
        event_bus=event_bus,
    )

    snapshot.state_manager = state_manager

    return state_manager
