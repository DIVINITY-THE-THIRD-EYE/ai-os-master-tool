# AI OS v4 — Plugin Lifecycle Manager Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** Core Runtime Lifecycle Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Lifecycle Architecture & State Machine

The **Plugin Lifecycle Manager (PLM)** controls the state transitions, initialization, dependency wiring, health tracking, zero-downtime updates, and graceful termination of plugins within AI OS v4.

```
       +------------------------------------------------------------------+
       |                           DISCOVERED                             |
       +--------------------------------+---------------------------------+
                                        | Validate Signature & Manifest
                                        v
       +------------------------------------------------------------------+
       |                            VALIDATED                             |
       +--------------------------------+---------------------------------+
                                        | Resolve Dependencies & Install
                                        v
       +------------------------------------------------------------------+
       |                            INSTALLED                             |
       +--------------------------------+---------------------------------+
                                        | Execute PreActivate Hooks
                                        v
       +------------------------------------------------------------------+
       |                             ACTIVE                               |
       |                   (Handling Tool Invocations)                    |
       +-------+------------------------+-------------------------+-------+
               |                        |                         |
  Health Fail  |             Pause Cmd  |            Upgrade Cmd  |
               v                        v                         v
       +---------------+        +---------------+        +----------------+
       |   DEGRADED    |        |    PAUSED     |        |  DEPRECATING   |
       +-------+-------+        +-------+-------+        +--------+-------+
               |                        |                         |
               +------------------------+-------------------------+
                                        | Uninstall / Deactivate
                                        v
       +------------------------------------------------------------------+
       |                           UNINSTALLED                            |
       +------------------------------------------------------------------+
```

---

## 2. State Transition Matrix & Actions

| Current State | Event Trigger | Next State | Allowed? | Required Action |
| :--- | :--- | :--- | :---: | :--- |
| `UNINSTALLED` | `PackageUploaded` | `DISCOVERED` | **YES** | Verify SHA-256 and store in OCI store |
| `DISCOVERED` | `ValidateCommand` | `VALIDATED` | **YES** | Signature check, vulnerability scan |
| `VALIDATED` | `InstallCommand` | `INSTALLED` | **YES** | Allocate sandbox resources, mount files |
| `INSTALLED` | `ActivateCommand` | `ACTIVE` | **YES** | Register tools into Tool Registry |
| `ACTIVE` | `HealthCheckFailed`| `DEGRADED` | **YES** | Trip circuit breaker, send alert |
| `ACTIVE` | `PauseCommand` | `PAUSED` | **YES** | Block new calls, complete active ones |
| `ACTIVE` | `UpgradeCommand` | `DEPRECATING` | **YES** | Deploy new version in parallel |
| `DEPRECATING` | `AllSessionsCompleted`| `UNINSTALLED` | **YES** | Clean up sandbox and unmount volumes |
| `PAUSED` | `ResumeCommand` | `ACTIVE` | **YES** | Unblock calls, re-enable tool index |
| `DEGRADED` | `SelfHealSuccess` | `ACTIVE` | **YES** | Reset health score to 100% |

---

## 3. Lifecycle Hooks Specification

Plugins can implement standard hook handlers executed at specific transition points:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PluginLifecycleHooks",
  "type": "object",
  "properties": {
    "on_pre_install": { "type": "string", "description": "Validation script path" },
    "on_post_install": { "type": "string", "description": "Database migration script path" },
    "on_pre_activate": { "type": "string", "description": "Environment warm-up script" },
    "on_post_deactivate": { "type": "string", "description": "Resource cleanup script" },
    "on_health_check": { "type": "string", "description": "Custom health check endpoint" }
  }
}
```

---

## 4. Zero-Downtime Hot Swapping Protocol

Upgrading an active plugin from version $V_1$ to $V_2$ proceeds without interrupting ongoing agent workflows:

1. **Parallel Instantiation:** $V_2$ is installed and activated in a new isolated sandbox container alongside $V_1$.
2. **Registry Routing Switch:** Tool Registry atomically swaps the routing pointer for new invocations to $V_2$.
3. **Graceful Drain:** Existing in-flight requests on $V_1$ are allowed to complete up to `max_drain_timeout_ms` (default 30,000 ms).
4. **Decommission:** $V_1$ transitions to `UNINSTALLED` and its sandbox container is destroyed.

---

## 5. Lifecycle Management API Contract

```typescript
export interface PluginLifecycleManagerAPI {
  installPlugin(pluginPackageUrl: string, tenantId: string): Promise<PluginLifecycleStatus>;
  activatePlugin(pluginId: string, version: string, tenantId: string): Promise<boolean>;
  deactivatePlugin(pluginId: string, tenantId: string): Promise<boolean>;
  upgradePluginHotSwap(pluginId: string, targetVersion: string, tenantId: string): Promise<HotSwapResult>;
  getPluginHealth(pluginId: string): Promise<PluginHealthReport>;
}
```

---

## 6. Summary Checklist for Plugin Lifecycle Manager Compliance

- [x] Complete state transition matrix with 8 states defined.
- [x] Pre/Post lifecycle hook JSON specification locked.
- [x] Zero-downtime hot swapping protocol detailed.
- [x] In-flight request graceful drain mechanism specified.
- [x] TypeScript management API contract published.
