---
title: System Versioning & Compatibility Strategy Specification
document_id: SPEC-P00-VER-002
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Release Management Committee
last_updated: 2026-08-05
---

# System Versioning & Compatibility Strategy

## Executive Summary
This document specifies the enterprise versioning policy for AI OS v4. It defines semantic versioning rules for platform runtime components, agents, schemas, workflows, domain skill packs, and protocol interfaces. It establishes strict rules for breaking change management, deprecation cycles, and API compatibility matrices.

---

## 1. Semantic Versioning Model (SemVer 2.0.0 + AI Extensions)

All components in AI OS v4 adhere to Semantic Versioning (`MAJOR.MINOR.PATCH`), extended with build metadata for model weights and prompt release tags:

```text
v<MAJOR>.<MINOR>.<PATCH>[-<PRERELEASE>][+<BUILD_METADATA>]
Example: v4.2.1-beta.2+model.gpt4o.20260805
```

### 1.1 Incrementation Rules Matrix

| Component Type | MAJOR Increment | MINOR Increment | PATCH Increment |
| :--- | :--- | :--- | :--- |
| **Core Kernel & APIs** | Incompatible API changes, lock protocol changes | Backward-compatible feature additions, new APIs | Bug fixes, performance optimizations |
| **JSON Schemas** | Field deletions, type change, new required fields | Optional field additions, enum value additions | Description changes, formatting fixes |
| **Agent Specs & Prompts**| Role/mission change, output contract breaking change | New capabilities, prompt refinement | Prompt typo fix, hyperparameter tweak |
| **Workflows** | Removal of workflow step, node topology change | New optional step, sub-workflow addition | Threshold adjustment, logging addition |
| **Domain Skill Packs** | Incompatible policy/schema change | Additional skill assets, new workflows | Fixes in prompt templates or docs |

---

## 2. Component Interface Versioning & Headers

All cross-component RPCs, REST endpoints, and Event Bus messages MUST carry explicit version headers:

```json
{
  "header": {
    "specVersion": "4.0.0",
    "componentVersion": "1.2.0",
    "schemaRef": "https://ai-os.org/schemas/v1/event_header.schema.json"
  }
}
```

---

## 3. Deprecation Lifecycle & Breaking Change Policy

```text
[ ACTIVE ] ──(Announce Deprecation)──> [ DEPRECATED ] ──(Sunset Window)──> [ RETIRED ]
   │                                           │
   └──(Normal Operation)                       └──(Emits Deprecation Warning Log)
```

1. **Deprecation Notice Window**: MINIMUM 90 days notice before retiring MAJOR version interfaces.
2. **Backward Compatibility Guarantee**: Core Kernel MUST maintain backward compatibility for at least 1 MAJOR version prior (`N-1`).
3. **Automated Compatibility Check**: CI/CD pipelines run breaking change verification using schema diff tools before merging any PR.

---

## 4. Verification Protocol

Verify version alignment across all packages:
```bash
agy check-version-matrix --root ./ai-os-v4
```
Outputs report detailing any mismatched schema references or breaking policy violations.
