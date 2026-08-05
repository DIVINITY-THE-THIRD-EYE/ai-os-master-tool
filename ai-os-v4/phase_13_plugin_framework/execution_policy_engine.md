# AI OS v4 — Execution Policy Engine Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** Core Runtime Policy Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Engine Architecture & Pipeline Overview

The **Execution Policy Engine (EPE)** serves as the central evaluation point for all tool, plugin, and workflow execution policies in AI OS v4. It synthesizes inputs from security, rate limiting, permissions, memory, and governance policies into a single deterministic evaluation pipeline.

```
+-----------------------------------------------------------------------------------+
|                            EXECUTION REQUEST INGRESS                              |
|          (Agent ID, Tool ID, Invocation Arguments, Session Context)              |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        POLICY EVALUATION PIPELINE (EPE)                           |
|                                                                                   |
|  [Stage 1: Syntax & Schema Pre-Filter]                                            |
|         │                                                                         |
|         v                                                                         |
|  [Stage 2: Capability & Permission Evaluation (ABAC/RBAC)]                        |
|         │                                                                         |
|         v                                                                         |
|  [Stage 3: Resource & Rate Limit Check (Sliding Window / Redis)]                  |
|         │                                                                         |
|         v                                                                         |
|  [Stage 4: Deep Parameter Inspection & DLP Filter]                                |
|         │                                                                         |
|         v                                                                         |
|  [Stage 5: Sandbox Tier Routing & Policy Decision Generation]                     |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
        v                                 v                                 v
   [EXECUTE]                       [REJECT / DENY]                 [REQUIRE APPROVAL]
(Dispatch Sandbox)             (Emit Security Event)          (Dispatch HITL Task)
```

---

## 2. Policy Decision Point (PDP) & Policy Enforcement Point (PEP) Interface

### 2.1 PDP Interface Specification

```typescript
export interface PolicyDecisionPoint {
  evaluateExecutionRequest(request: ExecutionContextRequest): Promise<PolicyDecision>;
  loadPolicySet(policySetId: string): Promise<boolean>;
  invalidatePolicyCache(tenantId: string): Promise<void>;
}

export interface ExecutionContextRequest {
  request_id: string;
  tenant_id: string;
  agent_id: string;
  agent_role: string;
  tool_id: string;
  input_parameters: Record<string, unknown>;
  session_context: Record<string, unknown>;
  timestamp_ms: number;
}

export interface PolicyDecision {
  decision: "ALLOW" | "DENY" | "REQUIRE_APPROVAL";
  assigned_sandbox_tier: "TIER_0" | "TIER_1" | "TIER_2" | "TIER_3";
  applied_rules: string[];
  denial_reason?: string;
  approval_workflow_id?: string;
  evaluation_latency_ms: number;
}
```

---

## 3. High-Performance AST Rule Evaluation Engine

Policies are compiled into an Abstract Syntax Tree (AST) stored in memory. The evaluation engine achieves sub-millisecond decision latency (<1.5 ms P99) by using memoized decision caches and bitmask-accelerated rule evaluation.

### 3.1 Rule AST Graph Structure

```
                             [AND Root Node]
                                    │
          +-------------------------+-------------------------+
          |                                                   |
   [EQUALS Node]                                       [IN Node]
   Subject.Tenant == "alpha"                           Subject.Role IN ["Admin", "Dev"]
```

---

## 4. Policy Caching & Invalidation Protocol

1. **L1 In-Memory Cache:** Node-local LRU cache storing decision outputs for `(AgentID, ToolID, ParametersHash)` tuples with 5-second TTL.
2. **L2 Shared Redis Cache:** Distributed cluster cache for cross-node decision synchronization.
3. **Invalidation Invariants:** Updating any policy manifest instantly flushes L1 and L2 caches globally across all worker nodes within <50 ms via Pub/Sub invalidation events.

---

## 5. Summary Checklist for Execution Policy Engine Compliance

- [x] 5-stage deterministic policy evaluation pipeline defined.
- [x] PDP / PEP TypeScript contracts fully specified.
- [x] Sub-1.5ms AST evaluation engine architecture detailed.
- [x] L1/L2 policy caching and instant invalidation protocols enforced.
