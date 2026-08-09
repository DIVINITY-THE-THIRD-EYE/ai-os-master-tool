"""
AIOS Core AgentRuntime Interface.
Abstract base class and core contracts that all agents (A00-A13) implement.
"""

from abc import ABC, abstractmethod
from typing import Set, Dict, Any, Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    task_id: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    requester_id: Optional[str] = None


class Result(BaseModel):
    task_id: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StateSnapshot(BaseModel):
    agent_id: str
    snapshot_id: str
    state_data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float


class AgentRuntime(ABC):
    """
    Abstract Base Class for all AIOS Canonical and Ephemeral Agent Runtimes.
    Must be implemented by agents A00-A13.
    """
    agent_id: str
    capabilities: Set[str]

    @abstractmethod
    async def execute(self, task: Task) -> Result:
        """Executes a task asynchronously."""
        pass

    @abstractmethod
    async def checkpoint(self) -> StateSnapshot:
        """Captures an atomic durable state snapshot of the agent."""
        pass

    @abstractmethod
    async def recover(self, snapshot: StateSnapshot) -> None:
        """Restores the agent state from a durable state snapshot."""
        pass
