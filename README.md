# AI OS — Master Tool

A production-grade AI Operating System (AI OS) v4 multi-agent skill repository.

## Structure

- **`ai-os-v4/`** — 650-file AI OS v4 architecture phases (Phase 00–15)
- **`ai-os-v4/ai-os-multi-agent-skill/`** — 103-file production multi-agent skill package
  - `orchestrator/` — Master Orchestrator, State Machine, Escalation Matrix
  - `agents/` — A01–A13 agent specifications
  - `workflows/` — Canonical DAG + SOP workflows
  - `knowledge/` — Ontology, Rules, SOPs, Best Practices, Anti-Patterns
  - `policies/` — Governance, Security, Compliance, Coding, Release, Approval
  - `quality/` — Quality Gates, Verification Modules, Checklists
  - `events/` — Event Topics, Payload Schema, Handoff Schema
  - `platform/` — Agent Registry, Capability Registry, Security, Observability, DR
  - `reports/` — Report Templates
  - `runtime/` — Python: EventBus, AgentRegistry, CapabilityRouter, WorkflowExecutor
  - `tools/` — Repository Validator

## Quick Start

```bash
# Validate repository structure
python ai-os-v4/ai-os-multi-agent-skill/tools/validate_repository.py
```

## Version

`1.0.0`
