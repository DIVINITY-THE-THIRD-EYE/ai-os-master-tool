---
title: System State Persister Specification
document_id: SPEC-P01-SAFE-033
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core State & Storage Group
last_updated: 2026-08-05
---

# System State Persister Specification

## Executive Summary
This document specifies the State Persister (`state_persister`), managing agent state serialization, checkpoint snapshots, Two-Phase Commit (2PC) write-ahead logging (WAL), state restoration, and multi-version concurrency control (MVCC) in AI OS v4.

---

## 1. State Persistence & Checkpoint Architecture

```text
[ RUNNING AGENT STATE MUTATION ]
               │
               ▼
+-----------------------------------------------------------------+
| 1. WRITE-AHEAD LOG (WAL) COMMIT                                 |
+-----------------------------------------------------------------+
               │
               ▼
+-----------------------------------------------------------------+
| 2. TWO-PHASE COMMIT (2PC) SNAPSHOT ENGINE                       |
|    - Phase 1: Prepare (Validate schema & lock target key)       |
|    - Phase 2: Commit (Persist state binary snapshot & checksum) |
+-----------------------------------------------------------------+
               │
               ▼
[ PERSISTENT STORAGE (PostgreSQL / RocksDB / S3 Checkpoint Bucket) ]
```

---

## 2. State Persister Schema & API Specification

```typescript
export interface CheckpointSnapshot {
  readonly checkpointId: string;
  readonly entityId: string; // Task or Session ID
  readonly stateVersion: number;
  readonly stateHash: string; // SHA-256
  readonly serializedData: Uint8Array;
  readonly timestamp: string;
}

export interface IStatePersister {
  saveCheckpoint(entityId: string, stateData: Record<string, unknown>): Promise<CheckpointSnapshot>;
  loadLatestCheckpoint(entityId: string): Promise<CheckpointSnapshot | null>;
  loadCheckpointVersion(entityId: string, version: number): Promise<CheckpointSnapshot | null>;
  verifyIntegrity(snapshot: CheckpointSnapshot): boolean;
}
```

---

## 3. Operational Rules & Checkpoint Integrity

1. **SHA-256 Checksum Validation**: Checkpoints are verified against SHA-256 state hashes prior to restoration. Corrupted snapshots trigger rollback to the previous valid version (`N-1`).
2. **Periodic Auto-Checkpointing**: Long-running workflow tasks generate automatic state snapshots every 60 seconds.

---

## 4. Verification Protocol

```bash
agy verify-state-persister --test-2pc --test-corruption-recovery
```
Saves state checkpoints, verifies 2PC atomic commits, simulates corrupt snapshot data, and tests state rollback recovery.
