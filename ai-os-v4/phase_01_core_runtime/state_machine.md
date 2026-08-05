---
title: Machine-Readable Agent State Machine Specification
document_id: SPEC-P01-KERN-005
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core Kernel Architecture Group
last_updated: 2026-08-05
---

# Machine-Readable Agent State Machine Specification

## Executive Summary
This document specifies the formal state machine (`state_machine`) governing agent runtime lifecycles. It defines the state transition matrix, guard conditions, side-effect actions, and state persistence rules enforced by the AI OS v4 kernel.

---

## 1. Formal State Transition Matrix

```text
               ┌────────────────────────────────────────────────────────┐
               │                                                        │
               ▼                                                        │
      [ INITIALIZATION ] ──(AgentRegistered)──> [ READY ]               │
                                                  │                     │
                                           (TaskAssigned)               │
                                                  │                     │
                                                  ▼                     │
                                           [ SCHEDULING ]               │
                                                  │                     │
                                           (ContextLoaded)              │
                                                  │                     │
                                                  ▼                     │
┌─────────────────── [ EXECUTING ] <──────────────┘                     │
│                           │                                           │
│                 (SelfValidationPassed)                                │
│                           │                                           │
│                           ▼                                           │
│                    [ UNDER_REVIEW ] ──(PolicyViolation)──┐            │
│                           │                              │            │
│                  (VerificationPassed)                    │            │
│                           │                              ▼            │
│                           ▼                      [ RECOVERY ] ────────┘
│                     [ COMPLETED ]                        │
│                                                 (MaxRetriesExceeded)
│                                                          │
└────────────(ResourceExhausted / Fault)───────────────────┼──> [ FAILED ]
```

---

## 2. Machine-Readable Transition Rules Table

| Current State | Trigger Event | Next State | Guard Condition / Action |
| :--- | :--- | :--- | :--- |
| `INITIALIZATION` | `AgentRegistered` | `READY` | Load config, verify tool permissions |
| `READY` | `TaskAssigned` | `SCHEDULING` | Check token & CPU quota reservation |
| `SCHEDULING` | `ContextLoaded` | `EXECUTING` | Bind sandbox container & acquire locks |
| `EXECUTING` | `SelfValidationPassed` | `UNDER_REVIEW` | Submit report to Verification Engine |
| `EXECUTING` | `ResourceExhausted` | `RECOVERY` | Save checkpoint; enqueue retry |
| `UNDER_REVIEW` | `VerificationPassed` | `COMPLETED` | Flush candidate memory & release locks |
| `UNDER_REVIEW` | `PolicyViolation` | `RECOVERY` | Escalate to Orchestrator for rework |
| `RECOVERY` | `RetryApproved` | `INITIALIZATION` | Reset environment; reload checkpoint |
| `RECOVERY` | `MaxRetriesExceeded`| `FAILED` | Emit `TaskFailedEvent` & write audit log |

---

## 3. Invariants & Guard Rule Engine

1. **Direct Execution Block**: `COMPLETED` and `FAILED` states are terminal and immutable. No event can transition an agent directly out of `EXECUTING` to `COMPLETED` without traversing `UNDER_REVIEW`.
2. **Deterministic State Auditing**: Every state transition emits a signed `AgentStateChangedEvent` containing timestamps, trigger event names, and state delta hashes.

---

## 4. Verification Protocol

```bash
agy verify-state-machine --matrix-check strict
```
Executes complete state transition simulation, tests forbidden transition blocks, and checks guard rule execution.
