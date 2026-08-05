# Phase 08 — Reflection and Learning
## Specification 08.02: Failure Analysis Engine Architecture (`failure_analysis_engine.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-02` |
| **Title** | Failure Analysis Engine Specification & Diagnostics |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Learning & Quality Subsystem` |
| **Dependencies** | `SPEC-01-01 (Kernel)`, `SPEC-08-01 (Reflection Engine)`, `SPEC-09-01 (Verification Engine)` |

---

## 1. Executive Summary

The **Failure Analysis Engine (FAE)** provides automated, deep-tier diagnostic capabilities for identifying, categorizing, and mitigating execution failures across the AI OS platform. When an agent operation, workflow execution, or quality gate check fails, the FAE intercepts the failure context, parses multi-modal trace logs, classifies the failure according to a 6-tier taxonomy, and calculates recovery viability. By isolating execution defects from systemic design flaws, the FAE prevents repeated execution loops and feeds actionable failure signatures into the Root Cause Analysis and Improvement Suggestion engines.

---

## 2. Architectural Overview & Workflow

```text
                  +----------------------------------------------+
                  |  Execution Failure Event (Kernel / Quality)  |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |   Failure Context & Stack Trace Extractor     |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | 6-Tier Failure Taxonomy Classifier Engine    |
                  | (Runtime, Logic, Context, Tool, Policy, Time) |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Anomaly Clustering & Signature Matcher       |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |    Retry vs. Escalate Decision Evaluator     |
                  +----------+------------------------+----------+
                             |                        |
               +-------------+                        +-------------+
               v                                                    v
+--------------+---------------+                    +---------------+---------------+
|  Auto-Retry Strategy Enforcer|                    | Escalation & RCA Trigger      |
| (Exponential Backoff, Circuit|                    | (Passes to Root Cause Spec)   |
|         Breaker)             |                    |                               |
+------------------------------+                    +-------------------------------+
```

---

## 3. Failure Classification Taxonomy

The FAE categorizes every observed failure into one of 6 standardized enterprise classes:

| Class Code | Category Name | Description | Example Root Factors |
| :--- | :--- | :--- | :--- |
| `FAIL-CAT-100` | **Runtime Exception** | Unhandled exception within agent execution environment or code sandbox. | Null pointer, syntax error in generated code, unhandled promise rejection. |
| `FAIL-CAT-200` | **Logical Defect** | Generated artifact fails specification requirements or logic validation checks. | Incorrect math, invalid business rule compliance, broken API contract. |
| `FAIL-CAT-300` | **Context Truncation** | LLM context window exceeded or critical history lost during window sliding. | System prompt evicted, missing prerequisite variables in prompt context. |
| `FAIL-CAT-400` | **Tool / API Failure** | External API timeout, authentication error, or schema mismatch during tool call. | HTTP 500 from third-party service, malformed JSON arguments to bash tool. |
| `FAIL-CAT-500` | **Policy & Security** | Action blocked by Security Checker, Sandbox Guardrail, or Compliance Policy. | Unauthorized file access attempt, prompt injection payload detected. |
| `FAIL-CAT-600` | **Resource & Timeout** | Token budget depleted, wall-clock timeout exceeded, or RAM/CPU cap reached. | Infinite loop in agent planning, memory leak during large artifact compilation. |

---

## 4. Technical Data Structures & Schemas

### 4.1 Failure Diagnostic Report Interface (TypeScript)

```typescript
export interface FailureDiagnosticReport {
  reportId: string; // Format: "FAR-YYYYMMDD-XXXX"
  taskId: string;
  agentId: string;
  timestamp: string;
  categoryCode: 'FAIL-CAT-100' | 'FAIL-CAT-200' | 'FAIL-CAT-300' | 'FAIL-CAT-400' | 'FAIL-CAT-500' | 'FAIL-CAT-600';
  severity: 'FATAL' | 'CRITICAL' | 'WARNING';
  failureSignature: string; // MD5 hash of sanitized stack trace / error message
  rawErrorDetails: {
    errorMessage: string;
    stackTrace?: string;
    failingStepId?: string;
    toolName?: string;
  };
  classificationConfidence: number; // 0.0 to 1.0
  isTransient: boolean;
  recommendedAction: 'IMMEDIATE_RETRY' | 'RETRY_WITH_PRUNED_CONTEXT' | 'CIRCUIT_BREAK' | 'ESCALATE_HUMAN' | 'ESCALATE_RCA';
}
```

### 4.2 Failure Diagnostic Report Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FailureDiagnosticReport",
  "type": "object",
  "required": [
    "reportId",
    "taskId",
    "agentId",
    "timestamp",
    "categoryCode",
    "severity",
    "failureSignature",
    "isTransient",
    "recommendedAction"
  ],
  "properties": {
    "reportId": { "type": "string", "pattern": "^FAR-[0-9]{8}-[A-Z0-9]{6}$" },
    "taskId": { "type": "string" },
    "agentId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "categoryCode": {
      "type": "string",
      "enum": ["FAIL-CAT-100", "FAIL-CAT-200", "FAIL-CAT-300", "FAIL-CAT-400", "FAIL-CAT-500", "FAIL-CAT-600"]
    },
    "severity": { "type": "string", "enum": ["FATAL", "CRITICAL", "WARNING"] },
    "failureSignature": { "type": "string", "pattern": "^[a-f0-9]{32}$" },
    "isTransient": { "type": "boolean" },
    "recommendedAction": {
      "type": "string",
      "enum": ["IMMEDIATE_RETRY", "RETRY_WITH_PRUNED_CONTEXT", "CIRCUIT_BREAK", "ESCALATE_HUMAN", "ESCALATE_RCA"]
    }
  }
}
```

---

## 5. Retry vs. Escalate Decision Matrix

The FAE applies the following deterministic rule tree to decide whether to retry or escalate:

```text
IF Category == FAIL-CAT-400 (Tool API Failure) AND HTTP_Code IN [429, 502, 503, 504]
    ==> Return IMMEDIATE_RETRY (Exponential Backoff with Jitter)

IF Category == FAIL-CAT-300 (Context Truncation)
    ==> Return RETRY_WITH_PRUNED_CONTEXT (Compress context by 40%, re-run)

IF Category == FAIL-CAT-500 (Policy & Security Violation)
    ==> Return CIRCUIT_BREAK & ESCALATE_RCA (Do NOT retry security blocks)

IF RetryCount >= MaxAllowedRetries (default: 3)
    ==> Return ESCALATE_RCA

OTHERWISE (Runtime / Logic Errors on First Attempt)
    ==> Return RETRY_WITH_REFLECTION_PROMPT (Inject error feedback into next attempt)
```

---

## 6. System Configuration

```yaml
failure_analysis_engine:
  enabled: true
  signature_clustering:
    similarity_threshold: 0.85
    window_minutes: 60
  circuit_breaker:
    consecutive_failures_threshold: 5
    cooldown_seconds: 300
  taxonomy_classifier:
    mode: "HYBRID" # Combination of Regex matchers and embedding classifier
  escalation:
    auto_trigger_rca: true
    notify_channels: ["event_bus", "admin_log"]
```

---

## 7. Operational Verification Criteria

- **Taxonomy Precision**: Accuracy of classification model across test suite >= 98%.
- **Latency Budget**: Diagnostic report generation must complete within 250ms of event receipt.
- **Circuit Breaker Integrity**: Verified that 5 consecutive identical API failures halt task execution and trigger `CircuitBreakerTrippedEvent`.
