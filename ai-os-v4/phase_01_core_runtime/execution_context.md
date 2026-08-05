---
title: Execution Context Engine Specification
document_id: SPEC-P01-KERN-003
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Core Kernel Architecture Group
last_updated: 2026-08-05
---

# Execution Context Engine Specification

## Executive Summary
This document specifies the Execution Context (`execution_context`), the runtime state object that encapsulates task payload, working memory pointers, tool bindings, session security tokens, trace metadata, and environment limits passed to executing agents.

---

## 1. Execution Context Architecture

```text
+-------------------------------------------------------------------------+
|                        EXECUTION CONTEXT ENVELOPE                       |
|                                                                         |
|  [ IDENTIFIERS ]              [ MEMORY BOUNDARIES ]                     |
|  - contextId: UUID            - workingMemoryRef: Redis key             |
|  - taskId: UUID               - sessionStoreRef: PG session ID          |
|  - agentId: string            - tokenWindowLimit: 128,000               |
|                                                                         |
|  [ TOOL CAPABILITIES ]        [ TRACE & SECURITY ]                      |
|  - grantedTools: Map<Name,Fn> - traceParent: W3C Header                 |
|  - filesystemScope: Path      - securityToken: Ephemeral JWT           |
+-------------------------------------------------------------------------+
```

---

## 2. Context Schema & API Specification

```typescript
export interface ExecutionContextSchema {
  readonly contextId: string;
  readonly taskId: string;
  readonly agentId: string;
  readonly workflowId: string;
  readonly createdAt: string;
  readonly maxTokens: number;
  readonly timeoutMs: number;
  readonly metadata: Record<string, unknown>;
  readonly traceContext: {
    readonly traceId: string;
    readonly spanId: string;
  };
}

export interface IExecutionContextManager {
  createContext(params: Partial<ExecutionContextSchema>): Promise<ExecutionContextSchema>;
  cloneContext(contextId: string, overrides: Partial<ExecutionContextSchema>): Promise<ExecutionContextSchema>;
  destroyContext(contextId: string): Promise<void>;
  getMemoryPointer(contextId: string, memoryType: "working" | "session" | "persistent"): string;
}
```

---

## 3. Invariants & Security Constraints

1. **Context Immutability**: Top-level identifiers (`contextId`, `taskId`, `agentId`) are immutable once created.
2. **Context Leak Prevention**: Upon task completion or exception, secret tokens stored in context memory are overwritten with zero-bytes.
3. **Trace Context Propagation**: All sub-operations executed within an execution context inherit its W3C trace span ID.

---

## 4. Verification Protocol

```bash
agy verify-context-engine --run-leak-check
```
Creates context objects, checks scope isolation, verifies zeroization on context teardown, and validates trace header generation.
