---
title: "Supply Chain & Logistics Skill Pack — Master Overview"
document_id: "SPEC-P12-SCM-README"
phase: "phase_12_domain_skill_packs"
domain: "supply_chain"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Supply Chain & Logistics Skill Pack — Master Overview

## Executive Summary
The **Supply Chain & Logistics Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Supply Chain & Logistics**.

- **Domain Category:** Supply Chain & Logistics
- **Domain Code:** SCM
- **Governing Guild:** Supply Chain Guild
- **Applicable Standards:** APICS SCOR Model, ISO 28000, GS1 Standards, Incoterms 2020

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
| `agents/` | `supply_chain_domain_agent.md` | Specification for Supply Chain Planner Agent |
| `prompts/` | `supply_chain_system_prompt.md` | System prompt instructions for Supply Chain & Logistics execution |
| `templates/` | `supply_chain_deliverable_template.md` | Deliverable template: Supplier Performance Scorecard & Evaluation Matrix Document |
| `policies/` | `supply_chain_governance_policy.md` | Governance policy: Global Trade Compliance & Responsible Sourcing Policy |
| `workflows/` | `supply_chain_execution_workflow.md` | End-to-end workflow: Global Demand Forecasting & Multi-Echelon Inventory Workflow |
| `knowledge/` | `supply_chain_domain_knowledge_base.md` | Knowledge repository: Logistics Network Optimization, Bullwhip Effect & Safety Stock Models |
| `verification/` | `supply_chain_quality_verification.md` | Verification gate: Vendor SLA Compliance & Cold Chain Audit Verification Gate |
| `examples/` | `supply_chain_case_study_example.md` | Enterprise case study: Pharmaceutical Cold Chain Logistics Network Optimization |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Supply Chain & Logistics Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "supply_chain",
  "domain_name": "Supply Chain & Logistics",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/supply_chain",
  "active_agent": "agents/supply_chain_domain_agent.md",
  "system_prompt": "prompts/supply_chain_system_prompt.md",
  "governance_policy": "policies/supply_chain_governance_policy.md",
  "verification_gate": "verification/supply_chain_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/supply_chain_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/supply_chain_quality_verification.md` before being marked complete.
