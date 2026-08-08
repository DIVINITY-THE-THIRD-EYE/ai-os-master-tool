# Standard Operating Procedure: SOP-004

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-004
- **Title**: Source Code Generation, Component Implementation, and Local Self-Verification
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Component Engineering & Implementation

---

## 2. Purpose & Objectives
The purpose of SOP-004 is to establish strict, repeatable guidelines for implementing production-grade source code, unit tests, and component documentation from assigned work packages, ensuring absolute integrity, minimal code footprint, zero hallucinated APIs, and complete test coverage.

### Key Objectives:
1. **Genuine Implementation**: Enforce strict anti-cheating rules: no hardcoded test assertions, no dummy stub implementations, and no facade returns.
2. **Minimal Change Principle**: Modify only the target files explicitly scoped within the work package task manifest. Prohibit unrelated refactoring.
3. **Co-located Test-Driven Generation**: Require high-coverage unit tests ($Coverage \ge 85\%$) created simultaneously alongside production logic.
4. **Zero-Lint Defect Standard**: Ensure code clean-compile status and zero style or static analysis violations before submitting handoff.

---

## 3. Scope & Applicability
This procedure applies to:
- All source code generation, bug fixing, refactoring, and local component editing.
- Primary execution agents, specifically the **Lead Developer (A05)**, supported by the **QA Verification Agent (A06)** and **Security Auditor (A07)**.

This procedure does **not** cover cross-component system release deployment (SOP-007) or post-deployment monitoring (SOP-008).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Execution DAG node transitions to `READY_FOR_EXECUTION` state in `execution_dag.json`.
- **Trigger Condition 2**: Automated task retry request issued after quality gate rejection during SOP-005.
- **Frequency**: Continuous and concurrent per dispatched task node.

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Target file system workspace mounted and write-accessible.
- Language-specific compilers/interpreters and test runners available in system PATH.
- Active task dispatch payload provided by Master Orchestrator (A01).

### Required Inputs
1. `task_package` (JSON object, required): Specific task node manifest from `execution_dag.json`.
2. `interface_contracts` (JSON/OpenAPI object, required): Explicit interface and model declarations.
3. `coding_conventions` (Markdown document, required): Reference formatting, naming, and style guidelines (`CONVENTIONS.md`).

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Lead Developer** | A05_LeadDev | **Accountable (A) / Responsible (R)** | Reads pre-edit state, generates code & tests, runs local build. |
| **QA Verification Agent** | A06_QAVerifier | **Consulted (C)** | Inspects unit test quality, boundary coverage, and mock validity. |
| **Security Auditor** | A07_SecurityAuditor | **Consulted (C)** | Performs pre-commit static security check (no hardcoded secrets). |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Dispatches task package and receives implementation handoff report. |

---

## 7. Step-by-Step Execution Procedure

```
 [Task Package] ---> (Step 1: File View & Context Pre-Read)
                           |
                           v
                    (Step 2: Minimal Implementation Plan)
                           |
                           v
                    (Step 3: Source Code Implementation)
                           |
                           v
                    (Step 4: Co-located Unit Test Creation)
                           |
                           v
                    (Step 5: Local Build & Compiler Run)
                           |
           +---------------+---------------+
           | Build Fail                    | Build PASS
           v                               v
(Self-Correction Loop: Max 3)     (Step 6: Unit Test Execution)
           |                               |
           +------------------------------>| PASS
                                           v
                               (Step 7: Static Lint Check)
                                           |
                                           v
                               [Task Code & Local Logs]
```

### Step 1: File Inspection & Pre-Read Verification
- **1.1 Pre-Read Mandate**: Before editing any target file, execute `view_file` to read the entire current content and verify existing functionality.
- **1.2 Target Scope Lock**: Confirm file paths against `task_package.target_files`. Modifying files outside this list is strictly forbidden without explicit re-scoping.

### Step 2: Implementation Plan Construction
- **2.1 Change Isolation**: Formulate a granular, line-by-line edit plan using minimal targeted replacement chunks (`replace_file_content` / `multi_replace_file_content`).
- **2.2 Integrity Assurance Check**: Verify that the planned code implements actual logic rather than hardcoding static mock return values tailored to cheat tests.

