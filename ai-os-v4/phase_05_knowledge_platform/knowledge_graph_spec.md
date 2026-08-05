# Enterprise Knowledge Graph Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-KG-001  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Core Invariants

The Enterprise Knowledge Graph (EKG) serves as the centralized, authoritative semantic knowledge backbone for AI OS v4. It stores structured relationships between system domains, architectural patterns, reusable components, technical requirements, business constraints, and agent execution experiences.

### Non-Negotiable Invariants
1. **No Direct Writes by Worker Agents:** Worker Agents MUST NEVER write directly to the active Enterprise Knowledge Graph. All candidate knowledge modifications MUST be submitted to Candidate Memory and pass through the Candidate Validation Pipeline, Automated Policy Verification, and Domain Authority Approval prior to committing.
2. **Deterministic Provenance Tracking:** Every node and edge in the graph MUST store cryptographic provenance metadata including authoring agent ID, task ID, source artifact hash, confidence rating, and commit timestamp.
3. **Strict Ontology Conformance:** All entities and relationships added to the graph MUST strictly conform to the schemas defined in `enterprise_ontology.md`. Non-conforming triples are rejected at the validation gate (`ERR-4004`).
4. **Idempotent Graph Commits:** Graph update transactions MUST be idempotent. Re-applying the same candidate graph patch must yield an identical graph topology without duplicate nodes or orphaned edges.

---

## 2. Graph Data Model & Schema

The EKG is modeled as a Labelled Property Graph (LPG) backed by RDF triple semantics where necessary for formal reasoning.

```text
  ┌─────────────────┐       DEPENDS_ON       ┌─────────────────┐
  │  Requirement    ├───────────────────────►│    Component    │
  └────────┬────────┘                        └────────┬────────┘
           │                                          │
           │ SATISFIES                                │ IMPLEMENTS
           ▼                                          ▼
  ┌─────────────────┐       SUPERCEDES       ┌─────────────────┐
  │    Decision     ├───────────────────────►│    Pattern      │
  └─────────────────┘                        └─────────────────┘
```

### Core Entity Types (Nodes)

| Node Label | Description | Mandatory Properties |
| :--- | :--- | :--- |
| `Domain` | Functional or technical boundary | `id`, `name`, `owner_authority`, `created_at` |
| `Concept` | Abstract technical or domain concept | `id`, `name`, `definition`, `domain_id`, `tags` |
| `Requirement` | Functional or non-functional constraint | `id`, `title`, `specification`, `priority`, `status` |
| `Component` | Implementation artifact or module | `id`, `name`, `repository_path`, `version`, `tech_stack` |
| `Decision` | Architectural decision record entry | `id`, `adr_id`, `title`, `status`, `consequences` |
| `Pattern` | Standardized engineering/architectural pattern | `id`, `name`, `category`, `structure_dsl` |
| `Experience` | Consolidated historical task trajectory | `id`, `task_id`, `outcome_score`, `execution_time_ms` |

### Core Relationship Types (Edges)

| Edge Type | Source Label | Target Label | Semantics |
| :--- | :--- | :--- | :--- |
| `DEPENDS_ON` | `Component` \| `Requirement` | `Component` \| `Requirement` | Target is required for Source execution |
| `IMPLEMENTS` | `Component` | `Pattern` \| `Requirement` | Component realizes design pattern or requirement |
| `SATISFIES` | `Decision` \| `Component` | `Requirement` | Decision or Component satisfies business/tech requirement |
| `DERIVED_FROM` | `Concept` \| `Requirement` | `Concept` \| `Experience` | Lineage tracking from prior knowledge/experience |
| `SUPERCEDES` | `Decision` \| `Pattern` | `Decision` \| `Pattern` | Replaces an older decision or pattern version |
| `BELONGS_TO` | `Concept` \| `Component` | `Domain` | Domain ownership boundary |

---

## 3. Storage Architecture & Indexing Strategy

