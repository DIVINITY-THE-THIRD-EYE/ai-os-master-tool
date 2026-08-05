---
title: "Healthcare & Clinical Operations Skill Pack — Master Overview"
document_id: "SPEC-P12-HEALTH-README"
phase: "phase_12_domain_skill_packs"
domain: "healthcare"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Healthcare & Clinical Operations Skill Pack — Master Overview

## Executive Summary
The **Healthcare & Clinical Operations Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Healthcare & Clinical Operations**.

- **Domain Category:** Healthcare & Clinical Operations
- **Domain Code:** HEALTH
- **Governing Guild:** Clinical Informatics Guild
- **Applicable Standards:** HIPAA Privacy/Security, HL7 FHIR v4, DICOM, FDA 21 CFR Part 820, ISO 13485

---

## Skill Pack Directory Structure

This domain skill pack contains all 8 mandatory domain subdirectories:

1. **`agents/`** — Dedicated domain agent specification defining role, authority, decision rules, quality metrics, and prompt configurations.
2. **`prompts/`** — Production-grade domain system prompt providing explicit task execution guidance, edge case handling, and reasoning protocols.
3. **`templates/`** — Standardized technical specification and document templates for domain deliverables.
4. **`policies/`** — Regulatory, compliance, safety, and operational governance policies.
5. **`workflows/`** — End-to-end execution process workflows with clear step-by-step phases, input/output interfaces, and gate conditions.
6. **`knowledge/`** — Deep domain knowledge base, architectural patterns, technical principles, and anti-patterns.
7. **`verification/`** — Quantitative quality verification gates, automated validation specs, and test criteria.
8. **`examples/`** — Real-world, concrete enterprise case studies and implementation walkthroughs.

---

## Subdirectory Manifest & File Inventory

| Subdirectory | Asset File | Purpose & Description |
| :--- | :--- | :--- |
| `agents/` | `healthcare_domain_agent.md` | Specification for Clinical Informatics Agent |
| `prompts/` | `healthcare_system_prompt.md` | System prompt instructions for Healthcare & Clinical Operations execution |
| `templates/` | `healthcare_deliverable_template.md` | Deliverable template: Clinical Trial Protocol & SaMD Software Requirements Document |
| `policies/` | `healthcare_governance_policy.md` | Governance policy: Patient Health Information (PHI) Security & HIPAA Compliance Policy |
| `workflows/` | `healthcare_execution_workflow.md` | End-to-end workflow: Telehealth Patient Intake & EHR FHIR Integration Workflow |
| `knowledge/` | `healthcare_domain_knowledge_base.md` | Knowledge repository: Medical Terminology (ICD-10, SNOMED CT, LOINC) & Clinical Pathways |
| `verification/` | `healthcare_quality_verification.md` | Verification gate: FDA SaMD Quality System & Clinical Safety Verification Gate |
| `examples/` | `healthcare_case_study_example.md` | Enterprise case study: AI-Assisted Diagnostic Radiography EHR Integration Pipeline |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Healthcare & Clinical Operations Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "healthcare",
  "domain_name": "Healthcare & Clinical Operations",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/healthcare",
  "active_agent": "agents/healthcare_domain_agent.md",
  "system_prompt": "prompts/healthcare_system_prompt.md",
  "governance_policy": "policies/healthcare_governance_policy.md",
  "verification_gate": "verification/healthcare_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/healthcare_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/healthcare_quality_verification.md` before being marked complete.
