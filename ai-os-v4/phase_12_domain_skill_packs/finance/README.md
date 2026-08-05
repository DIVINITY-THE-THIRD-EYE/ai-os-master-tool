---
title: "Financial Analysis & FinTech Skill Pack — Master Overview"
document_id: "SPEC-P12-FIN-README"
phase: "phase_12_domain_skill_packs"
domain: "finance"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Financial Analysis & FinTech Skill Pack — Master Overview

## Executive Summary
The **Financial Analysis & FinTech Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Financial Analysis & FinTech**.

- **Domain Category:** Financial Analysis & FinTech
- **Domain Code:** FIN
- **Governing Guild:** Corporate Finance Guild
- **Applicable Standards:** GAAP, IFRS, SOX 404, Basel III / IV, FINRA Rules

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
| `agents/` | `finance_domain_agent.md` | Specification for Financial Analyst Agent |
| `prompts/` | `finance_system_prompt.md` | System prompt instructions for Financial Analysis & FinTech execution |
| `templates/` | `finance_deliverable_template.md` | Deliverable template: Three-Statement Financial Model & Sensitivity Analysis Spec |
| `policies/` | `finance_governance_policy.md` | Governance policy: Financial Reporting Controls & Risk Governance Policy |
| `workflows/` | `finance_execution_workflow.md` | End-to-end workflow: Mergers & Acquisitions Discounted Cash Flow (DCF) Valuation Workflow |
| `knowledge/` | `finance_domain_knowledge_base.md` | Knowledge repository: Quantitative Finance, Capital Structure & Portfolio Optimization |
| `verification/` | `finance_quality_verification.md` | Verification gate: Financial Model Audit & SOX Compliance Verification Gate |
| `examples/` | `finance_case_study_example.md` | Enterprise case study: $500M Series C Enterprise Acquisition Financial Valuation |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Financial Analysis & FinTech Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "finance",
  "domain_name": "Financial Analysis & FinTech",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/finance",
  "active_agent": "agents/finance_domain_agent.md",
  "system_prompt": "prompts/finance_system_prompt.md",
  "governance_policy": "policies/finance_governance_policy.md",
  "verification_gate": "verification/finance_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/finance_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/finance_quality_verification.md` before being marked complete.
