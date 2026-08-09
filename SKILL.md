---
name: ai-os-multi-agent-skill
description: >-
  Experimental LLM Context & Prompt Engineering Framework for Multi-Agent Orchestration.
  Provides structured agent roles, DAG workflows, bounded loops, governance guardrails, and state management utilities.
---

# AI OS Multi-Agent Orchestration Skill

**Skill ID:** `ai-os-multi-agent-skill`  
**Version:** `4.0.0`  
**Type:** Context & Prompt Engineering Framework  

---

## 1. Purpose & Capabilities

This global skill equips AI agents and LLM pair programmers with multi-agent orchestration context:

1. **14 Canonical Specialized Agent Specifications (`A00`–`A13`)**:
   - `A00`: Master Orchestrator
   - `A01`: Intake & Requirements
   - `A02`: Context & Memory
   - `A03`: Knowledge Graph & Research
   - `A04`: Scheduler & Resource Allocation
   - `A05`: Domain Authority
   - `A06`: Task Worker Execution
   - `A07`: Quality & Verification Engine
   - `A08`: Policy & Decision Intelligence
   - `A09`: Security & Compliance
   - `A10`: Release & Deployment
   - `A11`: Observability & Operations
   - `A12`: Learning & Reflection
   - `A13`: Human Collaboration & Approval Gates

2. **Hybrid Graph Engine (`runtime/workflow_executor.py`)**:
   - Parallel DAG execution with thread pool concurrency.
   - Bounded iterative refinement loops (`loop_until`, max iterations, safe rollback).

3. **State Management & Persistence (`runtime/state_manager.py`)**:
   - SQLite VRAM image synchronized atomically via `.tmp` disk flushing and WAL journaling.

4. **Runtime Governance Control Plane (`runtime/governance_control_plane.py`)**:
   - Risk classification, prompt injection guardrails, memory poisoning defense, and delegation narrowing.

---

## 2. Directory Structure

```text
.
├── SKILL.md                   # Primary Skill Manifest & Discovery Entry Point
├── README.md                  # Framework Overview & Quickstart Guide
├── validate_repository.py     # Portable Repository Integrity Validator
├── pyproject.toml             # Python configuration & test settings
│
├── agents/                    # 14 Canonical Agent Prompt Specifications (A00 - A13)
├── workflows/                 # Canonical DAG & Bounded Loop Workflows
├── runtime/                   # Python state management, router, compiler, and persistence
├── policies/                  # Governance & Security Policies
├── schemas/                   # JSON Schemas
├── registry/                  # Component Registries (agents, workflows, etc.)
└── tests/                     # Automated Pytest Suite
```

---

## 3. Usage & Verification

```bash
# 1. Run Structural Repository Validator
python validate_repository.py

# 2. Run Automated Pytest Battery
python -m pytest -n auto
```
