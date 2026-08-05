# Working Memory Subsystem Specification

> **Subsystem:** Phase 06 — Memory System  
> **Document ID:** SPEC-06-WM-001  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. Subsystem Architecture & Execution Lifetime

Working Memory serves as the volatile, sub-millisecond ephemeral scratchpad for active agent task execution. It maintains active execution variables, local reasoning chains, step-by-step tool results, and immediate token context.

```text
[Task Start] ──► Allocate Working Memory Buffer (In-Memory Key-Value)
                       │
                       ▼
            [Active Task Execution Loop]
            ├── Stack Frames & Local Scratchpad
            ├── Tool Output Buffers
            └── Token Budget Tracker
                       │
                       ▼
[Task Finish] ──► Snapshot Candidate Knowledge ──► Flush & Garbage Collect Memory
```

---

## 2. Data Structure & State Representation

Working Memory is structured as an isolated, thread-safe in-memory key-value state store bound to a single task execution context ID.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WorkingMemoryState",
  "type": "object",
  "properties": {
    "execution_id": { "type": "string" },
    "agent_id": { "type": "string" },
    "allocated_token_budget": { "type": "integer", "default": 128000 },
    "used_tokens": { "type": "integer" },
    "scratchpad": {
      "type": "object",
      "additionalProperties": true
    },
    "step_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "step_index": { "type": "integer" },
          "prompt_snippet": { "type": "string" },
          "tool_call": { "type": "string" },
          "tool_response": { "type": "string" },
          "timestamp_ms": { "type": "integer" }
        }
      }
    }
  },
  "required": ["execution_id", "agent_id", "scratchpad", "step_history"]
}
```

---

## 3. Read/Write Performance & Concurrency Model

- **Storage Engine:** In-memory C++ / Rust extension with lock-free atomic pointer reads.
- **Latency SLAs:**
  - `GetVariable()`: P95 < 0.5 ms
  - `SetVariable()`: P95 < 0.8 ms
  - `AppendStepHistory()`: P95 < 1.2 ms
- **Thread Safety:** Per-agent execution isolation prevents cross-thread state pollution.

---

## 4. Checkpointing & Failure Recovery

Working Memory periodically serializes execution state to local disk or high-speed Redis:
- **Checkpoint Interval:** Every 3 tool executions or prior to invoking external APIs with side effects.
- **State Restoration:** If a worker pod crashes mid-task, the scheduler reads the latest checkpoint snapshot and resumes execution without re-running earlier completed steps.
