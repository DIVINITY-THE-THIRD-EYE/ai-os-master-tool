"""
Unit tests for agents/core/runtime.py AgentRuntime interface.
"""

import time
import pytest
from typing import Set
from agents.core.runtime import AgentRuntime, Task, Result, StateSnapshot


class DummyAgent(AgentRuntime):
    def __init__(self, agent_id: str, capabilities: Set[str]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.internal_state = {"executed_count": 0}

    async def execute(self, task: Task) -> Result:
        self.internal_state["executed_count"] += 1
        return Result(
            task_id=task.task_id,
            success=True,
            output=f"Executed {task.action} with params {task.parameters}"
        )

    async def checkpoint(self) -> StateSnapshot:
        return StateSnapshot(
            agent_id=self.agent_id,
            snapshot_id=f"SNAP-{self.internal_state['executed_count']}",
            state_data=dict(self.internal_state),
            timestamp=time.time()
        )

    async def recover(self, snapshot: StateSnapshot) -> None:
        self.internal_state = dict(snapshot.state_data)


@pytest.mark.anyio
async def test_agent_runtime_lifecycle():
    agent = DummyAgent(agent_id="A06", capabilities={"task_execution", "file_read"})
    assert agent.agent_id == "A06"
    assert "task_execution" in agent.capabilities

    # 1. Execute task
    task = Task(task_id="T100", action="run_analysis", parameters={"depth": "high"})
    res = await agent.execute(task)
    assert res.success is True
    assert res.task_id == "T100"
    assert agent.internal_state["executed_count"] == 1

    # 2. Checkpoint
    snap = await agent.checkpoint()
    assert snap.agent_id == "A06"
    assert snap.snapshot_id == "SNAP-1"
    assert snap.state_data["executed_count"] == 1

    # 3. Modify state and recover
    agent.internal_state["executed_count"] = 999
    await agent.recover(snap)
    assert agent.internal_state["executed_count"] == 1
