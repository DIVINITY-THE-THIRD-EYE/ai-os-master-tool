# Project Memory Subsystem Specification

> **Subsystem:** Phase 06 — Memory System  
> **Document ID:** SPEC-06-PRM-004  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Project Scope

Project Memory maintains shared, project-level context accessible across all worker agents assigned to a specific codebase, client initiative, or product milestone.

---

## 2. Project Memory Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProjectMemoryState",
  "type": "object",
  "properties": {
    "project_id": { "type": "string", "pattern": "^prj_[a-z0-9_-]+$" },
    "name": { "type": "string" },
    "repository_url": { "type": "string" },
    "active_branch": { "type": "string" },
    "codebase_summary": { "type": "string" },
    "architecture_conventions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "active_milestones": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "milestone_id": { "type": "string" },
          "title": { "type": "string" },
          "status": { "type": "string" }
        }
      }
    },
    "known_issues": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["project_id", "name", "repository_url", "codebase_summary"]
}
```

---

## 3. Git Synchronization & Automated Code Base Indexing

Project Memory automatically syncs with Git code repositories:
- **Webhook Ingestion:** GitHub/GitLab push events trigger incremental re-indexing.
- **AST Parsing:** Updates module map and function call graphs in the Project Memory index upon code commit.
- **Convention Scanning:** Detects repository configuration files (`.eslintrc`, `tsconfig.json`, `CONVENTIONS.md`) and updates project architecture conventions.

---

## 4. Multi-Agent Shared Access & RBAC Gates

Multiple agents working simultaneously on a project share Project Memory read access. Writes (e.g. updating active milestone status or conventions) require Domain Authority Agent authorization.
