---
title: System Security Baseline Policy & Threat Controls
document_id: SPEC-P00-SEC-007
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Platform Security Group
last_updated: 2026-08-05
---

# System Security Baseline Policy & Threat Controls

## Executive Summary
This document specifies the core security architecture, access control models, prompt injection defenses, sandboxing isolation levels, credential handling rules, and STRIDE threat mitigations for AI OS v4. Compliance with this baseline is mandatory for all agent frameworks, runtime services, and plugins.

---

## 1. Security Architecture & Threat Isolation Boundaries

```text
[ UNTRUSTED USER INPUT ]
          │
          ▼
+-------------------------------------------------------------+
| 1. INPUT SANITIZATION & PROMPT INJECTION FILTER             |
+-------------------------------------------------------------+
          │
          ▼
+-------------------------------------------------------------+
| 2. ROLE-BASED ACCESS CONTROL (RBAC) & PERMISSION GATE       |
+-------------------------------------------------------------+
          │
          ▼
+-------------------------------------------------------------+
| 3. ISOLATED AGENT EXECUTION SANDBOX (gVisor / Container)   |
|    - Restricted File System (Ephemeral overlay)             |
|    - Restricted Network (Allow-list Egress Proxy)          |
+-------------------------------------------------------------+
          │
          ▼
+-------------------------------------------------------------+
| 4. CRYPTOGRAPHIC AUDIT LOG & SANITIZED KNOWLEDGE COMMIT     |
+-------------------------------------------------------------+
```

---

## 2. Mandatory Security Rules & Invariants

1. **Principle of Least Privilege**: Agents execute with minimal necessary tool permissions. Broad wildcard permissions (`tools: ["*"]`) are strictly banned.
2. **Prompt Injection Guardrails**: All user/external text inputs passing into LLM context MUST be wrapped in explicit structural boundaries (e.g. `<user_input_xml>`) and checked by a secondary classifier model.
3. **Egress Proxying**: Direct external HTTP network access by agents is blocked by default. Requests must route through the Platform Outbound Proxy with domain whitelist verification.
4. **Secret Zero Protection**: Secrets (LLM API keys, DB passwords) MUST reside in safe vault storage (AWS Secrets Manager, HashiCorp Vault). Agent code receives short-lived ephemeral tokens.
5. **No Direct Writes to Knowledge Base**: Unverified agent outputs MUST pass through candidate memory validation before committing to the enterprise graph.

---

## 3. Threat Mitigation Matrix (STRIDE Adaptation)

| STRIDE Category | Vector in AI OS v4 | Primary Defense Mechanism |
| :--- | :--- | :--- |
| **Spoofing** | Subagent identity forgery | Cryptographic mTLS agent tokens & signed message headers |
| **Tampering** | Memory state corruption | HMAC-SHA256 checksums on all serialized state files |
| **Repudiation** | Denying task execution | Append-only immutable audit log stored in write-once bucket |
| **Information Disclosure**| PII/Secret leaking in LLM prompt | Automated regex scrubber + token masking proxy before API calls |
| **Denial of Service** | Infinite loop / context overload | Resource Quota Limiter (max execution time 300s, max tokens 100k) |
| **Elevation of Privilege**| Tool execution escape | System-call restriction via seccomp filters inside gVisor container |

---

## 4. Verification & Audit Protocol

Audit system security posture using the automated security scanner:
```bash
agy audit-security --level strict --root ./ai-os-v4
```
Fails if any unencrypted communication, exposed secrets, or loose permissions are detected.
