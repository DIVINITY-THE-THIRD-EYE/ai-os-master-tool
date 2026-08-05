---
title: "High-Speed PCB Design & EMC Verification Workflow"
document_id: "SPEC-P12-ELEC-WKF-001"
phase: "phase_12_domain_skill_packs"
domain: "electrical"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# High-Speed PCB Design & EMC Verification Workflow

## 1. Workflow Overview
The **High-Speed PCB Design & EMC Verification Workflow** specifies the end-to-end execution lifecycle for high-complexity initiatives in **Electrical & Power Engineering**. It coordinates domain agents, policy checks, artifact generation, and quality verification gates to deliver deterministic, production-grade results.

---

## 2. Process Architecture Diagram

```text
+-----------------------------------------------------------------------------------+
|                        High-Speed PCB Design & EMC Verification Workflow                        |
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
- **Action:** Parse input requirements; validate completeness against template `SPEC-P12-ELEC-TPL-001`.
- **Output:** Validated Task Context Object.

### Phase 2: Domain Engineering & Design Synthesis
- **Action:** Activate `Electrical & Embedded Systems Agent`. Query knowledge base `SPEC-P12-ELEC-KNB-001` for design patterns and standards (`IEEE 1584, IPC-2221, IEC 61000, NEC (NFPA 70), UL 60950-1`).
- **Output:** Candidate Design Draft & Architecture Diagrams.

### Phase 3: Governance Policy Check
- **Action:** Evaluate draft against Policy `SPEC-P12-ELEC-POL-001`.
- **Gate:** If compliance check returns any CRITICAL violation, halt execution and send rework payload to Phase 2.

### Phase 4: Full Artifact Construction
- **Action:** Synthesize final technical artifacts, configuration files, and documentation using tech stack: `Altium Designer, KiCad, SPICE, STM32CubeIDE, MATLAB/Simulink, Oscilloscopes, Spectrum Analyzers`.
- **Output:** Complete Deliverable Package.

### Phase 5: Verification Gate Audit
- **Action:** Execute verification suite `SPEC-P12-ELEC-VRF-001`. Calculate quantitative quality score.
- **Gate:** Pass threshold >= 0.95.

### Phase 6: Final Commit & Deployment Handoff
- **Action:** Register completed artifact with cryptographic signature in enterprise registry. Return final success payload.

---

## 4. Declarative Workflow DSL Definition (YAML)
```yaml
workflow_dsl:
  workflow_id: "WKF-ELEC-001"
  title: "High-Speed PCB Design & EMC Verification Workflow"
  domain: "electrical"
  steps:
    - step_id: "step_1_ingest"
      action: "validate_input"
    - step_id: "step_2_design"
      agent: "Electrical & Embedded Systems Agent"
      action: "synthesize_design"
    - step_id: "step_3_policy"
      policy: "SPEC-P12-ELEC-POL-001"
      action: "evaluate_governance"
    - step_id: "step_4_synthesize"
      action: "build_artifacts"
    - step_id: "step_5_verify"
      verification: "SPEC-P12-ELEC-VRF-001"
      action: "audit_quality"
```