### Dual-Database Backend Strategy
- **Graph Engine:** Neo4j Enterprise Cluster / AWS Neptune (Property Graph for high-speed multi-hop traversal).
- **Metadata & Vector Index:** Qdrant / Milvus (Vector embeddings of node definitions for semantic neighborhood matching).

### Graph Indexing Specifications

```cypher
// Core Indexing Rules for Neo4j Engine
CREATE CONSTRAINT constraint_requirement_id IF NOT EXISTS FOR (r:Requirement) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT constraint_component_id IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT constraint_decision_id IF NOT EXISTS FOR (d:Decision) REQUIRE d.id IS UNIQUE;

CREATE INDEX idx_component_tech_stack IF NOT EXISTS FOR (c:Component) ON (c.tech_stack);
CREATE INDEX idx_node_provenance IF NOT EXISTS FOR (n:Entity) ON (n.author_agent_id, n.commit_tx_id);
CREATE FULLTEXT INDEX ft_concept_search IF NOT EXISTS FOR (n:Concept|Requirement) ON EACH [n.name, n.definition, n.specification];
```

---

## 4. Candidate Validation & Commit Pipeline

Knowledge updates follow a formal 2-Phase Commit (2PC) transaction pipeline to preserve graph integrity.

```text
[Worker Agent] ──► Submits Candidate Graph Patch ──► [Candidate Memory Store]
                                                              │
                                                              ▼
                                                 [Graph Validation Engine]
                                                 ├── SHACL Schema Check
                                                 ├── Invariant Verification
                                                 └── Cycle / Anomaly Scan
                                                              │
                                                     Passed   │
                                             ┌────────────────┴────────────────┐
                                             ▼                                 ▼
                                   [Auto-Approved]                   [Escalated to Authority]
                                   (Low Risk Delta)                  (High Impact Delta)
                                             │                                 │
                                             └────────────────┬────────────────┘
                                                              │ Approved
                                                              ▼
                                                   [2PC Graph Commit Engine]
                                                   ├── Lock Target Nodes
                                                   ├── Apply Cypher Delta Patch
                                                   └── Sync Vector Index
```

---

## 5. Graph Traversal & Query APIs

### Cypher Query API Contract (gRPC / REST)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GraphTraversalRequest",
  "type": "object", "properties": {
    "start_node_id": { "type": "string" },
    "max_depth": { "type": "integer", "minimum": 1, "maximum": 5 },
    "edge_types": { "type": "array", "items": { "type": "string" } },
    "direction": { "type": "string", "enum": ["OUTGOING", "INCOMING", "BOTH"] },
    "filters": {
      "type": "object",
      "properties": {
        "min_confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
      }
    }
  },
  "required": ["start_node_id", "max_depth"]
}
```

### Example Cypher Impact Analysis Query

```cypher
// Impact Analysis: Find all components and requirements affected by modifying target Requirement
MATCH path = (start:Requirement {id: $req_id})<-[:DEPENDS_ON|SATISFIES*1..4]-(affected)
RETURN 
  start.id AS source_requirement,
  affected.id AS affected_entity_id,
  labels(affected) AS entity_type,
  length(path) AS blast_radius_distance
ORDER BY blast_radius_distance ASC;
```

---

## 6. Capacity Limits, Performance & Operational Metrics

- **Max Edge Capacity:** 1,000,000,000 active edges across platform tenants.
- **Query Latency SLA:**
  - 1-hop lookup: P95 < 20 ms
  - 3-hop graph traversal: P95 < 180 ms
  - Complex pattern traversal (k-hop <= 5): P95 < 450 ms
- **Graph Replication Factor:** Minimum 3 nodes (1 Primary Writer, 2 Read Replicas).
- **Automated Quarantine:** Any update causing cycle in strict DAG structures (e.g. `DEPENDS_ON` for modules) triggers `ERR-3003` and quarantines the transaction.
