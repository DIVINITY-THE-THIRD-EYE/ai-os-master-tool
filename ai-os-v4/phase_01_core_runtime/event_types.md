---
title: System Event Types Taxonomy & Schema Catalog
document_id: SPEC-P01-MSG-014
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Messaging & Data Architecture Group
last_updated: 2026-08-05
---

# System Event Types Taxonomy & Schema Catalog

## Executive Summary
This document specifies the global system event types, payload schemas, event categorization taxonomy, and topic hierarchy for AI OS v4.

---

## 1. System Event Subject Taxonomy

All event topics follow the structured hierarchy: `aios.<domain>.<subdomain>.<event_name>`

```text
aios/
├── kernel/
│   ├── boot / shutdown / panic / health_check
├── task/
│   ├── created / assigned / started / completed / failed / retried
├── agent/
│   ├── registered / state_changed / prompt_issued / tool_invoked
├── memory/
│   ├── working_written / session_expired / checkpoint_saved
└── security/
    ├── policy_violated / prompt_injection_flagged / token_revoked
```

---

## 2. Standard Event Schemas Catalog Table

| Event Type Name | Topic String | Key Data Payload Fields | Schema Reference |
| :--- | :--- | :--- | :--- |
| `TaskCreatedEvent` | `aios.task.created` | `taskId`, `workflowId`, `priority`, `inputSpec` | `task_created.schema.json` |
| `TaskCompletedEvent` | `aios.task.completed` | `taskId`, `agentId`, `durationMs`, `outputArtifacts` | `task_completed.schema.json` |
| `AgentStateChangedEvent`| `aios.agent.state_changed` | `agentId`, `previousState`, `newState`, `trigger` | `agent_state.schema.json` |
| `PolicyViolationEvent` | `aios.security.policy_violated` | `agentId`, `ruleId`, `attemptedAction`, `severity` | `policy_violation.schema.json` |
| `MemoryCheckpointEvent` | `aios.memory.checkpoint_saved` | `checkpointId`, `sessionId`, `stateHash`, `sizeBytes` | `checkpoint.schema.json` |

---

## 3. Schema Invariants & Schema Registry Enforcement

1. **Strict Version Validation**: Events published to the broker MUST include `$schema` URI and pass validation against the registered schema.
2. **Backward Compatible Schema Migration**: Adding optional fields is permitted; field deletion or type changes require a major schema version bump.

---

## 4. Verification Protocol

```bash
agy verify-event-schemas --schema-dir ./phase_11_schemas/
```
Validates JSON schemas for all registered event types and tests serialization/deserialization.
