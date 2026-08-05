---
title: Repository Structure & Taxonometric Blueprint Specification
document_id: SPEC-P00-REPO-001
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Platform Infrastructure Team
last_updated: 2026-08-05
---

# Repository Structure & Taxonometric Blueprint

## Executive Summary
This document specifies the complete file layout, directory hierarchy, module boundaries, and asset taxonomy for the AI OS v4 repository. It defines clear separation of concerns between core runtime kernel services, multi-agent frameworks, prompt/workflow libraries, knowledge platforms, memory systems, and enterprise documentation.

---

## 1. Top-Level Directory Taxonomy

```text
ai-os-v4/
├── .agents/                        # Agent workspace metadata & execution state tracking
│   └── worker_p0_p1/               # Working folder for worker_p0_p1
├── phase_00_foundation/           # Phase 00: Core System Standards & Governance Specs
├── phase_01_core_runtime/         # Phase 01: Kernel, Messaging, Scheduler & Health Specs
├── phase_02_agent_framework/      # Phase 02: 35 Specialized Agent Specs & Prompt Specifications
├── phase_03_prompt_library/       # Phase 03: 120-150 Enterprise Prompt Templates (20 categories)
├── phase_04_workflow_library/     # Phase 04: 50-70 End-to-End Multi-Agent Workflow Graphs
├── phase_05_knowledge_platform/   # Phase 05: Knowledge Graph, Rule Engine & Ontology Specs
├── phase_06_memory_system/        # Phase 06: Working, Session, Persistent Memory Engine Specs
├── phase_07_decision_engine/      # Phase 07: Decision Trees, Trade-off Matrix & Arbitration Specs
├── phase_08_reflection_learning/  # Phase 08: Reflection Engine, RCA & Prompt Optimizer Specs
├── phase_09_verification_platform/# Phase 09: Verification Engine, Quality Gates & Compliance Checkers
├── phase_10_template_library/     # Phase 10: 60-80 Document Templates (ADR, API, Incident, SOP)
├── phase_11_schemas/              # Phase 11: 40+ Enterprise JSON Schema Definitions
├── phase_12_domain_skill_packs/   # Phase 12: 18 Domain Skill Packs (Software, AI, Cloud, Legal, etc.)
├── phase_13_plugin_framework/     # Phase 13: Tool Registry, Sandbox Runtime & Security Policies
├── phase_14_runtime_policies/     # Phase 14: Runtime Governance, Security & Escalation Policies
└── phase_15_enterprise_docs/      # Phase 15: Developer Manuals, SDK Specs, Operator Guides & ADRs
```

---

## 2. Directory Taxonomies & File Distribution Rules

### 2.1 Subsystem Allocation Matrix

| Phase Directory | Min Files | Primary Target Components | Subdirectory Taxonomy |
| :--- | :---: | :--- | :--- |
| `phase_00_foundation` | 20 | Conventions, Coding Standards, Security Policies, Quotas | Flat root inside phase directory |
| `phase_01_core_runtime` | 40 | Kernel, Messaging, Scheduler, Health & Safety Specs | Flat root inside phase directory |
| `phase_02_agent_framework` | 70 | 35 Agent Specifications + 35 Matching Prompts | Categorized by function (Management, Engineering, etc.) |
| `phase_03_prompt_library` | 120 | System, Planning, Review, Verification, Optimization Prompts | 20 domain subdirectories |
| `phase_04_workflow_library` | 50 | Software, Hardware, Business, Cloud, Ops Workflows | Flat root inside phase directory |
| `phase_05_knowledge_platform` | 12 | Enterprise Knowledge Graph, Ontology, Rule Engine | Subdirectories: `graph/`, `rules/`, `ontology/` |
| `phase_06_memory_system` | 10 | Working, Session, Persistent Memory, Compression | Subdirectories: `working/`, `session/`, `persistent/` |
| `phase_07_decision_engine` | 10 | Decision Trees, Risk Engine, Conflict Arbitration | Flat root inside phase directory |
| `phase_08_reflection_learning`| 10 | RCA, Reflection, Prompt Auto-Tuning | Flat root inside phase directory |
| `phase_09_verification_platform`| 12| Logic, Security, Performance, Compliance Validators | Subdirectories: `checkers/`, `validators/` |
| `phase_10_template_library` | 60 | Architecture, Release, Plan, Spec, SOP Templates | Categorized by document archetype |
| `phase_11_schemas` | 40 | JSON Schema specs ($schema v7/2020-12) | Flat root with `.schema.json` extension |
| `phase_12_domain_skill_packs` | 144 | 18 Specialized Enterprise Domains | 18 domain folders, each containing 8 subdirs |
| `phase_13_plugin_framework` | 10 | Sandboxing, Tool Permissions, Capabilities | Flat root inside phase directory |
| `phase_14_runtime_policies` | 10 | Execution, Memory, Verification, Escalate Policies | Flat root inside phase directory |
| `phase_15_enterprise_docs` | 12 | Developer Guides, SDK Specs, ADRs | Subdirectories: `adrs/`, `guides/`, `sdks/` |

---

## 3. Storage Invariants & Layout Integrity

1. **Isolation of Agent Metadata**: The `.agents/` directory is reserved strictly for agent workspace tracking (`plan.md`, `progress.md`, `briefing.md`, `handoff.md`). No production specs or code assets may reside in `.agents/`.
2. **Deterministic File Resolution**: All references across phases MUST use repository-relative paths: `ai-os-v4/phase_xx_name/file_name.md`.
3. **No Circular Dependencies**: Dependencies between specification documents must follow a strict directed acyclic hierarchy from Phase 00 ➔ Phase 15.

---

## 4. Verification Protocol

The repository layout is verified using the layout auditor CLI command:
```bash
agy verify-layout --root ./ai-os-v4 --min-files 450
```
Validation checks:
- Absence of source/test files in `.agents/`.
- File count compliance per phase directory.
- Conformity with `CONVENTIONS.md` naming rules.
