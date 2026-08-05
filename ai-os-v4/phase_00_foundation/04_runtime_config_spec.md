---
title: Runtime Configuration Engine Specification
document_id: SPEC-P00-CONF-004
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Platform Infrastructure Team
last_updated: 2026-08-05
---

# Runtime Configuration Engine Specification

## Executive Summary
This document specifies the global runtime configuration schema, loading hierarchy, environment overrides, hot-reloading rules, and security controls for AI OS v4. It defines how platform settings, model endpoints, queue limits, persistence options, and logging parameters are declared and ingested by kernel processes.

---

## 1. Configuration Loading Hierarchy & Precedence

Configuration values are resolved in order of priority (highest priority first):

```text
[ 1. Command-line Flags (--config.kernel.max_threads=16) ]
                         │
                         ▼
[ 2. Environment Variables (AIOS_KERNEL_MAX_THREADS=16) ]
                         │
                         ▼
[ 3. Local Workspace Config (.aios/config.local.json) ]
                         │
                         ▼
[ 4. Global System Config (aios.runtime.config.yaml) ]
                         │
                         ▼
[ 5. Built-in Kernel Defaults ]
```

---

## 2. Declarative Specification Schema (`aios.runtime.config.yaml`)

```yaml
version: "4.0.0"
environment: "production"

kernel:
  id: "kernel-prod-node-01"
  log_level: "INFO"
  max_concurrent_agents: 64
  thread_pool_size: 16
  tick_interval_ms: 100
  enable_telemetry: true

messaging:
  broker_type: "nats" # nats | kafka | memory
  endpoint: "nats://localhost:4222"
  default_timeout_ms: 5000
  retry_attempts: 3
  dlq_topic: "aios.system.dlq"

scheduler:
  mode: "dag_parallel"
  max_queue_depth: 10000
  task_preemption: true
  resource_limit_cpu: 80.0 # percentage
  resource_limit_memory_mb: 16384

memory:
  working_memory_provider: "redis"
  persistent_store_provider: "postgresql"
  cache_ttl_seconds: 3600
  checkpoint_interval_seconds: 60

security:
  mTLS_enabled: true
  sandbox_enforcement: "STRICT"
  allowed_executables: ["node", "python3", "git"]

llm_providers:
  default_provider: "openai"
  fallback_provider: "anthropic"
  request_timeout_ms: 60000
  max_retries: 3
```

---

## 3. Hot-Reloading & Validation Rules

1. **Atomic Configuration Reload**: Non-disruptive configuration variables (e.g. log level, rate limits) MUST hot-reload via SIGUSR1 or RPC call `Kernel.ReloadConfig()`.
2. **Static Invariants**: Core parameters (`broker_type`, `kernel.id`, `working_memory_provider`) require graceful node restart and CANNOT be hot-reloaded.
3. **Strict Validation**: Invalid configuration schema or missing required credentials aborts runtime startup immediately with exit code `101`.

---

## 4. Verification Command

```bash
agy check-config --file ./aios.runtime.config.yaml --env production
```
Verifies formatting, types, secrets masking, and environment parameter integrity.
