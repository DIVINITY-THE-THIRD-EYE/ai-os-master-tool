"""
Unit Tests for AI OS Runtime — workflow_executor, capability_router,
agent_registry, event_bus, plugin_registry.

Run: pytest tools/test_runtime.py -v --cov=runtime
"""

import threading
import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from runtime.workflow_executor import (
    WorkflowExecutor, WorkflowStep, WorkflowResult,
    ConditionEvaluator, StepStatus
)
from runtime.agent_registry import AgentRegistry, AgentRecord
from runtime.capability_router import CapabilityRouter
from runtime.event_bus import EventBus, Event, get_event_bus
from runtime.plugin_registry import PluginRegistry, PluginRecord


# ---------------------------------------------------------------------------
# ConditionEvaluator Tests
# ---------------------------------------------------------------------------

class TestConditionEvaluator:
    def test_in_operator_match(self):
        ctx = {"step1": {"risk_classification": "high"}}
        assert ConditionEvaluator.evaluate("risk_classification IN [high, critical]", ctx) is True

    def test_in_operator_no_match(self):
        ctx = {"step1": {"risk_classification": "low"}}
        assert ConditionEvaluator.evaluate("risk_classification IN [high, critical]", ctx) is False

    def test_equals_operator_match(self):
        ctx = {"step1": {"approval_status": "approved"}}
        assert ConditionEvaluator.evaluate("approval_status == approved", ctx) is True

    def test_equals_operator_no_match(self):
        ctx = {"step1": {"approval_status": "rejected"}}
        assert ConditionEvaluator.evaluate("approval_status == approved", ctx) is False

    def test_not_equals_operator(self):
        ctx = {"step1": {"approval_status": "rejected"}}
        assert ConditionEvaluator.evaluate("approval_status != approved", ctx) is True

    def test_gte_operator(self):
        ctx = {"step1": {"quality_score": 0.90}}
        assert ConditionEvaluator.evaluate("quality_score >= 0.85", ctx) is True

    def test_gte_operator_fail(self):
        ctx = {"step1": {"quality_score": 0.80}}
        assert ConditionEvaluator.evaluate("quality_score >= 0.85", ctx) is False

    def test_empty_condition_always_true(self):
        assert ConditionEvaluator.evaluate("", {}) is True

    def test_none_condition_always_true(self):
        assert ConditionEvaluator.evaluate(None, {}) is True

    def test_missing_key_defaults_to_true(self):
        # Unknown key — defaults to True to avoid blocking
        assert ConditionEvaluator.evaluate("nonexistent_key == value", {}) is True


# ---------------------------------------------------------------------------
# WorkflowExecutor Tests
# ---------------------------------------------------------------------------

