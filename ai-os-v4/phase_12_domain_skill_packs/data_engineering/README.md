---
title: "Data Engineering & Analytics Skill Pack — Master Overview"
document_id: "SPEC-P12-DATA-README"
phase: "phase_12_domain_skill_packs"
domain: "data_engineering"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Data Engineering & Analytics Skill Pack — Master Overview

## Executive Summary
The **Data Engineering & Analytics Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Data Engineering & Analytics**.

- **Domain Category:** Data Engineering & Analytics
- **Domain Code:** DATA
- **Governing Guild:** Data Platform Guild
- **Applicable Standards:** DAMA-DMBOK, ISO/IEC 25012, Data Mesh Principles, OpenLineage

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
| `agents/` | `data_engineering_domain_agent.md` | Specification for Data Engineering Agent |
| `prompts/` | `data_engineering_system_prompt.md` | System prompt instructions for Data Engineering & Analytics execution |
| `templates/` | `data_engineering_deliverable_template.md` | Deliverable template: Data Pipeline Specification & Data Contract Schema Document |
| `policies/` | `data_engineering_governance_policy.md` | Governance policy: Data Governance, Privacy Anonymization & Lineage Tracking Policy |
| `workflows/` | `data_engineering_execution_workflow.md` | End-to-end workflow: Real-Time Streaming ETL & Lakehouse Data Modeling Workflow |
| `knowledge/` | `data_engineering_domain_knowledge_base.md` | Knowledge repository: Dimensional Data Modeling (Kimball), Lakehouse Architecture & Stream Processing |
| `verification/` | `data_engineering_quality_verification.md` | Verification gate: Data Quality Expectations & Schema Evolution Verification Gate |
| `examples/` | `data_engineering_case_study_example.md` | Enterprise case study: Real-Time E-Commerce Clickstream Analytics Lakehouse Pipeline |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Data Engineering & Analytics Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "data_engineering",
  "domain_name": "Data Engineering & Analytics",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/data_engineering",
  "active_agent": "agents/data_engineering_domain_agent.md",
  "system_prompt": "prompts/data_engineering_system_prompt.md",
  "governance_policy": "policies/data_engineering_governance_policy.md",
  "verification_gate": "verification/data_engineering_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/data_engineering_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/data_engineering_quality_verification.md` before being marked complete.
