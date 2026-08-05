---
title: System Health Checker Specification
document_id: SPEC-P01-SAFE-035
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Platform Reliability Group
last_updated: 2026-08-05
---

# System Health Checker Specification

## Executive Summary
This document specifies the Health Checker (`health_checker`), providing liveness (`/healthz/liveness`), readiness (`/healthz/readiness`), and startup probe endpoints, dependency ping probes, node status reporting, and automatic node isolation in AI OS v4.

---

## 1. Health Checker Probe Architecture

```text
[ KUBERNETES / LOAD BALANCER ]
         │
         ├── GET /healthz/liveness   ──> Is process event loop responsive? (HTTP 200)
         ├── GET /healthz/readiness  ──> Are dependencies (Broker, DB, Vector) connected? (HTTP 200)
         └── GET /healthz/startup    ──> Has bootstrap initialization completed? (HTTP 200)
         │
         ▼
+-----------------------------------------------------------------+
| HEALTH CHECKER SUBSYSTEM PROBER                                 |
|  - Broker Ping (NATS / Kafka)                                   |
|  - Storage Ping (Redis / PostgreSQL)                            |
|  - Memory & Disk Threshold Checker                              |
+-----------------------------------------------------------------+
```

---

## 2. Health Checker Schema & Interface Contract

```typescript
export interface SubsystemHealthStatus {
  readonly subsystemName: string;
  readonly status: "HEALTHY" | "DEGRADED" | "UNHEALTHY";
  readonly latencyMs: number;
  readonly details?: Record<string, unknown>;
}

export interface SystemHealthReport {
  readonly overallStatus: "HEALTHY" | "DEGRADED" | "UNHEALTHY";
  readonly nodeVersion: string;
  readonly uptimeSeconds: number;
  readonly subsystems: Record<string, SubsystemHealthStatus>;
  readonly timestamp: string;
}

export interface IHealthChecker {
  registerSubsystemCheck(name: string, checkFn: () => Promise<SubsystemHealthStatus>): void;
  getLiveness(): Promise<boolean>;
  getReadiness(): Promise<SystemHealthReport>;
}
```

---

## 3. Probe Failure & Node Isolation Rules

1. **Readiness Probe Failure**: If a critical subsystem (e.g. Message Broker) remains `UNHEALTHY` for 3 consecutive probes (15s), readiness returns HTTP 503, removing the node from service traffic.
2. **Liveness Probe Failure**: If the main thread event loop blocks for > 30s, liveness probe fails, triggering container orchestrator restart.

---

## 4. Verification Protocol

```bash
agy verify-health-checker --test-probes
```
Executes synthetic liveness, readiness, and startup probes, simulates dependency timeouts, and verifies HTTP status codes.
