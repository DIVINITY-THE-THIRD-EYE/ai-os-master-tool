# Standard Operating Procedure: SOP-010

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-010
- **Title**: Human Escalation, Intervention Management, and Human-in-the-Loop (HITL) Oversight
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Human-Machine Governance & Safety Control

---

## 2. Purpose & Objectives
The purpose of SOP-010 is to establish an immutable, fail-safe protocol for pausing autonomous agent execution, packaging context, and escalating decision authority to a qualified Human Operator when system boundaries, safety constraints, ambiguity limits, or unrecoverable error thresholds are reached.

### Key Objectives:
1. **Deterministic Safety Halt**: Instantly freeze execution state upon detection of high-risk scenarios, prompt injection attacks, or security policy violations.
2. **Context-Rich Escalation Packaging**: Provide human supervisors with clean, concise, decision-ready dossiers containing complete problem state, options, and recommended actions.
3. **Fail-Safe Default Behavior**: Mandate a strict default fallback to `STATE_SAFE_HALT` if human response SLAs timeout without authorization.
4. **Auditability of Human Decisions**: Require cryptographically signed human authorization for all overrides, policy bypasses, and manual parameter injections.

---

## 3. Scope & Applicability
This procedure applies to:
- All human-in-the-loop (HITL) approval gates, ambiguity resolution queries, policy exception requests, security breach escalations, and emergency kill-switch activations.
- The **Human Intervention Specialist (A11)** and **Master Orchestrator (A01)**, interacting directly with **Human Supervisors / Operators**.

This procedure overrides all routine agent autonomous execution SOPs (SOP-001 through SOP-009) when activated.

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Escalation mandate issued by any upstream SOP (e.g., SOP-001 ambiguity timeout, SOP-006 critical security block, SOP-008 unrecoverable incident).
- **Trigger Condition 2**: Policy rule trigger requiring explicit human approval (e.g., destructive database operation, API cost threshold $> \$50.00$).
- **Trigger Condition 3**: Manual intervention signal dispatched by Human Operator via CLI (`agy interrupt`) or Web UI.
- **Frequency**: Exception-driven (executes whenever human oversight is triggered).

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Active notification gateway (CLI output, Slack Webhook, REST Notification Endpoint).
- Escalation matrix loaded from `orchestrator/escalation_matrix.yaml`.
- State machine transition to `STATE_ESCALATION_PAUSE`.

### Required Inputs
1. `escalation_trigger_payload` (JSON object, required): Source SOP ID, trigger reason code, risk score, and error stack trace.
2. `system_context_dossier` (JSON object, required): Full current context state, modified files, and active execution memory.
3. `escalation_matrix` (YAML object, required): SLA thresholds, notification routes, and role authorization maps.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Human Intervention Agent** | A11_HumanIntervention | **Accountable (A) / Responsible (R)** | Freezes system, packages escalation dossier, dispatches alert, ingests response. |
| **Human Operator / Supervisor** | Human_Supervisor | **Accountable (A) [Decision]** | Evaluates options, signs decision payload (APPROVE/REJECT/RETRY/ABORT). |
| **Master Orchestrator** | A01_Orchestrator | **Consulted (C)** | Executes state pause and resumes workflow upon authorized response. |
| **Security Auditor** | A07_SecurityAuditor | **Consulted (C)** | Validates human credentials during security override requests. |

---

## 7. Step-by-Step Execution Procedure

```
 [Escalation Triggered] ---> (Step 1: Execution Freeze & State Preservation)
                                      |
                                      v
                               (Step 2: Urgency Scoring & Dossier Assembly)
                                      |
                                      v
                               (Step 3: Multi-Channel Notification Dispatch)
                                      |
                                      v
                               (Step 4: Human Response Listening Loop)
                                      |
           +--------------------------+--------------------------+
           | Response Received & Verified                        | SLA Timeout Exceeded
           v                                                     v
(Step 5: Apply Human Decision Action)                  (Step 6: Execute Safe Halt)
[RETRY | OVERRIDE | REJECT | TERMINATE]                          |
           |                                                     v
           +----------------------------->+----------------------+
                                          |
                                          v
                         [escalation_resolution.json]
```

### Step 1: Execution Freeze & State Preservation
- **1.1 Global Pause Signal**: Broadcast `PAUSE_EXECUTION` signal across event bus (`events/event_topics.yaml`). Terminate active worker sub-threads gracefully.
- **1.2 Snapshot Serialization**: Save active workspace state to `knowledge/artifacts/escalation/snapshot_pause.json`.

### Step 2: Urgency Scoring & Dossier Assembly
- **2.1 Priority Classification**:
  - **P1 CRITICAL (SLA: 15 min)**: Security breach, unrecoverable crash, destructive action request.
  - **P2 HIGH (SLA: 1 hour)**: Critical requirement ambiguity, architectural trade-off block.
  - **P3 MEDIUM (SLA: 4 hours)**: Standard approval gate, minor policy violation.
  - **P4 LOW (SLA: 24 hours)**: Informational notification.
