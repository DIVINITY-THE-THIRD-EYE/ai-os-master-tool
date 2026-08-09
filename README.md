# Multi-Agent AI OS Master Tool

An **Experimental LLM Context & Prompt Engineering Framework for Multi-Agent Orchestration**.

---

## 🎯 Purpose & Scope

This repository provides structured prompts, workflows, state management utilities, and governance guardrails designed to equip LLMs (such as Claude, ChatGPT, Gemini, and AI IDE assistants like Antigravity/Cursor) with a multi-agent orchestration context.

Rather than a standalone backend microservice, this repository acts as a **Global Agent Skill & Context Library** that can be loaded into an AI agent's workspace to guide complex planning, execution, verification, and durability routines.

---

## 🏗️ Architecture & Structure

```text
.
├── SKILL.md                   # Primary Agent Skill Manifest & Discovery Entry Point
├── README.md                  # Framework Documentation & Usage Guide
├── validate_repository.py     # Portable Repository Integrity & Path Validator
├── pyproject.toml             # Python package configuration & pytest settings
│
├── agents/                    # 14 Canonical Agent Prompt Specifications (A00 - A13)
├── workflows/                 # Canonical DAG & Bounded Loop Workflows
├── runtime/                   # Python state management, router, compiler, and persistence
├── policies/                  # Security & Governance Policies
├── schemas/                   # JSON Schemas
├── registry/                  # Component Lifecycle Registries (agents, workflows, etc.)
└── tests/                     # Automated Pytest Battery
```

---

## 🚀 How to Consume This Framework

1. **Load into AI IDEs / Agents**: Include this repository in your AI assistant's workspace or refer to `SKILL.md` to discover agent roles (`A00`–`A13`) and workflow templates.
2. **Execute Local Validation**:
   ```bash
   python validate_repository.py
   ```
3. **Run Automated Test Battery**:
   ```bash
   python -m pytest -n auto
   ```

---

## 📄 License
MIT License
