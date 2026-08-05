---
title: "Subcontractor Procurement & On-Site Safety Audit Workflow"
document_id: "SPEC-P12-CONST-WKF-001"
phase: "phase_12_domain_skill_packs"
domain: "construction"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Subcontractor Procurement & On-Site Safety Audit Workflow

## 1. Workflow Overview
The **Subcontractor Procurement & On-Site Safety Audit Workflow** specifies the end-to-end execution lifecycle for high-complexity initiatives in **Construction Management**. It coordinates domain agents, policy checks, artifact generation, and quality verification gates to deliver deterministic, production-grade results.

---

## 2. Process Architecture Diagram

```text
+-----------------------------------------------------------------------------------+
|                        Subcontractor Procurement & On-Site Safety Audit Workflow                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Phase 1: Ingestion & Requirements]                                              |
|            |                                                                      |
|            v                                                                      |
|  [Phase 2: Domain Analysis & Design]  <--->  [Knowledge Base Retrieval]           |
|            |                                                                      |
|            v                                                                      |
|  [Phase 3: Policy Check & Safety Audit] ----> (Fail: Trigger Rework)              |
|            | (Pass)                                                               |
|            v                                                                      |
|  [Phase 4: Synthesis & Output Generation]                                         |
|            |                                                                      |
|            v                                                                      |
|  [Phase 5: Automated Verification Gate] ----> (Fail: Reject Deliverable)          |
|            | (Pass)                                                               |
|            v                                                                      |
|  [Phase 6: Final Commit & Handoff]                                                |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Step-by-Step Execution Phases

### Phase 1: Requirements Ingestion & Validation
- **Input:** Task specification document, user constraints, environment parameters.
- **Action:** Parse input requirements; validate completeness against template `SPEC-P12-CONST-TPL-001`.
- **Output:** Validated Task Context Object.

### Phase 2: Domain Engineering & Design Synthesis
- **Action:** Activate `Construction Project Manager Agent`. Query knowledge base `SPEC-P12-CONST-KNB-001` for design patterns and standards (`OSHA 1926, CSI MasterFormat, PMI PMBOK Construction, FIDIC Contracts`).
- **Output:** Candidate Design Draft & Architecture Diagrams.

### Phase 3: Governance Policy Check
- **Action:** Evaluate draft against Policy `SPEC-P12-CONST-POL-001`.
- **Gate:** If compliance check returns any CRITICAL violation, halt execution and send rework payload to Phase 2.

### Phase 4: Full Artifact Construction
- **Action:** Synthesize final technical artifacts, configuration files, and documentation using tech stack: `Procore, Primavera P6, Autodesk Build, RSMeans Cost Data, HeavyBid, DroneDeploy`.
- **Output:** Complete Deliverable Package.

### Phase 5: Verification Gate Audit
- **Action:** Execute verification suite `SPEC-P12-CONST-VRF-001`. Calculate quantitative quality score.
- **Gate:** Pass threshold >= 0.95.

### Phase 6: Final Commit & Deployment Handoff
- **Action:** Register completed artifact with cryptographic signature in enterprise registry. Return final success payload.

---

## 4. Declarative Workflow DSL Definition (YAML)
```yaml
workflow_dsl:
  workflow_id: "WKF-CONST-001"
  title: "Subcontractor Procurement & On-Site Safety Audit Workflow"
  domain: "construction"
  steps:
    - step_id: "step_1_ingest"
      action: "validate_input"
    - step_id: "step_2_design"
      agent: "Construction Project Manager Agent"
      action: "synthesize_design"
    - step_id: "step_3_policy"
      policy: "SPEC-P12-CONST-POL-001"
      action: "evaluate_governance"
    - step_id: "step_4_synthesize"
      action: "build_artifacts"
    - step_id: "step_5_verify"
      verification: "SPEC-P12-CONST-VRF-001"
      action: "audit_quality"
```