- **2.2 Escalation Dossier Packaging**: Construct structured `escalation_dossier.json`:
  - Problem Summary & Trigger Source.
  - Options Analysis (Option A, Option B, Option C) with projected risks & trade-offs.
  - Recommended Agent Action.

### Step 3: Multi-Channel Notification Dispatch
- **3.1 Gateway Routing**: Format notification payload and transmit via active channels:
  - Interactive CLI Terminal Prompt (`[AGY HUMAN INPUT REQUIRED]`).
  - Webhook Notification (Slack / Microsoft Teams / PagerDuty).
  - Web UI Notification Banner.

### Step 4: Human Response Ingestion & Authentication
- **4.1 Response Listener**: Poll or listen for structured human decision response.
- **4.2 Authentication & Cryptographic Verification**: Verify human operator identity token and signature (`human_operator_id`, `auth_token`, `signature`).

### Step 5: Decision Route Execution
- **5.1 Action Selection Parsing**:
  - **Route A (RETRY)**: Inject corrected parameters and resume execution at failing SOP step.
  - **Route B (OVERRIDE)**: Apply human-specified modification, sign policy exception, and advance state machine.
  - **Route C (REJECT)**: Abort current sub-task, mark as `REJECTED_BY_HUMAN`, and return to planning phase.
  - **Route D (TERMINATE)**: Execute total workflow teardown, purge temporary resources, and return system to idle state.

### Step 6: SLA Timeout Management (If No Response Received)
- **6.1 Timeout Trigger**: If human response is not received within priority SLA window, execute default safe mode action:
  - Default Action for P1/P2: Transition to `STATE_SAFE_HALT` and maintain state freeze indefinitely. Never auto-approve critical risks.

### Step 7: System Unfreezing & Compliance Logging
- **7.1 State Machine Unfreeze**: Broadcast `RESUME_EXECUTION` signal with approved human decision payload attached.
- **7.2 Audit Record Archival**: Log complete interaction to `logs/audit/sops/sop_010_audit.json`.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 10: Human Escalation & Governance Gate
--------------------------------------------------------------------------------------
Check Metric                         | Threshold Target   | Result = PASS | Result = FAIL
--------------------------------------------------------------------------------------
Human Auth Signature                 | Valid & Authorized | Accept Action | REJECT (Security Lock)
SLA Timeout Check                    | Response <= SLA    | Execute Action| TRIGGER SAFE_HALT
Dossier Completeness                 | All Options Included| Dispatch Alert| Re-package Dossier
Human Decision Action Code           | Valid Enum         | Process Action| Request Re-entry
--------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- Human decision received, authenticated, and executed OR safe-halt state securely engaged upon SLA timeout.
- State machine safely unfrozen and unblocked.
- Full human intervention audit record archived.

### Deliverables
1. `knowledge/artifacts/escalation/escalation_dossier_ESC-XXX.json` — Escalation query package.
2. `knowledge/artifacts/escalation/escalation_resolution_ESC-XXX.json` — Signed human decision artifact.
3. `logs/audit/sops/sop_010_audit.json` — Governance compliance log.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Unauthorized Override Attempt (Invalid Signature)**
  - *Action*: Reject response payload instantly. Engage strict security lockdown (`STATE_SECURITY_LOCKDOWN`).
  - *Escalation*: Dispatch security breach alert to Chief Information Security Officer (CISO) notification channel.
- **Failure Scenario B: Communication Gateway Outage (Webhook Unreachable)**
  - *Action*: Fallback to local CLI interactive terminal prompt and write alert to disk (`URGENT_HUMAN_ACTION_REQUIRED.txt`).

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log generated upon resolution of human escalation, stored at `logs/audit/sops/sop_010_audit.json`:

```json
{
  "sop_id": "SOP-010",
  "execution_id": "exec_20260805_010992",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A11_HumanIntervention",
  "executing_agent": "A11_HumanIntervention",
  "escalation_details": {
    "escalation_id": "ESC-20260805-01",
    "trigger_sop": "SOP-001",
    "priority": "P2_HIGH",
    "reason_code": "ERR_INTAKE_AMBIGUITY_TIMEOUT",
    "human_operator_id": "usr_sec_lead_01",
    "decision_action": "OVERRIDE",
    "sla_elapsed_seconds": 340,
    "resolution_status": "RESOLVED_AND_RESUMED"
  },
  "deliverable_path": "knowledge/artifacts/escalation/escalation_resolution_ESC-20260805-01.json",
  "verification_status": "PASSED",
  "signature": "2a1f0e9d8c7b..."
}
```
