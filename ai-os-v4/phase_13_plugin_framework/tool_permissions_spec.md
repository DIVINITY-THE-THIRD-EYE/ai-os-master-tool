# AI OS v4 — Tool Permissions Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** System Security & Authorization Specification  
**Status:** Frozen / Production Standard  

---

## 1. Security Architecture & Authorization Model

The **Tool Permissions Engine** is responsible for evaluating, granting, and enforcing tool execution permissions in real time. It implements a hybrid **Attribute-Based Access Control (ABAC)** and **Role-Based Access Control (RBAC)** decision engine that checks agent identity, environmental context, tool safety classification, parameter contents, and active session attributes prior to tool execution.

```
+-----------------------------------------------------------------------------------+
|                            TOOL INVOCATION DISPATCHER                             |
+-----------------------------------------+-----------------------------------------+
                                          | Request Invocation
                                          v
+-----------------------------------------------------------------------------------+
|                        POLICY DECISION POINT (PDP) ENGINE                         |
|  +---------------------+   +---------------------+   +-------------------------+  |
|  | Context Sanitizer   |   | ABAC / RBAC Rule    |   | Argument Deep Inspector |  |
|  | & Attribute Fetcher |   | Evaluator Engine    |   | (Regex / AST / DLP)     |  |
|  +----------+----------+   +----------+----------+   +------------+------------+  |
+-------------|-------------------------|---------------------------|---------------+
              |                         |                           |
              +-------------------------+---------------------------+
                                        | Decision (ALLOW / DENY / REQUIRE_APPROVAL)
                                        v
+-----------------------------------------------------------------------------------+
|                       POLICY ENFORCEMENT POINT (PEP) GATE                         |
|   [ALLOW] ──► Execute Tool     [DENY] ──► Block & Audit     [REQUIRE_APPROVAL] ──► HITL |
+-----------------------------------------------------------------------------------+
```

---

## 2. Permission Evaluation Context & Attributes

The Authorization Context tuple $C$ evaluated for every tool execution consists of five distinct attribute domains:

$$C = \langle \text{Subject}, \text{Resource}, \text{Action}, \text{Environment}, \text{Risk} \rangle$$

1. **Subject Attributes ($S$):** Agent ID, Role, Tenant ID, Security Clearance Level, Active Session ID.
2. **Resource Attributes ($R$):** Tool ID, Tool Category, Target Path/Endpoint, Resource Owner Tenant ID.
3. **Action Attributes ($A$):** Execution Method, Invocation Parameters, Destructive Side-Effect Flag.
4. **Environment Attributes ($E$):** Time of day, Active Deployment Environment (Dev, Staging, Prod), System Threat Level.
5. **Risk Attributes ($K$):** Cumulative session risk score, token consumption velocity, recent policy violation count.

---

## 3. Tool Permission Rule DSL Schema

Tool permission rules are declared using a declarative YAML/JSON Policy Language.

```yaml
version: "4.0"
policy_id: "pol_filesystem_security_prod"
name: "Production Filesystem Access Rules"
tenant_id: "tenant_enterprise_alpha"
rules:
  - rule_id: "rule_deny_etc_access"
    effect: "DENY"
    tools: ["com.aios.system.file_reader", "com.aios.system.file_writer"]
    condition:
      field: "input.file_path"
      operator: "REGEX_MATCH"
      value: "^/(etc|proc|sys|var/run|root)/.*"
    action_on_trigger: "LOG_SECURITY_ALERT"

  - rule_id: "rule_allow_workspace_write"
    effect: "ALLOW"
    tools: ["com.aios.system.file_writer"]
    condition:
      and:
        - field: "subject.role"
          operator: "IN"
          value: ["ROLE_ENGINEER", "ROLE_ARCHITECT"]
        - field: "input.file_path"
          operator: "STARTS_WITH"
          value: "/workspace/project/"
        - field: "environment.type"
          operator: "NOT_EQUALS"
          value: "PROD_CRITICAL"

  - rule_id: "rule_require_approval_production_delete"
    effect: "REQUIRE_HUMAN_APPROVAL"
    tools: ["com.aios.system.file_deleter", "com.aios.db.drop_table"]
    condition:
      field: "environment.type"
      operator: "EQUALS"
      value: "PROD"
```

---

## 4. Parameter Validation & Deep Content Sanitization

Before approving an invocation, the Permission Engine performs deep parameter analysis to prevent path traversal, command injection, and data leakage.

### 4.1 Parameter Defense Protocols

1. **Path Traversal Protection:** Normalizes all file paths (`canonicalize()`) and verifies they remain inside permitted base directories. Resolves symlinks before evaluation.
2. **Command Injection Scrubbing:** Enforces strict shell escaping and disallows shell execution strings (`&&`, `;`, `|`, `` ` ``, `$()`).
3. **Data Loss Prevention (DLP):** Scans tool outputs and inputs for PII, API tokens, RSA keys, and credit card numbers using high-performance regex scanners.

---

## 5. Just-in-Time (JIT) Permission Elevation Workflows

When an agent requests execution of a restricted tool:

```
[Agent Tool Request] ──► [Deny by Default]
                               │
                               v
                     [Check JIT Elevation Policy]
                               │
                               ├── Is Temp Elevation Allowed?
                               │     │
                               │     ├── [YES] ──► Emit Approval Event to Slack / Teams / Webhook
                               │     │                 │
                               │     │                 ├── Human Admin Approves (TTL: 10m)
                               │     │                 │        │
                               │     │                 │        v
                               │     │                 │   [Inject Temp Permission Grant]
                               │     │                 │
                               │     │                 └── Human Admin Rejects
                               │     │                          │
                               │     │                          v
                               │     │                     [Hard Abort & Audit Log]
                               │     │
                               │     └── [NO] ──► [Hard Reject]
```

---

## 6. Security Invariants & Non-Negotiables

1. **Deny-by-Default:** Any tool invocation without an explicit `ALLOW` rule evaluates to `DENY`.
2. **No Dynamic Code String Execution:** Tools accepting raw code strings (`eval()`, `exec()`) are forbidden in multi-tenant environments.
3. **Immutable Path Anchors:** Path variables must be anchored relative to isolated workspace roots; system root (`/`) access is globally banned for non-kernel agents.
4. **Instant Revocation:** Revoking a role or permission takes effect globally across all active sessions within <100 milliseconds.

---

## 7. Summary Checklist for Tool Permissions Compliance

- [x] ABAC + RBAC policy evaluation model specified with 5 attribute domains.
- [x] Canonical Declarative YAML/JSON rule schema defined.
- [x] Path traversal, command injection, and DLP parameter sanitization mandated.
- [x] Human-in-the-loop JIT permission elevation workflow specified.
- [x] Deny-by-default and sub-100ms global revocation invariants enforced.
