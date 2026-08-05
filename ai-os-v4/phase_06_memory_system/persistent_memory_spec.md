# Persistent Memory Subsystem Specification

> **Subsystem:** Phase 06 — Memory System  
> **Document ID:** SPEC-06-PM-003  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Architecture & Long-Term Storage

Persistent Memory provides durable, cross-session long-term knowledge storage for AI OS v4. It integrates Relational Databases (PostgreSQL for structured metadata), Vector Databases (Qdrant for semantic embeddings), and Property Graph Stores (Neo4j for structural lineage).

```text
                               ┌────────────────────────────────┐
                               │    2PC Memory Transaction      │
                               └───────────────┬────────────────┘
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
    [PostgreSQL Metadata]           [Qdrant Vector Store]        [Neo4j Knowledge Graph]
    (ACID Key-Value & Relational)   (3072-d Dense Embeddings)   (LPG Traversal & Edges)
```

---

## 2. Tiered Storage Architecture

| Storage Tier | Storage Technology | Target Access Latency | Retention Period | Data Types |
| :--- | :--- | :--- | :--- | :--- |
| **Hot Tier** | In-Memory Redis / NVMe SSD | P95 < 5 ms | 1 - 30 days | Active sessions, hot vector cache |
| **Warm Tier** | PostgreSQL + Qdrant Cluster | P95 < 50 ms | 30 - 365 days | Completed task traces, project index |
| **Cold Tier** | AWS S3 / Parquet Storage | P95 < 2.0 sec | Indefinite | Archival logs, historical trajectories |

---

## 3. Data Integrity & 2-Phase Commit (2PC) Protocol

All writes to Persistent Memory covering multiple storage engines MUST execute under the Two-Phase Commit transaction manager:

```text
[Transaction Manager] ──► Prepare (Postgres, Qdrant, Neo4j)
                               │
                      All Ready?
                       ├── YES ──► Commit (Postgres, Qdrant, Neo4j)
                       └── NO  ──► Abort & Rollback All
```

---

## 4. Backup, Disaster Recovery & Replication

- **Replication Factor:** 3x multi-AZ replication.
- **RPO (Recovery Point Objective):** < 5 seconds.
- **RTO (Recovery Time Objective):** < 60 seconds (Automated failover).
- **Snapshot Schedule:** Continuous WAL archiving with automated full daily snapshots.
