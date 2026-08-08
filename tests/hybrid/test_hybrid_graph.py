"""
Phase 6 — Hybrid Graph (DAG + Bounded Loops) Test Suite.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ai-os-v4", "ai-os-multi-agent-skill"))

from runtime.workflow_executor import WorkflowExecutor, WorkflowStep, StepStatus

class TestHybridGraphEngine:
    def test_bounded_loop_convergence(self):
        """Iterative loop converges within max_iterations limit."""
        iterations = {"count": 0}

        def mock_step_executor(step: WorkflowStep) -> dict:
            iterations["count"] += 1
            quality = 0.70 + (iterations["count"] * 0.10)
            return {"quality_score": quality}

        executor = WorkflowExecutor(step_executor=mock_step_executor)
        step = WorkflowStep(
            step_id="LOOP_STEP",
            name="Iterative Refinement Step",
            agent_id="A06",
            loop_until="quality_score >= 0.85",
            max_iterations=5
        )

        result = executor.execute("wf-loop", "task-loop", "trace-loop", [step])
        assert result.status == "completed"
        assert step.iteration_count == 2
        assert step.outputs["quality_score"] == pytest.approx(0.90)

    def test_bounded_loop_max_iterations_exceeded_fails(self):
        """Loop failing to converge within max_iterations fails safely."""
        def mock_failing_loop(step: WorkflowStep) -> dict:
            return {"quality_score": 0.50}

        executor = WorkflowExecutor(step_executor=mock_failing_loop)
        step = WorkflowStep(
            step_id="STUCK_LOOP",
            name="Non-converging Loop Step",
            agent_id="A06",
            loop_until="quality_score >= 0.85",
            max_iterations=3
        )

        result = executor.execute("wf-stuck", "task-stuck", "trace-stuck", [step])
        assert result.status == "failed"
        assert "exceeded max iterations" in result.error
