---
title: System Event Bus Specification
document_id: SPEC-P01-KERN-004
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Messaging & Event Group
last_updated: 2026-08-05
---

# System Event Bus Specification

## Executive Summary
This document specifies the Event Bus (`event_bus`), the low-latency, asynchronous event publish-subscribe system facilitating decoupled communication across core kernel subsystems, schedulers, memory services, and multi-agent frameworks.

---

## 1. Event Bus Architecture

```text
[ PUBLISHERS ]                                                              [ SUBSCRIBERS ]
(Agents, Kernel, Scheduler)                                                 (Audit, Metrics, Routers)
      │                                                                           ▲
      │ Publish(Topic, EventPayload)                                              │ Deliver(Event)
      ▼                                                                           │
+---------------------------------------------------------------------------------+
|                                 SYSTEM EVENT BUS                                |
|  - Topic Matcher (Wildcard 'aios.system.*')                                    |
|  - In-Memory / NATS Core Engine                                                 |
|  - Idempotency Deduplication Cache (LRU Window)                                 |
+---------------------------------------------------------------------------------+
```

---

## 2. Event Payload Contract & Interface

```typescript
export interface SystemEvent<T = unknown> {
  readonly id: string;
  readonly topic: string;
  readonly type: string;
  readonly source: string;
  readonly timestamp: string;
  readonly traceId: string;
  readonly data: T;
}

export type EventHandler<T = unknown> = (event: SystemEvent<T>) => Promise<void>;

export interface IEventBus {
  publish<T>(topic: string, eventType: string, data: T, source?: string): Promise<string>;
  subscribe<T>(topicPattern: string, handler: EventHandler<T>): Promise<string>; // Returns subscriptionId
  unsubscribe(subscriptionId: string): Promise<void>;
  flush(): Promise<void>;
}
```

---

## 3. Operational Rules & Reliability Guarantees

1. **At-Least-Once Delivery**: The Event Bus guarantees at-least-once delivery for persistent system topics (`aios.audit.*`, `aios.task.*`).
2. **Wildcard Subscription Support**: Supports subject matching (`aios.kernel.*`, `aios.agent.task.>`).
3. **Idempotency Window**: Deduplicates events with identical `id` within a 300-second rolling sliding window.

---

## 4. Verification Protocol

```bash
agy test-event-bus --benchmark --topics 1000
```
Runs high-throughput pub/sub benchmark, verifies wildcard topic matching, checks deduplication logic, and reports P99 delivery latency.
