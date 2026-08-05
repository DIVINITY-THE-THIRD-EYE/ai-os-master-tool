# System Data & Application Migration Plan: {{MIGRATION_PROJECT_NAME}}

> **Document Type**: Migration Execution Strategy  
> **Status**: {{DOCUMENT_STATUS}}  
> **Migration Lead**: {{MIGRATION_LEAD}}  
> **Source Platform**: {{SOURCE_PLATFORM}}  
> **Target Platform**: {{TARGET_PLATFORM}}  
> **Planned Migration Date**: {{PLANNED_MIGRATION_DATE}}  
> **Estimated Maintenance Window**: {{ESTIMATED_WINDOW_HOURS}} Hours  

---

## 1. Executive Summary & Migration Objectives

### 1.1 Overview
*Instruction: Detail the migration objectives, legacy systems being retired, target environment, and cutover strategy (Big Bang vs Phased/Dual-Write).*

---

## 2. Pre-Migration Prerequisites & Readiness

- [ ] Complete full cold backup of legacy database `{{SOURCE_DB_NAME}}`.
- [ ] Schema DDL pre-created on target cluster `{{TARGET_DB_NAME}}`.
- [ ] Data validation scripts staged and tested on synthetic dataset.
- [ ] Network firewall rules opened between Source and Target subnet (`Port {{DB_PORT}}`).

---

## 3. Migration Phasing & Step-by-Step Cutover

```
Phase 1: Initial Bulk Copy ---> Phase 2: CDC Sync ---> Phase 3: Validation ---> Phase 4: DNS Cutover
```

| Phase | Task Description | Executed By | Estimated Time | Success Verification |
| :--- | :--- | :--- | :--- | :--- |
| Phase 1 | Bulk export/import of historical data | Data Ops | 2 Hours | Row count match within 0.01% |
| Phase 2 | Start Change Data Capture (CDC) replication | Data Ops | 1 Hour | CDC replication lag < 100ms |
| Phase 3 | Stop writes to legacy DB & freeze apps | Systems Team | 15 Mins | Application write locks verified |
| Phase 4 | Final CDC catch-up & checksum validation | Data Ops | 15 Mins | Table checksum hash matches 100% |
| Phase 5 | Switch application connection strings to Target | DevOps | 15 Mins | Target DB receiving active traffic |

---

## 4. Reconciliation & Data Validation Plan

Run automated verification queries:
```sql
-- Row Count Verification
SELECT COUNT(*) FROM {{SOURCE_TABLE}};
SELECT COUNT(*) FROM {{TARGET_TABLE}};

-- Hash Checksum Verification
SELECT MD5(BIT_XOR(CAST(id AS INT))) FROM {{SOURCE_TABLE}};
```

---

## 5. Rollback Strategy & Abort Criteria

### 5.1 Abort Criteria
If any of the following occur during cutover window:
- Data reconciliation checksum failure > 0%.
- Target cluster performance latency > {{MAX_ALLOWED_LATENCY_MS}} ms.
- Migration execution exceeds {{MAX_WINDOW_HOURS}} hours.

### 5.2 Rollback Steps
1. Re-enable writes on Legacy Database `{{SOURCE_DB_NAME}}`.
2. Revert DNS traffic back to Legacy API Gateway IP.
3. Post cancellation notice in `#migration-war-room`.
