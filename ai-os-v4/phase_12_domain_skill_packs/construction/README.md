---
title: "Construction Management Skill Pack — Master Overview"
document_id: "SPEC-P12-CONST-README"
phase: "phase_12_domain_skill_packs"
domain: "construction"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Construction Management Skill Pack — Master Overview

## Executive Summary
The **Construction Management Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Construction Management**.

- **Domain Category:** Construction Management
- **Domain Code:** CONST
- **Governing Guild:** Construction Operations Guild
- **Applicable Standards:** OSHA 1926, CSI MasterFormat, PMI PMBOK Construction, FIDIC Contracts

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
| `agents/` | `construction_domain_agent.md` | Specification for Construction Project Manager Agent |
| `prompts/` | `construction_system_prompt.md` | System prompt instructions for Construction Management execution |
| `templates/` | `construction_deliverable_template.md` | Deliverable template: Critical Path Method (CPM) Construction Master Schedule Spec |
| `policies/` | `construction_governance_policy.md` | Governance policy: OSHA Construction Safety & Quality Control Policy |
| `workflows/` | `construction_execution_workflow.md` | End-to-end workflow: Subcontractor Procurement & On-Site Safety Audit Workflow |
| `knowledge/` | `construction_domain_knowledge_base.md` | Knowledge repository: Building Construction Logistics, Cost Estimating & Site Risk Controls |
| `verification/` | `construction_quality_verification.md` | Verification gate: Building Code Quality & On-Site Inspection Verification Gate |
| `examples/` | `construction_case_study_example.md` | Enterprise case study: Commercial Distribution Center 18-Month Construction Project |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Construction Management Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "construction",
  "domain_name": "Construction Management",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/construction",
  "active_agent": "agents/construction_domain_agent.md",
  "system_prompt": "prompts/construction_system_prompt.md",
  "governance_policy": "policies/construction_governance_policy.md",
  "verification_gate": "verification/construction_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/construction_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/construction_quality_verification.md` before being marked complete.
