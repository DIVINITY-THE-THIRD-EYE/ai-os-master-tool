# Compliance Audit Workflow Specification

## 1. Purpose & Objective
Conduct enterprise compliance assessments against SOC2, ISO 27001, GDPR, and HIPAA frameworks, collecting evidence and gap analysis reports.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Regulatory framework baselines, policy documentation, system audit logs, IAM configurations.
- **Trigger Conditions**: Annual compliance cycle or external audit request.

## 3. Participating Agent Roles & Responsibilities
- **Compliance Officer**: Oversees compliance framework mapping, policy enforcement, and auditor liaison.
- **Security Auditor**: Collects technical evidence, reviews security configurations, and audits access controls.
- **Systems Specialist**: Provides system configurations, log exports, and infrastructure evidence artifacts.

## 4. Step-by-Step Execution Sequence

### Step 1: Framework Scope Definition & Policy Audit
- **Inputs**: Target regulatory framework (SOC2 Type II / ISO 27001), corporate policies.
- **Actions**: Map framework control criteria to internal operational policies; verify annual policy review status.
- **Outputs**: Compliance Control Matrix & Scope Document.
- **Verification**: Compliance Officer approval of control matrix.

### Step 2: Automated Evidence Collection
- **Inputs**: Cloud infrastructure account, Vanta / Drata compliance automation tool.
- **Actions**: Collect automated evidence (IAM policies, MFA enforcement, disk encryption, backup logs, access reviews).
- **Outputs**: Compliance Evidence Repository & Automated Log Collection.
- **Verification**: 100% automated evidence check execution across cloud accounts.

### Step 3: Manual Sampling & Access Review Audit
- **Inputs**: User access lists, ticket logs, HR termination records.
- **Actions**: Sample employee onboarding/offboarding tickets, verify timely access revocation, review privileged access logs.
- **Outputs**: Access Control & Sampling Audit Log.
- **Verification**: Zero unrevoked terminated employee accounts found in active directory.

### Step 4: Gap Analysis & Remediation Plan
- **Inputs**: Evidence repository, control matrix.
- **Actions**: Identify non-compliant controls, score risk levels, draft corrective action requests (CARs) for control owners.
- **Outputs**: Compliance Gap Analysis Report & Remediation Roadmap.
- **Verification**: Control owner sign-off on remediation timelines.

### Step 5: Audit Package Compilation & Filing
- **Inputs**: All evidence artifacts, gap analysis report, policy documents.
- **Actions**: Compile master compliance binder; submit package to external AICPA / ISO auditor for formal audit examination.
- **Outputs**: Final Audit Package & Compliance Certificate Request.
- **Verification**: External auditor formal receipt and acceptance of audit binder.

## 5. Decision Gates & Branching Rules
- Gate 1: Zero unrevoked access instances for terminated employees allowed in audit sampling.
- Gate 2: Remediation of high-risk compliance gaps required before final external audit submission.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Missing backup restoration evidence -> Action: Execute manual backup restoration test immediately, log evidence artifact.
- Failure Mode 2: Unencrypted database volume detected -> Action: Issue emergency ticket to encrypt volume, update infrastructure Terraform policy.

## 7. Artifact Delivery & Output Standard
Compliance Control Matrix, Automated Evidence Archives, Gap Analysis Report, and Final External Audit Package.
