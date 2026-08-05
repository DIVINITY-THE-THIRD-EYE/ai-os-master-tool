---
title: Multi-Language Coding Standards & Guidelines
document_id: SPEC-P00-CODE-005
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Quality Assurance Working Group
last_updated: 2026-08-05
---

# Multi-Language Coding Standards & Guidelines

## Executive Summary
This document specifies code quality, formatting, linting, error handling, and architectural guidelines for code assets in AI OS v4 across TypeScript, Python, Go, and Rust. Strict enforcement ensures maintainability, security, memory safety, and seamless multi-agent automation.

---

## 1. Universal Coding Invariants

1. **No Hardcoded Credentials**: API keys, passwords, bearer tokens, or sensitive endpoint URLs MUST NEVER appear in source code or specifications. Use environment secrets or secret managers.
2. **Explicit Type Safety**: No loose typing (`any` in TS, un-annotated types in Python). All functions MUST declare parameter and return type hints.
3. **Immutability by Default**: Prefer `const`, `readonly`, and immutable data structures over mutable state.
4. **Structured Error Handling**: Functions MUST return typed Result objects or throw explicit custom domain exceptions. Empty `catch` blocks or bare `except:` are strictly prohibited.

---

## 2. Language-Specific Standards Matrix

### 2.1 TypeScript / JavaScript Standard
- **Linter & Formatter**: ESLint + Prettier (`strict-type-checked`).
- **Target**: ES2022 / Node.js 20 LTS.
- **Rules**:
  - `no-explicit-any`: ERROR
  - `@typescript-eslint/explicit-function-return-type`: ERROR
  - Use `async/await` exclusively over raw Promises or callbacks.

```typescript
// Exemplar TypeScript Code Pattern
export interface AgentTaskRequest {
  readonly taskId: string;
  readonly payload: Record<string, unknown>;
  readonly priority: number;
}

export async function processTask(request: AgentTaskRequest): Promise<TaskResult> {
  if (!request.taskId) {
    throw new InvalidTaskError("Task ID cannot be empty");
  }
  // Processing logic...
  return { status: "COMPLETED", durationMs: 42 };
}
```

### 2.2 Python Standard
- **Linter & Formatter**: Ruff + Black + MyPy (`strict` mode).
- **Target**: Python 3.11+.
- **Rules**:
  - Full Type Hints (`from typing import Optional, List, Dict`).
  - Google Style Docstrings for all classes and public functions.
  - Asynchronous IO (`asyncio`) for network/disk I/O operations.

```python
# Exemplar Python Code Pattern
from typing import Dict, Any
import dataclasses

@dataclasses.dataclass(frozen=True)
class EventPayload:
    event_type: string
    data: Dict[str, Any]

async def dispatch_event(payload: EventPayload) -> bool:
    """Dispatches event payload to the async event broker.

    Args:
        payload: The immutable event payload object.

    Returns:
        True if event delivery was acknowledged, False otherwise.
    """
    if not payload.event_type:
        raise ValueError("event_type must be specified")
    return True
```

---

## 3. Mandatory Linting Rules & Pre-Commit Gates

Pre-commit hooks automatically execute:
- `eslint --max-warnings=0`
- `ruff check --select E,F,W,I,N,UP,ASYNC`
- `mypy --strict`
- `prettier --check .`

Failure at any stage rejects the commit.
