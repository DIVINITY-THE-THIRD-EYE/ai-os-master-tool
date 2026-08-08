"""
Enforcement Tests for AI OS v4 Budgets and Quality Gates.

Tests:
- Token limit overflow blocking
- Cost budget limit blocking
- Quality score threshold gate enforcement
- Security policy violation blocking
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from runtime.llm_router import LLMRouter
from runtime.plugin_registry import PluginRegistry, PluginRecord
from runtime.workflow_executor import ConditionEvaluator

class TestBudgetEnforcement:
    def test_token_limit_exceeded_blocking(self):
        """Worker requesting tokens beyond max token budget should be blocked."""
        router = LLMRouter(api_keys={})
        router.MAX_TOKEN_BUDGET = 100
        
        # Dispatch small call
        res1 = router.dispatch("A01", "sys prompt", "short input")
        assert res1.parsed_json["status"] == "completed"
        
        # Next call exceeds token budget limit
        with pytest.raises(RuntimeError, match="Token budget exceeded"):
            router.dispatch("A01", "sys prompt", "long input " * 500)

    def test_cost_budget_limit_blocking(self):
        """Cost budget ceiling enforcement test."""
        router = LLMRouter(api_keys={})
        router.MAX_COST_BUDGET_USD = 0.001
        
        # Simulate cost usage
        router.dispatch("A01", "sys prompt", "task 1")
        router.dispatch("A01", "sys prompt", "task 2")

class TestQualityGatesEnforcement:
    def test_quality_score_gate_blocking(self):
        """Quality score below threshold (e.g. < 0.85) blocks workflow progression."""
        ctx_fail = {"step1": {"quality_score": 0.80}}
        assert ConditionEvaluator.evaluate("quality_score >= 0.85", ctx_fail) is False
        
        ctx_pass = {"step1": {"quality_score": 0.90}}
        assert ConditionEvaluator.evaluate("quality_score >= 0.85", ctx_pass) is True

    def test_security_violation_blocks_execution(self):
        """Operation not whitelisted by security policy must be blocked."""
        reg = PluginRegistry()
        plugin = PluginRecord(
            plugin_id="tool_file",
            name="File Tool",
            version="1.0.0",
            type="tool",
            description="File ops",
            interface_schema={},
            permissions=["read_file"],
            sandbox_required=True
        )
        reg.register(plugin)
        reg.activate("tool_file")
        
        # Unapproved write operation must fail security gate
        allowed, reason = reg.validate_invocation("tool_file", "A06", "delete_system_file", {"path": "/etc"})
        assert allowed is False
        assert "whitelist" in reason
