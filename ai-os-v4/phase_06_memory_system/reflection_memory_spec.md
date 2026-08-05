# Reflection Memory Subsystem Specification

> **Subsystem:** Phase 06 — Memory System  
> **Document ID:** SPEC-06-RM-006  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Self-Correction Log Store

Reflection Memory captures self-critique traces, verification feedback loop results, error diagnosis details, and dynamic self-corrections recorded during task execution.

---

## 2. Reflection Memory Entry Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ReflectionMemoryEntry",
  "type": "object",
  "properties": {
    "reflection_id": { "type": "string", "pattern": "^refl_[a-z0-9_-]+$" },
    "task_id": { "type": "string" },
    "agent_id": { "type": "string" },
    "evaluated_step_index": { "type": "integer" },
    "critic_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "detected_flaws": {
      "type": "array",
      "items": { "type": "string" }
    },
    "proposed_correction": { "type": "string" },
    "correction_applied_successfully": { "type": "boolean" },
    "timestamp": { "type": "string", "format": "date-time" }
  },
  "required": ["reflection_id", "task_id", "agent_id", "critic_score", "detected_flaws", "proposed_correction"]
}
```

---

## 3. Dynamic Avoidance Guidance Engine

During active agent reasoning:
1. Active tool proposals are checked against Reflection Memory for similar tasks.
2. If a proposed action matches a previously logged `detected_flaw`, the agent is forced to apply the recorded `proposed_correction` prior to tool call execution.
