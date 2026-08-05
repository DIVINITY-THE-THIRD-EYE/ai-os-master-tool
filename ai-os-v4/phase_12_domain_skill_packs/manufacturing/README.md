---
title: "Manufacturing Engineering Skill Pack — Master Overview"
document_id: "SPEC-P12-MFG-README"
phase: "phase_12_domain_skill_packs"
domain: "manufacturing"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Manufacturing Engineering Skill Pack — Master Overview

## Executive Summary
The **Manufacturing Engineering Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Manufacturing Engineering**.

- **Domain Category:** Manufacturing Engineering
- **Domain Code:** MFG
- **Governing Guild:** Industrial Operations Guild
- **Applicable Standards:** ISO 9001, IATF 16949, IEC 62264 (ISA-95), Lean Six Sigma

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
| `agents/` | `manufacturing_domain_agent.md` | Specification for Manufacturing Operations Agent |
| `prompts/` | `manufacturing_system_prompt.md` | System prompt instructions for Manufacturing Engineering execution |
| `templates/` | `manufacturing_deliverable_template.md` | Deliverable template: Standard Operating Procedure (SOP) & Production Control Plan |
| `policies/` | `manufacturing_governance_policy.md` | Governance policy: Industrial Safety & Quality Management Policy |
| `workflows/` | `manufacturing_execution_workflow.md` | End-to-end workflow: Automated Assembly Line Optimization Workflow |
| `knowledge/` | `manufacturing_domain_knowledge_base.md` | Knowledge repository: Lean Manufacturing, OEE & Cellular Production Knowledge Base |
| `verification/` | `manufacturing_quality_verification.md` | Verification gate: Six Sigma Process Capability & Defect Verification Gate |
| `examples/` | `manufacturing_case_study_example.md` | Enterprise case study: Automotive Robotic Assembly Line Throughput Optimization |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Manufacturing Engineering Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "manufacturing",
  "domain_name": "Manufacturing Engineering",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/manufacturing",
  "active_agent": "agents/manufacturing_domain_agent.md",
  "system_prompt": "prompts/manufacturing_system_prompt.md",
  "governance_policy": "policies/manufacturing_governance_policy.md",
  "verification_gate": "verification/manufacturing_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/manufacturing_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/manufacturing_quality_verification.md` before being marked complete.
