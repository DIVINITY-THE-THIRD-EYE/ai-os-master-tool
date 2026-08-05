# Standard Operating Procedure: SOP-003

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-003
- **Title**: Task Decomposition, Directed Acyclic Graph (DAG) Construction, and Work Package Generation
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Task Planning & Multi-Agent Workflow Scheduling

---

## 2. Purpose & Objectives
The purpose of SOP-003 is to establish an automated, deterministic process for breaking down high-level architectural specifications into fine-grained, atomic, independent, and testable tasks structured into an executable Directed Acyclic Graph (DAG).

### Key Objectives:
1. **Atomicity & Isolation**: Ensure each work unit is bounded, self-contained, and implementable within a single agent execution turn.
2. **Dependency Management**: Construct explicit execution dependency trees, eliminating implicit coupling and preventing race conditions or deadlock loops.
3. **Parallel Execution Optimization**: Maximize parallel execution width across independent DAG branches to minimize total system execution wall-clock time.
4. **Contractual Verifiability**: Attach unambiguous entry/exit criteria and verification test suites to every generated task specification.

---

## 3. Scope & Applicability
This procedure applies to:
- Task plan synthesis, DAG compilation, work package serialization, and execution scheduling.
- The **Task Decomposition Specialist (A04)**, working in coordination with the **Solution Architect (A03)**, **Lead Developer (A05)**, and **Master Orchestrator (A01)**.

This procedure does **not** cover direct source code implementation (SOP-004) or system-level integration testing (SOP-005).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Successful signature and hash validation of `architecture_spec.json` (from SOP-002).
- **Trigger Condition 2**: Re-planning mandate issued due to task-level recovery failure during SOP-008.
- **Frequency**: Executed once per architecture release baseline or major feature iteration.

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Validated `architecture_spec.json` and API contract schemas.
- Active agent capability registry loaded from `platform/capability_registry.yaml`.
- State machine transition to state `STATE_DECOMPOSITION`.

### Required Inputs
1. `architecture_spec.json` (JSON object, required): Target system architecture blueprint.
2. `requirements_spec.json` (JSON object, required): Requirement mapping context.
3. `agent_capacity_matrix` (JSON object, required): Operational load limits and skill mappings for active implementer agents.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Task Planner** | A04_TaskPlanner | **Accountable (A) / Responsible (R)** | Decomposes modules, builds DAG topology, generates work packages. |
| **Solution Architect** | A03_Architect | **Consulted (C)** | Reviews task boundary alignment with architectural interfaces. |
| **Lead Developer** | A05_LeadDev | **Consulted (C)** | Validates task sizing, complexity estimates, and implementability. |
| **QA Verification Agent** | A06_QAVerifier | **Consulted (C)** | Ensures every task includes automated verification assertions. |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Ingests compiled DAG for runtime execution dispatch. |

---

## 7. Step-by-Step Execution Procedure

```
 [architecture_spec.json] ---> (Step 1: Module Extraction)
                                      |
                                      v
                               (Step 2: Task Sizing & Slicing)
                                      |
                                      v
                               (Step 3: Dependency Graph / DAG Construction)
                                      |
                                      v
                               (Step 4: Cycle Detection & Topology Verification)
                                      |
                                      v
                               (Step 5: Agent Capability & Load Assignment)
                                      |
                                      v
                               (Step 6: Work Package Serialization)
                                      |
                                      v
                           [execution_dag.json]
```

### Step 1: Module Extraction & Subsystem Partitioning
- **1.1 Component Parsing**: Read `architecture_spec.json` and break down each component into functional units (e.g., Data Models, Interfaces, Business Logic, Persistence, Integration Adapters).
- **1.2 Cross-Cutting Identification**: Separate infrastructure setup tasks (logging, configuration, security middleware) into root-level baseline nodes.

### Step 2: Task Sizing & Atomicity Verification
- **2.1 Sizing Thresholds**: Enforce strict constraints on task size:
  - Max Estimated LOC per Task: $\le 250 \text{ lines}$.
  - Max Expected Execution Duration: $\le 15 \text{ minutes}$.
  - Single Responsibility Principle (SRP): Each task modifies $\le 2$ closely related files.
