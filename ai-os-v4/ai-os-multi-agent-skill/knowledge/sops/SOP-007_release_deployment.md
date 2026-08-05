# Standard Operating Procedure: SOP-007

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-007
- **Title**: Release Management, Automated Deployment, Canary Traffic Shifting, and Verification
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Release Engineering & Continuous Deployment (CD)

---

## 2. Purpose & Objectives
The purpose of SOP-007 is to define a zero-downtime, deterministic release deployment process that packages, verifies, stages, and deploys software artifacts into production environments while maintaining automated rollback capabilities.

### Key Objectives:
1. **Dual-Attestation Enforcement**: Mandate that no code enters production without verified Quality (SOP-005) and Security (SOP-006) attestations.
2. **Zero-Downtime Deployment**: Utilize Canary or Blue/Green deployment topologies to ensure continuous service availability.
3. **Automated Rollback Guard**: Monitor real-time error telemetry; trigger instant automatic rollback if error rates exceed $\text{Error}_{rate} > 0.01\%$.
4. **Traceable Release Metadata**: Enforce Semantic Versioning (SemVer 2.0) and immutably record deployment provenance.

---

## 3. Scope & Applicability
This procedure applies to:
- Build packaging, container image tagging, database migrations, progressive traffic routing, smoke testing, and post-release validation.
- The **Release Engineer / DevOps Agent (A08)** as primary authority, in coordination with the **Solution Architect (A03)**, **QA Verification Agent (A06)**, and **Master Orchestrator (A01)**.

This procedure does **not** cover initial code implementation (SOP-004) or post-incident root cause reflection (SOP-009).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Receipt of dual cryptographically signed attestations (`quality_attestation.pem` and `security_attestation.pem`).
- **Trigger Condition 2**: Scheduled release window authorization dispatch from Master Orchestrator (A01).
- **Frequency**: Event-driven per approved release build candidate.

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Quality Attestation (SOP-005) and Security Attestation (SOP-006) cryptographically verified.
- Target cloud/k8s cluster infrastructure operational with active health status.
- Deployment configuration loaded from `policies/deployment_policy.yaml`.

### Required Inputs
1. `release_manifest.json` (JSON object, required): Target version string, commit SHA, and changed module index.
2. `quality_attestation.pem` (File, required): QA verification signoff.
3. `security_attestation.pem` (File, required): Security audit signoff.
4. `environment_config` (YAML object, required): Target cluster endpoint, namespace, and resource limits.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Release Engineer** | A08_DevOpsRelease | **Accountable (A) / Responsible (R)** | Executes build packaging, manages traffic shifting, monitors telemetry. |
| **Solution Architect** | A03_Architect | **Consulted (C)** | Approves schema migrations and infrastructure scaling rules. |
| **QA Verification Agent** | A06_QAVerifier | **Consulted (C)** | Executes post-deployment staging and canary smoke tests. |
| **Incident Manager** | A09_IncidentRecovery | **Consulted (C)** | Stands by during production rollout in case rollback triggers. |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Authorizes transition to `STATE_RELEASE`. |

---

## 7. Step-by-Step Execution Procedure

```
 [Signed Attestations] ---> (Step 1: Attestation Verification & SemVer Tagging)
                                     |
                                     v
                              (Step 2: Artifact Container Packaging)
                                     |
                                     v
                              (Step 3: Staging Deployment & Smoke Test)
                                     |
                                     v
                              (Step 4: Database Schema Migration)
                                     |
                              (Step 5: Canary Traffic Shifting)
                                  [10% -> 50% -> 100%]
                                     |
           +-------------------------+-------------------------+
           | Telemetry Error > 0.01%                           | Error <= 0.01% & P99 Healthy
           v                                                   v
(AUTOMATED ROLLBACK TO HEAD-1)                        (Step 6: Release Finalization)
           |                                                   |
           v                                                   v
[Trigger SOP-008 Incident]                          [release_deployment_report.json]
```

### Step 1: Pre-Flight Attestation & Semantic Versioning
- **1.1 Signature Audit**: Verify cryptographic signatures on `quality_attestation.pem` and `security_attestation.pem` against public release keyring.
- **1.2 Version Calculation**: Parse current release version (`vX.Y.Z`). Compute new version string following SemVer rules:
  - **MAJOR** (`vX+1.0.0`): Breaking API changes.
  - **MINOR** (`vX.Y+1.0`): Backward-compatible new features.
  - **PATCH** (`vX.Y.Z+1`): Backward-compatible bug fixes.

