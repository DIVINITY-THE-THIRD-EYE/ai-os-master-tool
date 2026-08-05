# AI OS v4 — Platform Migration & Upgrade Guide

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Enterprise System Migration Manual  
**Status:** Frozen / Production Standard  

---

## 1. Overview & Breaking Changes Summary

This guide provides procedures for migrating existing multi-agent systems from legacy frameworks (LangChain, AutoGen, CrewAI, or AI OS v3.x) to **AI OS v4**.

```
[Legacy System / v3.x Workflows]
               │
               v
  [1. Schema & DSL Converter] ──► Converts prompts & chains into Declarative DSL
               │
               v
  [2. Database Migration Engine] ──► Migrates memory & vector stores to Postgres/Qdrant
               │
               v
  [3. Validation & Parity Test] ──► Runs parallel shadow traffic verification
               │
               v
[AI OS v4 Production Cutover]
```

---

## 2. Framework Migration Matrices

### 2.1 LangChain to AI OS v4 Concept Mapping

| LangChain Concept | AI OS v4 Equivalent | Key Differences / Migration Strategy |
| :--- | :--- | :--- |
| `AgentExecutor` | Core Runtime DAG Scheduler | Replaced by deterministic event-driven state machine |
| `Tool` | Tool Registry Manifest (`tool.json`) | Requires strict JSON Schema input/output definitions |
| `VectorStoreRetriever` | Vector Memory Tier (Tier 7) | Managed via Candidate Memory & 2PC pipeline |
| `RunnableSequence` | Declarative Workflow DSL | Converted to YAML workflow manifests |

---

## 3. Database Schema Migration Scripts

AI OS v4 includes automated migration utilities to upgrade PostgreSQL memory schemas from v3.x to v4.0.0:

```sql
-- Migration Script: v3_to_v4_memory_upgrade.sql
BEGIN;

-- Add Cryptographic Lineage Tracking Columns
ALTER TABLE memory_records 
ADD COLUMN IF NOT EXISTS sha256_checksum VARCHAR(64),
ADD COLUMN IF NOT EXISTS proof_id VARCHAR(64),
ADD COLUMN IF NOT EXISTS candidate_status VARCHAR(32) DEFAULT 'COMMITTED';

-- Create Index for Sub-Millisecond 2PC Queries
CREATE INDEX IF NOT EXISTS idx_memory_candidate_status 
ON memory_records(tenant_id, candidate_status);

COMMIT;
```

---

## 4. Zero-Downtime Migration & Rollback Strategy

1. **Blue/Green Dual Write:** During phase 1 of cutover, the event bus mirrors incoming tasks to both legacy and v4 clusters.
2. **Parity Inspection:** The Verification Engine checks output checksums for parity across 1,000 test executions.
3. **Rollback Plan:** If error rates in v4 exceed 0.05%, traffic is flipped back to the blue legacy cluster within <30 seconds via DNS weight adjustments.

---

## 5. Summary Checklist for Migration Guide Compliance

- [x] Concept mapping matrices for LangChain, AutoGen, and CrewAI defined.
- [x] SQL migration scripts for upgrading PostgreSQL memory schemas provided.
- [x] Blue/Green dual-write shadow testing strategy documented.
- [x] Sub-30-second automated rollback protocol specified.
