# Standard Operating Procedure: SOP-009

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-009
- **Title**: Post-Execution Reflection, Root Cause Analysis (RCA), and Continuous Knowledge Improvement
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Machine Reflection, Learning Engine, & Knowledge Management

---

## 2. Purpose & Objectives
The purpose of SOP-009 is to establish an automated, continuous learning feedback loop that extracts structural insights, refines system prompts, codifies anti-patterns, updates domain rules, and improves multi-agent execution efficiency after every workflow run or operational incident.

### Key Objectives:
1. **Systemic Root Cause Analysis**: Perform standard 5-Whys RCA on all incidents and task failures to identify underlying systemic flaws rather than surface symptoms.
2. **Anti-Pattern Codification**: Identify repeating code smells, inefficient DAG topologies, or agent hallucinations and publish preventative rules to `knowledge/anti_patterns/`.
3. **Prompt & Workflow Optimization**: Continuously tune agent system prompts and workflow definitions to reduce token usage by $\ge 15\%$ and execution time by $\ge 10\%$.
4. **Knowledge Graph Enrichment**: Incrementally update internal domain ontologies, decision rules, and capability matrices based on verified real-world execution data.

---

## 3. Scope & Applicability
This procedure applies to:
- Post-task execution reflection, post-incident RCA processing, prompt template refinement, anti-pattern logging, and memory store updates.
- The **Reflection & Learning Agent (A10)** as primary authority, in coordination with the **Task Planner (A04)**, **Solution Architect (A03)**, and **Master Orchestrator (A01)**.

This procedure does **not** cover real-time incident emergency mitigation (SOP-008) or active release traffic deployment (SOP-007).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Resolution of a operational incident (receipt of `incident_report.json` from SOP-008).
- **Trigger Condition 2**: Successful completion of a major release deployment milestone (from SOP-007).
- **Trigger Condition 3**: Completion of a batch workflow execution run containing $\ge 10$ executed tasks.
- **Frequency**: Milestone-driven, post-incident, or scheduled batch cycle (e.g., daily/weekly audit).

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Execution logs, audit trails, and token consumption metrics collected in log repository (`logs/audit/sops/`).
- Read/write access to `knowledge/` platform subdirectories (`lessons_learned/`, `anti_patterns/`, `prompt_library/`).
- Active reflection rules loaded from `policies/learning_policy.yaml`.

### Required Inputs
1. `execution_history_manifest` (JSON array, required): Log files and metrics from recent workflow runs.
2. `incident_reports_index` (JSON array, optional): Incident artifacts generated during SOP-008.
3. `current_knowledge_base` (Directory path, required): Existing patterns, prompts, and ontology files.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Reflection Agent** | A10_ReflectionLearning | **Accountable (A) / Responsible (R)** | Analyzes execution traces, runs 5-Whys RCA, authors patterns/anti-patterns. |
| **Solution Architect** | A03_Architect | **Consulted (C)** | Validates proposed architectural pattern changes and ontology updates. |
| **Task Planner** | A04_TaskPlanner | **Consulted (C)** | Reviews DAG structural efficiency and task sizing feedback. |
| **QA Verification Agent** | A06_QAVerifier | **Consulted (C)** | Verifies prompt optimizations do not cause functional regression. |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Approves and reloads updated system prompts and knowledge packs. |

---

## 7. Step-by-Step Execution Procedure

```
 [Execution / Incident Logs] ---> (Step 1: Telemetry & Log Ingestion)
                                         |
                                         v
                                  (Step 2: Efficiency & Delta Analysis)
                                         |
                                         v
                                  (Step 3: 5-Whys RCA & Pattern Detection)
                                         |
                                         v
                                  (Step 4: Anti-Pattern & Lesson Extraction)
                                         |
                                         v
                                  (Step 5: Prompt & Workflow Optimization Draft)
                                         |
                                         v
                                  (Step 6: Regression Verification Test)
                                         |
           +-----------------------------+-----------------------------+
           | Regression Check FAIL                                     | Regression Check PASS
           v                                                           v
(Discard Prompt Optimization)                               (Step 7: Knowledge Base Commit)
           |                                                           |
           +----------------------------->+----------------------------+
                                          |
                                          v
                              [learning_reflection_report.json]
```

### Step 1: Telemetry & Log Ingestion
- **1.1 Data Aggregation**: Aggregate audit logs, task durations, token consumption metrics, self-correction retry counts, and test failure rates across target execution runs.
- **1.2 Benchmark Comparison**: Compare actual execution metrics against baseline performance metrics defined in `policies/learning_policy.yaml`.

