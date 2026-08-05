# Session Memory Subsystem Specification

> **Subsystem:** Phase 06 — Memory System  
> **Document ID:** SPEC-06-SM-002  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. Subsystem Architecture & Multi-Turn State Scope

Session Memory maintains conversational and multi-task context across an active user interaction or multi-stage project session. It bridges short-term volatile Working Memory and long-term Persistent Memory.

```text
[User / Client] ──► [Session Gateway] ──► Read Session Context (Redis Cluster)
                                               │
                                               ▼
                                  [Multi-Turn Agent Workflow]
                                               │
                                               ▼
                                 [Update Session Summary & Window]
```

---

## 2. Session Memory State Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SessionMemoryState",
  "type": "object",
  "properties": {
    "session_id": { "type": "string", "pattern": "^sess_[a-zA-Z0-9_-]+$" },
    "user_id": { "type": "string" },
    "tenant_id": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "last_active_at": { "type": "string", "format": "date-time" },
    "active_context_variables": { "type": "object" },
    "rolling_message_history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "role": { "type": "string", "enum": ["system", "user", "assistant", "tool"] },
          "content": { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" }
        }
      }
    },
    "summarized_session_context": { "type": "string" }
  },
  "required": ["session_id", "user_id", "tenant_id", "rolling_message_history"]
}
```

---

## 3. Context Rolling & Auto-Summarization Triggers

When `rolling_message_history` exceeds 32 messages or 16,000 tokens:
1. The oldest 16 messages are passed to the Context Compression Engine (`context_compression_engine.md`).
2. A high-density semantic summary is appended to `summarized_session_context`.
3. The raw messages are evicted from the active rolling window and archived to Persistent Storage.

---

## 4. Session Expiration & Security Controls

- **Default Inactivity TTL:** 3600 seconds (1 hour).
- **Hard Expiration Limit:** 86,400 seconds (24 hours).
- **PII & Data Isolation:** Multi-tenant separation enforced via Redis key namespace prefixing (`tenant:{tenant_id}:session:{session_id}`).