class TestWorkflowExecutor:

    def _make_executor(self, outputs=None):
        """Create executor with a mock step_executor."""
        def mock_step(step: WorkflowStep) -> dict:
            return outputs.get(step.step_id, {"done": True}) if outputs else {"done": True}
        return WorkflowExecutor(step_executor=mock_step)

    def test_simple_linear_workflow(self):
        executor = self._make_executor()
        steps = [
            WorkflowStep("A", "Step A", "A01", depends_on=[]),
            WorkflowStep("B", "Step B", "A06", depends_on=["A"]),
            WorkflowStep("C", "Step C", "A07", depends_on=["B"]),
        ]
        result = executor.execute("wf-1", "task-1", "trace-1", steps)
        assert result.status == "completed"
        assert result.steps_completed == 3
        assert result.steps_failed == 0

    def test_parallel_execution(self):
        """Independent steps should run concurrently."""
        execution_order = []
        lock = threading.Lock()

        def tracking_executor(step: WorkflowStep) -> dict:
            with lock:
                execution_order.append(step.step_id)
            return {"done": True}

        executor = WorkflowExecutor(step_executor=tracking_executor)
        steps = [
            WorkflowStep("A", "Step A", "A01", depends_on=[]),
            WorkflowStep("B", "Step B", "A06", depends_on=[]),  # Independent of A
            WorkflowStep("C", "Step C", "A07", depends_on=["A", "B"]),
        ]
        result = executor.execute("wf-2", "task-2", "trace-2", steps)
        assert result.status == "completed"
        assert result.steps_completed == 3
        assert "C" in execution_order  # C must have run
        assert execution_order.index("C") > 0  # C always after A and B

    def test_condition_skips_step(self):
        """
        Step B has condition 'approval_status == escalated'.
        Step A produces approval_status = 'approved'.
        B's condition is injected via dependency outputs into its inputs,
        then evaluated. Since 'approved' != 'escalated', B is skipped.
        """
        def output_executor(step: WorkflowStep) -> dict:
            if step.step_id == "A":
                return {"approval_status": "approved"}
            return {"done": True}

        executor = WorkflowExecutor(step_executor=output_executor)
        steps = [
            WorkflowStep("A", "Step A", "A01", depends_on=[]),
            WorkflowStep("B", "Step B", "A13", depends_on=["A"],
                         condition="approval_status == escalated"),  # Should be skipped
        ]
        result = executor.execute("wf-3", "task-3", "trace-3", steps)
        assert result.status == "completed"
        # B is skipped (condition not met) — only A increments steps_completed
        assert result.steps_completed == 1

    def test_circular_dependency_raises(self):
        executor = self._make_executor()
        steps = [
            WorkflowStep("A", "Step A", "A01", depends_on=["B"]),
            WorkflowStep("B", "Step B", "A06", depends_on=["A"]),
        ]
        with pytest.raises(ValueError, match="Circular dependency"):
            executor.execute("wf-4", "task-4", "trace-4", steps)

    def test_retry_on_failure(self):
        attempt_counter = {"count": 0}

        def failing_then_succeeding(step: WorkflowStep) -> dict:
            attempt_counter["count"] += 1
            if attempt_counter["count"] < 3:
                raise RuntimeError("Transient error")
            return {"done": True}

        executor = WorkflowExecutor(
            step_executor=failing_then_succeeding,
            max_workers=1
        )
        # Use 0 backoff for testing speed
        executor.RETRY_BACKOFF_SECONDS = [0, 0, 0]

        steps = [WorkflowStep("A", "Step A", "A01", depends_on=[], max_retries=3)]
        result = executor.execute("wf-5", "task-5", "trace-5", steps)
        assert result.status == "completed"
        assert attempt_counter["count"] == 3

    def test_max_retries_exceeded_fails(self):
        def always_failing(step: WorkflowStep) -> dict:
            raise RuntimeError("Permanent failure")

        executor = WorkflowExecutor(step_executor=always_failing)
        executor.RETRY_BACKOFF_SECONDS = [0, 0, 0]

        steps = [WorkflowStep("A", "Step A", "A01", depends_on=[], max_retries=2)]
        result = executor.execute("wf-6", "task-6", "trace-6", steps)
        assert result.status == "failed"
        assert result.steps_failed == 1


# ---------------------------------------------------------------------------
# AgentRegistry Tests
# ---------------------------------------------------------------------------

class TestAgentRegistry:

    def _make_registry(self):
        registry = AgentRegistry()
        agent = AgentRecord(
            agent_id="A01",
            name="Intake Agent",
            version="1.0.0",
            capabilities=["task_intake"],
            skills=["requirements_analysis"],
            tools=["tool_file_read"],
            permissions=["read_task", "write_charter"],
        )
        registry.register(agent)
        return registry, agent

    def test_register_and_retrieve(self):
        registry, _ = self._make_registry()
        retrieved = registry.get("A01")
        assert retrieved is not None
        assert retrieved.agent_id == "A01"
        assert retrieved.status == "registered"

    def test_duplicate_register_raises(self):
        registry, agent = self._make_registry()
        with pytest.raises(ValueError, match="already registered"):
            registry.register(agent)

    def test_ready_requires_configured(self):
        registry, _ = self._make_registry()
        with pytest.raises(ValueError, match="must be 'configured'"):
            registry.mark_ready("A01")

    def test_full_lifecycle(self):
        registry, _ = self._make_registry()
        registry.configure("A01")
        registry.mark_ready("A01")
        agent = registry.get("A01")
        assert agent.status == "ready"
        assert agent.health_status == "healthy"
        assert agent.is_available() is True

    def test_find_by_capability(self):
        registry, _ = self._make_registry()
        registry.configure("A01")
        registry.mark_ready("A01")
        results = registry.find_by_capability("task_intake")
        assert len(results) == 1
        assert results[0].agent_id == "A01"

    def test_disabled_agent_not_available(self):
        registry, _ = self._make_registry()
        registry.configure("A01")
        registry.mark_ready("A01")
        registry.disable("A01")
        assert registry.get("A01").is_available() is False
        assert registry.find_by_capability("task_intake") == []


# ---------------------------------------------------------------------------
# CapabilityRouter Tests
# ---------------------------------------------------------------------------

