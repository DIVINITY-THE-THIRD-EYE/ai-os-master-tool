# AI OS v4 — Capability Registry Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** System Security & Authorization Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Capability System Architecture

The **Capability Registry** governs system resource grants, entitlement scopes, and operating system primitive permissions within AI OS v4. Capabilities define fine-grained rights (such as network access, filesystem reads, memory allocation, hardware execution, or secret store access) assigned to agents, plugins, and tools.

The design relies on unforgeable capability tokens following object-capability (ocap) security principles.

```
                    +--------------------------------+
                    |      SECURITY SUPERVISOR       |
                    |  (Capability Granting Auth)    |
                    +---------------+----------------+
                                    | Issue Capability Token
                                    v
+-----------------------------------------------------------------------------------+
|                                CAPABILITY REGISTRY                                |
|  +----------------------+    +-----------------------+    +--------------------+  |
|  | Capability Taxonomy  |    | Hierarchy & Entitlement|    | Verification Gate  |  |
|  | Catalog              |    | Matrix                |    | Engine             |  |
|  +----------+-----------+    +-----------+-----------+    +---------+----------+  |
+-------------|----------------------------|--------------------------|-------------+
              |                            |                          |
              +----------------------------+--------------------------+
                                           | Verify Token
                                           v
+-----------------------------------------------------------------------------------+
|                             RUNTIME ENFORCEMENT POINTS                            |
|    [FS Access Controller]    [Network eBPF Filter]    [Secret Store Gatekeeper]   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Capability Hierarchy & Taxonomy

Capabilities are categorized hierarchically using dot-notation identifiers (`cap.<domain>.<subdomain>.<action>`).

```
cap
├── filesystem
│   ├── read               (Read files in sandboxed path)
│   ├── write              (Write/modify files in path)
│   └── execute            (Spawn local binary process)
├── network
│   ├── outbound_http      (Outbound HTTP/HTTPS requests)
│   ├── inbound_listen     (Open local network socket)
│   └── raw_socket         (Raw socket access - Admin only)
├── system
│   ├── process_spawn      (Spawn child processes)
│   ├── memory_expand      (Request working memory expansion)
│   └── dynamic_plugin     (Load dynamic runtime plugin)
├── memory
│   ├── working_read       (Read working memory)
│   ├── working_write      (Write working memory)
│   └── ekg_commit_request (Submit candidate memory to EKG pipeline)
└── secrets
    ├── read_key           (Read secret key from Vault)
    └── list_keys          (List secret key identifiers)
```

---

## 3. Capability Entitlement Schema

Each capability registration record defines the boundaries, constraints, and audit requirements associated with a capability grant.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CapabilityGrantRecord",
  "type": "object",
  "required": [
    "capability_id",
    "name",
    "domain",
    "risk_classification",
    "parameter_constraints",
    "audit_level",
    "requires_human_approval"
  ],
  "properties": {
    "capability_id": {
      "type": "string",
      "pattern": "^cap\\.[a-z0-9_]+\\.[a-z0-9_]+(\\.[a-z0-9_]+)?$"
    },
    "name": { "type": "string" },
    "domain": {
      "type": "string",
      "enum": ["filesystem", "network", "system", "memory", "secrets", "gpu"]
    },
    "risk_classification": {
      "type": "string",
      "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    },
    "parameter_constraints": {
      "type": "object",
      "description": "Constraints on invocation arguments, e.g. path prefixes or domain whitelists"
    },
    "audit_level": {
      "type": "string",
      "enum": ["STANDARD", "DETAILED", "FORENSIC_FULL"]
    },
    "requires_human_approval": { "type": "boolean" },
    "max_duration_seconds": { "type": "integer", "default": 3600 }
  }
}
```

---

## 4. Capability Binding & Token Lifecycle

### 4.1 Cryptographic Token Issuance

Capability grants are represented at runtime by HMAC-SHA256 signed JSON Web Tokens (JWT) or Macaroons containing:

```json
{
  "token_id": "tok_991823abf892",
  "agent_id": "agent.eng.developer_12",
  "tenant_id": "tenant_enterprise_alpha",
  "capabilities": [
    {
      "cap": "cap.filesystem.read",
      "constraints": { "allowed_paths": ["/workspace/project/*"] }
    },
    {
      "cap": "cap.network.outbound_http",
      "constraints": { "allowed_domains": ["api.github.com", "pypi.org"] }
    }
  ],
  "issued_at": 1770144000,
  "expires_at": 1770147600,
  "issuer_signature": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

---

## 5. Least-Privilege Escalation Protocol

When an agent requires temporary elevated capabilities beyond its static profile:

```
[Agent Request] 
      │
      v
[Capability Registry Check]
      │
      ├── Is Capability High/Critical Risk? ────► [YES] ──► [HITL Approval Request]
      │                                                           │
      │ [NO]                                                      ├── Approved? ──► [Issue Ephemeral Token]
      v                                                           └── Denied? ───► [Emit Policy Violation]
[Auto-Evaluate Policy Engine]
      │
      ├── Pass? ──► [Issue Ephemeral Token (15-min TTL)]
      └── Fail? ──► [Deny Request & Log]
```

---

## 6. Conflict Resolution & Overlapping Capability Arbitration

If a plugin requests `cap.filesystem.write` to `/etc/` while the Agent's security policy enforces `allowed_paths: ["/workspace/*"]`, the **Capability Arbitration Engine** applies the **Intersection Principle**:

$$\text{Effective Permissions} = \text{Agent Policy} \cap \text{Plugin Capability Request}$$

1. Path permissions narrow to the most restrictive bounding box.
2. Network domain whitelists use strict set intersection.
3. Any capability request outside the intersection boundary is silently pruned or triggers a hard authorization error.

---

## 7. Declarative Verification Engine & Audit Logging

- **Pre-execution Check:** Before any tool invocation, the runtime verifies capability signatures against the Capability Registry.
- **Audit Logging:** Every grant, denial, and JIT escalation emits a immutable cryptographic log event to `audit_log_framework`.
- **Revocation List:** Centralized Redis-backed capability revocation list checked on every verification attempt with sub-millisecond latency.

---

## 8. Summary Checklist for Capability Registry Compliance

- [x] Ocap security model implemented with HMAC/Macaroon capability tokens.
- [x] Comprehensive dot-notation capability taxonomy established.
- [x] Least-privilege JIT elevation workflow with human-in-the-loop triggers specified.
- [x] Strict set intersection capability arbitration rule codified.
- [x] Sub-millisecond revocation list checking integrated.
