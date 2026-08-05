---
title: System Documentation Standards & Formatting Policy
document_id: SPEC-P00-DOC-006
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Technical Writing & Governance Group
last_updated: 2026-08-05
---

# System Documentation Standards & Formatting Policy

## Executive Summary
This document specifies rules for writing, structuring, maintaining, and verifying technical documentation across AI OS v4. It defines required document headers, section hierarchies, visual diagram standards, code example requirements, and documentation freshness guarantees.

---

## 1. Documentation Taxonomy & Archetypes

All technical documentation in AI OS v4 falls into one of five recognized archetypes:

```text
DOCUMENT ARCHETYPES
├── 1. Specifications (SPEC-*)    --> Formal system rules, architecture, schemas
├── 2. ADRs (ADR-*)              --> Architecture Decision Records
├── 3. Standard Operating Procedures (SOP-*) --> Operational procedures & runbooks
├── 4. Developer Guides (GUIDE-*)--> Multi-language SDKs, tutorials, how-tos
└── 5. API References (REF-*)    --> Auto-generated OpenAPI/AsyncAPI specifications
```

---

## 2. Standard Document Anatomy & Header Hierarchy

Every document MUST follow this strict structural layout:

1. **YAML Frontmatter Header**: Document metadata block (see `CONVENTIONS.md`).
2. **Title (H1)**: Single H1 title matching YAML header `title`.
3. **Executive Summary / Purpose**: Concise overview (1-2 paragraphs) stating goal, scope, and target audience.
4. **Architecture & Visual Diagram**: ASCII or Mermaid diagram illustrating component interactions.
5. **Detailed Technical Sections (H2 & H3)**: Core specifications, contracts, and logic chains.
6. **Operational SLA & Error Matrix**: Latency bounds, failure recovery, error taxonomy.
7. **Verification & Audit Protocols**: Concrete CLI commands and test suites for verification.

---

## 3. Visual Diagram Standards (ASCII Rules)

To ensure rendering across terminal viewers, Markdown renderers, and diff tools, diagrams MUST use clean ASCII / Unicode box-drawing characters:

```text
+----------------------+         Event Message         +----------------------+
|  Agent Execution     | ----------------------------> |  Message Broker      |
|  Sandbox Engine      | <---------------------------- |  (NATS / EventBus)   |
+----------------------+       Acknowledgment          +----------------------+
```

Rules:
- Width MUST NOT exceed 80 characters.
- Use explicit direction labels (`--->`, `<---`, `===>`).
- Include a descriptive diagram caption.

---

## 4. Documentation Freshness & CI Automated Audits

1. **Stale Doc Warning**: Docs untouched for > 180 days flag an audit warning.
2. **Broken Link Verification**: All internal Markdown hyper-links are validated via `agy test-links`.
3. **Code Snippet Execution**: Code samples in specifications MUST be extracted and compiled during CI run.
