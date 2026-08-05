# AI OS v4 Multi-Agent Release Rules (`release_rules.md`)

## 1. Executive Summary & Release Lifecycle

Release operations in AI OS v4 are governed by strict automation, risk-weighted approval gates, canary rollouts, and zero-downtime deployment rules. Release Manager (A10) oversees all deployment cycles.

---

## 2. Release Rule Specifications

### Rule REL-001: Semantic Versioning (SemVer 2.0.0) Mandate
- **Rule ID**: `REL-001`
- **Severity**: `CRITICAL`
- **Scope**: All Package Releases, Skill Packs, and Core Engine Versions
- **Description**: Version numbers MUST follow `MAJOR.MINOR.PATCH` format:
  - `MAJOR`: Incompatible API or breaking ontology schema changes.
  - `MINOR`: Backwards-compatible new feature additions or new specialized agents.
  - `PATCH`: Backwards-compatible bug fixes, security patches, or prompt refinements.

### Rule REL-002: Mandatory Release Readiness Checklist (Gate Zero)
- **Rule ID**: `REL-002`
- **Severity**: `CRITICAL`
- **Scope**: Release Deployment Candidate
- **Description**: Before a release candidate (RC) can proceed to deployment, all items in the release checklist must evaluate to `PASS`:
  - [x] $100\%$ of automated test suites pass (unit, integration, end-to-end).
  - [x] Security Auditor (A07) attestation signed with zero `HIGH`/`CRITICAL` vulnerabilities.
  - [x] Compliance Auditor (A08) regulatory verification completed.
  - [x] Quality Assurance (A06) coverage requirement satisfied ($\ge 85\%$).
  - [x] Performance baseline latency within target bounds ($P_{99} \le 50\text{ms}$).

### Rule REL-003: Progressive Canary Deployment Strategy
- **Rule ID**: `REL-003`
- **Severity**: `HIGH`
- **Scope**: Production Deployments
- **Description**: Direct $100\%$ cutover to production is prohibited for `MAJOR` or `MINOR` releases. Deployments must follow progressive traffic shifting:
  1. `Stage 1 (Canary 5%)`: Route $5\%$ of workflow executions for 15 minutes.
  2. `Stage 2 (Canary 25%)`: Route $25\%$ traffic for 30 minutes if error rate is zero.
  3. `Stage 3 (Canary 50%)`: Route $50\%$ traffic for 1 hour.
  4. `Stage 4 (Full Cutover 100%)`: Complete deployment.

### Rule REL-004: Automated Rollback Triggers & Fast Recovery
- **Rule ID**: `REL-004`
- **Severity**: `EMERGENCY`
- **Scope**: Canary & Production Deployments
- **Description**: Rollback to the previous stable release hash MUST execute automatically if any of the following metric conditions occur during canary deployment:
  - Error rate increases by $> 0.1\%$ over baseline.
  - $P_{99}$ latency exceeds $150\text{ms}$ (3x SLA limit).
  - Any `EVT_SEC_VULNERABILITY` or uncaught panic event is emitted.
  - Rollback completion SLA: $< 60$ seconds.

### Rule REL-005: Dual Cryptographic Release Signing
- **Rule ID**: `REL-005`
- **Severity**: `CRITICAL`
- **Scope**: Release Artifacts & Git Tags
- **Description**: Release tags and release artifact bundles must be cryptographically signed using GPG or Cosign keys controlled by `A10 (Release Manager)` and `A07 (Security Auditor)`. Unsigned release bundles cannot be deployed to runtime environments.

### Rule REL-006: Zero-Downtime Database Migration Policy
- **Rule ID**: `REL-006`
- **Severity**: `HIGH`
- **Scope**: Schema Migrations
- **Description**: Database migrations must be backwards-compatible with the currently running application version. Expanding schema changes (adding tables/columns) must precede code deployment; contracting changes (dropping columns) must execute in a subsequent release cycle (`Expand-Contract Pattern`).

### Rule REL-007: Release Sign-off Matrix
- **Rule ID**: `REL-007`
- **Severity**: `CRITICAL`
- **Scope**: Release Approval Gate
- **Description**: Releases require explicit approval signatures based on scope:
  | Release Type | Required Approvers | Approval Mechanism |
  |---|---|---|
  | `PATCH` | Release Manager (A10) + QA Agent (A06) | Automated Verification |
  | `MINOR` | A10 + System Architect (A03) + Security (A07) | Automated + Security Sign-off |
  | `MAJOR` | A10 + A03 + A07 + Master Orchestrator (A01) + Human Lead | Multi-Signature Token Gate |

### Rule REL-008: Release Artifact Immutability & Registry Retention
- **Rule ID**: `REL-008`
- **Severity**: `HIGH`
- **Scope**: Container Images & Artifact Packages
- **Description**: Published release packages (Docker images, NPM/PyPI packages, skill zips) must be tagged with unique immutable hashes. Overwriting an existing version tag in the artifact registry is blocked.

### Rule REL-009: Mandatory Post-Deployment Smoke Test Protocol
- **Rule ID**: `REL-009`
- **Severity**: `HIGH`
- **Scope**: Post-Cutover Phase
- **Description**: Immediately following 100% traffic cutover, automated smoke test suites must execute synthetic end-to-end workflows. Failure of smoke tests immediately triggers Rule REL-004 (Rollback).

### Rule REL-010: Emergency Hotfix Protocol (P0 Bypass Path)
- **Rule ID**: `REL-010`
- **Severity**: `CRITICAL`
- **Scope**: Emergency Production Bugs
- **Description**: Critical production fixes (`P0`) may bypass canary staging windows provided:
  - Fix contains ONLY lines directly addressing the incident.
  - Security Auditor (A07) and Lead Engineer (A04) issue immediate override tokens.
  - Post-mortem ticket is created automatically within 2 hours.
