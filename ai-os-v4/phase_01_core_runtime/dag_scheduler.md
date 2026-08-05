---
title: Directed Acyclic Graph (DAG) Scheduler Specification
document_id: SPEC-P01-SCHED-019
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core Scheduler Group
last_updated: 2026-08-05
---

# Directed Acyclic Graph (DAG) Scheduler Specification

## Executive Summary
This document specifies the DAG Scheduler (`dag_scheduler`), responsible for parsing multi-agent workflow directed graphs, topological sorting, dependency validation, cycle detection, node state evaluation, and parallel branch dispatching in AI OS v4.

---

## 1. DAG Execution Architecture

```text
[ WORKFLOW DEFINITION (DSL / JSON) ]
                 │
                 ▼
+-----------------------------------------------------------------+
| 1. CYCLE DETECTION & TOPOLOGICAL SORT (Kahn's Algorithm)        |
+-----------------------------------------------------------------+
                 │
                 ▼
+-----------------------------------------------------------------+
| 2. READY NODE EVALUATION (All parent dependencies completed)    |
+-----------------------------------------------------------------+
                 │
                 ├── Node A Completed ──> Ready: [ Node B, Node C ] (Parallel Dispatch)
                 └── Node B/C Completed ─> Ready: [ Node D ] (Join Node)
                 │
                 ▼
[ PARALLEL SCHEDULER DISPATCH POOL ]
```

---

## 2. DAG Task Graph Schema & Interface Contract

```typescript
export interface DAGNode {
  readonly nodeId: string;
  readonly agentRole: string;
  readonly dependencies: string[]; // List of parent nodeIds
  readonly status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED" | "SKIPPED";
  readonly payload: Record<string, unknown>;
}

export interface DAGGraph {
  readonly graphId: string;
  readonly nodes: Record<string, DAGNode>;
}

export interface IDAGScheduler {
  validateGraph(graph: DAGGraph): { isValid: boolean; cyclePath?: string[] };
  getReadyNodes(graph: DAGGraph): DAGNode[];
  markNodeStatus(graphId: string, nodeId: string, status: DAGNode["status"]): Promise<DAGGraph>;
}
```

---

## 3. Scheduling Invariants & Topological Validation

1. **Strict Cycle Rejection**: Graphs containing circular dependencies (`Node A -> Node B -> Node A`) are rejected immediately with `ERR-SCHED-DAG-CYCLE`.
2. **Deterministic Join Nodes**: Join nodes with multiple dependencies execute ONLY after ALL parent dependencies transition to `COMPLETED`.

---

## 4. Verification Protocol

```bash
agy verify-dag-scheduler --test-cycles --test-topological-sort
```
Runs topological sort verification, tests graph cycle rejection algorithms, and validates parallel node execution streams.
