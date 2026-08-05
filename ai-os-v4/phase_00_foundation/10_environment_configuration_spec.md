---
title: Environment Configuration & Secret Management Specification
document_id: SPEC-P00-ENV-010
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Platform Operations Team
last_updated: 2026-08-05
---

# Environment Configuration & Secret Management Specification

## Executive Summary
This document specifies environment variable definitions, deployment profile configurations (`development`, `testing`, `staging`, `production`), secrets management, and environment isolation rules for AI OS v4.

---

## 1. Environment Profiles Matrix

AI OS v4 supports four deterministic runtime profiles:

```text
[ DEVELOPMENT ] ──> Mock LLM endpoints, local file storage, verbose debug logs
[ TESTING ]     ──> In-memory message broker, sandbox mock tools, strict assertions
[ STAGING ]     ──> Staging LLM keys, Redis cache, production-like sandbox
[ PRODUCTION ]  ──> Multi-region NATS broker, HashiCorp Vault secrets, strict mTLS
```

---

## 2. Global Environment Variable Catalog

| Environment Variable | Required Profile | Type | Default Value | Description |
| :--- | :---: | :--- | :--- | :--- |
| `AIOS_ENV` | ALL | enum | `development` | Profile: `development`, `testing`, `staging`, `production` |
| `AIOS_KERNEL_ID` | STG/PROD | string | `kernel-node-01` | Unique node identifier in cluster |
| `AIOS_LOG_LEVEL` | ALL | enum | `INFO` | `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `AIOS_BROKER_URL` | STG/PROD | string | `nats://localhost:4222` | Message broker connection URL |
| `AIOS_REDIS_URL` | STG/PROD | string | `redis://localhost:6379/0` | Working memory storage endpoint |
| `OPENAI_API_KEY` | STG/PROD | secret | `[REQUIRED]` | OpenAI provider API access key |
| `ANTHROPIC_API_KEY` | OPTIONAL | secret | `[NONE]` | Anthropic fallback provider API key |
| `AIOS_SANDBOX_MODE` | ALL | enum | `STRICT` | Sandboxing: `DISABLED`, `PERMISSIVE`, `STRICT` |

---

## 3. Secret Resolution & Vault Integration

```text
[ Secret Access Request ]
          │
          ▼
+------------------------------------+
| 1. ENVIRONMENT INJECTION GATE      |  Checks process environment
+------------------------------------+
          │ (If missing)
          ▼
+------------------------------------+
| 2. KUBERNETES SECRET / VAULT AGENT |  Fetches from HashiCorp Vault via mTLS
+------------------------------------+
          │
          ▼
+------------------------------------+
| 3. EPHEMERAL MEMORY DECRYPTION     |  In-memory RAM decryption (zero disk exposure)
+------------------------------------+
```

1. Secrets MUST NEVER be logged or serialized in error stack traces.
2. The runtime automatically redacts string patterns matching standard API key formats (`sk-proj-*`, `gsk_*`).

---

## 4. Verification Protocol

Verify environment configuration:
```bash
agy verify-env --profile production
```
Validates that all required environment variables are set and secrets are populated securely.
