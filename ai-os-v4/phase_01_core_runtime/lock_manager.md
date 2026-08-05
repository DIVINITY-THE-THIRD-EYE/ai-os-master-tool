---
title: Distributed Lock Manager Specification
document_id: SPEC-P01-SAFE-030
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core Kernel Architecture Group
last_updated: 2026-08-05
---

# Distributed Lock Manager Specification

## Executive Summary
This document specifies the Distributed Lock Manager (`lock_manager`), implementing Redlock/Redis distributed locking, 2PC lock coordination, reentrant locks, deadlock detection, and automatic lease renewal for shared resources in AI OS v4.

---

## 1. Lock Manager Architecture

```text
[ AGENT PROCESS A ]                        [ AGENT PROCESS B ]
        │                                          │
        ▼ AcquireLock("resource-01")               ▼ AcquireLock("resource-01")
+-------------------------------------------------------------------------+
|                        DISTRIBUTED LOCK MANAGER                         |
|  - Engine: Redlock / Distributed Lease Store                            |
|  - Automatic Lease Renewal Worker (Heartbeat every TTL / 3)             |
|  - Deadlock Detection Graph Engine (Cycle Check)                        |
+-------------------------------------------------------------------------+
        │                                          │
        ▼ (Lock Granted)                           ▼ (Lock Denied / Queued)
   [ EXECUTING ]                              [ WAITING ON LOCK ]
```

---

## 2. Lock Manager API Contract

```typescript
export interface LockLease {
  readonly lockKey: string;
  readonly lockToken: string;
  readonly leaseDurationMs: number;
  readonly acquiredAt: number;
}

export interface ILockManager {
  acquireLock(lockKey: string, ttlMs?: number, retryAttempts?: number): Promise<LockLease | null>;
  releaseLock(lease: LockLease): Promise<boolean>;
  renewLock(lease: LockLease, extensionMs: number): Promise<boolean>;
  detectDeadlocks(): Promise<string[][]>; // Returns cycle paths
}
```

---

## 3. Invariants & Safety Protocols

1. **Cryptographic Lock Fencing**: Released or expired locks generate fenced token increments. Stale processes presenting outdated fence tokens are rejected by storage engines.
2. **Mandatory Lock Leases**: All locks MUST specify finite lease durations (default 10,000ms). Infinite or non-expiring locks are forbidden.

---

## 4. Verification Protocol

```bash
agy verify-lock-manager --test-redlock --test-deadlock
```
Tests distributed lock acquisition, verifies lease renewal heartbeats, simulates process crashes to test lock expiration, and validates deadlock detection graphs.
