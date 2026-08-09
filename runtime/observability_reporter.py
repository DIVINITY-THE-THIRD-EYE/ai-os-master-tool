"""
AI OS Execution Observability Reporter — generates execution graphs, agent timelines, token & cost reports, and verification summaries.
Supports active span tracing and JSON telemetry exports.
"""

import json
import time
import uuid
from typing import Dict, Any, List, Optional

class ObservabilityReporter:
    def __init__(self):
        self.active_spans: Dict[str, dict] = {}
        self.completed_spans: List[dict] = []

    def start_span(self, trace_id: str, span_name: str, agent_id: str) -> str:
        """Start a new execution span and return span_id."""
        span_id = f"span-{str(uuid.uuid4())[:8]}"
        span_record = {
            "span_id": span_id,
            "trace_id": trace_id,
            "span_name": span_name,
            "agent_id": agent_id,
            "start_time": time.time(),
            "status": "RUNNING",
            "end_time": None,
            "output": None
        }
        self.active_spans[span_id] = span_record
        return span_id

    def end_span(self, span_id: str, status: str = "COMPLETED", output: Optional[Dict[str, Any]] = None) -> dict:
        """Complete an active span and log metrics."""
        if span_id not in self.active_spans:
            raise KeyError(f"Active span ID {span_id} not found.")

        span = self.active_spans.pop(span_id)
        span["end_time"] = time.time()
        span["duration_ms"] = round((span["end_time"] - span["start_time"]) * 1000, 3)
        span["status"] = status
        span["output"] = output or {}

        self.completed_spans.append(span)
        return span

    def export_telemetry_json(self) -> str:
        """Export all completed spans as structured JSON telemetry."""
        return json.dumps({
            "total_spans": len(self.completed_spans),
            "spans": self.completed_spans
        }, indent=2)

    @staticmethod
    def generate_execution_report(
        trace_id: str,
        task_id: str,
        workflow_id: str,
        steps_completed: int,
        steps_failed: int,
        total_tokens: int,
        total_cost_usd: float,
        retry_count: int,
        status: str
    ) -> Dict[str, Any]:
        return {
            "trace_id": trace_id,
            "task_id": task_id,
            "workflow_id": workflow_id,
            "metrics": {
                "steps_completed": steps_completed,
                "steps_failed": steps_failed,
                "total_tokens": total_tokens,
                "total_cost_usd": round(total_cost_usd, 6),
                "retry_count": retry_count,
            },
            "status": status,
            "execution_graph_summary": f"DAG Workflow {workflow_id} executed with {steps_completed} steps completed."
        }
