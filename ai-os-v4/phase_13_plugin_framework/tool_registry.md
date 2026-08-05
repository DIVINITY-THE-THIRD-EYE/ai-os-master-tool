# AI OS v4 — Tool Registry Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** Enterprise System Architecture Specification  
**Status:** Frozen / Production Standard  

---

## 1. Overview & Architecture Blueprint

The **Tool Registry** is the centralized control plane component responsible for indexing, validating, partitioning, and resolving all tool capabilities available to autonomous agents within AI OS v4. Tools represent executable capabilities—ranging from filesystem operations and network clients to domain-specific analytical engines and API connectors.

The Tool Registry guarantees strong isolation, strict contract enforcement, dynamic discovery, and permission-aware dispatching across multi-tenant runtime environments.

```
+-----------------------------------------------------------------------------------+
|                                 AGENT RUNTIME                                     |
|  +------------------+     +--------------------+     +-------------------------+  |
|  |   Worker Agent   |     |  Planner Agent     |     |   Security Supervisor   |  |
|  +--------+---------+     +---------+----------+     +------------+------------+  |
+-----------|-------------------------|-----------------------------|---------------+
            | Query Tools             | Resolve Capabilities        | Enforce Policy
            v                         v                             v
+-----------------------------------------------------------------------------------+
|                                 TOOL REGISTRY                                     |
|  +-------------------+    +--------------------+    +--------------------------+  |
|  | Tool Indexer &    |    |  Schema Validator  |    |  Multi-Tenant Access     |  |
|  | Catalog Engine    |    |  (JSON / OpenAPI)  |    |  Control Engine          |  |
|  +---------+---------+    +---------+----------+    +------------+-------------+  |
|            |                        |                            |                |
|            +------------------------+----------------------------+                |
|                                     |                                             |
|                                     v                                             |
|                     +-------------------------------+                             |
|                     | Storage & Dynamic Hot-Reload  |                             |
|                     | Memory State & Cache Layer    |                             |
|                     +---------------+---------------+                             |
+-------------------------------------|---------------------------------------------+
                                      | Dispatch Exec Request
                                      v
+-----------------------------------------------------------------------------------+
|                             EXECUTION SANDBOX LAYER                               |
|   [In-Process]       [WASM Micro-Engine]       [Docker Container]     [Firecracker] |
+-----------------------------------------------------------------------------------+
```

---

## 2. Tool Definition Contract & Schema

Every tool registered in AI OS v4 must declare an explicit JSON/YAML manifest. Tools without verified schemas are rejected during registration.