class TestCapabilityRouter:

    def _make_router(self):
        registry = AgentRegistry()
        for i, cap in enumerate(["task_intake", "verification", "scheduling"]):
            agent = AgentRecord(
                agent_id=f"A0{i+1}",
                name=f"Agent {i+1}",
                version="1.0.0",
                capabilities=[cap],
                skills=[],
                tools=[],
                permissions=[],
            )
            registry.register(agent)
            registry.configure(f"A0{i+1}")
            registry.mark_ready(f"A0{i+1}")
        return CapabilityRouter(registry), registry

    def test_routes_to_correct_agent(self):
        router, _ = self._make_router()
        agent = router.route("task_intake", "task-1", "trace-1")
        assert agent is not None
        assert agent.agent_id == "A01"

    def test_returns_none_for_unknown_capability(self):
        router, _ = self._make_router()
        result = router.route("nonexistent_capability", "task-1", "trace-1")
        assert result is None

    def test_thread_safe_routing(self):
        """Round-robin counter must not race under concurrent access."""
        router, _ = self._make_router()
        results = []
        lock = threading.Lock()

        def route_task(i):
            agent = router.route("task_intake", f"task-{i}", "trace-1")
            with lock:
                results.append(agent.agent_id if agent else None)

        threads = [threading.Thread(target=route_task, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 50
        assert all(r == "A01" for r in results)  # Only one agent for task_intake


# ---------------------------------------------------------------------------
# EventBus Tests
# ---------------------------------------------------------------------------

class TestEventBus:

    def test_publish_and_subscribe(self):
        bus = EventBus()
        received = []
        bus.subscribe("task.created", lambda e: received.append(e))
        event = Event(
            event_type="task.created",
            agent_id="A00",
            task_id="task-1",
            payload={"objective": "test"}
        )
        count = bus.publish(event)
        assert count == 1
        assert len(received) == 1
        assert received[0].task_id == "task-1"

    def test_no_subscriber_returns_zero(self):
        bus = EventBus()
        event = Event(event_type="task.created", agent_id="A00", task_id="t1", payload={})
        count = bus.publish(event)
        assert count == 0

    def test_persistence(self):
        bus = EventBus()
        bus.configure_persistence(["task.created"])
        bus.subscribe("task.created", lambda e: None)
        event = Event(event_type="task.created", agent_id="A00", task_id="t1", payload={})
        bus.publish(event)
        history = bus.get_history(topic="task.created")
        assert len(history) == 1

    def test_missing_required_fields_raises(self):
        bus = EventBus()
        with pytest.raises(ValueError):
            bus.publish({"not": "an event"})

    def test_filter_by_task_id(self):
        bus = EventBus()
        bus.configure_persistence(["task.created"])
        for i in range(3):
            event = Event(
                event_type="task.created", agent_id="A00",
                task_id=f"task-{i}", payload={}
            )
            bus.publish(event)
        result = bus.get_history(task_id="task-1")
        assert len(result) == 1
        assert result[0]["task_id"] == "task-1"


# ---------------------------------------------------------------------------
# PluginRegistry Tests
# ---------------------------------------------------------------------------

class TestPluginRegistry:

    def _make_plugin(self, plugin_id="tool_search"):
        return PluginRecord(
            plugin_id=plugin_id,
            name="Search Tool",
            version="1.0.0",
            type="tool",
            description="Web search",
            interface_schema={"input": {}, "output": {}},
            permissions=["search", "read_url"],
            sandbox_required=True,
            rate_limit_per_minute=30,
            timeout_seconds=15,
        )

    def test_register_and_activate(self):
        reg = PluginRegistry()
        plugin = self._make_plugin()
        reg.register(plugin)
        reg.activate("tool_search")
        assert reg.get("tool_search").is_available() is True

    def test_duplicate_register_raises(self):
        reg = PluginRegistry()
        reg.register(self._make_plugin())
        with pytest.raises(ValueError, match="already registered"):
            reg.register(self._make_plugin())

    def test_invocation_allowed(self):
        reg = PluginRegistry()
        reg.register(self._make_plugin())
        reg.activate("tool_search")
        allowed, reason = reg.validate_invocation(
            "tool_search", "A06", "search", {"query": "test"}
        )
        assert allowed is True

    def test_invocation_denied_wrong_operation(self):
        reg = PluginRegistry()
        reg.register(self._make_plugin())
        reg.activate("tool_search")
        allowed, reason = reg.validate_invocation(
            "tool_search", "A06", "delete_files", {"path": "/"}
        )
        assert allowed is False
        assert "whitelist" in reason

    def test_invocation_denied_not_registered(self):
        reg = PluginRegistry()
        allowed, reason = reg.validate_invocation("nonexistent", "A06", "search", {})
        assert allowed is False

    def test_audit_log_records_invocations(self):
        reg = PluginRegistry()
        reg.register(self._make_plugin())
        reg.activate("tool_search")
        reg.record_invocation("tool_search", "A06", "search", success=True)
        reg.record_invocation("tool_search", "A06", "search", success=False, error="timeout")
        log = reg.get_audit_log(plugin_id="tool_search")
        assert len(log) == 2
        assert log[1]["success"] is False
        assert log[1]["error"] == "timeout"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
