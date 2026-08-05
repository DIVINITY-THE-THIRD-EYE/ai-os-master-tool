---
title: System Resource Limits, Quotas & Capacity Specification
document_id: SPEC-P00-QUOTA-018
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Infrastructure & Resource Governance Group
last_updated: 2026-08-05
---

# System Resource Limits, Quotas & Capacity Specification

## Executive Summary
This document specifies default resource limits, token consumption quotas, process memory ceilings, file handle limits, execution timeouts, rate limits, and throttling policies across AI OS v4.

---

## 1. System Capacity & Resource Limits Matrix

```text
+--------------------------------------------------------------------+
|                         SYSTEM RESOURCE QUOTAS                     |
|                                                                    |
|  [ CPU & MEMORY ]                [ LLM & TOKEN CONSUMPTION ]       |
|  - Max Memory / Sandbox: 4GB     - Max Tokens / Task: 150,000      |
|  - Max CPU Shares / Agent: 2.0   - Max Prompt Cost / Task: $5.00   |
|  - Max Threads / Node: 128       - Max LLM Requests / Min: 120     |
|                                                                    |
|  [ FILE & NETWORK I/O ]          [ AGENT & WORKFLOW EXECUTION ]    |
|  - Max Open Files: 1024          - Max Subagents / Parent: 16      |
|  - Max Disk Scratch Space: 10GB  - Max Execution Time: 1,800 sec   |
+--------------------------------------------------------------------+
```

---

## 2. Default Resource Quotas Table

| Category | Limit Name | Default Ceiling | Enforcement Action |
| :--- | :--- | :--- | :--- |
| **Agent Memory** | `max_heap_size_mb` | 4096 MB | SIGKILL & state fallback |
| **Execution Time**| `max_task_duration_sec` | 1800 sec (30 min) | SIGTERM & checkpoint save |
| **Token Budget** | `max_tokens_per_agent` | 150,000 Tokens | Intercept request & pause task |
| **Financial Cost** | `max_cost_usd_per_task` | $5.00 USD | Escalation to approval gate |
| **Message Broker** | `max_payload_bytes` | 10 MB | Reject message (`ERR-MSG-0201`) |
| **File System** | `max_file_write_bytes` | 50 MB / file | Truncate write & alert |

---

## 3. Enforcement & Degradation Protocol

1. **Hard Limit Enforcement**: Resource limits marked Hard (e.g. Memory, Token budget) trigger immediate execution pause or sandbox container SIGTERM upon 100% threshold match.
2. **Soft Limit Warnings**: At 80% quota utilization, a telemetry warning (`WARN_QUOTA_NEAR_EXHAUSTION`) is emitted to the Event Bus.
3. **Graceful Degradation**: If system-wide LLM rate limits are hit, non-critical background reflection tasks are suspended to preserve capacity for interactive workflows.

---

## 4. Verification Protocol

Verify quota enforcement engine:
```bash
agy test-quotas --simulate-exhaustion memory
```
Simulates memory and token quota breaches and validates circuit breaker triggers.
