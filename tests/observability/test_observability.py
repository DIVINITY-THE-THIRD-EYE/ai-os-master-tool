"""
Phase 10 Observability Test Suite.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.observability_reporter import ObservabilityReporter

class TestObservability:
    def test_execution_report_generation(self):
        report = ObservabilityReporter.generate_execution_report(
            trace_id="tr-100",
            task_id="task-100",
            workflow_id="wf-100",
            steps_completed=5,
            steps_failed=0,
            total_tokens=1500,
            total_cost_usd=0.003,
            retry_count=0,
            status="completed"
        )
        
        assert report["trace_id"] == "tr-100"
        assert report["metrics"]["total_tokens"] == 1500
        assert report["metrics"]["total_cost_usd"] == 0.003
        assert report["status"] == "completed"
