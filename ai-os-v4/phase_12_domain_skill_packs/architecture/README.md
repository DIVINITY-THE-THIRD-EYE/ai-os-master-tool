---
title: "Architectural Design Skill Pack — Master Overview"
document_id: "SPEC-P12-ARCH-README"
phase: "phase_12_domain_skill_packs"
domain: "architecture"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Architectural Design Skill Pack — Master Overview

## Executive Summary
The **Architectural Design Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Architectural Design**.

- **Domain Category:** Architectural Design
- **Domain Code:** ARCH
- **Governing Guild:** Architectural Practice Guild
- **Applicable Standards:** AIA Document Standards, ISO 19650 (BIM), LEED v4.1, IBC Accessibility (ADA)

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
| `agents/` | `architecture_domain_agent.md` | Specification for Architectural Design Agent |
| `prompts/` | `architecture_system_prompt.md` | System prompt instructions for Architectural Design execution |
| `templates/` | `architecture_deliverable_template.md` | Deliverable template: Architectural Programming & Spatial Requirements Document |
| `policies/` | `architecture_governance_policy.md` | Governance policy: Sustainable Building & Passive Design Compliance Policy |
| `workflows/` | `architecture_execution_workflow.md` | End-to-end workflow: BIM Schematic Design to Construction Documentation Workflow |
| `knowledge/` | `architecture_domain_knowledge_base.md` | Knowledge repository: BIM Execution Standards, Urban Zoning & Building Envelope Performance |
| `verification/` | `architecture_quality_verification.md` | Verification gate: BIM Clash Detection & Accessibility Compliance Verification |
| `examples/` | `architecture_case_study_example.md` | Enterprise case study: 40-Story Net-Zero Energy Commercial Office Tower BIM Model |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Architectural Design Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "architecture",
  "domain_name": "Architectural Design",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/architecture",
  "active_agent": "agents/architecture_domain_agent.md",
  "system_prompt": "prompts/architecture_system_prompt.md",
  "governance_policy": "policies/architecture_governance_policy.md",
  "verification_gate": "verification/architecture_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/architecture_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/architecture_quality_verification.md` before being marked complete.
