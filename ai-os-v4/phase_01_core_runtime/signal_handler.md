---
title: POSIX Signal Handler Specification
document_id: SPEC-P01-SAFE-031
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Process Infrastructure Team
last_updated: 2026-08-05
---

# POSIX Signal Handler Specification

## Executive Summary
This document specifies the Signal Handler (`signal_handler`), trapping, parsing, and routing OS signals (`SIGINT`, `SIGTERM`, `SIGUSR1`, `SIGUSR2`, `SIGHUP`, `SIGCHILD`) to system lifecycle managers and runtime process supervisors in AI OS v4.

---

## 1. Signal Handling Matrix

```text
[ POSIX OPERATING SYSTEM SIGNAL ]
               │
               ▼
+-----------------------------------------------------------------+
| SIGNAL HANDLER ENGINE                                           |
|                                                                 |
|  - SIGINT  / SIGTERM ──> Trigger Graceful Drain & Shutdown      |
|  - SIGUSR1           ──> Hot-Reload Configuration               |
|  - SIGUSR2           ──> Trigger On-Demand Memory Heap Dump    |
|  - SIGHUP            ──> Re-open Log Sinks                      |
|  - SIGCHLD           ──> Reap Zombie Processes                  |
+-----------------------------------------------------------------+
```

---

## 2. Signal Handler API Interface Contract

```typescript
export type SignalType = "SIGINT" | "SIGTERM" | "SIGUSR1" | "SIGUSR2" | "SIGHUP" | "SIGCHLD";

export interface ISignalHandler {
  registerSignalListener(signal: SignalType, handler: () => Promise<void>): void;
  removeSignalListener(signal: SignalType): void;
  dispatchSignal(signal: SignalType): Promise<void>;
}
```

---

## 3. Signal Safety Rules

1. **Re-entrant Thread Safety**: Signal handlers execute async-signal-safe routines, delegating complex shutdown work to the main event loop thread via atomic flags.
2. **Double SIGINT Override**: A second `SIGINT` received within 5 seconds forces an immediate non-graceful hard exit (`exit(130)`).

---

## 4. Verification Protocol

```bash
agy verify-signal-handler --test-signals SIGINT,SIGUSR1
```
Emits synthetic OS signals, verifies listener invocation, tests configuration hot-reload via `SIGUSR1`, and checks exit codes.
