---
title: Event Router & Dynamic Message Routing Specification
document_id: SPEC-P01-MSG-013
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Messaging & Infrastructure Group
last_updated: 2026-08-05
---

# Event Router & Dynamic Message Routing Specification

## Executive Summary
This document specifies the Event Router (`event_router`), responsible for content-based message routing, topic pattern matching, event transformation, header enrichment, and multi-tenant isolation across message paths in AI OS v4.

---

## 1. Event Router Pipeline Architecture

```text
[ INCOMING EVENT FRAME ]
           │
           ▼
+---------------------------------------------------------------+
| 1. HEADER SANITIZATION & TENANT CONTEXT ENRICHMENT           |
+---------------------------------------------------------------+
           │
           ▼
+---------------------------------------------------------------+
| 2. CONTENT-BASED ROUTING TABLE EVALUATION (XPath / JSONPath)  |
+---------------------------------------------------------------+
           │
           ├── Matches Pattern 'agent.swe.*' ──────> SWE Agent Queue
           ├── Matches Pattern 'system.audit.*' ────> Audit Log Stream
           └── Default Fallback ───────────────────> Main Router Pool
```

---

## 2. Router Rule Schema & Interface Contract

```typescript
export interface RoutingRule {
  readonly ruleId: string;
  readonly pattern: string; // e.g. "aios.events.task.*"
  readonly conditionJsonPath?: string; // e.g. "$.data.priority == 'HIGH'"
  readonly targetSubject: string;
  readonly transformPipeline?: string[];
}

export interface IEventRouter {
  registerRule(rule: RoutingRule): void;
  removeRule(ruleId: string): void;
  routeEvent(eventFrame: Record<string, unknown>): Promise<string[]>; // Target subjects
}
```

---

## 3. Dynamic Routing Rules & Transformation Invariants

1. **Cycle Detection**: Event Router evaluates routing graph topology to prevent infinite forwarding loops between subjects.
2. **Sub-Millisecond Evaluation**: Router evaluates JSONPath expressions using pre-compiled regex engines to guarantee P95 evaluation < 1ms.

---

## 4. Verification Protocol

```bash
agy verify-event-router --test-rules ./rules/default_routing.json
```
Tests routing table resolution, JSONPath matching, cycle detection, and event header enrichment.
