# AI OS v4 — Memory Policy Specification

**Document Version:** 4.0.0  
**Phase:** Phase 14 — Runtime Policies  
**Classification:** Core Runtime Memory Governance  
**Status:** Frozen / Production Standard  

---

## 1. Multi-Tier Memory Governance Architecture

The **Memory Policy** dictates the allocation, lifecycle, mutation approval, garbage collection, and persistent storage of information across the 7 memory tiers in AI OS v4.

```
+-----------------------------------------------------------------------------------+
|                            MEMORY TIER ARCHITECTURE                               |
|                                                                                   |
|  [Tier 1: Working Memory]  ──► Fast RAM Scratchpad (Active Task Context)          |
|  [Tier 2: Session Memory]  ──► Redis Cluster Store (User Session Lifecycle)         |
|  [Tier 3: Persistent Mem]  ──► Enterprise PostgreSQL (Stateful Artifacts)          |
|  [Tier 4: Project Memory]   ──► Project Context Graph (Codebases, Architecture)     |
|  [Tier 5: Agent Memory]     ──► Agent Experience Store (Self-Improvement Records)  |
|  [Tier 6: Reflection Mem]  ──► Failure & Root-Cause Logs                          |
|  [Tier 7: Vector Context]  ──► HNSW Embeddings DB (Semantic RAG Search)            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        MEMORY MUTATION APPROVAL PIPELINE                          |
|  Candidate Memory ──► Verification Gate ──► 2PC Commit Engine ──► EKG Store       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Invariant Rule #1: No Direct Writes to Enterprise Knowledge Graph

> **CRITICAL INVARIANT:** Worker Agents MUST NEVER write directly to the Enterprise Knowledge Graph (EKG). All learned facts, code patterns, or architectural updates MUST flow through the Candidate Memory $\rightarrow$ Validation $\rightarrow$ Approval Gate $\rightarrow$ Commit pipeline.

```
[Worker Agent Output]
         │
         v
[Candidate Memory Buffer]
         │
         v
[Automated Verification Engine] (Consistency & Schema Check)
         │
         v
[Domain Lead / HITL Approval]
         │
         v
[Two-Phase Commit (2PC) Engine]
         │
         v
[Enterprise Knowledge Graph (EKG)]
```

---

## 3. Two-Phase Commit (2PC) Memory Consistency Protocol

To prevent state corruption across distributed memory nodes, mutations touching persistent memory and vector indices use a lightweight Two-Phase Commit protocol:

```
Coordinator (Kernel Memory Engine)               Participants (Postgres / Redis / HNSW)
               │                                                │
               ├────────────── 1. PREPARE(TxID) ───────────────►│
               │                                                │ (Locks Resources)
               │◄───────────── VOTE_COMMIT / ABORT ─────────────┤
               │                                                │
       [Evaluate Votes]                                         │
               │                                                │
               ├───────────── 2. GLOBAL_COMMIT(TxID) ──────────►│
               │                                                │ (Applies Write & Unlocks)
               │◄────────────── ACK_COMMITTED ──────────────────┤
```

---

## 4. Memory Policy Configuration Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MemoryPolicySpecification",
  "type": "object",
  "required": [
    "policy_id",
    "max_working_memory_tokens",
    "context_compression_threshold_tokens",
    "ephemeral_ttl_seconds",
    "two_phase_commit_required",
    "vector_similarity_threshold"
  ],
  "properties": {
    "policy_id": { "type": "string" },
    "max_working_memory_tokens": { "type": "integer", "default": 128000 },
    "context_compression_threshold_tokens": { "type": "integer", "default": 96000 },
    "ephemeral_ttl_seconds": { "type": "integer", "default": 86400 },
    "two_phase_commit_required": { "type": "boolean", "default": true },
    "vector_similarity_threshold": { "type": "number", "default": 0.82 },
    "gc_compaction_cron": { "type": "string", "default": "0 */4 * * *" }
  }
}
```

---

## 5. Memory Compression & Garbage Collection Rules

1. **Context Compression Trigger:** When working memory tokens exceed `context_compression_threshold_tokens` (96,000 tokens), the runtime invokes the Context Compression Engine to summarize historical dialogue while retaining strict JSON structural constraints.
2. **Garbage Collection (GC):** Ephemeral working memory scratchpads are unmounted and purged immediately upon task state transitioning to `COMPLETED` or `FAILED`.
3. **Persisted Vector Compaction:** Vector databases undergo nightly HNSW graph re-indexing and duplicate key compaction.

---

## 6. Summary Checklist for Memory Policy Compliance

- [x] 7-tier memory architecture specified.
- [x] Invariant Rule #1 (Candidate Memory pipeline to EKG) enforced.
- [x] Two-Phase Commit (2PC) memory mutation protocol detailed.
- [x] Declarative JSON schema for memory policies defined.
- [x] Context compression thresholds and automated GC rules locked.
