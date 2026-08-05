# Security Audit Workflow Specification

## 1. Purpose & Objective
Perform dynamic/static vulnerability assessments, IAM privilege audits, compliance posture reviews, and penetration testing.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Target application URLs, cloud infrastructure credentials, source code access, security scanning tools.
- **Trigger Conditions**: Scheduled quarterly audit or major infrastructure architecture overhaul.

## 3. Participating Agent Roles & Responsibilities
- **Security Auditor**: Leads security assessment, SAST/DAST scanner runs, and threat modeling.
- **Penetration Tester**: Executes manual penetration testing, exploit POCs, and privilege escalation tests.
- **DevOps Engineer**: Remediates infrastructure misconfigurations and updates security policy configurations.

## 4. Step-by-Step Execution Sequence

### Step 1: Scope Definition & Threat Modeling
- **Inputs**: Architecture diagrams, API specs, IAM role lists.
- **Actions**: Identify attack surface, define audit boundaries, perform STRIDE threat modeling on system components.
- **Outputs**: Security Audit Plan & Threat Model Matrix.
- **Verification**: Security Lead approval of audit scope.

### Step 2: Static & Dynamic Scanning (SAST/DAST)
- **Inputs**: Source repository, staging environment URL, OWASP ZAP / Burp Suite.
- **Actions**: Execute automated SAST on codebase; run DAST crawler against staging endpoints; execute dependency vulnerability scan.
- **Outputs**: Automated Security Scan Findings Log.
- **Verification**: Scan completion with 0 unhandled scanner exceptions.

### Step 3: Manual Penetration & Privilege Escalation Testing
- **Inputs**: Staging environment access, security test accounts.
- **Actions**: Attempt manual SQLi, XSS, CSRF, broken access control (IDOR), and privilege escalation attacks.
- **Outputs**: Penetration Testing Proof-of-Concept (PoC) Log.
- **Verification**: Documented PoC steps for all confirmed security flaws.

### Step 4: Infrastructure & IAM Posture Review
- **Inputs**: Cloud infrastructure account, Prowler / AWS Security Hub.
- **Actions**: Audit IAM roles for over-privileged permissions, inspect S3 bucket policies, verify TLS cipher suite strength.
- **Outputs**: Infrastructure Security Compliance Audit Report.
- **Verification**: Zero publicly exposed sensitive storage buckets or wildcard IAM admin policies.

### Step 5: Executive Findings Report & Remediation Roadmap
- **Inputs**: All audit findings (SAST, DAST, Pen-Test, Infra).
- **Actions**: Risk-rank vulnerabilities using CVSS v3.1 scoring; draft executive summary and prioritized remediation tickets.
- **Outputs**: Executive Security Audit Report & CVSS Remediation Roadmap.
- **Verification**: CISO sign-off on final audit report and remediation SLA targets.

## 5. Decision Gates & Branching Rules
- Gate 1: Critical CVSS score (>= 9.0) findings require immediate emergency patching within 24 hours.
- Gate 2: Executive Security Audit Report must be signed off by CISO before compliance filing.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: DAST scanner causing staging DB corruption -> Action: Pause DAST scan, restore staging database from snapshot, resume with read-only payload settings.
- Failure Mode 2: Over-privileged IAM role identified -> Action: Immediately apply least-privilege policy fix.

## 7. Artifact Delivery & Output Standard
Executive Security Audit Report PDF, CVSS-ranked Vulnerability Backlog, Penetration Testing PoC Artifacts, and Infrastructure Audit Log.
