# Standard Operating Procedure: SOP-006

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-006
- **Title**: Security Audit, Threat Modeling, Vulnerability Assessment, and Compliance Certification
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Cyber Security, Governance, and Risk Management

---

## 2. Purpose & Objectives
The purpose of SOP-006 is to establish an uncompromising, automated security auditing process that identifies, triages, and eliminates security vulnerabilities, credential leaks, dependency risks, and architectural security flaws before code enters production.

### Key Objectives:
1. **Zero High/Critical Vulnerabilities**: Enforce absolute rejection of any codebase containing CVSS v3.1 score $\ge 7.0$ (High/Critical) vulnerabilities.
2. **Credential Leak Prevention**: Ensure 0 hardcoded secrets, API keys, private keys, tokens, or environment credentials exist within source repositories.
3. **Software Bill of Materials (SBOM) Integrity**: Audit third-party dependencies against known CVE databases (NVD/GitHub Advisory) to eliminate supply chain attack vectors.
4. **OWASP Top 10 Compliance**: Guarantee complete mitigation against injection, broken authentication, sensitive data exposure, and insecure deserialization.

---

## 3. Scope & Applicability
This procedure applies to:
- Static Application Security Testing (SAST), Secret Scanning, Dependency Scanning (SCA), Container Security Audits, and Compliance Checks.
- The **Security Auditor (A07)** as primary authority, in coordination with the **Solution Architect (A03)**, **Lead Developer (A05)**, and **Human Safety Officer**.

This procedure does **not** cover general functional bug fixing (SOP-005) or infrastructure recovery (SOP-008).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Successful certification of Quality Assurance Gate from SOP-005.
- **Trigger Condition 2**: Modification of third-party dependency files (e.g., `requirements.txt`, `package.json`, `Cargo.toml`).
- **Frequency**: Triggered automatically per release candidate build prior to deployment phase.

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Code base verified functional with active quality attestation from SOP-005.
- SAST scanners (e.g., `bandit`, `semgrep`, `gitleaks`, `trivy`) installed and operational.
- Security policies loaded from `policies/security_policy.yaml`.

### Required Inputs
1. `quality_attestation.pem` (File, required): Valid quality signoff artifact from SOP-005.
2. `source_repository` (Directory path, required): Root path of source code to be scanned.
3. `security_policy_manifest` (YAML object, required): Active security policy baseline rules.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Security Auditor** | A07_SecurityAuditor | **Accountable (A) / Responsible (R)** | Runs SAST/SCA scanners, performs CVSS scoring, issues security attestation. |
| **Lead Developer** | A05_LeadDev | **Consulted (C)** | Remediates identified security vulnerabilities and updates libraries. |
| **Solution Architect** | A03_Architect | **Consulted (C)** | Redesigns security boundaries if architectural flaw is discovered. |
| **Human Safety Officer** | Human_Security_Lead | **Informed / Consulted (I/C)** | Notified immediately if zero-day or critical exploit path is detected. |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Blocks deployment pipeline upon security audit failure. |

---

## 7. Step-by-Step Execution Procedure

```
 [Quality Attestation] ---> (Step 1: Secret & Credential Leak Scan)
                                   |
                                   v
                            (Step 2: SAST Static Code Audit)
                                   |
                                   v
                            (Step 3: Dependency SCA & SBOM Audit)
                                   |
                                   v
                            (Step 4: Threat Model & Access Control Audit)
                                   |
           +-----------------------+-----------------------+
           | CVSS >= 7.0 or Secret Found                  | CVSS < 7.0 & Secrets == 0
           v                                               v
(Step 5: Security Block & Triage)                 (Step 6: Security Attestation)
           |                                               |
           v                                               v
[Remediation Package -> A05]                    [security_audit_report.json]
```

### Step 1: Secret & Credential Leak Scanning
- **1.1 Deep Entropy & Pattern Scan**: Run secret scanning tool (e.g., `gitleaks detect --verbose`) across all git commits, source files, documentation, and configuration files.
- **1.2 High-Entropy String Detection**: Flag any string exhibiting entropy $H \ge 4.5$ matching known credential signatures (e.g., AWS Access Keys, JWT secrets, RSA private keys, API tokens).

