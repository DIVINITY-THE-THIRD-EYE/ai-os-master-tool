# Enterprise Backup & Retention Policy: {{SYSTEM_NAME}}

> **Policy ID**: POL-BACKUP-{{POLICY_ID}}  
> **Document Type**: Data Backup & Retention Standard  
> **Status**: {{DOCUMENT_STATUS}}  
> **Policy Owner**: {{POLICY_OWNER}} (Database Administrator Lead)  
> **Compliance Target**: SOC 2 Type II / ISO 27001  
> **Effective Date**: {{EFFECTIVE_DATE}}  
> **Version**: {{DOCUMENT_VERSION}}  

---

## 1. Scope & Backup Objectives

### 1.1 Scope
This policy governs all persistent data stores, relational databases, document databases, file systems, and configuration state across production environments.

### 1.2 Recovery Targets
- **Recovery Point Objective (RPO)**: <= {{RPO_MINUTES}} Minutes (Continuous WAL Streaming)
- **Recovery Time Objective (RTO)**: <= {{RTO_HOURS}} Hours

---

## 2. Backup Schedules & Technical Specifications

| Data Store / Asset | Backup Type | Frequency | Storage Target / Bucket | Retention Period | Encryption Protocol |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Primary Database | Full Snapshot | Daily at 01:00 UTC | AWS S3 Bucket `{{BACKUP_BUCKET}}` | 30 Days | KMS AES-256 |
| Transaction Logs | Continuous WAL | Every 5 Minutes | AWS S3 Bucket `{{WAL_BUCKET}}` | 7 Days | KMS AES-256 |
| Configuration / Secrets | Export File | Weekly | Vault Encrypted Storage | 90 Days | AES-256 |
| Offsite Immutable Copy | Object Lock Snapshot | Monthly | Cross-Region Glacier Bucket | 7 Years | AWS S3 Object Lock |

---

## 3. Automated Backup Verification & Restore Testing

- **Automated Verification**: Nightly backup restoration script restores snapshot to sandbox database and runs integrity validation query:
  ```sql
  SELECT COUNT(*) FROM {{PRIMARY_TABLE}};
  ```
- **Quarterly Drill**: DR team conducts manual full restoration exercise every 90 days.

---

## 4. Roles & Responsibilities

| Role | Responsibility | Contact |
| :--- | :--- | :--- |
| Lead DBA | Manages automated backup configurations and snapshot policies | {{DBA_EMAIL}} |
| Security Analyst | Audits S3 Object Lock and encryption compliance | {{SECURITY_EMAIL}} |
