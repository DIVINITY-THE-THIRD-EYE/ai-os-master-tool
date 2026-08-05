# Phase 08 — Reflection and Learning
## Specification 08.04: Improvement Suggestion Engine Architecture (`improvement_suggestion_engine.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-04` |
| **Title** | Improvement Suggestion Engine & Automated Patch Generation |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Autonomous Optimization` |
| **Dependencies** | `SPEC-08-01 (Reflection)`, `SPEC-08-03 (RCA)`, `SPEC-09-01 (Verification Engine)` |

---

## 1. Executive Summary

The **Improvement Suggestion Engine (ISE)** bridges reflection/diagnostic analysis and active platform optimization. Using the outputs from the Reflection, Failure Analysis, and Root Cause Analysis engines, the ISE automatically generates concrete, prioritized improvement proposals and machine-executable patches for prompt templates, workflow DAG definitions, agent policies, and tool configuration parameter files. Every proposal undergoes automated pre-verification before being dispatched to approval gates or applied directly via autonomous optimization policies.

---

## 2. Architectural Overview & Workflow

```text
+-------------------+     +-------------------+     +-------------------+
| Reflection Engine |     | RCA Artifact Store|     | Pattern Detection |
+---------+---------+     +---------+---------+     +---------+---------+
          |                         |                         |
          +-------------------------+-------------------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |   Improvement Suggestion Engine   |
                  |     (ISE Candidate Synthesizer)   |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  | Machine-Executable Patch Generator|
                  |  (Unified Diff / JSON Patch)      |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  | Priority Matrix & Impact Scorer   |
                  |   (ROI, Risk, Execution Effort)   |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  | Sandbox Pre-Verification Engine   |
                  | (Runs Test Suite on Patched Spec)|
                  +--------+----------------+---------+
                           |                |
             +-------------+                +-------------+
             v                                            v
+------------+-----------------+            +-------------+-----------------+
| Autonomous Auto-Apply (Low Risk)|            | Human Governance Approval Gate  |
| (Direct Commit to Repo)      |            | (High Impact / Policy Shift)    |
+------------------------------+            +---------------------------------+
```

---

## 3. Patch Target Types & Formats

The ISE produces patches across four primary target domain types:

1. **Prompt Patches (`PROMPT`)**:
   - Delivered as Git Unified Diff (`.patch`) targeting prompt template files in `phase_03_prompt_library/`.

2. **Workflow DAG Patches (`WORKFLOW`)**:
   - Delivered as JSON Patch (RFC 6902) or YAML mutation targeting workflow definitions in `phase_04_workflow_library/`.

3. **Agent Policy Patches (`POLICY`)**:
   - Delivered as structural YAML updates modifying timeout caps, token limits, or permission policies in `phase_14_runtime_policies/`.

4. **Tool Configuration Patches (`TOOL`)**:
   - Delivered as key-value configuration overrides for tool wrappers in `phase_13_plugin_framework/`.

---

## 4. Technical Data Structures & Schemas

### 4.1 Improvement Proposal Interface (TypeScript)

```typescript
export interface ImprovementProposal {
  proposalId: string; // Format: "PROP-YYYYMMDD-XXXX"
  sourceRcaId?: string;
  sourceReflectionId?: string;
  timestamp: string;
  targetComponent: {
    type: 'PROMPT' | 'WORKFLOW' | 'POLICY' | 'TOOL';
    pathOrKey: string;
    currentVersion: string;
  };
  rationale: string;
  priorityScore: number; // Calculated ROI score (0 to 100)
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  patchPayload: {
    format: 'GIT_DIFF' | 'JSON_PATCH_RFC6902' | 'YAML_OVERRIDE';
    content: string;
  };
  preVerificationStatus: 'UNTESTED' | 'PASSED' | 'FAILED';
  approvalRequired: boolean;
}
```

### 4.2 Improvement Proposal Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ImprovementProposal",
  "type": "object",
  "required": [
    "proposalId",
    "timestamp",
    "targetComponent",
    "rationale",
    "priorityScore",
    "riskLevel",
    "patchPayload",
    "preVerificationStatus",
    "approvalRequired"
  ],
  "properties": {
    "proposalId": { "type": "string", "pattern": "^PROP-[0-9]{8}-[A-Z0-9]{6}$" },
    "timestamp": { "type": "string", "format": "date-time" },
    "targetComponent": {
      "type": "object",
      "required": ["type", "pathOrKey", "currentVersion"],
      "properties": {
        "type": { "type": "string", "enum": ["PROMPT", "WORKFLOW", "POLICY", "TOOL"] },
        "pathOrKey": { "type": "string" },
        "currentVersion": { "type": "string" }
      }
    },
    "rationale": { "type": "string" },
    "priorityScore": { "type": "number", "minimum": 0, "maximum": 100 },
    "riskLevel": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"] },
    "patchPayload": {
      "type": "object",
      "required": ["format", "content"],
      "properties": {
        "format": { "type": "string", "enum": ["GIT_DIFF", "JSON_PATCH_RFC6902", "YAML_OVERRIDE"] },
        "content": { "type": "string" }
      }
    },
    "preVerificationStatus": { "type": "string", "enum": ["UNTESTED", "PASSED", "FAILED"] },
    "approvalRequired": { "type": "boolean" }
  }
}
```

---

## 5. Priority Matrix & Impact Scoring Algorithm

The Priority Score ($P$) is calculated using the following formula:

$$P = \frac{(\text{Expected SLA Gain} \times 0.4) + (\text{Historical Failure Frequency} \times 0.4)}{(\text{Patch Complexity} \times 0.2)} \times 100$$

- **Risk Assignment & Approval Rules**:
  - If `riskLevel == LOW` AND `P >= 75` AND `preVerificationStatus == PASSED` $\rightarrow$ `approvalRequired = false` (Auto-Apply).
  - If `riskLevel >= MEDIUM` OR `P < 75` $\rightarrow$ `approvalRequired = true` (Escalate to Governance Gate).

---

## 6. Pre-Verification Lifecycle

```text
Stage 1: Apply patch in isolated ephemeral Git branch / memory environment.
Stage 2: Execute Verification Engine regression test suite (`SPEC-09-10`).
Stage 3: Measure baseline vs patched metrics (Latency, Token Cost, Output Accuracy).
Stage 4: If regression detected --> Flag `preVerificationStatus = FAILED`; log regression report.
Stage 5: If pass --> Flag `preVerificationStatus = PASSED`; prepare patch commit payload.
```

---

## 7. System Configuration

```yaml
improvement_suggestion_engine:
  auto_apply_enabled: true
  max_auto_patches_per_day: 10
  allowed_auto_apply_types: ["PROMPT", "TOOL"]
  priority_threshold_auto_apply: 80.0
  pre_verification:
    timeout_seconds: 60
    sandbox_environment: "ephemeral_container"
```

---

## 8. Verification & Conformance Criteria

- **Patch Validity**: 100% of generated JSON patches must conform to RFC 6902; 100% of GIT_DIFF patches must apply cleanly without merge conflicts against HEAD.
- **Safety Gate**: Zero patches flagged with `preVerificationStatus == FAILED` shall ever be executed or auto-applied.
