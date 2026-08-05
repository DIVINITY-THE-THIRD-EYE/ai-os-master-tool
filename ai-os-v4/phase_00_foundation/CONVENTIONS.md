---
title: System Specification Conventions & Standards
document_id: SPEC-P00-CONV-001
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Core Architecture Group
last_updated: 2026-08-05
---

# AI OS v4 — System Conventions & Specification Standard

## Executive Summary
This document establishes the binding repository-wide standards for naming conventions, directory organization, metadata headers, and structural guidelines across all 16 phases of the AI Operating System v4 (AI OS v4) enterprise suite. Strict adherence to this document ensures interoperability, deterministic parsing, schema validation, and automated compliance checking across agents, runtime engines, and verification tooling.

---

## 1. Naming Conventions

All assets in the AI OS v4 repository must strictly conform to naming rules determined by file type and role.

### 1.1 Directory & File Naming Matrix

| Asset Category | Target File/Dir Format | Case Convention | Example |
| :--- | :--- | :--- | :--- |
| **Phase Directories** | `phase_{xx}_{phase_name}` | `snake_case` with 2-digit prefix | `phase_00_foundation`, `phase_01_core_runtime` |
| **Specification Files** | `{index}_{name}.md` or `{name}.md` | `snake_case` | `01_repository_structure.md`, `ai_kernel.md` |
| **Agent Spec Files** | `{agent_name}_agent.md` | `snake_case` | `architect_agent.md`, `qa_engineer_agent.md` |
| **Agent Prompt Files** | `{agent_name}_prompt.md` | `snake_case` | `architect_prompt.md`, `qa_engineer_prompt.md` |
| **JSON Schema Files** | `{schema_name}.schema.json` | `snake_case` | `agent_definition.schema.json`, `workflow_task.schema.json` |
| **Workflow Files** | `{workflow_name}_workflow.md` | `snake_case` | `software_development_workflow.md` |
| **Template Files** | `{template_name}_template.md` | `snake_case` | `architecture_decision_record_template.md` |
| **Domain Skill Packs** | `{domain_name}` | `snake_case` | `software_engineering`, `cybersecurity` |
| **TypeScript / JS Modules** | `{component_name}.ts` | `kebab-case` | `execution-context.ts`, `dag-scheduler.ts` |
| **Python Modules** | `{module_name}.py` | `snake_case` | `runtime_manager.py`, `event_bus.py` |
| **JSON / Config Keys** | `camelCase` / `snake_case` | Standard per schema | JSON: `camelCase`, YAML/Env: `SNAKE_CASE` / `snake_case` |

### 1.2 Case Conversion Rules
- **snake_case**: Lowercase alphanumeric characters separated by underscores `_`. No consecutive underscores allowed (`foo__bar` is forbidden).
- **kebab-case**: Lowercase alphanumeric characters separated by hyphens `-`. Used for source code files in Web/TypeScript packages.
- **camelCase**: Starts with lowercase letter; each internal word capitalized. Used for JSON object field names.
- **PascalCase**: Starts with uppercase letter; used for TypeScript interfaces, classes, and JSON schema title fields.
- **SCREAMING_SNAKE_CASE**: Uppercase alphanumeric separated by underscores. Used exclusively for environment variables, system constants, and error codes (`ERR_KERNEL_PANIC`).

---

## 2. Directory Hierarchy & Taxonomy

The repository follows a deterministic 16-Phase structure rooted at `ai-os-v4/`.

```text
ai-os-v4/
├── .agents/                        # Agent workspace metadata (plan, briefing, progress, handoff)
│   └── worker_p0_p1/
├── phase_00_foundation/           # Phase 00: Foundation & Standards (20 files min)
│   ├── CONVENTIONS.md
│   ├── 01_repository_structure.md
│   └── ...
├── phase_01_core_runtime/         # Phase 01: Kernel, Messaging, Scheduler, Safety (40 files min)
│   ├── ai_kernel.md
│   ├── agent_communication_protocol.md
│   ├── dag_scheduler.md
│   └── ...
├── phase_02_agent_framework/      # Phase 02: 35 Agents + 35 Prompts (70 files)
├── phase_03_prompt_library/       # Phase 03: 120-150 Prompt Templates across 20 categories
├── phase_04_workflow_library/     # Phase 04: 50-70 End-to-End Workflows
├── phase_05_knowledge_platform/   # Phase 05: Knowledge Graph, Ontology, Rules
├── phase_06_memory_system/        # Phase 06: Working, Session, Persistent Memory
├── phase_07_decision_engine/      # Phase 07: Decision Trees, Risk, Priority Matrix
├── phase_08_reflection_learning/  # Phase 08: Failure Analysis, Pattern Detection
├── phase_09_verification_platform/# Phase 09: Output Validators & Quality Gates
├── phase_10_template_library/     # Phase 10: 60-80 Document Templates
├── phase_11_schemas/              # Phase 11: 40+ JSON Schemas
├── phase_12_domain_skill_packs/   # Phase 12: 18 Domain Skill Packs
├── phase_13_plugin_framework/     # Phase 13: Sandboxing, Permission, Tool Registry
├── phase_14_runtime_policies/     # Phase 14: Execution, Security, Memory Policies
└── phase_15_enterprise_docs/      # Phase 15: Developer Guides, SDK Specs, ADRs
```