- **2.2 Oversized Task Splitting**: If a task exceeds complexity limits, recursively partition it into sub-tasks (e.g., `Task-01A`, `Task-01B`).

### Step 3: Directed Acyclic Graph (DAG) Construction
- **3.1 Node Creation**: Create a unique task node ID (`TASK-XXX`) for each atomic work unit containing scope description, target file paths, and input/output contracts.
- **3.2 Edge Construction**: Define directed edges (`TASK-A` $\rightarrow$ `TASK-B`) representing strict prerequisite ordering (e.g., interface contract must precede component implementation).

### Step 4: Dependency Graph Verification & Cycle Detection
- **4.1 Topological Sort**: Run Kahn's algorithm or Depth-First Search (DFS) topological sort on candidate graph.
- **4.2 Cycle Check**: If any cycle is detected ($Nodes_{in\_degree} > 0$ with no zero-in-degree nodes remaining), abort and throw `ERR_DAG_CYCLE_DETECTED`.
- **4.3 Orphan Node Audit**: Verify that no unlinked orphan nodes exist unless explicitly flagged as independent root tasks.

### Step 5: Agent Capability & Resource Assignment
- **5.1 Skill Matching**: Query `platform/capability_registry.yaml` to assign the optimal implementer agent (e.g., Frontend Specialist, Backend Specialist, Database Specialist) to each task.
- **5.2 Load Balancing**: Cap maximum concurrent tasks assigned to any single agent instance to $\le 3$.

### Step 6: Work Package Serialization & Contract Locking
- **6.1 Manifest Assembly**: Format work package array into `execution_dag.json` conforming to `schemas/dag_schema.json`.
- **6.2 Unit Verification Attachment**: Attach automated verification commands (e.g., `pytest tests/unit/test_module_a.py`) to each task node.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 3: Task Decomposition Quality Gate
-------------------------------------------------------------------------------------
Check Condition                      | Threshold Target | Result = PASS | Result = FAIL
-------------------------------------------------------------------------------------
DAG Cycle Count                      | Exactly 0        | Advance       | Cyclic Dependency Fail
Max LOC per Task                     | <= 250 LOC       | Advance       | Re-split Task
Unassigned Capability Tasks          | Exactly 0        | Advance       | Unmapped Agent Skill
Verification Contract Attached       | 100% of Nodes    | Final Lock    | Missing Test Spec
-------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- Graph topological sort returns valid linear or parallel ordering without cycles.
- All task nodes have assigned implementer agents and explicit verification commands.
- `STATE_DECOMPOSITION` signed off by Task Planner (A04).

### Deliverables
1. `knowledge/artifacts/tasks/execution_dag.json` — Schema-validated execution DAG.
2. `knowledge/artifacts/tasks/work_packages.json` — Complete list of individual task manifests.
3. `knowledge/artifacts/tasks/task_plan_summary.md` — Visual task execution tree and timeline estimate.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Cyclic Dependency Failure**
  - *Action*: Halt graph compilation. Identify specific cyclic node list (`TASK-X -> TASK-Y -> TASK-X`).
  - *Escalation*: Trigger refactoring loop back to Solution Architect (A03) to break architectural coupling.
- **Failure Scenario B: Capability Resolution Deficit**
  - *Action*: Flag task as `UNASSIGNABLE_SKILL`.
  - *Escalation*: Escalate to Master Orchestrator (A01) to dynamically provision specialist sub-agent or trigger SOP-010.

---

## 11. Audit Logging & Compliance Recordkeeping
Audit record emitted upon task graph locking, logged at `logs/audit/sops/sop_003_audit.json`:

```json
{
  "sop_id": "SOP-003",
  "execution_id": "exec_20260805_003819",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A04_TaskPlanner",
  "input_architecture_hash": "b2c3d4e5f6a1...",
  "dag_metrics": {
    "total_tasks": 14,
    "max_parallel_width": 4,
    "critical_path_depth": 5,
    "cycle_count": 0,
    "unassigned_tasks": 0
  },
  "deliverable_path": "knowledge/artifacts/tasks/execution_dag.json",
  "verification_status": "PASSED",
  "signature": "1a2b3c4d5e..."
}
```
