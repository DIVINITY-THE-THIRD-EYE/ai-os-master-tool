# Phase 08 — Reflection and Learning
## Specification 08.06: Knowledge Update Pipeline Architecture (`knowledge_update_pipeline.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-06` |
| **Title** | Knowledge Update Pipeline & Enterprise Knowledge Graph Integration |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Knowledge Management & Invariant Governance` |
| **Dependencies** | `SPEC-05-01 (Knowledge Graph)`, `SPEC-06-01 (Memory Policies)`, `ADR-001 (Two-Phase Commit)` |

---

## 1. Executive Summary

The **Knowledge Update Pipeline (KUP)** enforces strict architectural governance over how newly discovered insights, lessons learned, and experience artifacts migrate into the Enterprise Knowledge Graph (EKG) and Long-Term Persistent Memory. In compliance with **Architecture Invariant 1 (No Direct Writes to Knowledge Graph)**, worker agents are strictly prohibited from mutating core knowledge directly. All candidate knowledge items must traverse a 4-stage pipeline: **Candidate Staging $\rightarrow$ Deduplication & Validation $\rightarrow$ Governance Approval $\rightarrow$ Two-Phase Atomic Commit (2PC)**.

---

## 2. Architectural Overview & Workflow Pipeline

```text
+-----------------------+     +-----------------------+     +-----------------------+
| Reflection Engine     |     | Experience Extraction |     | Pattern Detection     |
+-----------+-----------+     +-----------+-----------+     +-----------+-----------+
            |                             |                             |
            +-----------------------------+-----------------------------+
                                          |
                                          v
                        +-----------------+-----------------+
                        |   Stage 1: Candidate Staging      |
                        |   (Candidate Memory Buffer)       |
                        +-----------------+-----------------+
                                          |
                                          v
                        +-----------------+-----------------+
                        | Stage 2: Deduplication & Semantic |
                        | Validation (Embedding Similarity) |
                        +-----------------+-----------------+
                                          |
                                          v
                        +-----------------+-----------------+
                        | Stage 3: Governance & Verification|
                        | Gate (Auto or Human Sign-off)   |
                        +--------+----------------+---------+
                                 |                |
                   +-------------+                +-------------+
                   v                                            v
+------------------+------------------+      +------------------+------------------+
|  Stage 4: Two-Phase Commit (2PC)    |      | Rejection & Feedback Loop       |
|  - Prepare Phase (Lock Graph Nodes) |      | (Notify Originating Agent)      |
|  - Commit Phase (Atomic Mutation)   |      |                                 |
+-------------------------------------+      +---------------------------------+
```

---

## 3. The 4-Stage Invariant Pipeline Specification

### Stage 1: Candidate Staging
- Candidate knowledge items (triplets, guidelines, lessons learned) are submitted by agents via `SubmitCandidateKnowledge()` Kernel API.
- Items are stored in an isolated, immutable `CandidateMemoryStore` with state `STAGED`.

### Stage 2: Deduplication & Semantic Validation
- **Vector Cosine Similarity Check**: Candidate embeddings compared against existing EKG nodes.
  - If Similarity $\ge 0.92$: Flagged as **Duplicate**. Merge candidate metadata; skip graph node creation.
  - If $0.75 \le \text{Similarity} < 0.92$: Flagged as **Contradiction / Conflict Risk**. Trigger Conflict Resolution Engine (`SPEC-07-07`).
  - If Similarity $< 0.75$: Flagged as **Novel Knowledge**. Proceed to Stage 3.

### Stage 3: Governance & Verification Gate
- Automated compliance check against enterprise security, privacy (PII scrubbing), and factual consistency policies.
- Low-impact guidelines auto-approved; architectural changes routed to Domain Authority human queue.

### Stage 4: Two-Phase Commit (2PC) Protocol
In compliance with **ADR-001**, commit adheres to formal 2PC consensus locking:

```text
Coordinator (KUP)                     Participant (EKG Node Store)           Participant (Vector DB Index)
        |                                           |                                      |
        |--- PREPARE (lock target entity nodes) --->|                                      |
        |-------------------------------------------|--- PREPARE (allocate vector slot) -->|
        |<-- VOTE_COMMIT (locks acquired) ----------|                                      |
        |<------------------------------------------|<-- VOTE_COMMIT (slot allocated) -----|
        |                                           |                                      |
   [All Voted YES]                                  |                                      |
        |--- GLOBAL_COMMIT ------------------------>|                                      |
        |-------------------------------------------|--- GLOBAL_COMMIT ------------------->|
        |<-- ACK -----------------------------------|                                      |
        |<------------------------------------------|<-- ACK ------------------------------|
