# Phase 09 — Verification Platform
## Specification 09.12: Quality Gate Manager Architecture (`quality_gate_manager.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-12` |
| **Title** | Quality Gate Manager & Phase Transition Governance |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Quality Gate & Phase Transition Governance` |
| **Dependencies** | `SPEC-09-01 (Verification Engine)`, `SPEC-01-05 (State Machine)`, `SPEC-07-09 (Approval Gates)` |

---

## 1. Executive Summary

The **Quality Gate Manager (QGM)** is the final decision-making authority that governs task completion, artifact publishing, and phase-to-phase transitions in AI OS v4. Aggregating verification reports from all 10 checkers in the Verification Platform, the QGM enforces threshold policies, checks for human/governance approval overrides, emits atomic state transition events (`VerificationPassedEvent` vs `QualityGateFailedEvent`), and triggers automated rollbacks if quality gates fail.

---

## 2. Architectural Overview & Quality Gate Decision Pipeline

```text
                  +----------------------------------------------+
                  |  Verification Engine Aggregated Report       |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |   Phase Gate Policy Matrix Evaluator         |
                  |   (Calculates Threshold & Mandatory Rules)   |
                  +----------------------+-----------------------+
                                         |
                                         v
+----------------------------------------+----------------------------------------+
|                                        |                                        |
v                                        v                                        v
+-----------------------+  +-----------------------+  +-----------------------+
| Rule 1: Zero FATAL /  |  | Rule 2: Quality Score |  | Rule 3: Governance    |
| CRITICAL Violations   |  | Q >= Phase Threshold  |  | Override Check        |
+-----------------------+  +-----------------------+  +-----------------------+
|                                        |                                        |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |      Quality Gate Decision Evaluator         |
                  +----------+------------------------+----------+
                             |                        |
               +-------------+                        +-------------+
               v                                                    v
+--------------+---------------+                    +---------------+---------------+
| GATE PASSED                  |                    | GATE REJECTED                 |
| Emit VerificationPassedEvent |                    | Emit QualityGateFailedEvent   |
| Agent State -> Completed     |                    | Trigger Rollback / FAE Retry  |
+------------------------------+                    +-------------------------------+
```

---

## 3. Phase Quality Gate Threshold Matrix

| System Phase / Milestone | Minimum Quality Score ($Q$) | Mandatory Checkers Required | Allowed Critical Defects |
| :--- | :--- | :--- | :--- |
| **Phase 0-1 (Core Runtime)** | $95.0$ | OutputValidator, Architecture, Logic, Security | $0$ |
| **Phase 2-4 (Agents & Workflows)** | $90.0$ | OutputValidator, Logic, Consistency, Performance | $0$ |
| **Phase 5-8 (Knowledge & Learning)**| $88.0$ | OutputValidator, Consistency, Compliance, Security | $0$ |
| **Phase 9-16 (Platform & Enterprise)**| $90.0$ | All 10 Checkers Active | $0$ |

---

## 4. Technical Data Structures & Schemas

### 4.1 Quality Gate Scorecard Interface (TypeScript)

```typescript
export interface QualityGateScorecard {
  gateExecutionId: string; // Format: "QG-YYYYMMDD-XXXX"
  taskId: string;
  targetPhase: string;
  timestamp: string;
  verificationReportId: string;
  overallScore: number; // 0.0 to 100.0
  thresholdRequired: number;
  gateStatus: 'APPROVED' | 'REJECTED' | 'OVERRIDDEN_BY_HUMAN';
  evaluationDetails: {
    fatalDefectsCount: number;
    criticalDefectsCount: number;
    majorDefectsCount: number;
    mandatoryCheckersPassed: boolean;
  };
  overrideRecord?: {
    approvedByUserId: string;
    reason: string;
    overrideTimestamp: string;
  };
  actionsTriggered: string[]; // e.g., ["EMIT_VERIFICATION_PASSED_EVENT", "RELEASE_MEMORY_LOCKS"]
}
```

### 4.2 Quality Gate Scorecard Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QualityGateScorecard",
  "type": "object",
  "required": [
    "gateExecutionId",
    "taskId",
    "targetPhase",
    "timestamp",
    "verificationReportId",
    "overallScore",
    "thresholdRequired",
    "gateStatus",
    "evaluationDetails",
    "actionsTriggered"
  ],
  "properties": {
    "gateExecutionId": { "type": "string", "pattern": "^QG-[0-9]{8}-[A-Z0-9]{6}$" },
    "taskId": { "type": "string" },
    "targetPhase": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "verificationReportId": { "type": "string" },
    "overallScore": { "type": "number", "minimum": 0, "maximum": 100 },
    "thresholdRequired": { "type": "number" },
    "gateStatus": { "type": "string", "enum": ["APPROVED", "REJECTED", "OVERRIDDEN_BY_HUMAN"] },
    "evaluationDetails": {
      "type": "object",
      "required": ["fatalDefectsCount", "criticalDefectsCount", "mandatoryCheckersPassed"],
      "properties": {
        "fatalDefectsCount": { "type": "integer" },
        "criticalDefectsCount": { "type": "integer" },
        "mandatoryCheckersPassed": { "type": "boolean" }
      }
    },
    "actionsTriggered": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

---

## 5. Decision Rules & Automatic Rollback Protocol

```text
IF fatalDefectsCount > 0 OR criticalDefectsCount > 0:
    ==> GateStatus = REJECTED
    ==> Action: Trigger Automatic Rollback of candidate artifacts; emit QualityGateFailedEvent to FAE.

IF overallScore < thresholdRequired AND NO valid overrideRecord exists:
    ==> GateStatus = REJECTED
    ==> Action: Route to Failure Analysis Engine for retry or human escalation.

IF overallScore >= thresholdRequired AND fatalDefectsCount == 0 AND criticalDefectsCount == 0:
    ==> GateStatus = APPROVED
    ==> Action: Emit VerificationPassedEvent; unlock agent state transition to Completed.
```

---

## 6. System Configuration

```yaml
quality_gate_manager:
  enabled: true
  strict_mode: true
  allow_human_overrides: true
  rollback_strategy: "GIT_REVERT_AND_PURGE_CANDIDATE_MEMORY"
  publishing:
    event_bus_topic: "platform.quality_gates"
```

---

## 7. Verification & Audit Criteria

- **State Machine Enforcement**: Confirm 0 state transitions to `Completed` occur when `GateStatus == REJECTED`.
- **Scorecard Auditing**: 100% of quality gate evaluations must generate immutable `QualityGateScorecard` JSON records in the audit log repository.
