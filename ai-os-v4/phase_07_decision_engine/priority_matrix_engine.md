# Priority Matrix Engine Specification

> **Subsystem:** Phase 07 — Decision Engine  
> **Document ID:** SPEC-07-PME-005  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Dynamic Task Prioritization

The Priority Matrix Engine determines the execution order of queued tasks, agent requests, resource lock allocations, and background refactoring jobs using Weighted Shortest Job First (WSJF) and Eisenhower Matrix algorithms.

---

## 2. Weighted Shortest Job First (WSJF) Formula

$$\text{WSJF Score} = \frac{\text{Business Value} + \text{Time Criticality} + \text{Risk Reduction / Opportunity Enablement}}{\text{Job Size / Token Cost}}$$

Where all terms in the numerator are scored from 1 to 10 and Job Size is normalized from 1 (Tiny) to 10 (Large).

---

## 3. Priority Level Classification & Preemption Rules

| Priority Tier | WSJF Score Range | Queue SLA | Preemption Right |
| :--- | :--- | :--- | :--- |
| `P0_CRITICAL` | > 15.0 | Immediate (< 100 ms) | Can preempt running P2/P3 worker jobs |
| `P1_HIGH` | 8.0 - 15.0 | < 2.0 seconds | High queue priority |
| `P2_MEDIUM` | 3.0 - 7.9 | < 30.0 seconds | Standard queue processing |
| `P3_LOW` | < 3.0 | Best effort background | Yields compute slots under load |

---

## 4. Emergency Break-Glass Override

Kernel administrators or Security Authority Agents can issue a `PriorityOverrideEvent` attaching a `P0_CRITICAL` status to immediately halt lower-priority agent executions and resolve system-wide incidents.
