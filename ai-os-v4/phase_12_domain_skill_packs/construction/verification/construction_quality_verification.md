---
title: "Building Code Quality & On-Site Inspection Verification Gate"
document_id: "SPEC-P12-CONST-VRF-001"
phase: "phase_12_domain_skill_packs"
domain: "construction"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Building Code Quality & On-Site Inspection Verification Gate

## 1. Verification Gate Specification Overview
This document specifies the quantitative quality verification protocol for **Construction Management**. Every output generated within this domain MUST undergo automated verification against this specification before achieving `APPROVED` status.

---

## 2. Verification Gate Metric Framework

### Quantitative Scoring Equation
- **Final Score:** Quality Score = (0.40 * Spec Score) + (0.30 * Policy Score) + (0.30 * Performance Score)
- **Spec Score:** Conformance to template schema `SPEC-P12-CONST-TPL-001`.
- **Policy Score:** Compliance with policy rules in `SPEC-P12-CONST-POL-001`.
- **Performance Score:** Execution SLA & technical accuracy.

---

## 3. Mandatory Audit Checklist

| Check ID | Verification Item | Target Standard | Pass Threshold | Automated Test Method |
| :--- | :--- | :--- | :--- | :--- |
| VRF-001 | Frontmatter Metadata Validity | CONVENTIONS.md | 100% | Regex & Schema Linter |
| VRF-002 | Normative Standards Reference | OSHA 1926, CSI MasterFormat, PMI PMBOK Construction, FIDIC Contracts | Referenced | Text Parser |
| VRF-003 | Technology Stack Alignment | Procore, Primavera P6, Autodesk Build, RSMeans Cost Data, HeavyBid, DroneDeploy | Valid Stack | Dependency Analyzer |
| VRF-004 | Safety & Fail-Safe Definition | SPEC-P12-CONST-POL-001 | Pass | Policy Rule Engine |
| VRF-005 | Technical Prose Substantiveness | Minimum 300 words | Pass | Word Counter |

---

## 4. Test Suite Implementation (JSON Schema)
```json
{
  "verification_suite_id": "VRF-CONST-SUITE",
  "domain": "construction",
  "pass_threshold": 0.95,
  "test_cases": [
    {
      "id": "TC-CONST-01",
      "name": "Metadata Validation",
      "assertion": "frontmatter.status == 'APPROVED'"
    },
    {
      "id": "TC-CONST-02",
      "name": "Standards Check",
      "assertion": "contains_any(standards, ["OSHA 1926", "CSI MasterFormat", "PMI PMBOK Construction", "FIDIC Contracts"])"
    },
    {
      "id": "TC-CONST-03",
      "name": "Schema Conformance",
      "assertion": "validate_schema(artifact, 'SPEC-P12-CONST-TPL-001')"
    }
  ]
}
```
