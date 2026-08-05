---
title: Global Exception Handler & Fault Recovery Specification
document_id: SPEC-P01-SAFE-032
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Platform Reliability Group
last_updated: 2026-08-05
---

# Global Exception Handler & Fault Recovery Specification

## Executive Summary
This document specifies the Exception Handler (`exception_handler`), capturing unhandled promise rejections, fatal runtime exceptions, agent execution crashes, stack trace unwinding, error telemetry emission, and kernel state isolation in AI OS v4.

---

## 1. Exception Handling & Recovery Flow

```text
[ UNHANDLED EXCEPTION / FATAL ERROR ]
                  │
                  ▼
+-------------------------------------------------------------+
| 1. GLOBAL EXCEPTION CATCHER                                 |
+-------------------------------------------------------------+
                  │
                  ▼
+-------------------------------------------------------------+
| 2. ERROR TELEMETRY & STACK TRACE SANITIZATION ENGINE        |
|    - Mask Secrets & API Keys from Stack Frames              |
|    - Generate Error Payload with Trace ID                   |
+-------------------------------------------------------------+
                  │
                  ├── Fatal System Panic ────> Trigger Kernel Emergency Halt
                  └── Agent Process Crash ───> Isolate Node & Trigger Recovery Policy
```

---

## 2. Exception Handler Interface Contract

```typescript
export interface FatalExceptionReport {
  readonly errorId: string;
  readonly message: string;
  readonly stackTrace: string;
  readonly sanitizedStack: string;
  readonly subsystem: string;
  readonly isFatal: boolean;
  readonly timestamp: string;
}

export interface IExceptionHandler {
  handleException(error: Error, subsystem: string): Promise<FatalExceptionReport>;
  registerFatalCallback(callback: (report: FatalExceptionReport) => Promise<void>): void;
}
```

---

## 3. Operational Rules & Secret Sanitization

1. **Stack Trace Secret Sanitization**: Stack traces pass through regex scrubbers to strip embedded authorization headers, API keys, or raw connection strings prior to logging.
2. **Crash Loop Backoff**: If a process crashes > 3 times in 60 seconds, Exception Handler marks the node as `DEGRADED` and pauses automatic restarts.

---

## 4. Verification Protocol

```bash
agy verify-exception-handler --test-sanitization
```
Triggers synthetic unhandled errors, checks stack trace scrubber outputs, verifies telemetry logging, and validates fatal callbacks.
