---
title: Process Manager & Agent Process Supervisor Specification
document_id: SPEC-P01-KERN-009
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Process Infrastructure Team
last_updated: 2026-08-05
---

# Process Manager & Agent Process Supervisor Specification

## Executive Summary
This document specifies the Process Manager (`process_manager`), responsible for agent sub-process spawning, process isolation, PID table tracking, process signal handling (`SIGINT`, `SIGKILL`, `SIGUSR1`), and health monitoring across node clusters.

---

## 1. Process Supervision Architecture

```text
+-------------------------------------------------------------------------+
|                        PROCESS MANAGER (SUPERVISOR)                     |
+-------------------------------------------------------------------------+
    │                        │                        │
    ▼                        ▼                        ▼
[ AGENT PROC 101 ]      [ AGENT PROC 102 ]      [ AGENT PROC 103 ]
(PID: 4901, State: RUN)  (PID: 4902, State: RUN)  (PID: 4903, State: RECOVER)
```

---

## 2. Process Manager Interface Contract

```typescript
export interface ProcessDescriptor {
  readonly pid: number;
  readonly agentId: string;
  readonly taskId: string;
  readonly command: string;
  readonly args: string[];
  readonly memoryUsageMb: number;
  readonly cpuPercent: number;
  readonly startTime: string;
  readonly status: "RUNNING" | "STOPPED" | "ZOMBIE" | "FAILED";
}

export interface IProcessManager {
  spawnProcess(agentId: string, taskId: string, entrypoint: string, env: Record<string, string>): Promise<ProcessDescriptor>;
  killProcess(pid: number, signal: "SIGTERM" | "SIGKILL"): Promise<void>;
  listProcesses(): Promise<ProcessDescriptor[]>;
  getProcessByPid(pid: number): Promise<ProcessDescriptor | null>;
  reapZombies(): Promise<number>;
}
```

---

## 3. Supervision Policies & Zombie Reaping

1. **Erlang-Style Supervisor Restart**: If an agent process crashes due to memory limits, the Process Manager evaluates the restart policy (`NEVER`, `ON_FAILURE`, `ALWAYS`).
2. **Zombie Process Reaping**: A background reaper thread checks every 5 seconds for orphaned child processes (`zombies`) and issues `waitpid()` system calls.

---

## 4. Verification Protocol

```bash
agy verify-process-manager --test-reaping
```
Spawns child processes, simulates unhandled crashes, verifies zombie process cleanup, and checks PID table accounting.
