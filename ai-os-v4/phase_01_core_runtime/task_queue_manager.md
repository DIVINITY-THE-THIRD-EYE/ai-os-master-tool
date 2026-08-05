---
title: Task Queue Manager Specification
document_id: SPEC-P01-SCHED-025
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Messaging & Scheduler Subsystem Team
last_updated: 2026-08-05
---

# Task Queue Manager Specification

## Executive Summary
This document specifies the Task Queue Manager (`task_queue_manager`), responsible for task persistence, queue partitioning, FIFO/LIFO ordering policies, dead-letter storage, and queue depth monitoring in AI OS v4.

---

## 1. Task Queue System Architecture

```text
[ INCOMING TASKS ]
        │
        ▼
+-----------------------------------------------------------------+
| TASK QUEUE MANAGER                                              |
|  - Queue Partition 0: Interactive User Tasks (High Priority)    |
|  - Queue Partition 1: Standard Workflow Nodes                   |
|  - Queue Partition 2: Background Reflection & Optimization      |
|  - Storage Engine: Redis Streams / RocksDB / In-Memory WAL      |
+-----------------------------------------------------------------+
        │
        ▼ (Ack-Based Task Fetch)
[ WORKER POOL EXECUTORS ]
```

---

## 2. Queue Manager Schema & API Contract

```typescript
export interface TaskEnvelope {
  readonly taskId: string;
  readonly queueName: string;
  readonly payload: Record<string, unknown>;
  readonly enqueuedAt: string;
  readonly attempts: number;
}

export interface ITaskQueueManager {
  enqueueTask(queueName: string, payload: Record<string, unknown>): Promise<string>;
  dequeueTask(queueName: string, timeoutMs?: number): Promise<TaskEnvelope | null>;
  ackTask(taskId: string): Promise<void>;
  nackTask(taskId: string, requeue: boolean): Promise<void>;
  getQueueDepth(queueName: string): Promise<number>;
}
```

---

## 3. Operational Policies & Invariants

1. **Ack-Based Processing**: Dequeued tasks enter an `IN_FLIGHT` processing state. If no ACK or NACK is received within visibility timeout (60s), the task is requeued automatically.
2. **Persistent Queue Storage**: Tasks enqueued to production queues are written to Write-Ahead Log (WAL) to guarantee zero task loss across node restarts.

---

## 4. Verification Protocol

```bash
agy verify-task-queue --test-persistence --tasks 1000
```
Tests task enqueue/dequeue throughput, verifies ACK/NACK visibility timeouts, and validates WAL recovery.
