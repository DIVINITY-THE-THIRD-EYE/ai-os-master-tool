# Regulatory & Security Compliance Checklist: {{COMPLIANCE_STANDARD}}

> **Standard**: {{COMPLIANCE_STANDARD}} (SOC 2 Type II / ISO 27001 / HIPAA / PCI-DSS)  
> **Status**: {{DOCUMENT_STATUS}}  
> **Compliance Officer**: {{COMPLIANCE_OFFICER}}  
> **Audit Period**: {{AUDIT_PERIOD}}  
> **Last Assessed Date**: {{LAST_ASSESSED_DATE}}  

---

## 1. Compliance Control Evaluation Matrix

### Domain 1: Access Control & Identity Management (CC6.1 - CC6.3)

| Control ID | Requirement Description | Implementation Status (Compliant / Non-Compliant / NA) | Evidence Artifact Reference | Owner |
| :--- | :--- | :--- | :--- | :--- |
| CTRL-01 | Multi-Factor Authentication (MFA) required for all systems | Compliant | Okta Enforced Policy Screenshot | IAM Lead |
| CTRL-02 | Quarterly Access Reviews conducted for production systems | Compliant | Q2 Access Review Audit Log | Security Team |
| CTRL-03 | Immediate revoking of terminated user credentials (< 24h) | Compliant | Offboarding HR Ticket Log | HR / IT Ops |

---

### Domain 2: Change Management & SDLC Controls (CC8.1)

| Control ID | Requirement Description | Implementation Status | Evidence Artifact Reference | Owner |
| :--- | :--- | :--- | :--- | :--- |
| CTRL-04 | Pull requests require at least one independent code review | Compliant | GitHub Branch Protection Rule | Dev Lead |
| CTRL-05 | Separation of Duties between Developers and Production Deployer | Compliant | CI/CD RBAC Configuration | DevOps Lead |

---

## 2. Non-Compliance Exception Tracker

| Exception ID | Non-Compliant Control | Business Rationale | Compensating Control Implemented | Exception Expiry Date | Approved By |
| :--- | :--- | :--- | :--- | :--- | :--- |
| EXC-01 | Legacy DB lacks SAML SSO | Replacement scheduled Q4 | Strict IP Whitelisting & Bastion Host | {{EXPIRY_DATE_1}} | {{CISO_NAME}} |

---

## 3. Compliance Sign-off & Audit Readiness

- **Audit Readiness Rating**: 100% Ready for External Audit
- **Sign-off Officer**: {{COMPLIANCE_OFFICER}}  
- **Date**: {{LAST_ASSESSED_DATE}}
