---
title: "FDA SaMD Quality System & Clinical Safety Verification Gate"
document_id: "SPEC-P12-HEALTH-VRF-001"
phase: "phase_12_domain_skill_packs"
domain: "healthcare"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# FDA SaMD Quality System & Clinical Safety Verification Gate

## 1. Verification Gate Specification Overview
This document specifies the quantitative quality verification protocol for **Healthcare & Clinical Operations**. Every output generated within this domain MUST undergo automated verification against this specification before achieving `APPROVED` status.

---

## 2. Verification Gate Metric Framework

### Quantitative Scoring Equation
- **Final Score:** Quality Score = (0.40 * Spec Score) + (0.30 * Policy Score) + (0.30 * Performance Score)
- **Spec Score:** Conformance to template schema `SPEC-P12-HEALTH-TPL-001`.
- **Policy Score:** Compliance with policy rules in `SPEC-P12-HEALTH-POL-001`.
- **Performance Score:** Execution SLA & technical accuracy.

---

## 3. Mandatory Audit Checklist

| Check ID | Verification Item | Target Standard | Pass Threshold | Automated Test Method |
| :--- | :--- | :--- | :--- | :--- |
| VRF-001 | Frontmatter Metadata Validity | CONVENTIONS.md | 100% | Regex & Schema Linter |
| VRF-002 | Normative Standards Reference | HIPAA Privacy/Security, HL7 FHIR v4, DICOM, FDA 21 CFR Part 820, ISO 13485 | Referenced | Text Parser |
| VRF-003 | Technology Stack Alignment | Epic Systems APIs, Cerner Open Developer, HAPI FHIR, Python PyHealth, Orthanc DICOM | Valid Stack | Dependency Analyzer |
| VRF-004 | Safety & Fail-Safe Definition | SPEC-P12-HEALTH-POL-001 | Pass | Policy Rule Engine |
| VRF-005 | Technical Prose Substantiveness | Minimum 300 words | Pass | Word Counter |

---

## 4. Test Suite Implementation (JSON Schema)
```json
{
  "verification_suite_id": "VRF-HEALTH-SUITE",
  "domain": "healthcare",
  "pass_threshold": 0.95,
  "test_cases": [
    {
      "id": "TC-HEALTH-01",
      "name": "Metadata Validation",
      "assertion": "frontmatter.status == 'APPROVED'"
    },
    {
      "id": "TC-HEALTH-02",
      "name": "Standards Check",
      "assertion": "contains_any(standards, ["HIPAA Privacy/Security", "HL7 FHIR v4", "DICOM", "FDA 21 CFR Part 820", "ISO 13485"])"
    },
    {
      "id": "TC-HEALTH-03",
      "name": "Schema Conformance",
      "assertion": "validate_schema(artifact, 'SPEC-P12-HEALTH-TPL-001')"
    }
  ]
}
```
