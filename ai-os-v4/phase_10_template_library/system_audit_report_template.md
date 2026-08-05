# System Security & Compliance Audit Report: {{SYSTEM_NAME}}

> **Document Type**: Comprehensive Audit Report  
> **Status**: {{DOCUMENT_STATUS}}  
> **Lead Auditor**: {{LEAD_AUDITOR}}  
> **Audit Period**: {{AUDIT_START_DATE}} to {{AUDIT_END_DATE}}  
> **Audit Scope**: Infrastructure, IAM, CI/CD Pipelines, Database Controls  
> **Date Published**: {{PUBLISH_DATE}}  

---

## 1. Executive Summary & Audit Scorecard

### 1.1 Overall Audit Rating
- **Overall Result**: {{AUDIT_RESULT}} (PASS / PASS WITH FINDINGS / FAIL)
- **Compliance Score**: {{COMPLIANCE_SCORE}}%
- **Critical Findings**: {{CRITICAL_COUNT}}
- **High Findings**: {{HIGH_COUNT}}
- **Medium Findings**: {{MEDIUM_COUNT}}

---

## 2. Audit Findings & Non-Conformances

### Finding 1: {{FINDING_1_TITLE}}
- **Finding ID**: AUD-FIND-01
- **Severity**: {{FINDING_1_SEVERITY}} (Critical / High / Medium / Low)
- **Control Standard**: {{CONTROL_STANDARD_REF}} (e.g., SOC 2 CC6.1)
- **Observation**:
  *Instruction: Describe the exact non-conformance or vulnerability observed during system inspection.*
  {{FINDING_1_OBSERVATION}}
- **Remediation Recommendation**: {{FINDING_1_RECOMMENDATION}}
- **Target Remediation Date**: {{REMEDIATION_DATE_1}}
- **Management Response**: {{MANAGEMENT_RESPONSE_1}}

---

## 3. Evaluation of Technical Controls

| Control Domain | Evaluated Criteria | Status | Comments / Evidence |
| :--- | :--- | :--- | :--- |
| Identity & Access | MFA enforcement across all production accounts | Compliant | Verified via IAM Policy inspection |
| Network Defense | Public S3 buckets prohibited | Compliant | AWS Config rule active |
| Patch Management | Zero CVEs > 7.0 older than 30 days | Non-Compliant | 2 vulnerable container images detected |
| Log Auditing | Centralized immutable audit trail enabled | Compliant | CloudTrail logs streamed to S3 Object Lock |

---

## 4. Auditor Conclusion & Sign-off

| Role | Name | Signature / Decision | Date |
| :--- | :--- | :--- | :--- |
| Lead Auditor | {{LEAD_AUDITOR}} | Certified Pass | {{PUBLISH_DATE}} |
| VP of Infrastructure | {{VP_INFRA}} | Acknowledged | {{PUBLISH_DATE}} |