### Step 2: Efficiency & Variance Analysis
- **2.1 Token Variance Calculation**: Identify tasks exhibiting token consumption $> 200\%$ above mean baseline.
- **2.2 Retry Variance Calculation**: Pinpoint task steps requiring multiple self-correction loops ($Retries \ge 2$).
- **2.3 Bottleneck Identification**: Determine critical-path bottlenecks in execution DAG topology.

### Step 3: Root Cause Analysis (5-Whys Methodology)
- **3.1 Failure / Inefficiency Deconstruction**: Apply recursive 5-Whys breakdown:
  - *Why 1*: Task 004 failed unit tests.
  - *Why 2*: Code generator generated deprecated API signature.
  - *Why 3*: System prompt for Lead Dev lacked explicit version bounds.
  - *Why 4*: Requirements intake (SOP-001) did not enforce framework version constraint.
  - *Why 5*: Domain ontology missing framework version mapping schema (Root Cause).

### Step 4: Anti-Pattern & Lesson Extraction
- **4.1 Anti-Pattern Formatting**: Format identified bad practice into structured markdown file in `knowledge/anti_patterns/AP-XXX_<name>.md`:
  - Context & Symptom
  - Root Cause Explanation
  - Corrective Pattern / Rule
  - Automated Detection Pattern (Regex / Static rule)
- **4.2 Best Practice Logging**: Log success pattern to `knowledge/best_practices/BP-XXX_<name>.md`.

### Step 5: Prompt & Workflow Optimization Proposal
- **5.1 Prompt Modification**: Draft updated system prompt templates in `knowledge/prompt_library/` incorporating explicit negative constraints to eliminate identified failure modes.
- **5.2 DAG Optimizer Rules**: Update task decomposition heuristics (e.g., lower max task LOC from 250 to 150 for complex algorithm tasks).

### Step 6: Regression & Benchmark Verification
- **6.1 Benchmark Suite Run**: Test proposed prompt modifications against baseline prompt benchmark suite (`tests/benchmarks/prompt_eval.py`).
- **6.2 Regression Check**: Ensure new prompt yields $100\%$ functional accuracy without introducing hallucination regressions.

### Step 7: Knowledge Base Commit & Memory Synchronization
- **7.1 Knowledge Versioning**: Version and commit updated knowledge files to system repository.
- **7.2 Runtime Cache Invalidation**: Dispatch cache refresh signal to all active agents to reload updated prompts and domain rules dynamically.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 9: Reflection & Learning Gate
--------------------------------------------------------------------------------------
Check Metric                         | Target Requirement | PASS Action | FAIL Action
--------------------------------------------------------------------------------------
RCA 5-Whys Completeness              | 5-Level Depth      | Advance     | Reject Incomplete RCA
Pattern Confidence Index             | >= 0.85            | Publish     | Quarantine Pattern
Prompt Benchmark Accuracy Delta      | >= 0% (No Loss)    | Commit      | Rollback Prompt Change
Token Efficiency Gain                | Target >= 10%      | Log Metric  | Refine Optimization
--------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- 5-Whys RCA completed for all processed incidents/failures.
- At least one actionable lesson learned or anti-pattern codified per incident.
- Prompt optimization pass benchmark verification without regression.
- Knowledge base updated and synchronized across system memory.

### Deliverables
1. `knowledge/artifacts/learning/learning_reflection_report.json` — Summary of reflection findings.
2. `knowledge/anti_patterns/AP-XXX_*.md` — New anti-pattern specification files.
3. `knowledge/lessons_learned/LESSON-XXX_*.md` — Formatted lesson learned documents.
4. `knowledge/prompt_library/v2/` — Optimized system prompt templates.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Contradictory Knowledge Extraction**
  - *Action*: Suspend automated knowledge base commit. Flag proposed rule as `CONFLICTING_KNOWLEDGE`.
  - *Escalation*: Escalate to Solution Architect (A03) for human review and semantic reconciliation.
- **Failure Scenario B: Prompt Optimization Causes Functional Regression**
  - *Action*: Discard proposed prompt changes immediately. Retain previous stable prompt version.
  - *Escalation*: Log regression diagnostic details and retry prompt engineering loop.

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log generated upon completion of learning reflection cycle, stored at `logs/audit/sops/sop_009_audit.json`:

```json
{
  "sop_id": "SOP-009",
  "execution_id": "exec_20260805_009812",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A10_ReflectionLearning",
  "reflection_metrics": {
    "incidents_analyzed": 1,
    "rca_depth": 5,
    "anti_patterns_added": 1,
    "lessons_learned_added": 2,
    "prompts_optimized": 1,
    "token_reduction_estimated_pct": 18.4,
    "benchmark_regression_pass": true
  },
  "deliverable_path": "knowledge/artifacts/learning/learning_reflection_report.json",
  "verification_status": "PASSED",
  "signature": "3b2a1f0e9d8c..."
}
```
