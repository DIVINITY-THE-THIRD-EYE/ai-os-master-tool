# Data Privacy & Protection Specification: {{SYSTEM_NAME}}

> **Document Type**: Data Privacy & Regulatory Specification  
> **Status**: {{DOCUMENT_STATUS}}  
> **Data Protection Officer (DPO)**: {{DPO_NAME}}  
> **Lead Author**: {{DOCUMENT_AUTHOR}}  
> **Regulatory Frameworks**: GDPR / CCPA / HIPAA / PIPEDA  
> **Effective Date**: {{EFFECTIVE_DATE}}  
> **Version**: {{DOCUMENT_VERSION}}  

---

## 1. Executive Summary & Privacy Scope

### 1.1 Overview
*Instruction: Detail how {{SYSTEM_NAME}} collects, processes, stores, and safeguards Personally Identifiable Information (PII) and Sensitive Personal Data.*

---

## 2. PII Data Inventory & Classification

| Data Field / Attribute | Classification (PII / Sensitive PII / Anonymous) | Legal Basis for Processing | Storage Location | Retention Period | Encryption Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| User Full Name | PII | Contract Fulfillment | Primary PostgreSQL DB | Account Lifetime + 30 Days | AES-256 |
| Email Address | PII | Consent / Contract | Primary PostgreSQL DB | Account Lifetime + 30 Days | AES-256 |
| Credit Card Details | Sensitive PII (PCI-DSS) | Payment Processing | Tokenized (Stripe API) | Zero Local Storage | Tokenized External |
| IP Address / Geolocation | PII | Fraud Prevention | Audit Log Storage | 90 Days | TLS 1.3 / AES-256 |

---

## 3. Data Subject Rights (DSR) Workflows

### 3.1 Right to Access (DSAR)
- Automated API endpoint (`/api/v1/user/export-data`) returns full JSON export of user records within 48 hours of request.

### 3.2 Right to be Forgotten (Data Erasure)
- Permanent hard-deletion execution script purges user records from primary stores and replaces operational log references with anonymized hashes within 30 days.

---

## 4. Third-Party Data Sharing & Sub-Processors

| Sub-Processor Name | Service Provided | Data Shared | Processing Region | Privacy Shield / DPA Status |
| :--- | :--- | :--- | :--- | :--- |
| {{SUBPROCESSOR_1}} | Transactional Email | Email, Name | USA (US-EU DPF Certified) | DPA Signed |
| {{SUBPROCESSOR_2}} | Cloud Infrastructure | Encrypted Database Snapshots | EU-Central (Frankfurt) | DPA Signed |

---

## 5. Privacy Impact Assessment (PIA) & Controls

- **Pseudonymization**: User IDs obfuscated in analytics and logging environments.
- **Breach Notification Protocol**: Mandated notification to DPO and affected regulatory bodies within 72 hours of verified data leak.
