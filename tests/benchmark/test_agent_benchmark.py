"""
Phase 5 — Agent Complexity Benchmark Suite.
Benchmarks identical task workloads across Mode A (1-Agent), Mode B (3-Agent), Mode C (5-Agent), and Mode D (13-Agent AI OS).
"""

import time
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.workflow_executor import WorkflowExecutor, WorkflowStep
from runtime.agent_registry import AgentRegistry, AgentRecord

class TestAgentBenchmark:
    def _create_registry(self, num_agents: int) -> AgentRegistry:
        registry = AgentRegistry()
        for i in range(num_agents):
            agent_id = f"A{i:02d}"
            agent = AgentRecord(
                agent_id=agent_id,
                name=f"Agent {i}",
                version="1.0.0",
                capabilities=[f"cap_{i}"],
                skills=[],
                tools=[],
                permissions=[]
            )
            registry.register(agent)
            registry.configure(agent_id)
            registry.mark_ready(agent_id)
        return registry

    def _run_mode(self, mode_name: str, num_agents: int):
        registry = self._create_registry(num_agents)
        steps = [
            WorkflowStep(f"S{i}", f"Step {i}", f"A{i % num_agents:02d}", depends_on=[f"S{i-1}"] if i > 0 else [])
            for i in range(10)
        ]
        
        start_time = time.perf_counter()
        
        executor = WorkflowExecutor(step_executor=lambda step: {"status": "ok", "cost_usd": 0.001, "tokens": 150})
        result = executor.execute(f"wf-{mode_name}", "task-bench", "trace-bench", steps)
        
        elapsed = round((time.perf_counter() - start_time) * 1000, 3)
        return {
            "mode": mode_name,
            "num_agents": num_agents,
            "latency_ms": elapsed,
            "steps_completed": result.steps_completed,
            "status": result.status
        }

    def test_benchmark_comparison(self):
        mode_a = self._run_mode("Mode A (1-Agent)", 1)
        mode_b = self._run_mode("Mode B (3-Agent)", 3)
        mode_c = self._run_mode("Mode C (5-Agent)", 5)
        mode_d = self._run_mode("Mode D (13-Agent AI OS)", 13)

        assert mode_a["status"] == "completed"
        assert mode_b["status"] == "completed"
        assert mode_c["status"] == "completed"
        assert mode_d["status"] == "completed"

        assert mode_a["steps_completed"] == 10
        assert mode_b["steps_completed"] == 10
        assert mode_c["steps_completed"] == 10
        assert mode_d["steps_completed"] == 10
