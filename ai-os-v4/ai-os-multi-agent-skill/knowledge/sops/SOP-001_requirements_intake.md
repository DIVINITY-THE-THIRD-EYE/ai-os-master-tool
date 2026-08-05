# Standard Operating Procedure: SOP-001

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-001
- **Title**: Requirements Intake, Ambiguity Resolution, and Specification Normalization
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Multi-Agent System Core Lifecycle Management

---

## 2. Purpose & Objectives
The primary purpose of SOP-001 is to establish a deterministic, repeatable, and automated standard operating procedure for ingesting, validating, clarifying, and normalizing user and system requests within the AI OS Multi-Agent framework.

### Key Objectives:
1. **Ambiguity Minimization**: Reduce requirement ambiguity scores below an threshold of $\epsilon < 0.05$ prior to downstream architectural planning.
2. **Completeness Verification**: Enforce mandatory coverage of functional requirements (FRs), non-functional requirements (NFRs), boundary constraints, and threat considerations.
3. **Structured Specification Generation**: Convert natural language, semi-structured, or fuzzy prompts into an immutable, schema-validated Requirements Specification Artifact (`requirements_spec.json`).
4. **Scope Encroachment Prevention**: Define explicit acceptance criteria and out-of-scope boundaries to prevent hallucinated scope creep during component implementation.

---

## 3. Scope & Applicability
This procedure applies to:
- All incoming user requests, feature requests, system redesigns, bug fixes, and autonomous task dispatches.
- All primary agent roles involved in initial request ingestion, specifically the **Master Orchestrator (A01)** and **Requirements Specialist (A02)**.
- Autonomous execution pipelines operating under `ai-os-multi-agent-skill`.

This procedure does **not** cover real-time production incident triage (covered under SOP-008) or post-release retrospective reflection (covered under SOP-009).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Ingestion of a new user prompt via CLI, REST API, Webhook, or Messaging Gateway.
- **Trigger Condition 2**: Receipt of an automated inter-agent task delegation requesting new functionality.
- **Trigger Condition 3**: Re-activation of a stalled workflow requiring re-scoping after architectural invalidation.
- **Frequency**: Event-driven (executes once per discrete task dispatch).

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Active runtime session initialized with valid agent authorization tokens.
- Accessible domain ontology schema located at `knowledge/ontology/domain_ontology.json`.
- Operational state machine in state `STATE_INTAKE`.

### Required Inputs
1. `raw_user_prompt` (String, required): The original unparsed user or caller request.
2. `system_context` (JSON object, required): Environment specifications, workspace directory path, active platform constraints.
3. `user_preferences` (JSON object, optional): Custom style guides, language preferences, or budget/latency constraints.
4. `existing_artifacts_manifest` (JSON array, optional): Manifest of pre-existing codebase files relevant to the workspace.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Master Orchestrator** | A01_Orchestrator | **Accountable (A)** | Initiates SOP-001, monitors pipeline SLA, approves final intake state transition. |
| **Requirements Specialist** | A02_ReqSpecialist | **Responsible (R)** | Executes syntactic parsing, calculates ambiguity metrics, generates formal spec. |
| **Solution Architect** | A03_Architect | **Consulted (C)** | Evaluates technical feasibility and structural constraints of draft spec. |
| **Security Auditor** | A07_SecurityAuditor | **Consulted (C)** | Assesses safety risk profile and compliance policies. |
| **Human Operator** | Human_Supervisor | **Informed / Consulted (I/C)** | Responds to clarify questions if ambiguity exceeds automatic threshold. |

---

## 7. Step-by-Step Execution Procedure

```
 [Raw Input] ---> (Step 1: Ingestion & Sanity Check)
                         |
                         v
                  (Step 2: Semantic Parsing & Classification)
                         |
                         v
                  (Step 3: Ambiguity Scoring & Gap Detection)
                         |
           +-------------+-------------+
           | Score > 0.05              | Score <= 0.05
           v                           v
(Step 4: Clarification Loop)   (Step 5: SRS Generation & Locking)
           |                           |
           +------------->+------------+
                          |
                          v
               [requirements_spec.json]
```

### Step 1: Ingestion & Sanity Verification
- **1.1 Payload Receiving**: Capture `raw_user_prompt` and compute SHA-256 hash (`input_hash`).
- **1.2 Length & Character Verification**: Ensure prompt length is within bounds ($10 \text{ chars} \le L \le 250,000 \text{ chars}$). Reject empty or payload-flooding requests.
- **1.3 Encoding Normalization**: Normalize text encoding to UTF-8 standard. Strip non-printable control characters except standard whitespace (`\n`, `\t`, `\r`).
- **1.4 Threat Pre-Screening**: Pass input string to regex guardrails to filter prompt injection attempts (e.g., `ignore previous instructions`, `system prompt extract`).

