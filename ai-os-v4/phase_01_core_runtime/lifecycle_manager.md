---
title: System Lifecycle Manager Specification
document_id: SPEC-P01-KERN-008
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Platform Reliability Group
last_updated: 2026-08-05
---

# System Lifecycle Manager Specification

## Executive Summary
This document specifies the Lifecycle Manager (`lifecycle_manager`), governing orderly boot hooks, system component initialization ordering, shutdown orchestration, health transitions, and graceful drain procedures for AI OS v4 kernel nodes.

---

## 1. Subsystem Boot & Shutdown Dependency Graph

```text
[ STAGE 1: LOGGING & CONFIG ] ──> [ STAGE 2: SECURITY & METRICS ] ──> [ STAGE 3: BROKER & PERSISTENCE ]
                                                                                   │
[ STAGE 6: AGENT EXECUTION ]  <── [ STAGE 5: WORKER POOL READY ] <── [ STAGE 4: SCHEDULER & STATE ENGINE ]
```

Shutdown operates in exact reverse order (Stage 6 down to Stage 1).

---

## 2. Lifecycle Manager API Contract

```typescript
export type LifecycleHook = () => Promise<void>;

export interface ILifecycleManager {
  registerBootHook(stageName: string, hook: LifecycleHook, priority?: number): void;
  registerShutdownHook(stageName: string, hook: LifecycleHook, priority?: number): void;
  executeBootSequence(): Promise<void>;
  executeShutdownSequence(reason: string): Promise<void>;
  getLifecycleState(): "UNINITIALIZED" | "BOOTING" | "READY" | "DRAINING" | "SHUTDOWN";
}
```

---

## 3. Graceful Draining & Timeout Rules

1. **Graceful Draining Phase**: Upon receiving `SIGTERM`, Lifecycle Manager sets state to `DRAINING`, rejecting new incoming tasks while allowing active agent executions up to 30 seconds to reach an immutable checkpoint.
2. **Hard Timeout Enforcement**: If background processes fail to terminate within the 30-second drain window, hard shutdown is executed.

---

## 4. Verification Protocol

```bash
agy verify-lifecycle --test-drain
```
Executes mock boot sequence, triggers synthetic `SIGTERM`, verifies graceful drain execution, and confirms shutdown hook ordering.
