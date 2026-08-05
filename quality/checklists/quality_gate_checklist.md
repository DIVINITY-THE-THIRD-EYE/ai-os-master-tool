# Quality Gate Evaluation Checklist
**Document ID:** CHK-GATE-006  
**Version:** 4.0.0  
**Package:** `ai-os-multi-agent-skill`  
**Target Role:** A05 Quality & Verification Authority  
**Scope:** Automated & manual quality gate evaluation, threshold verification, and override governance  

---

## 1. Metadata & Control Header

| Attribute | Value |
|---|---|
| **Checklist ID** | CHK-GATE-006 |
| **Target Specification** | `quality/quality_gates.yaml` & `quality/scoring_thresholds.yaml` |
| **Required Sign-Off** | Quality Authority (A05) |
| **Evaluation Scope** | All 7 Quality Gates (GATE-01 through GATE-07) |
| **Execution Engine** | `MOD-SYNTAX-01` through `MOD-COMP-06` |

---

## 2. Pre-Evaluation Prerequisites

- [ ] **Target Commit / Artifact Identified**: Commit SHA or build artifact ID captured.
- [ ] **Verification Engine Status**: All verification engine modules operational and online.
- [ ] **Scoring Metric Inputs Available**: Raw metrics (lint, security, test, arch, compliance) ingested.

---

## 3. Step-by-Step Gate Evaluation Procedure

### 3.1 Gate-01 (Syntax & Format Gate) Verification
- [ ] **AST Parsing**: 0 syntax errors detected across Python, SQL, JS files.
- [ ] **YAML & JSON Schema Parsing**: All YAML configs and JSON schema files parse validly.
- [ ] **Markdown Structure**: Header structures and link formatting valid.
- [ *Gate Status* ]: **PASSED / FAILED**

### 3.2 Gate-02 (Static Analysis & Lint Gate) Verification
- [ ] **Lint Violations**: 0 Critical, 0 Major lint violations reported by `MOD-LINT-02`.
- [ ] **Maintainability Index**: Codebase maintainability index >= 75.0 (or environment threshold).
- [ ] **Complexity Limit**: Maximum function cyclomatic complexity <= 10.
- [ *Gate Status* ]: **PASSED / FAILED**

### 3.3 Gate-03 (Unit & Integration Test Gate) Verification
- [ ] **Test Execution**: Unit test pass rate = 100.0%, integration test pass rate = 100.0%.
- [ ] **Line Coverage**: Line coverage >= 85.0% (Production threshold 92.0%).
- [ ] **Branch Coverage**: Branch coverage >= 80.0% (Production threshold 92.0%).
- [ *Gate Status* ]: **PASSED / FAILED**

### 3.4 Gate-04 (Security & Vulnerability Gate) Verification
- [ ] **SAST Findings**: 0 Critical, 0 High vulnerabilities.
- [ ] **Secret Leaks**: 0 secret leak alerts detected by secret scanner.
- [ ] **Dependency Audit**: 0 unmitigated vulnerabilities in third-party packages.
- [ *Gate Status* ]: **PASSED / FAILED**

### 3.5 Gate-05 (Architecture & Design Gate) Verification
- [ ] **Dependency Loops**: 0 circular dependencies detected by graph analyzer.
- [ ] **Layer Crossing**: 0 forbidden architectural layer crossings.
- [ ] **Coupling Factor**: Package coupling factor <= 0.45.
- [ *Gate Status* ]: **PASSED / FAILED**

### 3.6 Gate-06 (Compliance & Licensing Gate) Verification
- [ ] **License Compatibility**: 0 incompatible/copyleft license inclusions.
- [ ] **PII Protection**: 0 unencrypted or unflagged PII fields in state/logs.
- [ ] **SOC 2 Audit Controls**: Change management and audit logging requirements met.
- [ *Gate Status* ]: **PASSED / FAILED**

### 3.7 Gate-07 (Production Readiness Gate) Verification
- [ ] **Prior Gate Summary**: Gates GATE-01 through GATE-06 explicitly marked `PASSED`.
- [ ] **Performance SLA**: Smoke and load tests pass within SLA latency targets.
- [ ] **Operational Artifacts**: Rollback runbooks and operational dashboards verified.
- [ *Gate Status* ]: **PASSED / FAILED**

---

## 4. Scoring Calculation & Composite Evaluation

```
CQI Score:   ____  x 0.25 = ____
SPS Score:   ____  x 0.30 = ____
ACI Score:   ____  x 0.15 = ____
TCRI Score:  ____  x 0.20 = ____
CPR Score:   ____  x 0.10 = ____
---------------------------------
COMPOSITE SCORE:          ____ / 100.00

MINIMUM REQUIRED THRESHOLD: [ dev: 70.0 | integration: 80.0 | staging: 90.0 | prod: 95.0 ]
EVALUATION RESULT: [ PASS / FAIL ]
```

---

## 5. Gate Override Governance Protocol

If a gate fails but emergency deployment is requested:

1. **Check Override Eligibility**: Confirm target gate permits override per `quality/quality_gates.yaml`.
2. **Mandatory Justification**: Document root cause, business impact, and temporary mitigation.
3. **Authority Approval**: Obtain digital signature from required authority (e.g. A05 / A06 / A01).
4. **Time-Bound Expiration**: Set maximum override expiration (max 4h to 24h).
5. **Log Audit Trail**: Record override event into `logs/quality_gates_audit.jsonl`.

---

## 6. Gate Authority Audit Sign-Off

```markdown
### Quality Gate Evaluation Certificate
- **Evaluator Agent**: A05 Quality & Verification Authority
- **Evaluation Date**: YYYY-MM-DD THH:MM:SS Z
- **Target Artifact**: Build Candidate ID #_____
- **Final Evaluation**: ALL_GATES_PASSED / OVERRIDE_GRANTED / GATE_FAILED
- **Audit Record ID**: QG-AUDIT-2026-____
- **Signature Hash**: [A05_QUALITY_AUTHORITY_SIG_HASH]
```