### Step 2: Container & Artifact Packaging
- **2.1 Immudb Build**: Compile immutable binaries / container images tagged with release version and git commit hash (e.g., `ai-os-core:v1.4.0-a7f3b9c`).
- **2.2 Artifact Registry Push**: Push signed image artifacts to target private container registry.

### Step 3: Staging Environment Deployment & Smoke Testing
- **3.1 Staging Provisioning**: Deploy packaged artifacts to staging namespace (`env-staging`).
- **3.2 Synthetic Smoke Test**: QA Agent (A06) executes automated synthetic user workflow suite (`tests/smoke/staging_smoke.py`). Ensure 100% pass rate before production approval.

### Step 4: Zero-Downtime Migration Execution
- **4.1 Forward Migration**: Execute database schema migrations using backward-compatible expansion strategy (add columns without dropping existing fields).

### Step 5: Canary Rollout & Traffic Shifting
- **5.1 Stepwise Shifting Phase**:
  - **Phase A (Canary 10%)**: Route 10% of live production traffic to new deployment pods. Observe for 5 minutes.
  - **Phase B (Canary 50%)**: Increase traffic routing to 50%. Observe for 10 minutes.
  - **Phase C (Full Release 100%)**: Route 100% traffic to new release pods upon sustained healthy metrics.

### Step 6: Telemetry Monitoring & Automated Rollback Safety
- **6.1 Metric Guard Verification**: Continuously evaluate telemetry over 15-minute window:
  - Service Availability $\ge 99.99\%$.
  - HTTP 5xx Error Rate $\le 0.01\%$.
  - Latency $p99 \le 120\text{ms}$.
- **6.2 Automated Rollback Action**: If any threshold is breached, instant rollback protocol activates: terminate canary pods, revert ingress route to previous stable release tag, and emit incident event.

### Step 7: Post-Deployment Finalization & Promotion
- **7.1 Baseline Promotion**: Promote new deployment tag as stable HEAD. Decommission legacy pods gracefully.
- **7.2 Release Notes Generation**: Publish automated release notes (`RELEASE_NOTES_vX.Y.Z.md`) documenting merged FRs and commit history.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 7: Release & Deployment Gate
--------------------------------------------------------------------------------------
Check Metric                         | Threshold Requirement | PASS Action | FAIL Action
--------------------------------------------------------------------------------------
Quality & Security Attestations      | Valid Cryptographic   | Advance     | Reject Deployment
Staging Smoke Test Pass Rate         | Exactly 100%          | Advance     | Abort Rollout
Canary HTTP 5xx Error Rate           | <= 0.01%              | Shift Next  | TRIGGER ROLLBACK
Canary Latency p99                   | <= 120 ms             | Shift Next  | TRIGGER ROLLBACK
Infrastructure Pod Health           | 100% Ready Status     | Final Lock  | Freeze Deployment
--------------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- 100% traffic shifted to new version with zero downtime.
- Telemetry guard metrics clean for $\ge 15$ continuous minutes.
- Release tagged in git repository.

### Deliverables
1. `knowledge/artifacts/release/release_deployment_report.json` — Deployment execution log.
2. `knowledge/artifacts/release/RELEASE_NOTES_vX.Y.Z.md` — User-facing changelog document.
3. `knowledge/artifacts/release/provenance_manifest.json` — Cryptographic provenance metadata.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Canary Telemetry Breach (Error Rate > 0.01%)**
  - *Action*: Automated Instant Rollback executed in $< 30 \text{ seconds}$. Traffic restored to previous version.
  - *Escalation*: Trigger SOP-008 (Incident Recovery) for immediate telemetry diagnostic.
- **Failure Scenario B: Database Schema Migration Failure**
  - *Action*: Trigger migration rollback script (`down.sql`). Suspend deployment pipeline.
  - *Escalation*: Escalate to Solution Architect (A03) and Lead Developer (A05).

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log generated upon successful release deployment, saved to `logs/audit/sops/sop_007_audit.json`:

```json
{
  "sop_id": "SOP-007",
  "execution_id": "exec_20260805_007621",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A08_DevOpsRelease",
  "release_details": {
    "target_version": "v1.4.0",
    "previous_version": "v1.3.9",
    "git_commit_sha": "a7f3b9c812d4...",
    "deployment_strategy": "CANARY_STEPWISE",
    "rollback_triggered": false,
    "telemetry_error_rate_p99": 0.002
  },
  "deliverable_path": "knowledge/artifacts/release/release_deployment_report.json",
  "verification_status": "PASSED",
  "signature": "5e4d3c2b1a0f..."
}
```
