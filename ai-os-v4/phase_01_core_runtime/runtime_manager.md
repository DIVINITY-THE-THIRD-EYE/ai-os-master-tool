---
title: Agent Runtime Manager Specification
document_id: SPEC-P01-KERN-002
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Runtime Subsystem Team
last_updated: 2026-08-05
---

# Agent Runtime Manager Specification

## Executive Summary
This document specifies the Runtime Manager (`runtime_manager`), responsible for agent container instantiation, runtime environment setup, resource binding, context mounting, and execution supervision in AI OS v4.

---

## 1. Runtime Manager Architecture

```text
[ Kernel Process Manager ] ──> SpawnAgentRuntime() ──> [ RUNTIME MANAGER ]
                                                              │
        ┌─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────┐
        ▼                                                     ▼                                                     ▼
[ Container / gVisor Sandbox ]                       [ Context Hydration Engine ]                          [ Resource Monitor Proxy ]
(Isolated FS & Syscalls)                            (Inject memory & prompt spec)                         (Track CPU, Memory, Tokens)
```

---

## 2. Agent Execution Container Contract

```typescript
export interface AgentRuntimeDescriptor {
  readonly agentId: string;
  readonly roleName: string;
  readonly sandboxMode: "STRICT" | "PERMISSIVE" | "MOCK";
  readonly allocatedMemoryMb: number;
  readonly environmentVars: Record<string, string>;
  readonly mountedVolumes: Array<{ readonly hostPath: string; readonly containerPath: string; readonly mode: "ro" | "rw" }>;
}

export interface IRuntimeManager {
  createRuntime(descriptor: AgentRuntimeDescriptor): Promise<string>;
  startRuntime(runtimeId: string): Promise<void>;
  pauseRuntime(runtimeId: string): Promise<void>;
  terminateRuntime(runtimeId: string, signal: "SIGTERM" | "SIGKILL"): Promise<void>;
  inspectRuntime(runtimeId: string): Promise<AgentRuntimeDescriptor>;
}
```

---

## 3. Operational Rules & Safety Policies

1. **Strict Ephemeral Isolation**: Each agent execution creates a clean, ephemeral sandbox container. Scratch files created during task execution are auto-cleaned unless explicitly committed.
2. **Resource Throttling**: If container CPU utilization exceeds allocation for > 30 seconds, Runtime Manager applies cgroup CPU throttling.
3. **Graceful Termination Policy**: Termination sends `SIGTERM`, allowing 10 seconds for checkpoint serialization before issuing `SIGKILL`.

---

## 4. Verification Protocol

```bash
agy verify-runtime-manager --sandbox-check strict
```
Spawns synthetic test agent container, verifies volume isolation, tests `SIGTERM` handling, and checks resource cleanup.
