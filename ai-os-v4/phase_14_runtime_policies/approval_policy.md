# AI OS v4 — Approval Policy Specification

**Document Version:** 4.0.0  
**Phase:** Phase 14 — Runtime Policies  
**Classification:** Enterprise Governance & Human-in-the-Loop Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Governance Architecture & Approval Tiers

The **Approval Policy** establishes automated and Human-in-the-Loop (HITL) approval gates for actions that impact system state, financial budgets, enterprise data, or production infrastructure.

```
                                [Action Triggered]
                                        │
                                        v
                          [Risk Rating Evaluator]
                                        │
         +------------------------------+------------------------------+
         |                              |                              |
         v                              v                              v
[Tier 1: Low Risk]            [Tier 2: Medium Risk]           [Tier 3: High / Critical]
  - Read-Only Tool              - Dev Database Migration        - Prod DB Schema Change
  - Temp File Creation          - Code Commit to Staging        - Production Deployment
  - Routine Memory Log          - Budget < $100 API Call        - Budget > $100 API Call
         │                              │                              │
         v                              v                              v
[Automated Approval]          [Agent Lead Sign-off]           [Multi-Sig HITL Approval]
(Passes in <50ms)             (Architect Agent Review)        (Human Admin Required)
```

---

## 2. Risk Matrix & Approval Requirements

| Risk Level | Action Category | Financial Threshold | Approval Authority | Timeout SLA | Default Fallback Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LOW** | Read-only tools, ephemeral writes | $0.00 | Automated Policy PDP | Immediate | Auto-Approve |
| **MEDIUM** | Code generation, staging deploy | < $100.00 | Architect Agent | 30 minutes | Auto-Reject on Timeout |
| **HIGH** | Production deploy, secret read | < $1,000.00 | Single Human Admin | 4 hours | Auto-Reject on Timeout |
| **CRITICAL** | Production DB drop, high budget | > $1,000.00 | Multi-Sig (2 Humans) | 24 hours | Auto-Reject on Timeout |

---

## 3. Multi-Signature (Multi-Sig) Approval Protocol

For **CRITICAL** actions (such as dropping production databases or releasing unverified production builds):

1. **Quorum Requirement:** Requires $M$-of-$N$ explicit cryptographic approvals (e.g. 2 of 3 authorized Human Security Administrators).
2. **Approval Payload:** Approval requests contain complete cryptographic hashes of proposed state changes, parameter values, and execution plans.
3. **Immutability:** Every sign-off is logged in the `audit_log_framework` with the administrator's public key signature.

---

## 4. Approval Policy Definition Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ApprovalPolicySpecification",
  "type": "object",
  "required": [
    "policy_id",
    "risk_level",
    "required_approvers_count",
    "approver_roles",
    "timeout_seconds",
    "timeout_fallback_action"
  ],
  "properties": {
    "policy_id": { "type": "string" },
    "risk_level": {
      "type": "string",
      "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    },
    "required_approvers_count": { "type": "integer", "default": 1 },
    "approver_roles": {
      "type": "array",
      "items": { "type": "string" }
    },
    "timeout_seconds": { "type": "integer", "default": 14400 },
    "timeout_fallback_action": {
      "type": "string",
      "enum": ["AUTO_REJECT", "ESCALATE_SUPERVISOR", "AUTO_APPROVE"]
    },
    "notification_channels": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

---

## 5. Approval Workflow Engine Interfaces

```typescript
export interface ApprovalEngineService {
  requestApproval(request: ApprovalRequestPayload): Promise<ApprovalTicket>;
  submitDecision(ticketId: string, approverId: string, decision: "APPROVED" | "REJECTED", signature: string): Promise<ApprovalStatus>;
  getTicketStatus(ticketId: string): Promise<ApprovalTicketDetails>;
}

export interface ApprovalRequestPayload {
  tenant_id: string;
  requester_agent_id: string;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  action_summary: string;
  proposed_diff_hash: string;
  metadata: Record<string, unknown>;
}
```

---

## 6. Summary Checklist for Approval Policy Compliance

- [x] 3-tier risk-based approval matrix established.
- [x] Multi-signature quorum approval protocol for critical operations specified.
- [x] Declarative JSON schema for Approval Policies defined.
- [x] Automated notification dispatch and timeout fallback rules specified.
- [x] TypeScript Approval Engine interface published.
