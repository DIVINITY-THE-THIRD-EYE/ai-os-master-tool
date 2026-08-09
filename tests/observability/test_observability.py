"""
Phase 10 Observability Test Suite.
"""

import json
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

    def test_span_tracing_and_telemetry_export(self):
        reporter = ObservabilityReporter()
        span_id = reporter.start_span("tr-200", "A01 Intake Requirements", "A01")
        assert span_id.startswith("span-")
        assert span_id in reporter.active_spans

        span_res = reporter.end_span(span_id, "COMPLETED", {"output_file": "spec.md"})
        assert span_res["status"] == "COMPLETED"
        assert span_res["output"]["output_file"] == "spec.md"
        assert span_res["duration_ms"] >= 0

        telemetry_raw = reporter.export_telemetry_json()
        telemetry = json.loads(telemetry_raw)
        assert telemetry["total_spans"] == 1
        assert telemetry["spans"][0]["span_name"] == "A01 Intake Requirements"
