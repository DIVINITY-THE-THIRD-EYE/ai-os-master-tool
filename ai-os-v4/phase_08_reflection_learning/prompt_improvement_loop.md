# Phase 08 — Reflection and Learning
## Specification 08.08: Prompt Improvement Loop Architecture (`prompt_improvement_loop.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-08` |
| **Title** | Autonomous Prompt Improvement Loop & Meta-Prompting Harness |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Prompt Engineering & Meta-Optimization` |
| **Dependencies** | `SPEC-03-01 (Prompt Library Core)`, `SPEC-08-04 (Improvement Suggestion)`, `SPEC-09-10 (Regression Checker)` |

---

## 1. Executive Summary

The **Prompt Improvement Loop (PIL)** establishes an autonomous meta-optimization cycle for refining system prompts, specialized agent role prompts, and domain review prompts in `phase_03_prompt_library/`. By pairing continuous performance metric collection (pass rate, token efficiency, output quality score) with meta-prompting mutation algorithms and automated A/B sandbox evaluation, the PIL iteratively updates prompt templates without manual human prompt tuning.

---

## 2. Architectural Overview & Meta-Optimization Loop

```text
                  +----------------------------------------------+
                  | Prompt Performance Monitor (Metric Aggregator)|
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Prompt Candidate Trigger (Pass Rate < 85%)  |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |    Meta-Prompting Optimizer Engine           |
                  |  (Generates Mutated Prompt Variations)       |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |   A/B Sandbox Test Harness & Evaluator       |
                  |  (Runs Candidate vs Baseline on Benchmarks)  |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Significance Calculator (Paired t-test / MCMC)|
                  +----------+------------------------+----------+
                             |                        |
               +-------------+                        +-------------+
               v                                                    v
+--------------+---------------+                    +---------------+---------------+
| Candidate Wins (Stat Sig p<0.05)|                  | Baseline Retained             |
| Auto-Promote to Production    |                    | Discard Mutated Candidate     |
| Update Semantic Version      |                    |                               |
+------------------------------+                    +-------------------------------+
```

---

## 3. Meta-Prompting Mutation Strategies

The PIL applies four standardized prompt transformation operations:

1. **Instruction Disambiguation**: Injects explicit formatting boundaries, negative constraints, and edge-case handling rules.
2. **Context Compression & Pruning**: Identifies redundant prompt verbiage and rewrites instructions to minimize prompt token overhead.
3. **Few-Shot Exemplar Selection**: Replaces static prompt exemplars with high-scoring historical Experience Cards (`SPEC-08-07`).
4. **Structured Reasoning Injection**: Dynamically inserts chain-of-thought (CoT) or structured step decomposition directives.

---

## 4. Technical Data Structures & Schemas

### 4.1 Prompt Optimization Session Interface (TypeScript)

```typescript
export interface PromptOptimizationSession {
  sessionId: string; // Format: "POS-YYYYMMDD-XXXX"
  targetPromptPath: string; // e.g., "phase_03_prompt_library/software/software_architect_system.md"
  baselineVersion: string; // e.g., "1.2.0"
  timestamp: string;
  triggerReason: 'LOW_PASS_RATE' | 'HIGH_TOKEN_COST' | 'EXPLICIT_RCA' | 'PERIODIC_SCHEDULE';
  baselineMetrics: {
    passRate: number; // 0.0 to 1.0
    avgTokenConsumption: number;
    avgLatencyMs: number;
    sampleSize: number;
  };
  mutationsGenerated: Array<{
    mutationId: string;
    mutationStrategy: 'INSTRUCTION_DISAMBIGUATION' | 'CONTEXT_PRUNING' | 'FEW_SHOT_REFRESH' | 'COT_INJECTION';
    candidatePromptContent: string;
    diffFromBaseline: string;
  }>;
  abTestResults?: Array<{
    mutationId: string;
    candidateMetrics: {
      passRate: number;
      avgTokenConsumption: number;
      avgLatencyMs: number;
      sampleSize: number;
    };
    pValue: number; // Statistical significance score
    isWinner: boolean;
  }>;
  finalOutcome: 'PROMOTED_NEW_VERSION' | 'RETAINED_BASELINE' | 'FAILED_SANDBOX';
}
```

### 4.2 Prompt Optimization Session Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PromptOptimizationSession",
  "type": "object",
  "required": [
    "sessionId",
    "targetPromptPath",
    "baselineVersion",
    "timestamp",
    "triggerReason",
    "baselineMetrics",
    "mutationsGenerated",
    "finalOutcome"
  ],
  "properties": {
    "sessionId": { "type": "string", "pattern": "^POS-[0-9]{8}-[A-Z0-9]{6}$" },
    "targetPromptPath": { "type": "string" },
    "baselineVersion": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "triggerReason": {
      "type": "string",
      "enum": ["LOW_PASS_RATE", "HIGH_TOKEN_COST", "EXPLICIT_RCA", "PERIODIC_SCHEDULE"]
    },
    "baselineMetrics": {
      "type": "object",
      "required": ["passRate", "avgTokenConsumption", "avgLatencyMs"],
      "properties": {
        "passRate": { "type": "number", "minimum": 0, "maximum": 1 },
        "avgTokenConsumption": { "type": "number" },
        "avgLatencyMs": { "type": "number" }
      }
    },
    "mutationsGenerated": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["mutationId", "mutationStrategy", "candidatePromptContent", "diffFromBaseline"],
        "properties": {
          "mutationId": { "type": "string" },
          "mutationStrategy": {
            "type": "string",
            "enum": ["INSTRUCTION_DISAMBIGUATION", "CONTEXT_PRUNING", "FEW_SHOT_REFRESH", "COT_INJECTION"]
          },
          "candidatePromptContent": { "type": "string" },
          "diffFromBaseline": { "type": "string" }
        }
      }
    },
    "finalOutcome": {
      "type": "string",
      "enum": ["PROMOTED_NEW_VERSION", "RETAINED_BASELINE", "FAILED_SANDBOX"]
    }
  }
}
```

---

## 5. Statistical Significance Gate & Promotion Rules

A mutated candidate prompt candidate is auto-promoted if and only if all three conditions are satisfied:

1. **Pass Rate Non-Inferiority**: $\text{PassRate}_{\text{Candidate}} \ge \text{PassRate}_{\text{Baseline}}$.
2. **Performance Gain**: $(\text{PassRate}_{\text{Candidate}} - \text{PassRate}_{\text{Baseline}}) \ge +0.05$ OR $(\text{Tokens}_{\text{Baseline}} - \text{Tokens}_{\text{Candidate}}) / \text{Tokens}_{\text{Baseline}} \ge 0.15$.
3. **Statistical Confidence**: Calculated $p$-value $< 0.05$ over minimum benchmark sample size $N \ge 30$.

---

## 6. System Configuration

```yaml
prompt_improvement_loop:
  enabled: true
  evaluation_benchmark_suite: "standard_domain_benchmarks"
  min_sample_size: 30
  p_value_threshold: 0.05
  versioning_rule: "SEMVER_MINOR" # Increments minor version on promotion (e.g. 1.2.0 -> 1.3.0)
  max_concurrent_sessions: 3
```

---

## 7. Verification & Safety Criteria

- **Regression Prevention**: 100% of candidate prompts must pass the full verification checker suite (`SPEC-09-01`) before entering A/B testing.
- **Auditability**: Every prompt promotion must generate a structured Git commit with explicit diff logs and optimization session metadata attached.
