---
title: System Logging & Telemetry Standard
document_id: SPEC-P00-LOG-009
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Observability & Telemetry Team
last_updated: 2026-08-05
---

# System Logging & Telemetry Standard

## Executive Summary
This document specifies the enterprise logging schema, OpenTelemetry (OTel) integration standards, metric naming conventions, structured log levels, and distributed trace context propagation for AI OS v4.

---

## 1. Observability Architecture

```text
[ AGENT ENGINE / KERNEL NODE ]
  │
  ├── 1. Structured JSON Logs ──────> Log Collector (Vector / FluentBit) ──> Elasticsearch / Loki
  │
  ├── 2. OpenTelemetry Traces ──────> OTel Collector ─────────────────────> Jaeger / Tempo
  │
  └── 3. Prometheus Metrics ────────> Metric Exporter (/metrics) ─────────> Prometheus / Grafana
```

---

## 2. Standard Structured Log Payload Schema

All log outputs MUST emit single-line JSON with standardized keys:

```json
{
  "timestamp": "2026-08-05T15:46:12.345Z",
  "level": "INFO",
  "service": "aios-kernel",
  "component": "dag_scheduler",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "spanId": "00f067aa0ba902b7",
  "message": "Task graph execution step completed successfully",
  "attributes": {
    "taskId": "task-swe-901",
    "workflowId": "wf-build-app-04",
    "agentId": "agent-qa-verifier-02",
    "durationMs": 142.5,
    "tokensUsed": 1850,
    "promptCostUSD": 0.0037
  }
}
```

---

## 3. Metric Naming & Standard Metric Catalog

Prometheus metrics follow the convention `aios_<subsystem>_<name>_<unit>`:

| Metric Name | Type | Description |
| :--- | :--- | :--- |
| `aios_kernel_active_agents_total` | Gauge | Current count of active agent execution sandboxes |
| `aios_scheduler_task_queue_depth` | Gauge | Total tasks waiting in DAG execution queue |
| `aios_llm_request_duration_seconds` | Histogram | Latency distribution of LLM provider API requests |
| `aios_llm_token_consumption_total` | Counter | Total prompt and completion tokens consumed |
| `aios_security_policy_violations_total` | Counter | Cumulative count of intercepted security violations |

---

## 4. Distributed Tracing Protocol & W3C Headers

Inter-agent RPC calls and HTTP requests MUST propagate W3C Trace Context headers:
- `traceparent`: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`
- `tracestate`: `aios=agent-01;sample=1`

---

## 5. Verification Protocol

Validate telemetry exporters and JSON log schema:
```bash
agy verify-telemetry --endpoint http://localhost:4318
```
Verifies active trace propagation, OTel metric collection, and structured log compliance.
