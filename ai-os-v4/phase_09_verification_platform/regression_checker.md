# Phase 09 — Verification Platform
## Specification 09.10: Regression Checker Architecture (`regression_checker.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-10` |
| **Title** | Regression Checker & Benchmark Suite Harness |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Benchmark & Regression Prevention` |
| **Dependencies** | `SPEC-09-01 (Verification Engine)`, `SPEC-08-08 (Prompt Improvement Loop)` |

---

## 1. Executive Summary

The **Regression Checker** prevents performance, accuracy, and functional degradation when system prompts, workflow definitions, or core kernel modules are updated. By running candidate modifications against standardized historical golden benchmark datasets, calculating AST/output diffs, evaluating semantic equivalence via embeddings, and measuring pass rate shifts against historical baselines, the Regression Checker protects the platform from unexpected regressions.

---

## 2. Benchmark Execution & Regression Pipeline

```text
                  +----------------------------------------------+
                  | Candidate Patch / Modified Spec Ingestion    |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Historical Golden Benchmark Suite Executor   |
                  | (Executes test dataset N=50 to 500 cases)    |
                  +----------------------+-----------------------+
                                         |
                                         v
+----------------------------------------+----------------------------------------+
|                                        |                                        |
v                                        v                                        v
+-----------------------+  +-----------------------+  +-----------------------+
| Output Snapshot AST   |  | Semantic Equivalence  |  | Accuracy & Pass Rate  |
| Diff Generator        |  | Embedding Evaluator   |  | Shift Calculator      |
+-----------------------+  +-----------------------+  +-----------------------+
|                                        |                                        |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Statistical Non-Inferiority Evaluator         |
                  | (Triggers Alert if Pass Rate Drops > 1.0%)   |
                  +----------------------------------------------+
```

---

## 3. Technical Data Structures & Schemas

### 3.1 Regression Analysis Payload Interface (TypeScript)

```typescript
export interface RegressionCheckResult {
  checkerId: 'CHECKER-REGRESSION';
  artifactId: string;
  timestamp: string;
  passed: boolean;
  benchmarkSuiteName: string;
  totalBenchmarkCases: number;
  baselineMetrics: {
    passRate: number; // 0.0 to 1.0
    avgExecutionTimeMs: number;
    avgTokenCostUsd: number;
  };
  candidateMetrics: {
    passRate: number;
    avgExecutionTimeMs: number;
    avgTokenCostUsd: number;
  };
  deltaSummary: {
    passRateDeltaPercent: number; // Candidate - Baseline
    latencyDeltaPercent: number;
    costDeltaPercent: number;
    regressionDetected: boolean;
  };
  regressedCases: Array<{
    caseId: string;
    promptInputSummary: string;
    baselineOutputHash: string;
    candidateOutputHash: string;
    failureReason: string;
  }>;
}
```

### 3.2 Regression Check Result Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RegressionCheckResult",
  "type": "object",
  "required": [
    "checkerId",
    "artifactId",
    "timestamp",
    "passed",
    "benchmarkSuiteName",
    "totalBenchmarkCases",
    "baselineMetrics",
    "candidateMetrics",
    "deltaSummary",
    "regressedCases"
  ],
  "properties": {
    "checkerId": { "type": "string", "enum": ["CHECKER-REGRESSION"] },
    "artifactId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "passed": { "type": "boolean" },
    "benchmarkSuiteName": { "type": "string" },
    "totalBenchmarkCases": { "type": "integer" },
    "baselineMetrics": { "type": "object" },
    "candidateMetrics": { "type": "object" },
    "deltaSummary": {
      "type": "object",
      "required": ["passRateDeltaPercent", "regressionDetected"],
      "properties": {
        "passRateDeltaPercent": { "type": "number" },
        "regressionDetected": { "type": "boolean" }
      }
    },
    "regressedCases": {
      "type": "array",
      "items": { "type": "object" }
    }
  }
}
```

---

## 4. System Configuration

```yaml
regression_checker:
  enabled: true
  max_allowed_pass_rate_drop_percent: 1.0 # Max 1% pass rate drop allowed
  max_allowed_latency_increase_percent: 10.0
  default_benchmark_suite: "ai_os_core_golden_v4"
  semantic_similarity_threshold: 0.90
```

---

## 5. Verification Criteria

- **Regression Detection Sensitivity**: Must flag 100% of benchmark runs where candidate pass rate drops $> 1.0\%$ below baseline.
- **Zero False Negatives**: All cases where previously passing golden tests fail must be logged in `regressedCases`.
