---
title: "Software Engineering Skill Pack — Master Overview"
document_id: "SPEC-P12-SW-README"
phase: "phase_12_domain_skill_packs"
domain: "software"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Software Engineering Skill Pack — Master Overview

## Executive Summary
The **Software Engineering Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Software Engineering**.

- **Domain Category:** Software Engineering
- **Domain Code:** SW
- **Governing Guild:** Software Architecture Guild
- **Applicable Standards:** IEEE 829, ISO/IEC 25010, OWASP Top 10, Twelve-Factor App

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
| `agents/` | `software_domain_agent.md` | Specification for Software Architect Agent |
| `prompts/` | `software_system_prompt.md` | System prompt instructions for Software Engineering execution |
| `templates/` | `software_deliverable_template.md` | Deliverable template: Software Architecture & System Design Document |
| `policies/` | `software_governance_policy.md` | Governance policy: Software Development Lifecycle & Code Quality Policy |
| `workflows/` | `software_execution_workflow.md` | End-to-end workflow: Full-Stack Microservices Feature Execution Workflow |
| `knowledge/` | `software_domain_knowledge_base.md` | Knowledge repository: Distributed Systems & Enterprise Software Architecture Patterns |
| `verification/` | `software_quality_verification.md` | Verification gate: Software Code & Security Verification Gate Specification |
| `examples/` | `software_case_study_example.md` | Enterprise case study: Legacy Monolith to Event-Driven Microservices Migration |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Software Engineering Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "software",
  "domain_name": "Software Engineering",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/software",
  "active_agent": "agents/software_domain_agent.md",
  "system_prompt": "prompts/software_system_prompt.md",
  "governance_policy": "policies/software_governance_policy.md",
  "verification_gate": "verification/software_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/software_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/software_quality_verification.md` before being marked complete.
