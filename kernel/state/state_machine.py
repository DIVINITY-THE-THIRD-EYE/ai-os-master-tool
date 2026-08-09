"""
AIOS Kernel State Machines — Typed Pydantic state machines for Task Lifecycle and Artifact Lifecycle.
Enforces deterministic state transition matrices and recovery state routing.
"""

from enum import Enum
from typing import Set, Dict, Optional
from pydantic import BaseModel, Field


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class TaskState(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    BLOCKED = "blocked"
    VERIFYING = "verifying"
    CONDITIONALLY_APPROVED = "conditionally_approved"
    CONDITION_REMEDIATION = "condition_remediation"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    ROLLED_BACK = "rolled_back"


class ArtifactState(str, Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    APPROVED = "approved"
    RELEASED = "released"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


# Deterministic Task Lifecycle Transition Table
TASK_TRANSITIONS: Dict[TaskState, Set[TaskState]] = {
    TaskState.CREATED: {TaskState.QUEUED, TaskState.CANCELLED},
    TaskState.QUEUED: {TaskState.RUNNING, TaskState.CANCELLED, TaskState.TIMEOUT},
    TaskState.RUNNING: {TaskState.BLOCKED, TaskState.VERIFYING, TaskState.FAILED, TaskState.CANCELLED, TaskState.TIMEOUT, TaskState.ROLLED_BACK},
    TaskState.BLOCKED: {TaskState.RUNNING, TaskState.CANCELLED, TaskState.TIMEOUT, TaskState.FAILED},
    TaskState.VERIFYING: {TaskState.APPROVED, TaskState.CONDITIONALLY_APPROVED, TaskState.REJECTED, TaskState.FAILED},
    TaskState.CONDITIONALLY_APPROVED: {TaskState.CONDITION_REMEDIATION, TaskState.CANCELLED},  # CANNOT go directly to COMPLETED!
    TaskState.CONDITION_REMEDIATION: {TaskState.VERIFYING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.APPROVED: {TaskState.COMPLETED, TaskState.ROLLED_BACK},
    TaskState.REJECTED: {TaskState.CANCELLED, TaskState.ROLLED_BACK},
    TaskState.FAILED: {TaskState.ROLLED_BACK, TaskState.QUEUED},
    TaskState.COMPLETED: set(),
    TaskState.CANCELLED: set(),
    TaskState.TIMEOUT: {TaskState.QUEUED, TaskState.CANCELLED, TaskState.ROLLED_BACK},
    TaskState.ROLLED_BACK: {TaskState.QUEUED, TaskState.CANCELLED},
}


# Deterministic Artifact Lifecycle Transition Table
ARTIFACT_TRANSITIONS: Dict[ArtifactState, Set[ArtifactState]] = {
    ArtifactState.DRAFT: {ArtifactState.VALIDATED, ArtifactState.ARCHIVED},
    ArtifactState.VALIDATED: {ArtifactState.APPROVED, ArtifactState.DRAFT, ArtifactState.ARCHIVED},
    ArtifactState.APPROVED: {ArtifactState.RELEASED, ArtifactState.SUPERSEDED, ArtifactState.ARCHIVED},
    ArtifactState.RELEASED: {ArtifactState.SUPERSEDED, ArtifactState.ARCHIVED},
    ArtifactState.SUPERSEDED: {ArtifactState.ARCHIVED},
    ArtifactState.ARCHIVED: set(),
}


class TaskStateMachine(BaseModel):
    task_id: str
    current_state: TaskState = TaskState.CREATED
    history: list[TaskState] = Field(default_factory=lambda: [TaskState.CREATED])

    def transition_to(self, new_state: TaskState) -> None:
        allowed = TASK_TRANSITIONS.get(self.current_state, set())
        if new_state not in allowed:
            raise InvalidStateTransitionError(
                f"Invalid TaskState transition: Cannot transition task '{self.task_id}' from '{self.current_state.value}' to '{new_state.value}'."
            )
        self.current_state = new_state
        self.history.append(new_state)


class ArtifactStateMachine(BaseModel):
    artifact_id: str
    current_state: ArtifactState = ArtifactState.DRAFT
    history: list[ArtifactState] = Field(default_factory=lambda: [ArtifactState.DRAFT])

    def transition_to(self, new_state: ArtifactState) -> None:
        allowed = ARTIFACT_TRANSITIONS.get(self.current_state, set())
        if new_state not in allowed:
            raise InvalidStateTransitionError(
                f"Invalid ArtifactState transition: Cannot transition artifact '{self.artifact_id}' from '{self.current_state.value}' to '{new_state.value}'."
            )
        self.current_state = new_state
        self.history.append(new_state)
