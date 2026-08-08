import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class SystemEvent:
    """Legacy base class for system events (keep for compatibility)."""

    timestamp: float = field(default_factory=time.time)
    workflow_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PersistenceEvent:
    """V2.0 Universal Persistence Event Base Class."""

    timestamp: float = field(default_factory=time.time)
    workflow_id: Optional[str] = None
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    image_version: int = 0
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)


# -- Database Load Events --
@dataclass
class DatabaseLoadedEvent(PersistenceEvent):
    pass


# -- Flush Pipeline Events --
@dataclass
class BeforeFlushEvent(PersistenceEvent):
    pass


@dataclass
class FlushStartedEvent(PersistenceEvent):
    pass


@dataclass
class FlushCompletedEvent(PersistenceEvent):
    duration_ms: float = 0.0
    rows_changed: int = 0


@dataclass
class FlushFailedEvent(PersistenceEvent):
    error: str = ""


@dataclass
class FlushSkippedEvent(PersistenceEvent):
    reason: str = "clean"


# -- Backup Pipeline Events --
@dataclass
class BeforeBackupEvent(PersistenceEvent):
    pass


@dataclass
class BackupStartedEvent(PersistenceEvent):
    pass


@dataclass
class BackupCompletedEvent(PersistenceEvent):
    backup_path: str = ""


@dataclass
class BackupFailedEvent(PersistenceEvent):
    error: str = ""


# -- Snapshot Pipeline Events --
@dataclass
class SnapshotCreatedEvent(PersistenceEvent):
    snapshot_id: str = ""


# -- Journal Events --
@dataclass
class JournalCommittedEvent(PersistenceEvent):
    sequence_no: int = 0


# -- Recovery Events --
@dataclass
class RecoveryStartedEvent(PersistenceEvent):
    reason: str = ""


@dataclass
class RecoveryCompletedEvent(PersistenceEvent):
    success: bool = True


@dataclass
class IntegrityCheckFailedEvent(PersistenceEvent):
    error_message: str = ""


# -- Workflow Event --
@dataclass
class WorkflowPersistedEvent(PersistenceEvent):
    workflow_id: str = ""
