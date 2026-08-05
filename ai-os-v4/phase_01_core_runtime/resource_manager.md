---
title: System Resource Manager & Allocation Specification
document_id: SPEC-P01-SCHED-022
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Infrastructure & Resource Governance Group
last_updated: 2026-08-05
---

# System Resource Manager & Allocation Specification

## Executive Summary
This document specifies the Resource Manager (`resource_manager`), tracking CPU core availability, memory allocation pools, GPU slice assignments, token budget allocations, and execution slot reservations across AI OS v4 cluster nodes.

---

## 1. Resource Allocation Architecture

```text
[ SCHEDULER TASK REQUEST ] ──> AcquireReservation(CPU: 2, RAM: 2048MB, Token: 50k)
                                              │
                                              ▼
+-------------------------------------------------------------------------+
|                        SYSTEM RESOURCE MANAGER                          |
|  - Available CPU Pool: 16 Cores | Reserved: 8 Cores                     |
|  - Available RAM Pool: 32 GB    | Reserved: 12 GB                     |
|  - Active Token Reservation Bucket                                      |
+-------------------------------------------------------------------------+
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼ (Resources Available)                             ▼ (Insufficient Resources)
        [ RESERVATION GRANTED ]                             [ RESERVATION QUEUED ]
```

---

## 2. Resource Manager API Contract

```typescript
export interface ResourceReservationRequest {
  readonly taskId: string;
  readonly cpuCores: number;
  readonly memoryMb: number;
  readonly tokenBudget: number;
  readonly priority: number;
}

export interface ResourceReservation {
  readonly reservationId: string;
  readonly taskId: string;
  readonly allocatedCpuCores: number;
  readonly allocatedMemoryMb: number;
  readonly grantedAt: string;
}

export interface IResourceManager {
  requestReservation(req: ResourceReservationRequest): Promise<ResourceReservation>;
  releaseReservation(reservationId: string): Promise<void>;
  getSystemCapacity(): Promise<{ totalCpu: number; freeCpu: number; totalMemMb: number; freeMemMb: number }>;
}
```

---

## 3. Allocation Invariants & Overcommit Rules

1. **No Memory Overcommit**: Memory allocations are strict and hard-reserved. Total reservations CANNOT exceed 90% of host physical RAM.
2. **Fair Share CPU Scheduling**: If CPU utilization hits 95%, low-priority task threads are throttled to ensure high-priority agent execution.

---

## 4. Verification Protocol

```bash
agy verify-resource-manager --test-exhaustion
```
Simulates concurrent resource allocation requests, tests queueing under resource pressure, and verifies reservation cleanup.