### 2.1 Manifest JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AIOSv4ToolDefinition",
  "type": "object",
  "required": [
    "tool_id",
    "name",
    "version",
    "namespace",
    "description",
    "category",
    "execution_type",
    "input_schema",
    "output_schema",
    "capabilities_required",
    "idempotent",
    "side_effects"
  ],
  "properties": {
    "tool_id": {
      "type": "string",
      "pattern": "^[a-z0-9_\\-]+\\.[a-z0-9_\\-]+\\.[a-z0-9_\\-]+$"
    },
    "name": { "type": "string", "maxLength": 128 },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "namespace": { "type": "string" },
    "description": { "type": "string", "minLength": 20 },
    "category": {
      "type": "string",
      "enum": ["filesystem", "network", "database", "analytics", "security", "utility", "system"]
    },
    "execution_type": {
      "type": "string",
      "enum": ["builtin", "wasm", "docker", "gRPC", "http_endpoint"]
    },
    "input_schema": { "type": "object" },
    "output_schema": { "type": "object" },
    "capabilities_required": {
      "type": "array",
      "items": { "type": "string" }
    },
    "idempotent": { "type": "boolean" },
    "side_effects": {
      "type": "array",
      "items": { "type": "string" }
    },
    "timeout_ms": { "type": "integer", "default": 30000, "maximum": 600000 },
    "rate_limit_group": { "type": "string" }
  }
}
```

### 2.2 Concrete Tool Manifest Example

```json
{
  "tool_id": "com.aios.system.file_reader",
  "name": "Secure File Reader",
  "version": "1.0.0",
  "namespace": "com.aios.system",
  "description": "Reads specified file path within approved agent workspace directory.",
  "category": "filesystem",
  "execution_type": "builtin",
  "input_schema": {
    "type": "object",
    "required": ["file_path"],
    "properties": {
      "file_path": { "type": "string" },
      "start_line": { "type": "integer", "minimum": 1 },
      "end_line": { "type": "integer", "minimum": 1 }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["status", "content", "byte_size"],
    "properties": {
      "status": { "type": "string", "enum": ["SUCCESS", "FILE_NOT_FOUND", "ACCESS_DENIED"] },
      "content": { "type": "string" },
      "byte_size": { "type": "integer" }
    }
  },
  "capabilities_required": ["cap.filesystem.read"],
  "idempotent": true,
  "side_effects": [],
  "timeout_ms": 10000,
  "rate_limit_group": "fs_read_ops"
}
```

---

## 3. Tool Discovery & Metadata Indexing

The Tool Registry maintains a real-time index optimized for LLM tool-calling efficiency and agent prompt injection reduction.

### 3.1 Metadata Index Engine

1. **Category & Tag Indexing:** Indexing tools by namespace, domain category, semantic tags, and required capability scopes.
2. **Semantic Embedding Index:** Vector embeddings of tool descriptions stored in in-memory HNSW index for natural-language semantic tool selection (`find_tools_for_intent(prompt)`).
3. **Context-Aware Filtering:** Automatically filters available tools based on agent identity, active session permissions, and current tenant context before embedding tools into LLM prompts.

```typescript
export interface ToolRegistryInterface {
  registerTool(manifest: ToolManifest): Promise<RegistrationResult>;
  unregisterTool(toolId: string): Promise<boolean>;
  getTool(toolId: string): Promise<ToolManifest | null>;
  searchTools(query: SemanticSearchQuery): Promise<ToolManifest[]>;
  listToolsByCapability(capability: string, tenantId: string): Promise<ToolManifest[]>;
  validateInvocationInput(toolId: string, inputData: Record<string, unknown>): ValidationResult;
}
```

---

## 4. Multi-Tenant Tool Partitioning & Access Control

Tools are partitioned into three isolation tiers:

| Isolation Tier | Accessibility Scope | Registration Authority | Risk Level |
| :--- | :--- | :--- | :--- |
| **Platform System** | All agents, read-only system tools | Kernel Core Developer | Low |
| **Tenant Shared** | Agents within single enterprise tenant | Tenant Security Admin | Medium |
| **Agent Ephemeral** | Scoped strictly to single agent lifecycle | Dynamic Runtime Supervisor | Variable |

### 4.1 Access Control Evaluation Rule

```text
ALLOWED = (Agent.Capabilities SUPERSET_OF Tool.CapabilitiesRequired)
          AND (Agent.TenantID == Tool.TenantID OR Tool.IsPlatformSystem)
          AND (SecurityPolicyEngine.Evaluate(Agent, Tool, Context) == ALLOW)
```

---

## 5. Dynamic Tool Ingestion, Hot Reloading & Version Pinning

1. **Hot Reloading:** The registry supports zero-downtime registration, updates, and deprecation. Active invocations complete using the tool version pinned at task initialization.
2. **Version Pinning:** Agents bind to explicit SemVer identifiers (`1.2.0`) or semantic ranges (`^1.0.0`). Deprecated versions trigger warning telemetry and grace-period schedules.
3. **Hot Unloading:** Removing a tool instantly revokes permission tokens and prevents new invocations while waiting for current async executions to terminate safely.

---

## 6. Built-in System Tools vs Dynamic Plugin Tools

```
               +-------------------------------------------------+
               |                TOOL REGISTRY CATALOG            |
               +------------------------+------------------------+
                                        |
                 +----------------------+----------------------+
                 |                                             |
                 v                                             v
    +--------------------------+                 +--------------------------+
    |   BUILT-IN SYSTEM TOOLS  |                 |   DYNAMIC PLUGIN TOOLS   |
    |  - Fast C++ / Go / WASM  |                 |  - External RPC / HTTP   |
    |  - Kernel Access         |                 |  - Isolated Containers   |
    |  - Pre-approved Policy   |                 |  - Dynamic Verification  |
    +--------------------------+                 +--------------------------+
```

---

## 7. Telemetry, Health Checks & Circuit Breaking

Every registered tool is monitored by an automated health checker:

- **Liveness Probes:** Regular health check invocations for gRPC/HTTP endpoints every 30 seconds.
- **Circuit Breaker:** If a tool experiences a >15% error rate or 3 consecutive timeout failures within a 60-second window, its state transitions to `DEGRADED` or `UNAVAILABLE`.
- **Latency SLAs:** P95 and P99 latency limits are tracked continuously. Over-budget tools trigger automatic rate degradation.

---

## 8. Summary Checklist for Tool Registry Compliance

- [x] Full JSON Schema contract for tool manifests validated.
- [x] Multi-tenant isolation verified with tenant ID scope rules.
- [x] Semantic vector discovery and prompt context filtering enabled.
- [x] Hot-reloading and dynamic unloading without system restart supported.
- [x] Integrated circuit breaker and automated health checker operational.
