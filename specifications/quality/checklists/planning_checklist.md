# Planning Checklist (Gate 1 & Gate 2)

**Responsible Agent:** A04 (Scheduler), A08 (Policy Agent)
**Gate:** Gate 1 (Planning Gate), Gate 2 (Policy Pre-Check Gate)

## Task Structure
- [ ] Objective is clearly stated and measurable — **Blocking**
- [ ] Acceptance criteria are testable (not subjective) — **Blocking**
- [ ] Task type classified from approved taxonomy — **Blocking**
- [ ] Risk level assigned: Low / Medium / High / Critical — **Blocking**
- [ ] Dependencies explicitly declared — **Blocking**

## Execution Plan (DAG)
- [ ] DAG has zero circular dependencies — **Blocking**
- [ ] Critical path identified — **Blocking**
- [ ] Each node has clearly defined inputs, outputs, and responsible agent — **Blocking**
- [ ] Parallel branches identified for concurrent execution — **Advisory**
- [ ] Merge strategy defined for parallel branch outputs — **Blocking**

## Resource Allocation
- [ ] Token budget allocated per task — **Blocking**
- [ ] Cost budget allocated per task — **Blocking**
- [ ] Time budget allocated per task — **Blocking**
- [ ] API call budget allocated per task — **Blocking**
- [ ] Storage budget allocated per task — **Blocking**

## Agent Readiness
- [ ] All required agents are registered in Agent Registry — **Blocking**
- [ ] All required agents are in READY state — **Blocking**
- [ ] All required tool permissions are provisioned — **Blocking**

## Policy Pre-Check
- [ ] Execution plan complies with governance policies — **Blocking**
- [ ] Security policies satisfied for all proposed tool calls — **Blocking**
- [ ] Compliance policies satisfied for data types involved — **Blocking**
- [ ] Human approval required steps identified — **Blocking**
- [ ] Rollback plan identified (required for production changes) — **Blocking**
