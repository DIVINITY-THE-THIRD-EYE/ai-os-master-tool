---
title: Task Timeout Manager Specification
document_id: SPEC-P01-SCHED-024
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core Scheduler Group
last_updated: 2026-08-05
---

# Task Timeout Manager Specification

## Executive Summary
This document specifies the Timeout Manager (`timeout_manager`), managing deadline timers, context cancellation signals, asynchronous execution timeouts, and resource cleanup for long-running or stalled operations in AI OS v4.

---

## 1. Timeout Architecture & Timer Wheel

```text
[ TASK DISPATCH ] ──> RegisterDeadlineTimer(taskId, durationMs)
                              │
                              ▼
+-----------------------------------------------------------------+
| TIMEOUT MANAGER TIMER WHEEL (10ms Slot Granularity)            |
+-----------------------------------------------------------------+
                              │ (Timer Expiration Event)
                              ▼
+-----------------------------------------------------------------+
| CANCELLATION HANDLER                                            |
| 1. Send AbortController signal / SIGTERM to agent process        |
| 2. Save partial execution state checkpoint                       |
| 3. Emit TaskTimeoutEvent & release locks                        |
+-----------------------------------------------------------------+
```

---

## 2. Timeout Manager API Contract

```typescript
export interface TimeoutRegistration {
  readonly timerId: string;
  readonly taskId: string;
  readonly timeoutMs: number;
  readonly expiresAt: number;
  readonly callback: () => Promise<void>;
}

export interface ITimeoutManager {
  registerTimeout(taskId: string, timeoutMs: number, onTimeout: () => Promise<void>): Promise<string>;
  cancelTimeout(timerId: string): Promise<boolean>;
  extendTimeout(timerId: string, additionalMs: number): Promise<boolean>;
}
```

---

## 3. Operational Bounds & Safety Policies

1. **Hard Max Task Timeout**: Maximum allowable task duration is 1,800 seconds (30 minutes). Enforcing hard caps prevents infinite hangs.
2. **Timer Wheel Granularity**: The low-overhead Timer Wheel operates at 10ms tick resolution to minimize CPU scheduling overhead.

---

## 4. Verification Protocol

```bash
agy verify-timeout-manager --test-cancellation --timer-resolution 10ms
```
Registers synthetic timers, tests early cancellation, verifies timeout callback execution, and checks timer wheel precision.
