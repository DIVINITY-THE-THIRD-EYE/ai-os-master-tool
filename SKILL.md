---
name: ai-os-multi-agent-skill
description: >-
  Enterprise multi-agent AI Operating System skill for autonomous planning,
  execution, verification, governance, hybrid DAG + bounded loops, zero-data-loss
  persistence, and continuous learning.
---

# AI Operating System Multi-Agent Skill

**Skill ID:** `ai-os-multi-agent-skill`  
**Version:** `4.0.0`  
**Mode:** Production  

---

## 1. Purpose & Capabilities

This global skill equips any AI pair programming agent with an enterprise-grade AI Operating System (AI OS v4) capabilities:

1. **14 Canonical Specialized Agents (`A00`–`A13`)**:
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
   - Deterministic DAG execution with TRUE parallel worker threads (up to 5 parallel workers).
   - Bounded iterative refinement loops (`loop_until`, max iterations, safe rollback).

3. **Zero-Data-Loss ACID Persistence (`runtime/state_manager.py`)**:
   - In-memory SQLite VRAM image synchronized atomically via `.tmp` disk flushing and WAL journaling.
   - Self-healing corruption detection (`PRAGMA integrity_check`).

4. **Runtime Governance Control Plane (`runtime/governance_control_plane.py`)**:
   - Risk classification, security policy whitelist checks, and human approval gates (`A13`).

5. **Multi-Provider LLM Gateway (`runtime/llm_router.py`)**:
   - Provider cascade across Google Gemini, OpenAI, Anthropic Claude, and offline deterministic mock fallbacks.
   - Enforced token ceilings (`MAX_TOKEN_BUDGET`) and cost tracking.

---

## 2. Directory Structure

```text
.
├── SKILL.md                   # Primary Skill Manifest & Discovery Entry Point
├── README.md                  # Comprehensive Architecture & Usage Guide
├── pyproject.toml             # Python configuration & test settings
├── validate_repository.py     # Structural Authority Repository Validator
│
├── agents/                    # 14 Canonical Agent Specifications (A00 - A13)
├── workflows/                 # Canonical DAG & Bounded Loop Workflows
├── runtime/                   # Production ACID StateManager, EventBus, Router, Compiler
├── policies/                  # Governance & Security Policies
├── schemas/                   # JSON Schemas
├── registry/                  # Component Lifecycle Registries (agents, workflows, etc.)
├── docs/                      # Capability Matrix & Architecture Documents
└── tests/                     # Automated Pytest Battery (58 tests)
```

---

## 3. Quick Start & Verification

```bash
# 1. Run Structural Repository Validator
python validate_repository.py

# 2. Run Complete Pytest Suite (58 passed tests)
python -m pytest
```
