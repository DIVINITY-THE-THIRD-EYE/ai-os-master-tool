# Phase 08 — Reflection and Learning
## Specification 08.01: Reflection Engine Architecture (`reflection_engine.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-01` |
| **Title** | Reflection Engine Core Architecture & Lifecycle |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Learning Subsystem` |
| **Dependencies** | `SPEC-01-01 (Kernel)`, `SPEC-01-03 (Event Router)`, `SPEC-06-01 (Reflection Memory)` |

---

## 1. Executive Summary

The **Reflection Engine** is the central self-observation and meta-cognitive reasoning subsystem of the AI Operating System (AI OS v4). It continuously monitors task execution events, agent output artifacts, and operational telemetry to distill insights, detect performance gaps, and update systemic memory. By transforming transient execution trajectories into structured reflection records, the Reflection Engine enables autonomous agent self-correction, continuous prompt refinement, and system-wide capability evolution without requiring human re-training or manual prompt modifications.

---

## 2. Architectural Overview & Workflow

```text
                                  +---------------------------------------+
                                  |     Agent Execution Environment       |
                                  +-------------------+-------------------+
                                                      |
                                     Task Executed / Event Published
                                                      v
+-------------------+             +-------------------+-------------------+
|  Event Router /   |---------->  |        Reflection Trigger         |
|  Event Bus        |             |  (Post-Task, Periodic, Anomaly)   |
+-------------------+             +-------------------+-------------------+
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |     Context & Trajectory Harvester    |
                                  | (Prompts, Tool Calls, Memory Check) |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |    Meta-Cognitive Evaluation Pipeline |
                                  | (Outcome vs Goal, Variance Analysis)  |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +-------------------+-------------------+
                                  |     Reflection Record Synthesizer     |
                                  +---------+-----------------+-----------+
                                            |                 |
                      +---------------------+                 +---------------------+
                      v                                                             v
    +-----------------+-----------------+                         +-----------------+-----------------+
    |  Reflection Memory Commit (2PC)   |                         |  Knowledge Update Dispatch      |
    +-----------------------------------+                         +-----------------------------------+
```

---

## 3. Subsystem Trigger Conditions

The Reflection Engine executes under three primary trigger conditions:

1. **Post-Task Triggers (Immediate)**:
   - Fired automatically upon arrival of `TaskCompletedEvent` or `TaskFailedEvent`.
   - Analyzes execution trajectory, token efficiency, tool call sequence, and validation scores.

2. **Periodic Triggers (Schedule-Based)**:
   - Cron-scheduled background evaluation (e.g., every 6 hours or 100 executed tasks).
   - Aggregates multi-agent trajectories to identify systemic trends and cross-agent patterns.

3. **Anomaly Triggers (Event-Driven Reactive)**:
   - Activated when a `QualityGateFailedEvent`, `PolicyViolationEvent`, or `ResourceExhaustedEvent` occurs.
   - Performs rapid diagnostic reflection to prevent immediate cascade failures.

---

## 4. Technical Data Structures & Schemas

### 4.1 Reflection Context Data Interface (TypeScript)

```typescript
export interface ReflectionContext {
  reflectionId: string; // Format: "REFL-YYYYMMDD-XXXX"
  taskId: string;
  agentId: string;
  triggerType: 'POST_TASK' | 'PERIODIC' | 'ANOMALY';
  executionDurationMs: number;
  tokenConsumption: {
    promptTokens: number;
    completionTokens: number;
    totalCostUsd: number;
  };
  trajectoryTrace: Array<{
    stepNumber: number;
    actionType: string;
    inputPayload: Record<string, unknown>;
    outputPayload: Record<string, unknown>;
    durationMs: number;
    status: 'SUCCESS' | 'FAILURE' | 'RETRY';
    errorMessage?: string;
  }>;
  expectedGoal: string;
  actualArtifacts: Array<{
    artifactId: string;
    artifactType: string;
    checksumSha256: string;
    verificationStatus: 'PASSED' | 'FAILED' | 'PENDING';
  }>;
}
```

### 4.2 Reflection Output Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ReflectionRecord",
  "type": "object",
  "required": [
    "reflectionId",
    "taskId",
    "agentId",
    "timestamp",
    "successRating",
    "keyInsights",
    "rootCauseAnalysis",
    "actionableRecommendations"
  ],
  "properties": {
    "reflectionId": { "type": "string", "pattern": "^REFL-[0-9]{8}-[A-Z0-9]{6}$" },
    "taskId": { "type": "string" },
    "agentId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "successRating": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "keyInsights": {
      "type": "array",
      "items": { "type": "string" }
    },
    "rootCauseAnalysis": {
      "type": "object",
      "properties": {
        "primaryCategory": { "type": "string", "enum": ["LOGIC_ERROR", "CONTEXT_TRUNCATION", "TOOL_FAILURE", "PROMPT_AMBIGUITY", "RESOURCE_LIMIT", "NONE"] },
        "explanation": { "type": "string" }
      }
    },
    "actionableRecommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["targetComponent", "recommendationType", "description", "priority"],
        "properties": {
          "targetComponent": { "type": "string", "enum": ["PROMPT", "WORKFLOW", "MEMORY", "TOOL", "POLICY"] },
          "recommendationType": { "type": "string", "enum": ["UPDATE_TEMPLATE", "ADJUST_TIMEOUT", "ADD_GUARDRAIL", "PRUNE_CONTEXT", "RETRY_STRATEGY"] },
          "description": { "type": "string" },
          "priority": { "type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"] }
        }
      }
    }
  }
}
```