### Step 3: Source Code Implementation
- **3.1 Code Generation**: Write functional implementation following project architectural conventions:
  - Strong typing with explicit type annotations.
  - Complete docstrings and inline comments explaining non-trivial logic.
  - Explicit error handling (catch specific exception classes; never swallow exceptions blindly).
- **3.2 Anti-Pattern Suppression**: Avoid anti-patterns such as global state modification, magic numbers, or hardcoded API keys/passwords.

### Step 4: Co-located Unit Test Creation
- **4.1 Test File Creation**: Create or update matching unit test file co-located or positioned in designated test directory (e.g., `tests/unit/test_<module_name>.py`).
- **4.2 Comprehensive Coverage**: Write test cases targeting:
  - Happy path standard execution.
  - Edge cases (null/empty inputs, maximum bound values, boundary conditions).
  - Exception and failure recovery handling.

### Step 5: Local Build & Compilation Verification
- **5.1 Compile Check**: Trigger workspace compiler or syntax validator (e.g., `python -m py_compile`, `cargo check`, `npm run build`).
- **5.2 Compilation Correction**: If syntax or compilation errors occur, parse line error logs and execute targeted fix. Max retries: 3 attempts.

### Step 6: Local Unit Test Execution
- **6.1 Test Runner Dispatch**: Execute local test runner (e.g., `pytest tests/unit/test_<module_name>.py`).
- **6.2 Coverage Audit**: Verify test coverage meets or exceeds mandatory threshold ($Coverage \ge 85\%$).

### Step 7: Static Linting & Code Hygiene Enforcement
- **7.1 Linter Run**: Execute static linter and formatting checker (e.g., `flake8`, `eslint`, `clippy`).
- **7.2 Zero Violation Resolution**: Fix all lint warnings and errors. Do not insert inline `# pylint: disable` suppressions unless explicitly approved by Security Auditor (A07).

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 4: Local Code Implementation Gate
--------------------------------------------------------------------------------------
Check Metric                         | Required Threshold | PASS Action | FAIL Action
--------------------------------------------------------------------------------------
Local Build / Compilation            | Exit Code == 0     | Advance     | Retries 1-3 -> Fail
Unit Test Suite                      | 100% Pass Rate     | Advance     | Fix Code -> Retry
Test Coverage Ratio                  | >= 85%             | Advance     | Add Edge Test Cases
Linter Violations                    | Exactly 0          | Pass Gate   | Clean Lint Errors
Genuine Logic Audit                  | No Hardcoded Stubs | Final Lock  | REJECT & ESCALATE
--------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- Code compiles cleanly with zero warnings or errors.
- Unit tests pass with $\ge 85\%$ coverage.
- Linter reports 0 violations.
- Genuine implementation verified (no mock-stub cheating).

### Deliverables
1. `modified_source_files` — Updated target source modules.
2. `unit_test_files` — Corresponding test suites.
3. `knowledge/artifacts/execution/local_verification_log.json` — Local build and test execution transcript.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Compilation or Test Failure After 3 Retries**
  - *Action*: Revert target files to git workspace HEAD state.
  - *Escalation*: Mark task as `FAILED_IMPLEMENTATION` and route to QA Verification Agent (A06) / Task Planner (A04) for task re-decomposition.
- **Failure Scenario B: Integrity / Hardcoded Cheating Detection**
  - *Action*: Instantly invalidate task execution payload. Flag implementation log.
  - *Escalation*: Trigger SOP-010 with priority `CRITICAL_INTEGRITY_VIOLATION`.

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log recorded upon task execution complete, stored at `logs/audit/sops/sop_004_audit.json`:

```json
{
  "sop_id": "SOP-004",
  "execution_id": "exec_20260805_004902",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A05_LeadDev",
  "task_id": "TASK-004_AUTH_MODULE",
  "execution_metrics": {
    "files_modified": 2,
    "lines_added": 184,
    "lines_deleted": 12,
    "unit_tests_run": 14,
    "unit_tests_passed": 14,
    "coverage_percentage": 92.4,
    "lint_errors": 0,
    "self_correction_loops": 1
  },
  "deliverable_path": "src/auth/token_verifier.py",
  "verification_status": "PASSED",
  "signature": "9d8c7b6a5e4f..."
}
```
