---
title: "Electrical & Power Engineering Skill Pack — Master Overview"
document_id: "SPEC-P12-ELEC-README"
phase: "phase_12_domain_skill_packs"
domain: "electrical"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Electrical & Power Engineering Skill Pack — Master Overview

## Executive Summary
The **Electrical & Power Engineering Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Electrical & Power Engineering**.

- **Domain Category:** Electrical & Power Engineering
- **Domain Code:** ELEC
- **Governing Guild:** Electrical Engineering Guild
- **Applicable Standards:** IEEE 1584, IPC-2221, IEC 61000, NEC (NFPA 70), UL 60950-1

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
| `agents/` | `electrical_domain_agent.md` | Specification for Electrical & Embedded Systems Agent |
| `prompts/` | `electrical_system_prompt.md` | System prompt instructions for Electrical & Power Engineering execution |
| `templates/` | `electrical_deliverable_template.md` | Deliverable template: Hardware Schematic & Bill of Materials (BOM) Specification |
| `policies/` | `electrical_governance_policy.md` | Governance policy: Electrical Safety, Insulation, and EMI/EMC Compliance Policy |
| `workflows/` | `electrical_execution_workflow.md` | End-to-end workflow: High-Speed PCB Design & EMC Verification Workflow |
| `knowledge/` | `electrical_domain_knowledge_base.md` | Knowledge repository: Power Converter Topologies & Signal Integrity Fundamentals |
| `verification/` | `electrical_quality_verification.md` | Verification gate: Printed Circuit Board Electrical & Thermal Verification Gate |
| `examples/` | `electrical_case_study_example.md` | Enterprise case study: Industrial IoT Sensor Node PCB Design & Wireless Certification |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Electrical & Power Engineering Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "electrical",
  "domain_name": "Electrical & Power Engineering",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/electrical",
  "active_agent": "agents/electrical_domain_agent.md",
  "system_prompt": "prompts/electrical_system_prompt.md",
  "governance_policy": "policies/electrical_governance_policy.md",
  "verification_gate": "verification/electrical_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/electrical_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/electrical_quality_verification.md` before being marked complete.
