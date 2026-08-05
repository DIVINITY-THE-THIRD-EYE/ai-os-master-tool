# AI OS v4 — Execution Policy Specification

**Document Version:** 4.0.0  
**Phase:** Phase 14 — Runtime Policies  
**Classification:** Core Runtime Policy Specification  
**Status:** Frozen / Production Standard  

---

## 1. Overview & Policy Objective

The **Execution Policy** sets mandatory, deterministic runtime boundary conditions for task scheduling, thread/process execution, resource allocation, concurrency limits, timeout boundaries, and cancellation handling across all agents operating within AI OS v4.

```
+-----------------------------------------------------------------------------------+
|                           SCHEDULER & RUNTIME KERNEL                              |
+-----------------------------------------+-----------------------------------------+
                                          | Invocation Request
                                          v
+-----------------------------------------------------------------------------------+
|                           EXECUTION POLICY ENFORCER                               |
|  +--------------------+    +--------------------+    +-------------------------+  |
|  | Priority Scheduler |    | Resource Governor  |    | Determinism & Timeout   |  |
|  | Guardrails         |    | (cgroups / Memory) |    | Tracker                 |  |
|  +---------+----------+    +---------+----------+    +------------+------------+  |
+------------|-------------------------|----------------------------|----------------+
             |                         |                            |
             +-------------------------+----------------------------+
                                       | Validated Execution Context
                                       v
+-----------------------------------------------------------------------------------+
|                            WORKER EXECUTION POOL                                  |
|     [Priority Queue 0]      [Priority Queue 1]      [Priority Queue 2]            |
+-----------------------------------------------------------------------------------+
```

---

## 2. Resource Boundaries & Guarantees

Every agent execution context MUST operate within fixed resource envelopes determined by agent class:

| Agent Class | CPU Shares (Weight) | Max RAM Hard Limit | Max Ephemeral Disk | Default Timeout | Max Parallel Threads |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **System / Kernel** | 4096 (Highest) | 8192 MB | 20 GB | 600 s | 32 |
| **Architect / Lead** | 2048 | 4096 MB | 10 GB | 300 s | 16 |
| **Worker Agent** | 1024 | 2048 MB | 5 GB | 180 s | 8 |
| **Subagent / Tool** | 512 | 512 MB | 1 GB | 60 s | 2 |

---

## 3. Execution Policy Declaration Manifest Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExecutionPolicySpecification",
  "type": "object",
  "required": [
    "policy_id",
    "agent_class",
    "cpu_shares",
    "memory_hard_limit_mb",
    "execution_timeout_seconds",
    "preemption_allowed",
    "max_concurrent_tasks"
  ],
  "properties": {
    "policy_id": { "type": "string" },
    "agent_class": {
      "type": "string",
      "enum": ["SYSTEM_KERNEL", "ARCHITECT_LEAD", "WORKER_AGENT", "SUBAGENT_TOOL"]
    },
    "cpu_shares": { "type": "integer" },
    "memory_hard_limit_mb": { "type": "integer" },
    "execution_timeout_seconds": { "type": "integer" },
    "preemption_allowed": { "type": "boolean" },
    "max_concurrent_tasks": { "type": "integer" },
    "graceful_shutdown_timeout_ms": { "type": "integer", "default": 5000 },
    "checkpoint_interval_seconds": { "type": "integer", "default": 30 }
  }
}
```

---

## 4. Priority Scheduling & Starvation Prevention

Tasks are scheduled into priority queues using **Weighted Fair Queuing (WFQ)**:

$$\text{TimeSlice}_k = \text{Quantum} \times \frac{\text{Weight}_k}{\sum_{i} \text{Weight}_i}$$

1. **Preemption Policy:** Higher-priority system tasks (`Priority 0`) can preempt lower-priority batch tasks (`Priority 2`), saving a state checkpoint before pausing the lower-priority task.
2. **Anti-Starvation Boost:** Tasks waiting in queue for > 120 seconds receive dynamic priority promotion (+1 level per 60s) to prevent indefinite starvation.

---

## 5. Determinism & State Checkpointing Rules

- **Deterministic Execution Seeds:** Pseudo-random number generators (PRNG) and sampling calls must accept explicit deterministic seeds (`system_seed + task_id`).
- **Checkpointing Protocol:** Tasks running longer than 30 seconds MUST produce atomic checkpoints serialized to persistent context storage every 30 seconds.

---

## 6. Emergency Cancellation & Halt Rules

When an execution cancellation signal is received (`SIGTERM` / `CANCEL_TASK` event):

1. The runtime sends an interrupt signal to the active execution context.
2. The agent has `graceful_shutdown_timeout_ms` (5000 ms) to save state and release database/memory locks.
3. If the process does not exit within the grace period, a hard `SIGKILL` is issued and resource cleanup is handled by the kernel.

---

## 7. Summary Checklist for Execution Policy Compliance

- [x] Agent-class resource boundaries (CPU, RAM, Disk, Timeout) specified.
- [x] Declarative JSON Schema for execution policies defined.
- [x] Weighted Fair Queuing and anti-starvation boost algorithms formulated.
- [x] Deterministic PRNG seeding and 30s state checkpointing mandated.
- [x] 2-stage (SIGTERM grace -> SIGKILL) emergency cancellation protocol locked.
