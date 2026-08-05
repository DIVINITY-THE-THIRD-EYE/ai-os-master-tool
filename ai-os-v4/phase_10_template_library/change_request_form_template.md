# Change Request Form: RFC-CR-{{CR_NUMBER}} - {{CR_TITLE}}

> **Change Request ID**: CR-{{CR_NUMBER}}  
> **Document Type**: Change Advisory Board (CAB) Request Form  
> **Status**: {{CR_STATUS}} (Submitted / Under CAB Review / Approved / Rejected / Completed)  
> **Requester**: {{REQUESTER_NAME}}  
> **System Impacted**: {{IMPACTED_SYSTEM}}  
> **Target Execution Window**: {{CR_START_TIME}} to {{CR_END_TIME}} UTC  
> **Risk Category**: {{RISK_CATEGORY}} (Low / Medium / High / Emergency)  

---

## 1. Description of Proposed Change

### 1.1 Summary & Business Purpose
*Instruction: Provide a comprehensive description of the change, reason for change, and business benefit.*

{{CHANGE_DESCRIPTION}}

---

## 2. Risk & Impact Assessment

- **System Downtime Required**: {{DOWNTIME_REQUIRED}} (Yes / No)
- **Estimated Downtime Duration**: {{DOWNTIME_DURATION}}
- **Impacted Customer Segment**: {{IMPACTED_USERS_PERCENTAGE}}%
- **Security / Compliance Impact**: {{SECURITY_IMPACT_RATIONALE}}

---

## 3. Implementation Plan & Steps

| Sequence Step | Description of Technical Step | Executing Role / Person | Estimated Time |
| :--- | :--- | :--- | :--- |
| Step 1 | Place service in maintenance mode banner | DevOps Lead | 5 mins |
| Step 2 | Execute database DDL migration script | Database Administrator | 10 mins |
| Step 3 | Deploy target container image build v{{BUILD_ID}} | Release Engineer | 15 mins |
| Step 4 | Run post-release smoke test suite | QA Lead | 10 mins |

---

## 4. Backout / Rollback Strategy

In the event of execution failure or post-change regression:
1. Trigger automated rollback script: `{{ROLLBACK_SCRIPT}}`
2. Restore database state from snapshot `{{PRE_CHANGE_SNAPSHOT_ID}}`
3. Verify legacy service endpoints return HTTP 200.

---

## 5. Change Advisory Board (CAB) Sign-off

| CAB Role | Name | Decision (Approve/Reject) | Date | Comments |
| :--- | :--- | :--- | :--- | :--- |
| Infrastructure Lead | {{CAB_INFRA_LEAD}} | Approved | {{CAB_DATE_1}} | Validated rollback plan |
| Security Lead | {{CAB_SEC_LEAD}} | Approved | {{CAB_DATE_2}} | Vulnerability scan clean |
| Product Manager | {{CAB_PRODUCT_LEAD}} | Approved | {{CAB_DATE_3}} | Window aligned with product |
