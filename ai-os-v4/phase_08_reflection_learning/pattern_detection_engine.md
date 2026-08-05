# Phase 08 — Reflection and Learning
## Specification 08.05: Pattern Detection Engine Architecture (`pattern_detection_engine.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-05` |
| **Title** | Pattern Detection Engine & Execution Trajectory Mining |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Pattern Mining & Analytics` |
| **Dependencies** | `SPEC-01-02 (Message Broker)`, `SPEC-05-09 (Pattern Library)`, `SPEC-08-01 (Reflection Engine)` |

---

## 1. Executive Summary

The **Pattern Detection Engine (PDE)** continuously analyzes multi-agent execution traces, tool invocation streams, and system event logs to discover recurring behavioural patterns across the AI OS enterprise environment. The engine extracts both **Anti-Patterns** (repetitive failure sequences, inefficient tool loops, redundant context passing) and **Success Patterns** (high-efficiency task workflows, optimal agent delegation chains). Discovered patterns are indexed in the global Pattern Library (`phase_05_knowledge_platform/pattern_library.md`) and ingested by the Workflow Optimization Engine for systemic graph tuning.

---

## 2. Architectural Overview & Mining Pipeline

```text
                  +----------------------------------------------+
                  | Event Bus Stream / Trajectory Log Collector  |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Sequence Normalizer & Tokenizer Engine      |
                  | (Converts tool calls/states into canonical   |
                  |  sequence tokens: e.g., A->B->T1->A)         |
                  +----------------------+-----------------------+
                                         |
                                         v
+----------------------------------------+----------------------------------------+
|                                        |                                        |
v                                        v                                        v
+-----------------------+  +-----------------------+  +-----------------------+
| PrefixSpan Sequential  |  | Apriori Frequent Item |  | Statistical Anomaly   |
| Pattern Mining        |  | Set Mining            |  | Detector (Z-Score)    |
+-----------------------+  +-----------------------+  +-----------------------+
|                                        |                                        |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Pattern Classifier & Significance Evaluator  |
                  | (Calculates Support, Confidence, Lift)       |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Pattern Catalog Update & Alert Dispatch     |
                  +----------------------------------------------+
```

---

## 3. Pattern Mining Algorithms & Metrics

### 3.1 Support, Confidence & Lift Metrics

For a candidate execution sequence $S = (e_1, e_2, \dots, e_k) \rightarrow Y$:

- **Support ($Supp(S)$)**:
  $$Supp(S) = \frac{\text{Number of Trajectories Containing } S}{\text{Total Trajectories Analyzed}}$$
- **Confidence ($Conf(S \rightarrow Y)$)**:
  $$Conf(S \rightarrow Y) = \frac{Supp(S \cup Y)}{Supp(S)}$$
- **Lift ($Lift(S \rightarrow Y)$)**:
  $$Lift(S \rightarrow Y) = \frac{Conf(S \rightarrow Y)}{Supp(Y)}$$

A sequence is classified as a **Systemic Anti-Pattern** if $Supp(S) \ge 0.05$, $Conf(S \rightarrow \text{FAILURE}) \ge 0.70$, and $Lift \ge 1.5$.

---

## 4. Technical Data Structures & Schemas

### 4.1 Detected Pattern Record Interface (TypeScript)

```typescript
export interface DetectedPatternRecord {
  patternId: string; // Format: "PAT-YYYYMMDD-XXXX"
  patternType: 'ANTI_PATTERN' | 'SUCCESS_PATTERN' | 'ANOMALY';
  title: string;
  sequenceTokens: string[]; // e.g., ["AGENT_INIT", "TOOL_BASH_EXEC", "TOOL_BASH_EXEC", "RETRY_LOOP"]
  metrics: {
    support: number;
    confidence: number;
    lift: number;
    occurrenceCount: number;
    timeWindowHours: number;
  };
  impact: {
    averageLatencyImpactMs: number;
    averageTokenCostImpactUsd: number;
    failureProbability: number;
  };
  recommendedMitigation?: string;
  catalogStatus: 'CANDIDATE' | 'VERIFIED' | 'COMMITTED';
}
```

### 4.2 Pattern Detection Event Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DetectedPatternRecord",
  "type": "object",
  "required": [
    "patternId",
    "patternType",
    "title",
    "sequenceTokens",
    "metrics",
    "impact",
    "catalogStatus"
  ],
  "properties": {
    "patternId": { "type": "string", "pattern": "^PAT-[0-9]{8}-[A-Z0-9]{6}$" },
    "patternType": { "type": "string", "enum": ["ANTI_PATTERN", "SUCCESS_PATTERN", "ANOMALY"] },
    "title": { "type": "string" },
    "sequenceTokens": {
      "type": "array",
      "items": { "type": "string" }
    },
    "metrics": {
      "type": "object",
      "required": ["support", "confidence", "lift", "occurrenceCount"],
      "properties": {
        "support": { "type": "number", "minimum": 0, "maximum": 1 },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "lift": { "type": "number" },
        "occurrenceCount": { "type": "integer" }
      }
    },
    "impact": {
      "type": "object",
      "required": ["averageLatencyImpactMs", "failureProbability"],
      "properties": {
        "averageLatencyImpactMs": { "type": "number" },
        "failureProbability": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "catalogStatus": { "type": "string", "enum": ["CANDIDATE", "VERIFIED", "COMMITTED"] }
  }
}
```

---

## 5. Standard Catalog of Detectable Patterns

| Pattern Code | Type | Pattern Sequence Signature | Default Threshold & Action |
| :--- | :--- | :--- | :--- |
| `PAT-AP-001` | **Anti-Pattern** | `TOOL_EXEC` $\rightarrow$ `ERR_JSON` $\rightarrow$ `RETRY_SAME_PROMPT` $\rightarrow$ `ERR_JSON` | **Ping-Pong Failure Loop**: Detects agent repeating identical failing tool calls without parameter adjustment. Trigger circuit breaker. |
| `PAT-AP-002` | **Anti-Pattern** | `DELEGATE_AGENT_A` $\rightarrow$ `DELEGATE_AGENT_B` $\rightarrow$ `DELEGATE_AGENT_A` | **Circular Delegation Ping-Pong**: Agents passing task back and forth without progress. Abort & escalate. |
| `PAT-SP-001` | **Success Pattern** | `PROMPT_FEW_SHOT` $\rightarrow$ `AST_CHECK` $\rightarrow$ `COMPILE` | **Pre-Flight Verification**: Highly reliable code generation flow. Auto-promote to default workflow. |

---

## 6. Subsystem Configuration

```yaml
pattern_detection_engine:
  min_support: 0.05
  min_confidence: 0.65
  window_sliding_hours: 24
  max_sequence_length: 15
  mining_cron_schedule: "0 */4 * * *" # Run every 4 hours
  event_bus_publishing:
    publish_candidates: true
    publish_anomalies: true
```

---

## 7. Verification & Performance Metrics

- **Mining Throughput**: Must process 100,000 trace events in < 45 seconds on 8-core CPU.
- **Pattern Verification Rate**: > 95% of automatically detected anti-patterns must pass validation against historical ground-truth log samples.
