---
title: System Message Broker Architecture Specification
document_id: SPEC-P01-MSG-012
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Messaging & Infrastructure Group
last_updated: 2026-08-05
---

# System Message Broker Architecture Specification

## Executive Summary
This document specifies the Message Broker (`message_broker`), providing high-performance, fault-tolerant message queues, topic subscriptions, dead-letter queues (DLQ), NATS/Kafka connection management, and persistence backings for AI OS v4.

---

## 1. Message Broker Architecture

```text
[ AGENTS & SERVICES ]
         │
         ├── Publish / Subscribe / Request
         ▼
+-------------------------------------------------------------------------+
|                         MESSAGE BROKER ENGINE                           |
|  - Engine Adapter: NATS JetStream / Kafka / Memory                      |
|  - Queue Groups & Load Balancing                                        |
|  - Persistent Stream Store & WAL                                        |
|  - Dead Letter Queue (DLQ) Handler                                      |
+-------------------------------------------------------------------------+
         │
         ▼
[ DEAD LETTER QUEUE (DLQ) ] ──> Escalation / Re-play Queue
```

---

## 2. Broker Interface Contract

```typescript
export interface BrokerOptions {
  readonly provider: "nats" | "kafka" | "memory";
  readonly url: string;
  readonly clusterId: string;
  readonly ackTimeoutMs: number;
}

export interface IMessageBroker {
  connect(options: BrokerOptions): Promise<void>;
  disconnect(): Promise<void>;
  publish(subject: string, payload: Uint8Array): Promise<void>;
  subscribe(subject: string, queueGroup: string, handler: (msg: Uint8Array) => Promise<void>): Promise<string>;
  sendToDLQ(subject: string, payload: Uint8Array, errorReason: string): Promise<void>;
}
```

---

## 3. Queue Groups & Dead Letter Policies

1. **Competing Consumers**: Queue groups ensure that messages published to worker queues (`aios.tasks.workers`) are load-balanced across active worker instances.
2. **DLQ Threshold Policy**: If a message fails delivery after 3 retry attempts, it is routed to subject `aios.system.dlq` for manual or automated inspection.

---

## 4. Verification Protocol

```bash
agy verify-broker --provider memory --test-dlq
```
Runs broker load tests, verifies queue group message distribution, and checks DLQ routing upon simulated consumer crashes.
