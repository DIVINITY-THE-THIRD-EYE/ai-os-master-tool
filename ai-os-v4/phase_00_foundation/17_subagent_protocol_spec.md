---
title: Subagent Inter-Process Protocol & Communication Standard
document_id: SPEC-P00-SUB-017
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Agent Architecture Working Group
last_updated: 2026-08-05
---

# Subagent Inter-Process Protocol & Communication Standard

## Executive Summary
This document specifies the communication protocol, message framing, context propagation rules, handoff formats, and state synchronization contracts between parent agents and spawned subagents in AI OS v4.

---

## 1. Parent-Subagent Hierarchy & Message Flow

```text
+-------------------------------------------------------------------------+
|                              PARENT AGENT                               |
+-------------------------------------------------------------------------+
    │                                                                  ▲
    │ 1. Spawn Subagent (Task Specification & Scoped Context Envelope)│ 4. Handoff Report
    ▼                                                                  │
+-------------------------------------------------------------------------+
|                              SUBAGENT                                   |
| (Executes task inside isolated runtime container)                        |
|                                                                         |
| 2. Heartbeat via progress.md (Every 300s or step completion)           |
| 3. Step execution & intermediate verification                           |
+-------------------------------------------------------------------------+
```

---

## 2. Parent-Subagent Inter-Process Contract

### 2.1 Subagent Invocation Payload Schema

```json
{
  "invocationId": "sub-spawn-9921",
  "parentId": "agent-orchestrator-main",
  "subagentRole": "implementer_p0_p1",
  "assignedTask": {
    "taskId": "task-phase00-construction",
    "description": "Construct Phase 00 Foundation specifications",
    "workingDirectory": "./.agents/worker_p0_p1/",
    "projectRoot": "./ai-os-v4/"
  },
  "contextEnvelope": {
    "originalRequest": "ai-os-v4/ORIGINAL_REQUEST.md",
    "conventionsRef": "ai-os-v4/phase_00_foundation/CONVENTIONS.md",
    "grantedCapabilities": ["fs_read", "fs_write", "run_command"]
  },
  "limits": {
    "maxDurationSeconds": 3600,
    "maxMemoryMb": 4096
  }
}
```

---

## 3. Subagent Lifecycle & Mandatory Handoff Protocol

1. **Heartbeat Requirement**: Subagent MUST update `.agents/<subagent_id>/progress.md` with timestamp and state after every completed subtask.
2. **Standard 5-Component Handoff Report**: Upon task completion, subagent MUST generate `.agents/<subagent_id>/handoff.md` containing:
   - **Observation**: Verbatim observations, paths, tool command outputs.
   - **Logic Chain**: Step-by-step reasoning from observations to conclusions.
   - **Caveats**: Scope assumptions, unverified edge cases.
   - **Conclusion**: Final operational state summary.
   - **Verification Method**: Exact reproducible shell commands to verify work.
3. **Completion Message**: Subagent MUST send a structured completion message back to the parent agent via `send_message`.

---

## 4. Verification Protocol

Verify parent-subagent protocol compliance:
```bash
agy verify-subagent-protocol --subagent worker_p0_p1
```
Checks progress log freshness, handoff formatting, and message contract compliance.
