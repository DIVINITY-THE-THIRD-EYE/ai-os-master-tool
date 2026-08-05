# Enterprise Risk Assessment Matrix: {{PROJECT_NAME}}

> **Document Type**: Qualitative & Quantitative Risk Assessment Matrix  
> **Status**: {{DOCUMENT_STATUS}}  
> **Risk Analyst**: {{ANALYST_NAME}}  
> **Target Scope**: Enterprise Architecture & Project Delivery  
> **Last Evaluated**: {{LAST_EVALUATED_DATE}}  

---

## 1. Risk Scoring Framework

```
                 IMPACT
          Low(1)   Med(2)   High(3)  Crit(4)
       +--------+--------+--------+--------+
Crit(4)|   4    |   8    |   12   |   16   | <-- High Risk (Urgent Action)
High(3)|   3    |   6    |   9    |   12   |
Med(2) |   2    |   4    |   6    |   8    |
Low(1) |   1    |   2    |   3    |   4    | <-- Acceptable Risk
       +--------+--------+--------+--------+
```

---

## 2. Risk Assessment Findings Table

| Threat / Risk Event | Likelihood (1-4) | Impact (1-4) | Overall Rating | Inherent Risk Score | Current Controls Implemented | Residual Risk Score | Action Required? | Risk Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Unencrypted Database Backups | 2 | 4 | High | 8 | Automated AWS KMS Encryption | 2 (Low) | No | {{DBA_LEAD}} |
| Third-party API Service Outage | 3 | 3 | High | 9 | Multi-provider Fallback | 3 (Low) | No | {{TECH_LEAD}} |
| Single Point of Failure in Auth Service | 2 | 4 | High | 8 | Multi-region Cluster Deployment | 2 (Low) | No | {{INFRA_LEAD}} |

---

## 3. Residual Risk Sign-off

- **Acceptable Threshold**: Residual score <= 4.
- **Risk Acceptance Sign-off**: Approved by {{ANALYST_NAME}} and {{CISO_NAME}}.
