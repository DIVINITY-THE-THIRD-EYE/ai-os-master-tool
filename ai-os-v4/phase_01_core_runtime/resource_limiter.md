---
title: System Resource Limiter Specification
document_id: SPEC-P01-SCHED-028
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Infrastructure & Resource Governance Group
last_updated: 2026-08-05
---

# System Resource Limiter Specification

## Executive Summary
This document specifies the Resource Limiter (`resource_limiter`), enforcing hard cgroup limits (CPU shares, memory bytes, I/O rates, file descriptor caps) on executing agent sub-processes in AI OS v4.

---

## 1. Resource Limiter Architecture

```text
[ AGENT PROCESS ] ──> [ RESOURCE LIMITER (Linux Cgroups v2) ]
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
[ CPU Shares Ceiling ]  [ Memory Limit (4GB) ]  [ Disk I/O Throttling ]
(cgroups cpu.max)       (cgroups memory.max)    (cgroups io.max)
```

---

## 2. Resource Limiter Interface Contract

```typescript
export interface ResourceLimits {
  readonly maxMemoryBytes: number;
  readonly cpuQuotaUs: number;
  readonly cpuPeriodUs: number;
  readonly diskReadBytesPerSec: number;
  readonly diskWriteBytesPerSec: number;
  readonly maxFileDescriptors: number;
}

export interface IResourceLimiter {
  applyLimits(pid: number, limits: ResourceLimits): Promise<void>;
  updateLimits(pid: number, limits: Partial<ResourceLimits>): Promise<void>;
  getUsage(pid: number): Promise<{ memoryBytes: number; cpuUsageUs: number }>;
}
```

---

## 3. Mandatory Limits & Enforcement Rules

1. **OOM Killer Configuration**: Container processes exceeding allocated `maxMemoryBytes` are terminated immediately by Linux OOM killer (`SIGKILL`), emitting `ERR-KERNEL-OOM`.
2. **Disk I/O Rate Capping**: Prevents rogue agents from exhausting host disk bandwidth by enforcing strict read/write byte ceilings (default 50 MB/s).

---

## 4. Verification Protocol

```bash
agy verify-resource-limiter --test-cgroup-limits
```
Applies test limits to synthetic sub-process, attempts memory breach, and verifies kernel OOM signal interception.
