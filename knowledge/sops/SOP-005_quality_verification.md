# Standard Operating Procedure: SOP-005

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-005
- **Title**: Quality Assurance, Multi-Tier Automated Verification, and Quality Gate Evaluation
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Quality Assurance & Automated Verification

---

## 2. Purpose & Objectives
The purpose of SOP-005 is to establish an automated, non-bypassable quality verification pipeline that validates functional correctness, cross-module integration, performance SLAs, and regression safety for all generated components.

### Key Objectives:
1. **Multi-Tiered Verification**: Execute end-to-end validation across Unit, Integration, System, and Performance test layers.
2. **Defect Zero Tolerance**: Enforce zero blocking defects ($P1 = 0, P2 = 0$) for release baseline qualification.
3. **Comprehensive Coverage Thresholds**: Require $\ge 85\%$ aggregate line coverage and $\ge 80\%$ branch coverage across all active modules.
4. **Independent Quality Gate Certification**: Provide immutable cryptographic attestations certifying that code meets quality standards prior to release deployment.

---

## 3. Scope & Applicability
This procedure applies to:
- Test execution, static code analysis, code coverage computation, performance profiling, and regression testing.
- The **QA Verification Agent (A06)** as primary authority, in coordination with the **Lead Developer (A05)** and **Master Orchestrator (A01)**.

This procedure does **not** cover security vulnerability scanning (SOP-006) or post-release incident recovery (SOP-008).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Task handoff submitted by Lead Developer (A05) following SOP-004 completion.
- **Trigger Condition 2**: Aggregated pull request or system release candidate build triggered in CI/CD pipeline.
- **Frequency**: Triggered automatically per task submission and per release candidate build.

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Code compiles cleanly with local self-verification pass logs from SOP-004.
- Test runner environment initialized with necessary database containers and mock service fixtures.
- Quality configuration loaded from `quality/quality_gates.yaml`.

### Required Inputs
1. `implemented_code_manifest` (JSON object, required): List of changed source files and unit test paths.
2. `quality_gate_rules` (YAML object, required): Target thresholds for coverage, pass rates, and latency bounds.
3. `system_test_suite` (Directory, required): Integration and E2E test scripts.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **QA Verification Agent** | A06_QAVerifier | **Accountable (A) / Responsible (R)** | Executes verification pipeline, computes coverage, certifies gates. |
| **Lead Developer** | A05_LeadDev | **Consulted (C)** | Fixes identified test failures, remediates regression defects. |
| **Solution Architect** | A03_Architect | **Consulted (C)** | Evaluates system performance degradation or architectural defects. |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Blocks/unblocks workflow transitions based on Quality Gate signoff. |

---

## 7. Step-by-Step Execution Procedure

```
 [Code Handoff] ---> (Step 1: Test Environment Initialization)
                             |
                             v
                      (Step 2: Full Unit Test Suite Run)
                             |
                             v
                      (Step 3: Integration Test Suite Run)
                             |
                             v
                      (Step 4: End-to-End System Test Run)
                             |
                             v
                      (Step 5: Regression & Backward Safety Check)
                             |
                             v
                      (Step 6: Coverage Calculation & Analysis)
                             |
           +-----------------+-----------------+
           | Fail Metrics                      | Metrics PASS
           v                                   v
(Step 7: Defect Categorization)       (Step 8: Gate Signoff)
           |                                   |
           v                                   v
[Rejection Report -> A05]           [quality_verification_report.json]
```

### Step 1: Test Environment & Fixture Setup
- **1.1 Workspace Isolation**: Prepare clean temporary test workspace. Inject mock context variables, test database schemas, and stub external API end-points.
- **1.2 Fixture Health Check**: Verify test runner dependencies and database migrations complete without errors before launching test suites.

### Step 2: Comprehensive Unit Test Suite Execution
- **2.1 Global Unit Test Run**: Trigger project-wide unit test suite runner (e.g., `pytest --cov=src tests/unit`).
- **2.2 Flaky Test Filter**: Run failing tests up to 2 additional times to detect non-deterministic flaky tests. Any test demonstrating intermittency is flagged for refactoring (`FLAG_FLAKY`).

### Step 3: Integration Test Suite Execution
- **3.1 Inter-Module Contract Verification**: Execute integration test suite exercising IPC channels, API routes, database access layers, and message broker schemas (`tests/integration/`).
- **3.2 Interface Mismatch Detection**: Confirm request and response payloads adhere strictly to OpenAPI and JSON schemas validated in SOP-002.

