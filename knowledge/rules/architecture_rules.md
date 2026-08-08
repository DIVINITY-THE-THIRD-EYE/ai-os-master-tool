# AI OS v4 Multi-Agent Architectural Rules (`architecture_rules.md`)

## 1. Architectural Philosophy & Core Principles

The AI OS v4 architecture is designed for **extreme modularity**, **event-driven orchestration**, **fault isolation**, and **semantic predictability**. Autonomous agents operate as loosely-coupled micro-services communicating via standardized event topics and strongly-typed interface contracts.

```
+-----------------------------------------------------------------------+
|                       Event Bus & Message Router                       |
+-----------------------------------------------------------------------+
       ^                      ^                      ^
       |                      |                      |
+--------------+      +--------------+      +--------------+
| Agent A01    |      | Agent A04    |      | Agent A06    |
| Orchestrator |      | Lead Engineer|      | QA Agent     |
+--------------+      +--------------+      +--------------+
       |                      |                      |
       v                      v                      v
+-----------------------------------------------------------------------+
|                     Shared State & Memory Engine                      |
+-----------------------------------------------------------------------+
```

---

## 2. Architecture Rule Specifications

### Rule ARC-001: Strict Agent Decoupling & Isolation
- **Rule ID**: `ARC-001`
- **Severity**: `CRITICAL`
- **Scope**: Agent Architecture (A01–A13)
- **Description**: Agents MUST NOT directly inspect or manipulate the internal memory state, private variables, or local scratchpads of other agents. All inter-agent interaction occurs exclusively via published event topics or formal JSON schema handoff payloads.

### Rule ARC-002: Explicit Interface Contracts & Schema Schema Binding
- **Rule ID**: `ARC-002`
- **Severity**: `CRITICAL`
- **Scope**: All System Subsystems & APIs
- **Description**: Every interface between agents, workflows, tools, and storage layers must be formally defined by a versioned JSON Schema or Protobuf definition. Direct untyped dictionary or raw string passing across agent boundaries is prohibited.

### Rule ARC-003: Stateless Agent Execution Engine
- **Rule ID**: `ARC-003`
- **Severity**: `HIGH`
- **Scope**: Agent Runtime Engine
- **Description**: Agent execution loops must be stateless. All context required to resume or execute a task must be supplied via the `ExecutionContext` object passed during invocation. Agents must be fully restartable on any node without state loss.

### Rule ARC-004: Event-Driven Asynchronous Communication
- **Rule ID**: `ARC-004`
- **Severity**: `HIGH`
- **Scope**: System Event Bus
- **Description**: Synchronous blocking HTTP/RPC calls between agents are discouraged for long-running operations ($>500\text{ms}$). Agents emit events (`EVT_TASK_COMPLETED`, `EVT_VERIFICATION_FAILED`) and listen asynchronously.

### Rule ARC-005: Strict Boundary Between Ephemeral & Persistent Memory
- **Rule ID**: `ARC-005`
- **Severity**: `HIGH`
- **Scope**: Memory Subsystem
- **Description**: Working memory (prompt scratchpads) exists only for the duration of a single task execution cycle. Data required across tasks must be explicitly flushed to Persistent Memory or Knowledge Graph via validated memory write transactions.

### Rule ARC-006: Sub-Second Message Router Latency SLA
- **Rule ID**: `ARC-006`
- **Severity**: `MEDIUM`
- **Scope**: Message Bus & Broker
- **Description**: The internal event bus message routing latency must not exceed $50\text{ms}$ at the 99th percentile ($P_{99}$). Agent task response initiation must occur within $500\text{ms}$.

### Rule ARC-007: Graceful Degradation & Fallback Circuit Breakers
- **Rule ID**: `ARC-007`
- **Severity**: `HIGH`
- **Scope**: Workflow Orchestrator & Tool Integrations
- **Description**: If a primary LLM model provider or external tool fails or experiences rate limits, the system must trip a circuit breaker and automatically fall back to an secondary model or alternative execution strategy without throwing uncaught runtime exceptions.
- **Circuit Breaker Configuration**:
  - Failure Threshold: 5 consecutive errors.
  - Reset Timeout: 60 seconds.
  - Fallback Target: Secondary LLM Provider / Cached Analysis.

### Rule ARC-008: Single Responsibility Principle for Specialized Agents
- **Rule ID**: `ARC-008`
- **Severity**: `HIGH`
- **Scope**: Agent Specification Design
- **Description**: Each agent spec must focus on a single domain specialty (e.g., A07 focuses strictly on Security Audit, A09 strictly on Documentation). Blending unrelated responsibilities into a single agent is an architectural violation.

### Rule ARC-009: Strict Semantic Versioning of Agent Capabilities
- **Rule ID**: `ARC-009`
- **Severity**: `MEDIUM`
- **Scope**: Agent Manifest & Capabilities
- **Description**: Agent specs and prompt interfaces follow Semantic Versioning (`MAJOR.MINOR.PATCH`). Non-backwards-compatible prompt modifications or tool schema changes require a `MAJOR` version increment.

### Rule ARC-010: Complete System Observability & Tracing
- **Rule ID**: `ARC-010`
- **Severity**: `HIGH`
- **Scope**: Telemetry & Monitoring Subsystem
- **Description**: Every multi-agent execution thread must inject OpenTelemetry trace headers (`trace_id`, `span_id`, `parent_span_id`). Full execution paths must be reconstructible in real-time.
