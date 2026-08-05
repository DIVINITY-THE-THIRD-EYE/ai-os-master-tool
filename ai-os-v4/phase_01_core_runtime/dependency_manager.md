---
title: Task Dependency Manager Specification
document_id: SPEC-P01-SCHED-021
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core Scheduler Group
last_updated: 2026-08-05
---

# Task Dependency Manager Specification

## Executive Summary
This document specifies the Dependency Manager (`dependency_manager`), tracking explicit task prerequisites, artifact availability dependencies, schema contract fulfillment, and conditional branching evaluation for workflow scheduling in AI OS v4.

---

## 1. Dependency Resolution Pipeline

```text
[ TASK ENQUEUE REQUEST ] ──> [ DEPENDENCY MANAGER ]
                                    │
    ┌────────────────---------------+-------------------------------+
    ▼                               ▼                               ▼
[ Parent Task Status ]    [ Required Artifact Check ]    [ Input Schema Check ]
(Must be COMPLETED)       (Checksum & Path Valid)        (Validation Passed)
    │                               │                               │
    └────────────────---------------+-------------------------------+
                                    │
                                    ▼
                     [ DEPENDENCIES SATISFIED ] ──> Move Task to Ready Queue
```

---

## 2. Dependency Schema & API Specification

```typescript
export interface TaskDependency {
  readonly dependencyId: string;
  readonly type: "TASK_COMPLETION" | "ARTIFACT_EXISTS" | "EXPRESSION_TRUE";
  readonly targetId: string;
  readonly expression?: string; // Evaluated JS/Python expression
}

export interface IDependencyManager {
  addDependency(taskId: string, dependency: TaskDependency): Promise<void>;
  checkSatisfied(taskId: string): Promise<boolean>;
  getUnresolvedDependencies(taskId: string): Promise<TaskDependency[]>;
  resolveOnCompletion(completedTaskId: string): Promise<string[]>; // Returns now-ready taskIds
}
```

---

## 3. Operational Rules & Edge Cases

1. **Cascade Failure Handling**: If a parent task transitions to `FAILED`, dependent tasks without alternative conditional paths automatically transition to `SKIPPED`.
2. **Atomic Dependency Evaluation**: Dependency checks execute atomically to avoid race conditions when multiple parent tasks complete simultaneously.

---

## 4. Verification Protocol

```bash
agy verify-dependency-manager --test-cascade
```
Simulates parent task failures, validates cascade skip logic, checks artifact availability resolution, and tests expression evaluation.
