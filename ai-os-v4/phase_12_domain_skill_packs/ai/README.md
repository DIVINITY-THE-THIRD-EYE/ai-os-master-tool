---
title: "Artificial Intelligence & Machine Learning Skill Pack — Master Overview"
document_id: "SPEC-P12-AI-README"
phase: "phase_12_domain_skill_packs"
domain: "ai"
version: "1.0.0"
status: "APPROVED"
owner: "Domain Engineering Guild"
last_updated: "2026-08-05"
---

# Artificial Intelligence & Machine Learning Skill Pack — Master Overview

## Executive Summary
The **Artificial Intelligence & Machine Learning Skill Pack** is a comprehensive, production-grade domain module designed for the AI Operating System (AI OS v4). It encapsulates deep domain expertise, normative standards, actionable templates, governance policies, automated workflows, and verification gates tailored specifically for **Artificial Intelligence & Machine Learning**.

- **Domain Category:** Artificial Intelligence & Machine Learning
- **Domain Code:** AI
- **Governing Guild:** AI/ML Engineering Guild
- **Applicable Standards:** NIST AI RMF, ISO/IEC 42001, EU AI Act, MLOps Lifecycle Standard

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
| `agents/` | `ai_domain_agent.md` | Specification for AI Researcher & MLOps Agent |
| `prompts/` | `ai_system_prompt.md` | System prompt instructions for Artificial Intelligence & Machine Learning execution |
| `templates/` | `ai_deliverable_template.md` | Deliverable template: Machine Learning Model Card & Evaluation Specification |
| `policies/` | `ai_governance_policy.md` | Governance policy: Responsible AI Governance & Model Safety Policy |
| `workflows/` | `ai_execution_workflow.md` | End-to-end workflow: End-to-End LLM Fine-Tuning & Evaluation Workflow |
| `knowledge/` | `ai_domain_knowledge_base.md` | Knowledge repository: Deep Neural Network Architectures & LLM Alignment Techniques |
| `verification/` | `ai_quality_verification.md` | Verification gate: ML Model Performance & Bias Verification Specification |
| `examples/` | `ai_case_study_example.md` | Enterprise case study: Enterprise Retrieval-Augmented Generation (RAG) Pipeline Deployment |

---

## Integration & Execution Guidelines

### Loading the Domain Skill Pack into AI OS v4 Kernel
To activate the **Artificial Intelligence & Machine Learning Skill Pack** in runtime, register the domain manifest with the AI OS Runtime Engine:

```json
{
  "domain_id": "ai",
  "domain_name": "Artificial Intelligence & Machine Learning",
  "version": "1.0.0",
  "base_path": "phase_12_domain_skill_packs/ai",
  "active_agent": "agents/ai_domain_agent.md",
  "system_prompt": "prompts/ai_system_prompt.md",
  "governance_policy": "policies/ai_governance_policy.md",
  "verification_gate": "verification/ai_quality_verification.md"
}
```

### Safety and Compliance Invariants
1. All generated artifacts in this domain MUST strictly comply with the governance rules specified in `policies/ai_governance_policy.md`.
2. Every output MUST pass the automated verification criteria defined in `verification/ai_quality_verification.md` before being marked complete.
