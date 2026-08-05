---
title: Task Retry Manager & Exponential Backoff Specification
document_id: SPEC-P01-SCHED-023
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Platform Reliability Group
last_updated: 2026-08-05
---

# Task Retry Manager & Exponential Backoff Specification

## Executive Summary
This document specifies the Retry Manager (`retry_manager`), governing failure classification, retry policies, jittered exponential backoff calculation, prompt strategy fallback, and dead-letter escalation for failing tasks in AI OS v4.

---

## 1. Retry Pipeline & Backoff Logic

```text
[ TASK EXECUTION FAILURE ]
            │
            ▼
+---------------------------------------------------------------+
| 1. FAILURE CLASSIFIER                                         |
|    - Non-retryable (Security violation, invalid schema) ────> DLQ / Mark Failed
|    - Retryable (Network timeout, LLM rate limit, 503) ──────> Process Retry
+---------------------------------------------------------------+
            │
            ▼
+---------------------------------------------------------------+
| 2. EXPONENTIAL BACKOFF + JITTER CALCULATION                   |
|    delay = min(max_delay, initial_delay * (2 ^ attempt))      |
|    jittered_delay = delay + random_uniform(-jitter, +jitter)  |
+---------------------------------------------------------------+
            │
            ▼
[ ENQUEUE RETRY TASK (After Backoff Delay) ]
```

---

## 2. Retry Policy Schema & API Specification

```typescript
export interface RetryPolicy {
  readonly maxAttempts: number;
  readonly initialDelayMs: number;
  readonly maxDelayMs: number;
  readonly backoffFactor: number;
  readonly jitterFactor: number; // e.g. 0.2 (20% random jitter)
  readonly retryableErrorCodes: string[];
}

export interface IRetryManager {
  shouldRetry(taskId: string, errorCode: string, currentAttempt: number, policy: RetryPolicy): boolean;
  calculateBackoffDelayMs(attempt: number, policy: RetryPolicy): number;
  scheduleRetry(taskId: string, attempt: number, delayMs: number): Promise<void>;
}
```

---

## 3. Operational Rules & Fallback Strategies

1. **Jitter Requirement**: All exponential backoff calculations MUST apply random jitter to prevent thundering herd spikes on downstream API endpoints.
2. **Prompt Fallback Escalation**: On attempt 2, Retry Manager injects reflection feedback hints into the agent execution context to correct failure causes.

---

## 4. Verification Protocol

```bash
agy verify-retry-manager --test-backoff-math
```
Tests exponential backoff delay formulas, verifies random jitter bounds, and validates non-retryable error interception.
