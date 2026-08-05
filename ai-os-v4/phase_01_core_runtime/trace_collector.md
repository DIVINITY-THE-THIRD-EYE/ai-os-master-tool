---
title: Distributed Trace Collector Specification
document_id: SPEC-P01-SAFE-036
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Telemetry & Observability Team
last_updated: 2026-08-05
---

# Distributed Trace Collector Specification

## Executive Summary
This document specifies the Trace Collector (`trace_collector`), managing distributed trace span creation, W3C trace parent propagation, OpenTelemetry span exporting, inter-agent trace sampling, and performance bottleneck profiling in AI OS v4.

---

## 1. Trace Collector Architecture

```text
[ AGENT EXECUTION SPAN ] ──> StartSpan("AgentTaskExecution")
                                      │
                                      ▼
+-----------------------------------------------------------------+
| OPENTELEMETRY TRACE COLLECTOR                                   |
|  - W3C TraceContext Propagation (traceparent, tracestate)       |
|  - Adaptive Span Sampler (100% Errors, 10% Normal Traces)       |
|  - OTLP Exporter (gRPC to Jaeger / Tempo / Zipkin)              |
+-----------------------------------------------------------------+
```

---

## 2. Trace Collector Interface Contract

```typescript
export interface TraceSpan {
  readonly traceId: string;
  readonly spanId: string;
  readonly parentSpanId?: string;
  readonly name: string;
  readonly startTimeMs: number;
  readonly attributes: Record<string, string | number | boolean>;
}

export interface ITraceCollector {
  startSpan(name: string, parentTraceContext?: string): TraceSpan;
  endSpan(span: TraceSpan, error?: Error): void;
  injectTraceHeaders(span: TraceSpan): Record<string, string>;
  flushTraces(): Promise<void>;
}
```

---

## 3. Operational Rules & Sampling Strategy

1. **Adaptive Trace Sampling**: Captures 100% of trace spans containing exceptions (`error=true`) and 10% of normal execution traces to balance observability against storage costs.
2. **Standard Span Attributes**: Every span MUST record `agent.id`, `task.id`, `workflow.id`, and `llm.tokens_used`.

---

## 4. Verification Protocol

```bash
agy verify-trace-collector --test-otlp --exporter http://localhost:4317
```
Generates synthetic distributed trace graphs, verifies W3C header injection, tests adaptive sampling, and checks OTLP exporter delivery.