```

---

## 4. Technical Data Structures & Schemas

### 4.1 Candidate Knowledge Packet Interface (TypeScript)

```typescript
export interface CandidateKnowledgePacket {
  candidateId: string; // Format: "CKP-YYYYMMDD-XXXX"
  originatingAgentId: string;
  sourceTaskId: string;
  timestamp: string;
  knowledgeType: 'LESSON_LEARNED' | 'PATTERN' | 'BEST_PRACTICE' | 'FACTUAL_TRIPLET' | 'CODE_SNIPPET';
  contentPayload: {
    subject: string;
    predicate: string;
    object: string;
    contextScope: string[]; // e.g., ["react", "frontend", "state_management"]
    confidenceScore: number; // 0.0 to 1.0
  };
  provenance: {
    inputChecksums: string[];
    reflectionId?: string;
  };
  pipelineStatus: 'STAGED' | 'VALIDATED' | 'APPROVED' | 'COMMITTED' | 'REJECTED';
}
```

### 4.2 Candidate Knowledge Packet Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CandidateKnowledgePacket",
  "type": "object",
  "required": [
    "candidateId",
    "originatingAgentId",
    "sourceTaskId",
    "timestamp",
    "knowledgeType",
    "contentPayload",
    "provenance",
    "pipelineStatus"
  ],
  "properties": {
    "candidateId": { "type": "string", "pattern": "^CKP-[0-9]{8}-[A-Z0-9]{6}$" },
    "originatingAgentId": { "type": "string" },
    "sourceTaskId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "knowledgeType": {
      "type": "string",
      "enum": ["LESSON_LEARNED", "PATTERN", "BEST_PRACTICE", "FACTUAL_TRIPLET", "CODE_SNIPPET"]
    },
    "contentPayload": {
      "type": "object",
      "required": ["subject", "predicate", "object", "confidenceScore"],
      "properties": {
        "subject": { "type": "string" },
        "predicate": { "type": "string" },
        "object": { "type": "string" },
        "confidenceScore": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "provenance": {
      "type": "object",
      "required": ["inputChecksums"],
      "properties": {
        "inputChecksums": { "type": "array", "items": { "type": "string" } },
        "reflectionId": { "type": "string" }
      }
    },
    "pipelineStatus": {
      "type": "string",
      "enum": ["STAGED", "VALIDATED", "APPROVED", "COMMITTED", "REJECTED"]
    }
  }
}
```

---

## 5. System Configuration

```yaml
knowledge_update_pipeline:
  deduplication:
    exact_match_action: "MERGE_METADATA"
    high_similarity_threshold: 0.92
    conflict_similarity_threshold: 0.75
  governance:
    auto_approval_confidence_min: 0.88
    require_human_signoff_for_types: ["CODE_SNIPPET", "FACTUAL_TRIPLET"]
  two_phase_commit:
    lock_timeout_ms: 5000
    retry_attempts: 3
```

---

## 6. Verification & Invariant Audit Criteria

- **Invariant Audit Rule 1**: Scan system codebase and API gateway logs to confirm **0 direct write operations** bypass the KUP pipeline into the Knowledge Graph database.
- **2PC Transaction Atomicity**: Execute forced crash simulation during 2PC Phase 2; verify 100% rollback consistency in state graph and vector database.
