# Semantic Search Engine Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-SSE-002  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. Subsystem Architecture & Multi-Stage Retrieval

The Semantic Search Engine provides hybrid dense-sparse vector retrieval across system documentation, code artifacts, memory logs, decision records, and pattern libraries.

```text
[User / Agent Query] ──► [Query Preprocessor & Ontology Expansion]
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        [Sparse Index Search (BM25)]          [Dense Vector Search (HNSW)]
        (Keyword & Token Matching)           (Semantic Embedding Cosine)
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       ▼
                       [Reciprocal Rank Fusion (RRF)]
                                       │
                                       ▼
                      [Cross-Encoder Reranking Model]
                                       │
                                       ▼
                     [Filtered & Ranked Search Results]
```

---

## 2. Vector Index & Dense/Sparse Configuration

### Embedding Model Specs
- **Dense Embedding Model:** `text-embedding-3-large` (3072 dimensions) / Domain fine-tuned BGE-large-en-v1.5.
- **Sparse Indexing Model:** SPLADE v2 / BM25 token frequency index.
- **Distance Metric:** Cosine Similarity (`1.0 - dot_product`).
- **Vector DB Store:** Qdrant Enterprise / Milvus v2.4.

### HNSW Index Configuration

```json
{
  "vector_dimensions": 3072,
  "distance_metric": "Cosine",
  "hnsw_config": {
    "m": 16,
    "ef_construct": 200,
    "full_scan_threshold": 10000,
    "max_indexing_threads": 8
  },
  "optimizers_config": {
    "deleted_threshold": 0.2,
    "vacuum_min_vector_number": 1000,
    "indexing_threshold": 20000
  }
}
```

---

## 3. Document Chunking & Ingestion Pipeline

### Chunking Strategies
1. **Source Code Files:** Tree-Sitter AST-aware chunking (preserves full class, method, or function boundaries with docstrings).
2. **Markdown & Specifications:** Structural header chunking (splits on H2/H3 headers, preserves context path header breadcrumbs).
3. **Logs & Memory Traces:** Windowed sliding chunking (512 tokens with 64-token overlap).

### Ingestion Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "IngestedDocumentChunk",
  "type": "object",
  "properties": {
    "chunk_id": { "type": "string" },
    "source_file_path": { "type": "string" },
    "domain": { "type": "string" },
    "content": { "type": "string" },
    "content_hash": { "type": "string" },
    "metadata": {
      "type": "object",
      "properties": {
        "author_agent": { "type": "string" },
        "language": { "type": "string" },
        "security_classification": { "type": "string" },
        "created_at": { "type": "string", "format": "date-time" }
      }
    },
    "dense_vector": {
      "type": "array",
      "items": { "type": "number" }
    }
  },
  "required": ["chunk_id", "source_file_path", "content", "dense_vector"]
}
```

---

## 4. Query Expansion & Multi-Stage Reranking

### Stage 1: Ontology Context Expansion
Queries are expanded using the Enterprise Ontology (`enterprise_ontology.md`). Synonyms, parent concepts, and related tech stack terms are injected into the search query payload.

### Stage 2: Reciprocal Rank Fusion (RRF)
Combines BM25 sparse results and HNSW dense results:

$$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where $k = 60$, $M = \{BM25, HNSW\}$, and $r_m(d)$ is the rank position of document $d$ in method $m$.

### Stage 3: Cross-Encoder Reranking
Top 50 candidate documents from RRF are fed into a lightweight Cross-Encoder model (`bge-reranker-large`) to produce the final top-k reranked results.

---

## 5. API Contracts & SDK Interfaces

### REST / gRPC Search API Endpoint

```json
{
  "query": "Find microservice retry circuit breaker patterns for gRPC endpoints",
  "domain_filter": "backend_services",
  "top_k": 5,
  "score_threshold": 0.72,
  "hybrid_weights": {
    "dense": 0.65,
    "sparse": 0.35
  },
  "rerank": true
}
```

### Search Response Format

```json
{
  "total_hits": 42,
  "execution_time_ms": 38.5,
  "results": [
    {
      "chunk_id": "chk_88192a_003",
      "score": 0.941,
      "source_file_path": "phase_05_knowledge_platform/pattern_library.md",
      "content": "## Circuit Breaker & Retry Strategy for gRPC Communication...",
      "metadata": {
        "author_agent": "arch_agent_01",
        "security_classification": "INTERNAL"
      }
    }
  ]
}
```

---

## 6. Performance Benchmarks & SLAs

- **Index Freshness:** Incremental ingestion via Kafka event stream within < 500 ms of artifact update.
- **Latency Budgets:**
  - Sparse BM25 Search: P95 < 25 ms
  - Dense HNSW Vector Search: P95 < 45 ms
  - Cross-Encoder Reranking (top 50): P95 < 80 ms
  - End-to-End Hybrid Search Latency: P95 < 150 ms
- **Recall Target:** MRR@10 > 0.88, Recall@20 > 0.94 across platform benchmark queries.
