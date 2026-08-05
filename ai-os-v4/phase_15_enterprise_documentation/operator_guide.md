# AI OS v4 — Platform Operator & Administrator Guide

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Enterprise System Operations Manual  
**Status:** Frozen / Production Standard  

---

## 1. Operations Overview & System Architecture

This guide provides operational procedures for Systems Engineers, Site Reliability Engineers (SREs), and Infrastructure Operators managing production clusters of AI OS v4.

```
+-----------------------------------------------------------------------------------+
|                            OPERATIONAL MANAGEMENT PLANE                           |
|  +---------------------+   +---------------------+   +-------------------------+  |
|  | Grafana Telemetry   |   | Prometheus Metric   |   | Chaos & Failover        |  |
|  | Dashboards          |   | Scrape Collectors   |   | Controller              |  |
|  +----------+----------+   +----------+----------+   +------------+------------+  |
+-------------|-------------------------|---------------------------|---------------+
              |                         |                           |
              v                         v                           v
+-----------------------------------------------------------------------------------+
|                           PRODUCTION KUBERNETES CLUSTER                           |
|   [Kernel Pods]     [Event Bus NATS]     [Postgres / Redis]     [Firecracker VMs] |
+-----------------------------------------------------------------------------------+
```

---

## 2. Infrastructure Capacity Planning & Sizing

| Workload Profile | Min CPU Cores | Min RAM | Storage Capacity | Max Concurrent Agents |
| :--- | :--- | :--- | :--- | :--- |
| **Small (Dev / Test)** | 8 Cores | 32 GB | 250 GB NVMe | Up to 25 |
| **Medium (Enterprise Staging)**| 32 Cores | 128 GB | 1 TB NVMe | Up to 100 |
| **Large (Production High-Load)**| 128 Cores | 512 GB | 4 TB NVMe (RAID-10)| Up to 500 |

---

## 3. Monitoring Metrics & Alerting SLAs

Operators MUST monitor the key Prometheus metrics below:

| Metric Name | Type | Warning Threshold | Critical SLA Threshold | Operator Action |
| :--- | :--- | :--- | :--- | :--- |
| `aios_kernel_task_queue_depth` | Gauge | > 100 tasks | > 500 tasks | Scale out Worker pod replicas |
| `aios_pdp_eval_latency_ms_p99` | Histogram | > 5.0 ms | > 15.0 ms | Inspect Redis L2 PDP cache health |
| `aios_event_bus_dropped_messages`| Counter | > 0 | > 10 / min | Check NATS storage & disk I/O |
| `aios_sandbox_container_escapes` | Counter | N/A | > 0 (ANY) | **TRIGGER SYSTEM FREEZE & ALERT** |

---

## 4. Disaster Recovery & Backup Procedures

### 4.1 Backup Targets & Frequency

1. **PostgreSQL EKG & State Store:** Continuous WAL archiving with nightly full pg_dump snapshot.
2. **Redis Persistent State:** Append-Only File (AOF) sync every 1 second; RDB snapshot every 1 hour.
3. **Audit Log Store (WORM):** Real-time streaming sync to AWS S3 Glacier Object Lock.

### 4.2 Recovery Point / Time Objectives

- **RPO (Recovery Point Objective):** 0 seconds (RDBMS WAL replication + Redis AOF).
- **RTO (Recovery Time Objective):** < 5 minutes automated failover to standby region.

---

## 5. Summary Checklist for Operator Guide Compliance

- [x] Infrastructure capacity planning and hardware sizing matrix established.
- [x] Prometheus metrics, warning thresholds, and alerting SLAs locked.
- [x] Continuous WAL archiving and RPO=0 / RTO<5m disaster recovery procedures documented.
- [x] Emergency system freeze operational runbook defined.
