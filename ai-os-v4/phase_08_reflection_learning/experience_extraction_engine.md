# Phase 08 — Reflection and Learning
## Specification 08.07: Experience Extraction Engine Architecture (`experience_extraction_engine.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-07` |
| **Title** | Experience Extraction Engine & Memory Distillation |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Memory Distillation & CBR` |
| **Dependencies** | `SPEC-06-01 (Working Memory)`, `SPEC-06-03 (Persistent Memory)`, `SPEC-08-01 (Reflection Engine)` |

---

## 1. Executive Summary

The **Experience Extraction Engine (EEE)** processes raw, high-volume episodic execution traces from Working Memory and distills them into compact, high-value **Semantic Experience Cards**. Operating on Case-Based Reasoning (CBR) principles, the EEE indexes problem-solution-outcome triplets, compresses long conversation histories, and embeds reusable execution trajectories into the Case-Based Reasoning Vector Store. This enables agents to retrieve past successful strategies when encountering similar task goals in future execution sessions.

---

## 2. Architectural Overview & Distillation Workflow

```text
                  +----------------------------------------------+
                  | Working / Session Memory (Raw Execution Trace)|
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Trajectory Summarizer & Token Compressor     |
                  | (Reduces raw trace by 80-90% token volume)   |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Case-Based Reasoning (CBR) Distiller        |
                  |  (Extracts Problem, Solution, Outcome)        |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Vector Indexer & Meta-Tagging Pipeline       |
                  | (Generates 1536-dim Task Context Embeddings) |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Case-Based Reasoning Store (`phase_05_...`) |
                  +----------------------------------------------+
```

---

## 3. Distillation Architecture & Case-Based Reasoning (CBR)

The CBR distillation model extracts four structural components from every task trajectory:

1. **Problem Context ($P$)**: The initial task request, ambient parameters, constraints, and environment preconditions.
2. **Solution Strategy ($S$)**: The sequence of high-level sub-goals, chosen agent tools, and decision branches.
3. **Outcome ($O$)**: The produced artifacts, verification score, execution time, and total token cost.
4. **Distilled Lesson ($L$)**: Key takeaway detailing why the strategy succeeded or failed, and key caveats for reuse.

---

## 4. Technical Data Structures & Schemas

### 4.1 Experience Card Interface (TypeScript)

```typescript
export interface ExperienceCard {
  experienceId: string; // Format: "EXP-YYYYMMDD-XXXX"
  domainCategory: string; // e.g., "software_development/react"
  taskSignature: string; // Natural language summary of task objective
  problemContext: {
    goalDescription: string;
    keyConstraints: string[];
    environmentVariables: Record<string, string>;
  };
  solutionStrategy: {
    stepsSummary: string[];
    keyToolsUsed: string[];
    criticalDecisions: Array<{
      decisionPoint: string;
      chosenOption: string;
      reasoning: string;
    }>;
  };
  outcome: {
    verificationScore: number; // 0.0 to 1.0
    executionTimeMs: number;
    tokenCostUsd: number;
    artifactChecksums: string[];
  };
  distilledLessons: string[];
  embeddingVector: number[]; // 1536-dimensional embedding
  accessFrequency: number;
  lastRetrievedTimestamp?: string;
}
```

### 4.2 Experience Card Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExperienceCard",
  "type": "object",
  "required": [
    "experienceId",
    "domainCategory",
    "taskSignature",
    "problemContext",
    "solutionStrategy",
    "outcome",
    "distilledLessons",
    "embeddingVector",
    "accessFrequency"
  ],
  "properties": {
    "experienceId": { "type": "string", "pattern": "^EXP-[0-9]{8}-[A-Z0-9]{6}$" },
    "domainCategory": { "type": "string" },
    "taskSignature": { "type": "string" },
    "problemContext": {
      "type": "object",
      "required": ["goalDescription", "keyConstraints"],
      "properties": {
        "goalDescription": { "type": "string" },
        "keyConstraints": { "type": "array", "items": { "type": "string" } }
      }
    },
    "solutionStrategy": {
      "type": "object",
      "required": ["stepsSummary", "keyToolsUsed"],
      "properties": {
        "stepsSummary": { "type": "array", "items": { "type": "string" } },
        "keyToolsUsed": { "type": "array", "items": { "type": "string" } }
      }
    },
    "outcome": {
      "type": "object",
      "required": ["verificationScore", "executionTimeMs", "tokenCostUsd"],
      "properties": {
        "verificationScore": { "type": "number", "minimum": 0, "maximum": 1 },
        "executionTimeMs": { "type": "number" },
        "tokenCostUsd": { "type": "number" }
      }
    },
    "distilledLessons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "embeddingVector": {
      "type": "array",
      "items": { "type": "number" },
      "minItems": 1536,
      "maxItems": 1536
    },
    "accessFrequency": { "type": "integer", "minimum": 0 }
  }
}
```

---

## 5. Experience Retrieval API

```typescript
export interface ExperienceRetrievalQuery {
  currentGoalDescription: string;
  domainCategory: string;
  maxResults?: number; // Default: 3
  minVerificationScore?: number; // Default: 0.80
}

export interface ExperienceRetrievalResponse {
  queryId: string;
  matches: Array<{
    experienceCard: ExperienceCard;
    similarityScore: number; // Cosine similarity 0.0 to 1.0
  }>;
}
```

---

## 6. Compression & Eviction Policy

- **Compression Ratio Target**: Distillation must achieve at least an 85% reduction in total token representation compared to raw trace logs.
- **Eviction Protocol**: Low-utility experience cards (`accessFrequency == 0` after 30 days AND `verificationScore < 0.70`) are compressed into cold archival storage and purged from the vector index.

---

## 7. Verification & Quality Criteria

- **Semantic Relevance**: Vector search precision @ Top-3 matches across benchmark test queries $\ge 90\%$.
- **Distillation Integrity**: 100% of generated Experience Cards must contain non-empty `distilledLessons` and valid 1536-dimensional embeddings.
