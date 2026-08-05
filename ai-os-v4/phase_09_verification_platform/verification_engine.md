# Phase 09 — Verification Platform
## Specification 09.01: Verification Engine Architecture (`verification_engine.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-01` |
| **Title** | Verification Engine Architecture & Master Dispatch Pipeline |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Quality & Verification Platform` |
| **Dependencies** | `SPEC-01-01 (Kernel)`, `SPEC-01-02 (Event Bus)`, `SPEC-09-12 (Quality Gate)` |

---

## 1. Executive Summary

The **Verification Engine (VE)** is the core orchestrator of the AI OS Verification Platform. Operating in compliance with **Agent State Machine Transition Rules** (state `UnderReview`), the VE intercepts generated code, specifications, workflows, and enterprise artifacts prior to task completion. It coordinates parallel and sequential execution across 10 specialized checkers (Logic, Consistency, Architecture, Performance, Security, Compliance, Documentation, Accessibility, Regression, and Output Validation), aggregates diagnostic findings, and calculates a unified Quality Score.

---

## 2. Architectural Overview & Workflow Pipeline

```text
                                  +---------------------------------------+
                                  |   Worker Agent Artifact Submission    |
                                  |    (State: UnderReview Initiated)     |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |    Verification Engine Orchestrator  |
                                  |     (Check Suite Plan Generator)      |
                                  +-------------------+-------------------+
                                                      |
                   +----------------------------------+----------------------------------+
                   |                                  |                                  |
                   v                                  v                                  v
    +--------------+---------------+   +--------------+---------------+   +--------------+---------------+
    |  Parallel Checker Group A    |   |  Parallel Checker Group B    |   |  Parallel Checker Group C    |
    | (OutputValidator, Security,  |   | (Logic, Consistency,         |   | (Performance, Documentation, |
    |  Architecture Checkers)      |   |  Compliance Checkers)        |   |  Accessibility Checkers)      |
    +--------------+---------------+   +--------------+---------------+   +--------------+---------------+
                   |                                  |                                  |
                   +----------------------------------+----------------------------------+
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  | Aggregated Diagnostic & Score     |
                                  |           Calculator                  |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |  Quality Gate Manager Dispatch    |
                                  |  (PASSED -> Complete / REJECTED)  |
                                  +---------------------------------------+
```

---

## 3. Core Verification Pipeline Lifecycle

1. **Ingestion & Registry Binding**:
   - The VE intercepts worker artifacts via `SubmitArtifactForVerification()`.
   - Binds the artifact to its declared domain and schema registry.

2. **Check Suite Resolution**:
   - Resolves required checkers based on artifact target type (e.g., Code artifacts trigger Logic, Security, Architecture, Performance; UI artifacts trigger Accessibility, Documentation).

3. **Concurrent Suite Execution**:
   - Dispatches checkers in parallel threads/workers with per-checker timeout caps (default: 5000ms).

4. **Severity Matrix & Score Computation**:
   - Aggregates findings categorized into `FATAL`, `CRITICAL`, `MAJOR`, `MINOR`, and `INFO`.
   - Computes overall Quality Score ($Q \in [0.0, 100.0]$).

5. **Event Emission & State Transition**:
   - Emits `VerificationPassedEvent` or `VerificationFailedEvent`.

---

## 4. Technical Data Structures & Schemas

### 4.1 Verification Report Interface (TypeScript)

```typescript
export interface VerificationFinding {
  findingId: string;
  checkerId: string; // e.g., "CHECKER-SECURITY"
  ruleId: string; // e.g., "SEC-RULE-004"
  severity: 'FATAL' | 'CRITICAL' | 'MAJOR' | 'MINOR' | 'INFO';
  message: string;
  filePath?: string;
  lineNumber?: number;
  remediationHint?: string;
}

export interface VerificationReport {
  verificationId: string; // Format: "VRF-YYYYMMDD-XXXX"
  taskId: string;
  artifactId: string;
  timestamp: string;
  overallScore: number; // 0.0 to 100.0
  passed: boolean;
  checkerSummaries: Array<{
    checkerId: string;
    status: 'PASSED' | 'FAILED' | 'SKIPPED' | 'TIMEOUT';
    executionTimeMs: number;
    findingsCount: number;
  }>;
  detailedFindings: VerificationFinding[];
}
```

### 4.2 Verification Report Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VerificationReport",
  "type": "object",
  "required": [
    "verificationId",
    "taskId",
    "artifactId",
    "timestamp",
    "overallScore",
    "passed",
    "checkerSummaries",
    "detailedFindings"
  ],
  "properties": {
    "verificationId": { "type": "string", "pattern": "^VRF-[0-9]{8}-[A-Z0-9]{6}$" },
    "taskId": { "type": "string" },
    "artifactId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "overallScore": { "type": "number", "minimum": 0, "maximum": 100 },
    "passed": { "type": "boolean" },
    "checkerSummaries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["checkerId", "status", "executionTimeMs", "findingsCount"],
        "properties": {
          "checkerId": { "type": "string" },
          "status": { "type": "string", "enum": ["PASSED", "FAILED", "SKIPPED", "TIMEOUT"] },
          "executionTimeMs": { "type": "number" },
          "findingsCount": { "type": "integer" }
        }
      }
    },
    "detailedFindings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["findingId", "checkerId", "ruleId", "severity", "message"],
        "properties": {
          "findingId": { "type": "string" },
          "checkerId": { "type": "string" },
          "ruleId": { "type": "string" },
          "severity": { "type": "string", "enum": ["FATAL", "CRITICAL", "MAJOR", "MINOR", "INFO"] },
          "message": { "type": "string" },
          "filePath": { "type": "string" },
          "lineNumber": { "type": "integer" },
          "remediationHint": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 5. Quality Score Deduction Formula

$$Q = \max\left(0, 100 - (N_{\text{FATAL}} \times 50) - (N_{\text{CRITICAL}} \times 20) - (N_{\text{MAJOR}} \times 10) - (N_{\text{MINOR}} \times 2)\right)$$

- **Pass Threshold**: $Q \ge 85.0$ AND $N_{\text{FATAL}} = 0$ AND $N_{\text{CRITICAL}} = 0$.

---

## 6. System Configuration

```yaml
verification_engine:
  parallel_execution: true
  max_concurrent_checkers: 10
  default_checker_timeout_ms: 5000
  pass_score_threshold: 85.0
  severity_weights:
    fatal: 50.0
    critical: 20.0
    major: 10.0
    minor: 2.0
  check_suite_matrix:
    CODE: ["OutputValidator", "Security", "Architecture", "Logic", "Performance", "Regression"]
    DOC: ["Documentation", "Consistency", "Compliance"]
    UI: ["Accessibility", "OutputValidator", "Security"]
```

---

## 7. Verification Criteria & SLAs

- **Pipeline Throughput**: Full 10-checker verification run must complete within 2.5 seconds total latency for standard code artifacts (< 1000 LOC).
- **Zero Bypass Enforcement**: Invariant 6: State change to `Completed` is strictly blocked without valid `VerificationPassedEvent` signature.