### Step 4: System Integration & End-to-End (E2E) Testing
- **4.1 Workflow Execution**: Run end-to-end simulated user scenarios covering full multi-agent lifecycles (`tests/e2e/`).
- **4.2 Latency & Performance Checks**: Measure task completion execution latency. Verify processing speed satisfies performance bounds ($T_{execution} \le T_{max\_threshold}$).

### Step 5: Regression & Backward Safety Checks
- **5.1 Historical Test Suite Run**: Run baseline regression test matrix against all existing unmodified modules.
- **5.2 Backward Compatibility Verification**: Confirm public API signatures remain backward compatible and schema versioning bump requirements are satisfied.

### Step 6: Coverage Calculation & Metric Analysis
- **6.1 Coverage Parsing**: Extract raw coverage data (`coverage.xml` / `cobertura.xml`). Compute overall line coverage $C_{line}$ and branch coverage $C_{branch}$:
  $$C_{line} = \frac{Lines_{executed}}{Lines_{total}} \ge 0.85, \quad C_{branch} = \frac{Branches_{covered}}{Branches_{total}} \ge 0.80$$
- **6.2 Uncovered Line Identification**: Pinpoint uncovered source code blocks and generate explicit delta report.

### Step 7: Defect Triage & Categorization (If Failures Occur)
- **7.1 Severity Classification**:
  - **P1 Blocker**: System crash, data corruption, failed E2E test, or coverage failure.
  - **P2 Major**: Integration failure under rare boundary conditions.
  - **P3 Minor**: Formatting, non-blocking log warning, or trivial documentation drift.
- **7.2 Rejection Package Assembly**: Package failing test stack traces, input parameters, and environment logs into `quality_rejection_report.json` for Lead Developer (A05).

### Step 8: Quality Gate Certification & Signoff
- **8.1 Quality Gate Evaluation**: Evaluate results against `quality_gates.yaml`. If all gates pass ($P1=0, P2=0, Coverage \ge 85\%$), issue signed verification attestation.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 5: Quality Gate Decision Table
-------------------------------------------------------------------------------------
Check Condition                      | Threshold Required | Result = PASS | Result = FAIL
-------------------------------------------------------------------------------------
Unit Test Pass Rate                  | Exactly 100%       | Advance       | P1 Blocker -> Reconcile
Integration Test Pass Rate           | Exactly 100%       | Advance       | P1 Blocker -> Reconcile
Line Code Coverage C_line            | >= 85.0%           | Advance       | Coverage Deficit Fail
Branch Code Coverage C_branch        | >= 80.0%           | Advance       | Coverage Deficit Fail
P1 / P2 Open Defects                 | Exactly 0          | Pass Gate     | Reject Handoff
-------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- 100% pass rate across unit, integration, and E2E test suites.
- Line coverage $\ge 85\%$ and Branch coverage $\ge 80\%$.
- Zero P1/P2 defects remaining open.
- Cryptographically signed quality attestation document generated.

### Deliverables
1. `knowledge/artifacts/quality/quality_verification_report.json` — Detailed execution report.
2. `knowledge/artifacts/quality/coverage_summary.json` — Module-by-module coverage breakdown.
3. `knowledge/artifacts/quality/quality_attestation.pem` — Digital sign-off attestation file.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Quality Gate Rejection (P1/P2 Defects Present)**
  - *Action*: Reject code submission. Revert state machine to `STATE_CODE_GENERATION`.
  - *Escalation*: Dispatch structured rejection report back to Lead Developer (A05) with mandatory fix SLA (Max 2 repair attempts).
- **Failure Scenario B: Systemic Architecture Defect Uncovered in E2E**
  - *Action*: Halt quality pipeline.
  - *Escalation*: Escalate to Solution Architect (A03) and Master Orchestrator (A01) to review structural flaw.

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log generated upon completion of quality verification, recorded at `logs/audit/sops/sop_005_audit.json`:

```json
{
  "sop_id": "SOP-005",
  "execution_id": "exec_20260805_005811",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A06_QAVerifier",
  "verification_summary": {
    "unit_tests_run": 84,
    "unit_tests_passed": 84,
    "integration_tests_run": 22,
    "integration_tests_passed": 22,
    "e2e_tests_run": 6,
    "e2e_tests_passed": 6,
    "line_coverage": 89.2,
    "branch_coverage": 83.5,
    "p1_defects": 0,
    "p2_defects": 0
  },
  "deliverable_path": "knowledge/artifacts/quality/quality_verification_report.json",
  "verification_status": "PASSED",
  "signature": "7a6b5c4d3e2f..."
}
```
