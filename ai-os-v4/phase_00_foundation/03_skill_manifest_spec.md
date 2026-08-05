---
title: Skill Manifest Specification & Schema Definition
document_id: SPEC-P00-SKILL-003
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Skill Architecture Working Group
last_updated: 2026-08-05
---

# Skill Manifest Specification & Schema Definition

## Executive Summary
This document specifies the declarative format, validation rules, runtime capabilities, and schema structure for Skill Manifests in AI OS v4. A Skill Manifest (`SKILL.md` or `skill_manifest.json`) defines an agent skill package, declaring its metadata, required tools, prompt files, sub-workflows, permissions, and security boundaries.

---

## 1. Skill Manifest Architecture

```text
+-------------------------------------------------------------------+
|                        SKILL MANIFEST HEADER                      |
| (name, version, description, domain, security_level, sandbox_mode)|
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                       CAPABILITY & TOOL DECLARATIONS               |
| - Allowed Tools: [fs_read, fs_write, git_commit, http_request]    |
| - Max Concurrent Instances: 5                                     |
| - Sandbox Isolation: SECURE_CONTAINER                             |
+-------------------------------------------------------------------+
                                  │
                                  ▼
+-------------------------------------------------------------------+
|                    RESOURCE & ASSET DEPENDENCIES                  |
| - Prompt Files: [system_prompt.md, review_prompt.md]               |
| - Workflows: [build_pipeline.json]                                |
| - Schemas: [input_spec.schema.json, output_spec.schema.json]      |
+-------------------------------------------------------------------+
```

---

## 2. Declarative YAML Manifest Specification

```yaml
skill_manifest_version: "1.0.0"
name: "software_engineering_architect"
id: "skill-domain-swe-arch-001"
title: "Software Engineering Architecture & Design Skill"
domain: "software_engineering"
version: "2.1.0"
security_classification: "RESTRICTED"

metadata:
  author: "Enterprise Platform Team"
  description: "Provides full architectural synthesis, ADR generation, and system design analysis."
  tags: ["architecture", "adr", "uml", "system-design"]

runtime_requirements:
  min_runtime_version: "4.0.0"
  memory_mb: 2048
  cpu_units: 2.0
  gpu_required: false
  timeout_seconds: 300

capabilities:
  tools_granted:
    - name: "read_file"
      scope: "read_only"
    - name: "write_file"
      scope: "workspace_relative"
    - name: "run_command"
      scope: "sandboxed_shell"

  permissions:
    network_access: "restricted"
    allowed_domains: ["github.com", "api.openai.com"]
    file_system_write: ["./build", "./docs", "./.agents"]

dependencies:
  required_skills:
    - id: "skill-foundation-git-001"
      version: ">=1.0.0"
  schemas:
    input: "schemas/swe_input.schema.json"
    output: "schemas/swe_output.schema.json"
```

---

## 3. Schema Constraints & Validation Rules

1. **Unique Manifest ID**: Every skill MUST have a globally unique UUID or canonical URN (`skill-domain-name-000`).
2. **Explicit Tool Declaration**: No skill may invoke an ungranted tool. Execution of undeclared tools triggers an immediate runtime exception (`ERR_SECURITY_UNAUTHORIZED_TOOL`).
3. **Sandbox Compliance**: If `security_classification` is `RESTRICTED` or `SECRET`, `sandbox_runtime` MUST be set to `ISOLATED_CONTAINER`.

---

## 4. Verification Protocol

Validate skill manifests prior to deployment:
```bash
agy validate-skill --manifest ./phase_12_domain_skill_packs/software/SKILL.md
```
Outputs validation tree confirming schema adherence and security boundary sanity.