### Step 2: Semantic Parsing & Classification
- **2.1 Intent Classification**: Categorize the intent into one of standard archetypes: `FEATURE_NEW`, `BUG_FIX`, `REFACTOR`, `DOCUMENTATION`, `INFRASTRUCTURE`, or `ANALYSIS`.
- **2.2 Entity Extraction**: Extract target paths, language references, frameworks, modules, external dependencies, and performance constraints.
- **2.3 Ontology Alignment**: Map extracted entities against `knowledge/ontology/domain_ontology.json` to ensure concept consistency.

### Step 3: Ambiguity Scoring & Gap Detection
- **3.1 Ambiguity Metric Calculation**: Compute ambiguity index $A_{score} \in [0.0, 1.0]$ based on missing parameters:
  $$A_{score} = w_1 M_{target} + w_2 M_{acceptance} + w_3 M_{tech\_stack} + w_4 M_{constraints}$$
  where $w_i$ are normalized weights ($0.25$ each) and $M_i = 1$ if parameter is missing/vague, $0$ if explicit.
- **3.2 Gap Identification**: Document specific missing dimensions:
  - Missing Target Output Location
  - Unclear Operational Environment / Language Version
  - Undefined Acceptance Criteria
  - Missing Failure / Edge Case Expectations

### Step 4: Interactive Clarification & Self-Resolution Loop
- **4.1 Context Search**: Query internal memory repository (`memory/persistent_memory.db`) for matching historical patterns to infer missing context automatically.
- **4.2 Synthetic Question Generation**: If $A_{score} > 0.05$ and self-resolution fails, construct precise, numbered targeted clarification questions.
- **4.3 Intervention Dispatch**: If automatic resolution is unavailable, route clarification payload to Human Escalation channel (refer to SOP-010). Maximum auto-retry loops: 3.

### Step 5: Requirements Specification Generation & Locking
- **5.1 Draft Generation**: Assemble structured markdown and JSON specification document containing:
  - System Boundaries
  - Functional Requirements (FR-001 through FR-N) with priority tagging (MUST, SHOULD, COULD)
  - Non-Functional Requirements (NFR-001 through NFR-N) covering performance, security, and scalability
  - Out-of-Scope Declarations
- **5.2 Integrity Validation**: Validate draft `requirements_spec.json` against `schemas/requirements_schema.json`.
- **5.3 Hash Locking**: Append digital signature and write frozen specification to `knowledge/artifacts/intake/requirements_spec.json`.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 1: Ambiguity Check
---------------------------------------------------------------------
Check Condition                    | Result = PASS     | Result = FAIL
---------------------------------------------------------------------
Ambiguity Score A_score <= 0.05    | Advance to Step 5 | Trigger Step 4
Security Threat Level == NONE      | Advance to Step 2 | Reject Request
Schema Validation == TRUE          | Lock Spec & Exit  | Re-draft Step 5
---------------------------------------------------------------------
```

### Mandatory Verification Gates:
1. **Gate 1.1 (Schema Gate)**: `requirements_spec.json` must conform strictly to JSON Schema draft-07.
2. **Gate 1.2 (Constraint Gate)**: Every FR must possess at least one quantifiable verification criterion.
3. **Gate 1.3 (Boundary Gate)**: Out-of-scope list must not be empty.

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- Ambiguity score $A_{score} \le 0.05$.
- Formal specification approved by Master Orchestrator (A01).
- `STATE_INTAKE` completed with status `SUCCESS`.

### Deliverables
1. `knowledge/artifacts/intake/requirements_spec.json` — Immutable machine-readable requirement specification.
2. `knowledge/artifacts/intake/requirements_summary.md` — Human-readable summary report.
3. `knowledge/artifacts/intake/intake_audit_log.json` — Compliance log file.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Persistent Ambiguity ($A_{score} > 0.05$ after 3 loops)**
  - *Action*: Suspend Intake Workflow. Mark request status as `STALLED_AMBIGUOUS`.
  - *Escalation*: Trigger SOP-010 (Human Escalation) with issue code `ERR_INTAKE_AMBIGUITY_TIMEOUT`.
- **Failure Scenario B: Prompt Injection / Malicious Payload Detected**
  - *Action*: Immediately terminate execution. Quarantine payload.
  - *Escalation*: Trigger SOP-006 (Security Audit) with issue code `ERR_SECURITY_PROMPT_INJECTION`.
- **Failure Scenario C: Schema Validation Failure**
  - *Action*: Re-route draft spec back to Requirements Specialist (A02) for corrective formatting. Maximum retries: 2.

---

## 11. Audit Logging & Compliance Recordkeeping
Every execution of SOP-001 MUST emit an audit record formatted according to the following schema to `logs/audit/sops/sop_001_audit.json`:

```json
{
  "sop_id": "SOP-001",
  "execution_id": "exec_20260805_001928",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A02_ReqSpecialist",
  "input_hash_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "metrics": {
    "raw_prompt_length": 1420,
    "ambiguity_score_initial": 0.32,
    "ambiguity_score_final": 0.02,
    "clarification_iterations": 1
  },
  "deliverable_path": "knowledge/artifacts/intake/requirements_spec.json",
  "verification_status": "PASSED",
  "signature": "3a8d9f10c4...b7e2"
}
```