---

## 5. Algorithmic Evaluation Pipeline

The Reflection Engine processes trajectories through a 4-stage pipeline:

```text
Step 1: Trajectory Ingestion & Normalization
        Extract task spec, actual tool call sequence, error logs, and validation scores.
Step 2: Goal vs. Outcome Variance Computation
        Calculate Goal Realization Index (GRI) using embedding similarity & AST verification.
Step 3: Meta-Prompting Evaluation Synthesis
        Construct meta-prompt containing task context, expected goals, trajectory steps, and failure modes.
Step 4: Structured Insight Extraction & Memory Dispatch
        Extract standardized JSON reflection payload and publish events to Event Bus.
```

---

## 6. Event Schema Definitions

### 6.1 `ReflectionTriggeredEvent`

```json
{
  "eventId": "EVT-REFL-TRIG-9921",
  "eventType": "ReflectionTriggeredEvent",
  "timestamp": "2026-08-05T21:15:00Z",
  "payload": {
    "reflectionId": "REFL-20260805-AB8921",
    "taskId": "TASK-88192",
    "agentId": "agent_software_engineer",
    "triggerType": "POST_TASK"
  }
}
```

### 6.2 `ReflectionCompletedEvent`

```json
{
  "eventId": "EVT-REFL-COMP-9922",
  "eventType": "ReflectionCompletedEvent",
  "timestamp": "2026-08-05T21:15:12Z",
  "payload": {
    "reflectionId": "REFL-20260805-AB8921",
    "taskId": "TASK-88192",
    "agentId": "agent_software_engineer",
    "successRating": 0.85,
    "insightsCount": 3,
    "recommendationsCount": 1
  }
}
```

---

## 7. Subsystem Configuration

```yaml
reflection_engine:
  enabled: true
  concurrency_limit: 8
  evaluation_model: "gpt-4o-reflection-v1"
  sampling_rate:
    successful_tasks: 0.20 # Sample 20% of successful tasks for continuous optimization
    failed_tasks: 1.00     # 100% reflection on failures
  max_trajectory_length: 50
  memory_commit_policy: "TWO_PHASE_COMMIT"
  timeouts:
    synthesis_timeout_ms: 15000
```

---

## 8. Failure Modes & Operational Safeguards

| Failure Scenario | Mitigation & Safeguard Strategy |
| :--- | :--- |
| **Reflection Model Timeout** | Fall back to heuristic rule-based reflection; emit warning event `ReflectionDegradedEvent`. |
| **Recursion Loop (Reflection reflecting on Reflection)** | Hard restriction: Tasks with domain `META_REFLECTION` cannot trigger Reflection Engine. |
| **Token Budget Exhaustion** | Trajectory summarization prior to meta-prompting; enforce strict byte limit on context payload. |
| **Invalid Schema Output from Synthesizer** | Retry synthesis up to 2 times with explicit JSON format enforcement; drop to raw log if failed. |

---

## 9. Verification & Conformance Criteria

- **Automated Validation Test**: Execute 10 simulated failed tasks; verify 10 `ReflectionCompletedEvent` instances published within 15 seconds.
- **Coverage**: 100% of failed tasks and 20% of passing tasks generate valid `ReflectionRecord` JSON compliant with section 4.2 schema.
