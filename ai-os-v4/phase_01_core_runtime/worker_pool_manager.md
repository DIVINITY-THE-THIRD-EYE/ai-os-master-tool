---
title: Agent Worker Pool Manager Specification
document_id: SPEC-P01-SCHED-027
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Agent Execution Subsystem Team
last_updated: 2026-08-05
---

# Agent Worker Pool Manager Specification

## Executive Summary
This document specifies the Worker Pool Manager (`worker_pool_manager`), managing pre-warmed agent container pools, container reuse, worker state sanitization, worker allocation, and horizontal auto-scaling in AI OS v4.

---

## 1. Worker Pool Architecture

```text
[ SCHEDULER DISPATCH ] ──> AcquireWorker(role="architect")
                                  │
                                  ▼
+-----------------------------------------------------------------+
| AGENT WORKER POOL MANAGER                                       |
|                                                                 |
|  - Pre-Warmed Container Pool: 8 Clean Instances                 |
|  - Active Executing Pool:     12 Active Containers              |
|  - Sanitization Pipeline:      4 Recycling Instances            |
+-----------------------------------------------------------------+
                                  │
                                  ▼
[ WORKER ASSIGNED & CONTAINER BOUND ]
```

---

## 2. Worker Pool API Interface Contract

```typescript
export interface WorkerDescriptor {
  readonly workerId: string;
  readonly role: string;
  readonly status: "PRE_WARMED" | "BUSY" | "RECYCLING";
  readonly executionCount: number;
}

export interface IWorkerPoolManager {
  acquireWorker(role: string): Promise<WorkerDescriptor>;
  releaseWorker(workerId: string, dirty: boolean): Promise<void>;
  getPoolStatus(): Promise<{ totalWorkers: number; available: number; busy: number }>;
  scalePool(targetSize: number): Promise<void>;
}
```

---

## 3. Worker Sanitization & Recycled Warm Instances

1. **Mandatory Sanitization on Release**: Releasing a worker executes container memory wipe and clears scratch filesystem overlays before returning to the `PRE_WARMED` pool.
2. **Max Execution Lifetime**: To prevent memory leaks, workers are retired and destroyed after completing 50 execution cycles.

---

## 4. Verification Protocol

```bash
agy verify-worker-pool --test-recycling --pool-size 10
```
Tests pre-warmed container acquisition latency (target < 50ms), validates sanitization wiping, and checks pool scaling.
