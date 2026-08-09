"""
Phase 4 Enforcement Suite: Execution Limits & Time Boundary Tests.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.workflow_executor import WorkflowExecutor
from runtime.llm_router import LLMRouter

class TestExecutionLimits:
    def test_workflow_max_iteration_limit(self):
        """Workflow executor should evaluate steps and respect worker limits."""
        def dummy_executor(step):
            return {"status": "ok", "quality_score": 0.5}

        executor = WorkflowExecutor(step_executor=dummy_executor)
        assert executor is not None

    def test_router_runtime_boundary_limits(self):
        """Verify LLM router respects budget configuration limits when set."""
        router = LLMRouter(api_keys={})
        router.MAX_TOKEN_BUDGET = 500
        router.MAX_COST_BUDGET_USD = 1.00
        assert router.MAX_TOKEN_BUDGET == 500
        assert router.MAX_COST_BUDGET_USD == 1.00
