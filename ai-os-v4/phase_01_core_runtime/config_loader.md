---
title: System Configuration Loader Specification
document_id: SPEC-P01-SAFE-038
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Platform Infrastructure Team
last_updated: 2026-08-05
---

# System Configuration Loader Specification

## Executive Summary
This document specifies the Configuration Loader (`config_loader`), responsible for ingesting, validating, parsing, schema checking, and broadcasting runtime configuration files across AI OS v4 kernel nodes.

---

## 1. Config Loader Pipeline Architecture

```text
[ SOURCE CONFIGURATION FILES / ENV ]
                 │
                 ▼
+-----------------------------------------------------------------+
| 1. FILE READ & ENVIRONMENT VARIABLE SUBSTITUTION (${SECRET})    |
+-----------------------------------------------------------------+
                 │
                 ▼
+-----------------------------------------------------------------+
| 2. JSON SCHEMA VALIDATION against 'runtime_config.schema.json'  |
+-----------------------------------------------------------------+
                 │
                 ▼
+-----------------------------------------------------------------+
| 3. IN-MEMORY IMMUTABLE CONFIG MAP CREATION & BROADCAST          |
+-----------------------------------------------------------------+
```

---

## 2. Config Loader Interface Contract

```typescript
export interface ParsedSystemConfig {
  readonly environment: string;
  readonly kernel: Record<string, unknown>;
  readonly messaging: Record<string, unknown>;
  readonly scheduler: Record<string, unknown>;
  readonly rawConfigHash: string;
}

export interface IConfigLoader {
  loadConfig(configPath: string): Promise<ParsedSystemConfig>;
  validateConfig(configObj: Record<string, unknown>): { isValid: boolean; errors?: string[] };
  reloadConfig(): Promise<ParsedSystemConfig>;
  onConfigChange(listener: (newConfig: ParsedSystemConfig) => void): void;
}
```

---

## 3. Mandatory Safety Constraints

1. **Zero Raw Secret Exposure**: Variable interpolation replacing `${SECRET_KEY}` masks secret values in memory inspection endpoints.
2. **Atomic Hot-Reloading**: Configuration reloads build a secondary candidate config map; the active config pointer swaps atomically only if validation succeeds 100%.

---

## 4. Verification Protocol

```bash
agy verify-config-loader --file ./aios.runtime.config.yaml
```
Tests YAML parsing, validates secret interpolation, simulates invalid config file schemas, and checks hot-reload callbacks.