### Step 2: Static Application Security Testing (SAST)
- **2.1 Rule Set Dispatch**: Run AST static security scanners (e.g., `bandit -r src/`, `semgrep --config p/security-audit`).
- **2.2 OWASP Risk Check**: Audit for critical code flaws:
  - SQL / Command / Prompt Injection vulnerabilities.
  - Path Traversal (`../../`) exploits.
  - Insecure Cryptographic Algorithms (e.g., MD5, SHA1 usage for hashing passwords).
  - Unsanitized User Input rendering.

### Step 3: Software Bill of Materials (SBOM) & Dependency Audit
- **3.1 SBOM Generation**: Generate standard CycloneDX or SPDX JSON SBOM listing all direct and transitive third-party dependencies.
- **3.2 Vulnerability Lookup (SCA)**: Scan SBOM against the National Vulnerability Database (NVD) using tools like `trivy fs` or `pip-audit`.

### Step 4: Threat Model & Access Control Verification
- **4.1 Privilege Escalation Check**: Audit API endpoints for explicit authentication and role-based access control (RBAC) middleware decorators.
- **4.2 Data Protection Audit**: Verify sensitive data fields (PII, tokens) are encrypted at rest (AES-256-GCM) and in transit (TLS 1.3).

### Step 5: Vulnerability Severity Scoring & Triaging (If Flaws Exist)
- **5.1 CVSS v3.1 Scoring**: Compute vector score for every detected finding:
  - **CRITICAL** ($9.0 - 10.0$): Immediate release block. Fix SLA: $< 4 \text{ hours}$.
  - **HIGH** ($7.0 - 8.9$): Immediate release block. Fix SLA: $< 24 \text{ hours}$.
  - **MEDIUM** ($4.0 - 6.9$): Conditional release block depending on context.
  - **LOW** ($0.1 - 3.9$): Non-blocking warning logged to technical debt registry.
- **5.2 Remediation Package Assembly**: Construct detailed remediation guide including exact CVE ID, line number, vector description, and suggested patch version.

### Step 6: Security Certification & Attestation Sign-off
- **6.1 Security Gate Verification**: If Critical = 0, High = 0, and Secrets Found = 0, issue cryptographically signed `security_attestation.pem`.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 6: Security Verification Gate
--------------------------------------------------------------------------------------
Check Category                       | Tolerance Limit    | Result = PASS | Result = FAIL
--------------------------------------------------------------------------------------
Hardcoded Secrets / Credentials     | Exactly 0          | Advance       | CRITICAL SECURITY BLOCK
CVSS Critical (9.0-10.0) CVEs       | Exactly 0          | Advance       | CRITICAL SECURITY BLOCK
CVSS High (7.0-8.9) CVEs            | Exactly 0          | Advance       | HIGH SECURITY BLOCK
OWASP Injection Vulnerabilities      | Exactly 0          | Advance       | HIGH SECURITY BLOCK
SBOM Dependency Scan                | Clean / Patched    | Pass Gate     | Reject Dependencies
--------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- Zero detected hardcoded secrets across all files.
- Zero CVSS $\ge 7.0$ (High/Critical) security vulnerabilities present.
- 100% dependency license and CVE audit pass rate.
- Formal signoff by Security Auditor (A07).

### Deliverables
1. `knowledge/artifacts/security/security_audit_report.json` — Comprehensive audit report.
2. `knowledge/artifacts/security/sbom.json` — CycloneDX format Software Bill of Materials.
3. `knowledge/artifacts/security/security_attestation.pem` — Signed cryptographic security passport.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Hardcoded Secret Discovered in Code Repository**
  - *Action*: Instantly revoke detected credential key via cloud API. Block release pipeline.
  - *Escalation*: Trigger SOP-010 immediately for incident notification and secret rotation.
- **Failure Scenario B: Unfixable Zero-Day CVE in Upstream Library**
  - *Action*: Halt release. Quarantine target library.
  - *Escalation*: Escalate to Solution Architect (A03) to replace dependency with secure alternative module.

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log generated upon completion of security audit, stored at `logs/audit/sops/sop_006_audit.json`:

```json
{
  "sop_id": "SOP-006",
  "execution_id": "exec_20260805_006734",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A07_SecurityAuditor",
  "security_summary": {
    "total_files_scanned": 142,
    "secrets_detected": 0,
    "sast_findings_critical": 0,
    "sast_findings_high": 0,
    "sast_findings_medium": 1,
    "cve_vulnerabilities_high_critical": 0,
    "sbom_component_count": 38
  },
  "deliverable_path": "knowledge/artifacts/security/security_audit_report.json",
  "verification_status": "PASSED",
  "signature": "6f5e4d3c2b1a..."
}
```
