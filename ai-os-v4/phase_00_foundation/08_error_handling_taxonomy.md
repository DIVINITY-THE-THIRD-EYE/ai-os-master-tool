---
title: System Error Handling & Standard Error Taxonomy
document_id: SPEC-P00-ERR-008
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Platform Reliability Group
last_updated: 2026-08-05
---

# System Error Handling & Standard Error Taxonomy

## Executive Summary
This document specifies the global error handling architecture, error classification taxonomy, standardized error message schemas, retry strategies, and circuit-breaker guidelines for AI OS v4. All runtime modules, SDKs, agent frameworks, and workflows MUST implement this error contract.

---

## 1. Global Error Architecture & Taxonomy

Errors in AI OS v4 are categorized into five primary subsystem domains:

```text
ERR-<DOMAIN>-<NUMBER>
│
├── ERR-KERNEL-*    --> Core Runtime, Memory Allocation, Process Lifecycle
├── ERR-SCHED-*     --> Task Queue, Resource Exhaustion, Dependency Cycles
├── ERR-MSG-*       --> Broker Timeout, Serialization, Routing Failures
├── ERR-SEC-*       --> Authentication, Authorization, Sandbox Escape, Injection
└── ERR-AGENT-*     --> LLM Timeout, Tool Failure, Validation Rejection
```

---

## 2. Standardized Error Payload Schema (JSON / RFC 7807)

```json
{
  "$schema": "https://ai-os.org/schemas/v1/error_response.schema.json",
  "errorCode": "ERR-SEC-UNAUTHORIZED-TOOL-0403",
  "httpStatus": 403,
  "category": "SECURITY_VIOLATION",
  "severity": "CRITICAL",
  "message": "Agent requested execution of ungranted tool 'system_reboot'",
  "timestamp": "2026-08-05T15:45:00Z",
  "context": {
    "agentId": "agent-swe-arch-007",
    "taskId": "task-workflow-9921",
    "attempt": 1,
    "requestedTool": "system_reboot"
  },
  "remediation": "Verify tool permissions in skill manifest SKILL.md before execution.",
  "traceId": "trace-7f8a9b0c1d2e"
}
```

---

## 3. Error Classification Matrix

| Error Code Range | Category | Retry Behavior | Escalation Path |
| :--- | :--- | :--- | :--- |
| `ERR-KERNEL-0001..0099` | Kernel System Panic | DO NOT RETRY | Emergency Sysadmin Alert |
| `ERR-SCHED-0100..0199` | Scheduling / Quota Limit | Exponential Backoff (3x) | Resource Scaling Manager |
| `ERR-MSG-0200..0299` | Messaging / Broker Timeout| Immediate Retry (2x), then DLQ | Message Broker Manager |
| `ERR-SEC-0300..0399` | Security Violation | DO NOT RETRY | Security Officer / Audit Log |
| `ERR-AGENT-0400..0499` | LLM / Tool Execution Failure| Retry with prompt fallback (2x)| Verification / Reflection Engine|

---

## 4. Circuit Breaker Guidelines

When a downstream service or LLM provider reaches an error threshold (> 5% failures over 60s window):
1. **State transition**: `CLOSED` ➔ `OPEN`.
2. **Behavior**: Intercept requests immediately, returning `ERR-AGENT-CIRCUIT-OPEN`.
3. **Recovery**: After 30 seconds, transition to `HALF-OPEN` to test downstream availability.

---

## 5. Verification Protocol

Verify error handling compliance:
```bash
agy test-error-taxonomy --root ./ai-os-v4
```
Ensures all code paths return valid error codes registered in the system error catalog.