### 2.1 Directory Isolation Rules
1. `.agents/` contains only runtime task state, briefings, execution plans, and handoff reports. Source files, production code, or system specifications MUST NOT be placed inside `.agents/`.
2. Each Phase folder must be self-contained; cross-phase references MUST use absolute repository-relative paths (e.g., `ai-os-v4/phase_00_foundation/CONVENTIONS.md`).

---

## 3. Metadata Header Standard (YAML Frontmatter)

Every Markdown specification file across all phases MUST begin with a strict YAML frontmatter block enclosed between triple hyphens `---`.

### 3.1 Metadata Field Specifications

```yaml
---
title: <Human-readable Document Title>
document_id: SPEC-<PHASE_CODE>-<COMPONENT_CODE>-<NUMBER>
phase: <phase_folder_name>
version: <Semantic Version string, e.g., 1.0.0>
status: <DRAFT | UNDER_REVIEW | APPROVED | DEPRECATED>
owner: <Group or Role Name, e.g., Kernel Working Group>
last_updated: <YYYY-MM-DD>
---
```

### 3.2 Required Header Fields Matrix

| Field | Type | Regex / Validation | Description |
| :--- | :--- | :--- | :--- |
| `title` | string | `^[A-Z][A-Za-z0-9 \-\—\(\)]+$` | Full formal title of document |
| `document_id` | string | `^SPEC-P[0-1][0-5]-[A-Z0-9]+-[0-9]{3}$` | Unique identifier across system |
| `phase` | string | `^phase_[0-1][0-9]_[a-z_]+$` | Target directory name |
| `version` | string | `^[0-9]+\.[0-9]+\.[0-9]+$` | Semantic version |
| `status` | enum | `DRAFT \| UNDER_REVIEW \| APPROVED \| DEPRECATED` | Current document lifecycle state |
| `owner` | string | Non-empty string | Group or role owning specification |
| `last_updated` | string | `^\d{4}-\d{2}-\d{2}$` | ISO 8601 Date string |

---

## 4. File Format Guidelines

### 4.1 Markdown Structure
All Markdown specifications MUST contain the following structural sections:
1. **Title H1 (`# Title`)**: Matches frontmatter `title`.
2. **Executive Summary & Overview**: High-level motivation, scope, and target state.
3. **Architecture & Component Diagram**: ASCII diagram illustrating boundaries and state flow.
4. **Configuration / Schema / Type Contracts**: Formal TypeScript interfaces, JSON schemas, or YAML definitions.
5. **Behavioral Rules & State Machine**: Invariants, guards, and transition definitions.
6. **API Specifications & Interfaces**: Method signatures, parameters, return types, error codes.
7. **Operational Guidelines & SLA Constraints**: P95 latency, retry limits, logging, telemetry rules.

### 4.2 Code Snippet Formatting
- Code blocks MUST declare explicit language identifiers (`yaml`, `json`, `typescript`, `python`, `bash`).
- JSON configuration samples MUST be strictly valid JSON (no trailing commas, double-quoted keys).
- TypeScript interface definitions MUST use explicit types (`string`, `number`, `boolean`, `Record<string, unknown>`), avoiding `any`.

---

## 5. Verification & Compliance Checking

Specification files are verified against these standards using automated linter scripts (`agy spec-lint`):
1. **Header Validation**: Verifies YAML frontmatter presence and schema compliance.
2. **Naming Check**: Validates file path matches kebab/snake case rules.
3. **Link Integrity**: Checks relative and absolute markdown link targets exist.
4. **Substantive Quality Gate**: Ensures minimum 300 words per specification file, with at least one code snippet or ASCII diagram.

---

## 6. Revision History

| Version | Date | Author | Description |
| :--- | :--- | :--- | :--- |
| `1.0.0` | 2026-08-05 | Core Architecture Group | Initial Release of AI OS v4 Specification Standards |
