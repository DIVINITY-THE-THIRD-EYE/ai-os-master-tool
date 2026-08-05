# Enterprise Security Policy: {{POLICY_TITLE}}

> **Policy ID**: SEC-POL-{{POLICY_NUMBER}}  
> **Document Type**: Information Security Policy  
> **Status**: {{DOCUMENT_STATUS}}  
> **Chief Information Security Officer (CISO)**: {{CISO_NAME}}  
> **Policy Owner**: {{POLICY_OWNER}}  
> **Effective Date**: {{EFFECTIVE_DATE}}  
> **Compliance Standard**: ISO 27001 / SOC 2 Type II / NIST CSF  
> **Version**: {{DOCUMENT_VERSION}}  

---

## 1. Purpose & Scope

### 1.1 Purpose
*Instruction: State the core security objectives, compliance mandates, and organizational risk tolerance addressed by this policy.*

### 1.2 Scope
This policy applies to all employees, contractors, third-party partners, and automated systems accessing {{ORGANIZATION_NAME}} infrastructure and data assets.

---

## 2. Security Standards & Mandatory Mandates

### 2.1 Identity & Access Governance (IAM)
- **Multi-Factor Authentication (MFA)**: Mandatory for all accounts across all environments without exception.
- **Password Complexity**: Minimum 16 characters, mandatory upper/lower/number/symbol combinations, auto-expiry every 90 days.
- **Principle of Least Privilege**: Access granted based strictly on role requirements (RBAC) and recertified quarterly.

### 2.2 Data Security & Encryption Standards
- **In-Transit Encryption**: TLS 1.3 required for external ingress; minimum TLS 1.2 for internal service mesh communication.
- **At-Rest Encryption**: AES-256 bit encryption required for all block storage, database storage, and backup snapshots.
- **Secret Management**: Plaintext credentials forbidden in source code or configuration files. Must use Vault or Cloud Secret Manager.

### 2.3 Network & Endpoint Security
- All endpoints must run corporate EDR agent with automatic definitions update.
- Production networks isolated inside private VPC subnets with ingress firewalls denying all incoming traffic by default.

---

## 3. Incident Reporting & Vulnerability Disclosure

- Any suspected data breach or security incident must be reported immediately to `security@{{DOMAIN}}` or via `#security-incidents`.
- Critical vulnerabilities discovered via SAST/DAST or bug bounty must be remediated within 24 hours.

---

## 4. Compliance Audits & Non-Compliance Enforcement

- **Audits**: Internal security reviews conducted bi-monthly; third-party SOC 2 audits conducted annually.
- **Violations**: Failure to adhere to this policy may result in immediate suspension of access credentials and formal disciplinary action up to termination.

---

## 5. Policy Sign-off & Revision History

| Version | Revision Date | Author | Approved By |
| :--- | :--- | :--- | :--- |
| 1.0.0 | {{EFFECTIVE_DATE}} | {{POLICY_OWNER}} | {{CISO_NAME}} |
