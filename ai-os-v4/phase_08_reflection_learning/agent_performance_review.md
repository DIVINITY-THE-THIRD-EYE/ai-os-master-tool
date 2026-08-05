# Phase 08 — Reflection and Learning
## Specification 08.10: Agent Performance Review Framework (`agent_performance_review.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-10` |
| **Title** | Automated Agent Performance Review & Governance Rubric |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Governance & Agent Management` |
| **Dependencies** | `SPEC-02-01 (Agent Specs)`, `SPEC-08-01 (Reflection)`, `SPEC-14-01 (Runtime Policies)` |

---

## 1. Executive Summary

The **Agent Performance Review (APR)** framework provides automated, objective evaluation of all 35 specialized agents operating within AI OS v4. The APR subsystem continuously calculates multi-dimensional KPI scores—including Task Success Rate, Token Budget Efficiency, Verification Pass Rate, Policy Compliance Index, and Average Latency—against established SLAs. Agents that drop below threshold performance bounds are flagged for automated skill refinement, prompt tuning, or temporary suspension from high-criticality task queues.

---

## 2. Architectural Overview & Evaluation Engine

```text
                  +----------------------------------------------+
                  |  Agent Execution Telemetry & Outcome Logs    |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Multi-Metric Score Calculator               |
                  |  (Computes TSR, TBE, VPR, PCI, ALT metrics)   |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Composite SLA Rubric Evaluator Engine        |
                  | (Calculates Overall Composite Score 0-100)    |
                  +----------------------+-----------------------+
                                         |
                                         v
+----------------------------------------+----------------------------------------+
|                                        |                                        |
v                                        v                                        v
+-----------------------+  +-----------------------+  +-----------------------+
| Score >= 85:          |  | 70 <= Score < 85:     |  | Score < 70:           |
| EXCELLENT / GOOD      |  | NEEDS_IMPROVEMENT     |  | CRITICAL_UNDERPERFORM |
| Retain Active Status  |  | Trigger PIL & Prompt  |  | Demote / Suspend from |
|                       |  | Tune Session          |  | High-Risk Tasks       |
+-----------------------+  +-----------------------+  +-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Agent Performance Review Report Dispatch    |
                  +----------------------------------------------+
```

---

## 3. Evaluation Rubric & Metric Formulas

The Composite Performance Score ($S_{\text{composite}}$) is calculated on a 0 to 100 scale:

$$S_{\text{composite}} = (w_1 \cdot \text{TSR}) + (w_2 \cdot \text{VPR}) + (w_3 \cdot \text{PCI}) + (w_4 \cdot \text{TBE}) + (w_5 \cdot \text{ALT})$$

| Metric Code | Metric Name | Definition & Formula | Default Weight ($w$) |
| :--- | :--- | :--- | :--- |
| **TSR** | Task Success Rate | $\frac{\text{Successful Tasks Completed}}{\text{Total Assigned Tasks}} \times 100$ | $w_1 = 0.30$ |
| **VPR** | Verification Pass Rate | $\frac{\text{Verification Checks Passed}}{\text{Total Verification Checks}} \times 100$ | $w_2 = 0.30$ |
| **PCI** | Policy Compliance Index | $\frac{\text{Total Executions} - \text{Policy Violations}}{\text{Total Executions}} \times 100$ | $w_3 = 0.20$ |
| **TBE** | Token Budget Efficiency | $\min\left(100, \frac{\text{Budgeted Tokens}}{\text{Actual Tokens Consumed}} \times 100\right)$ | $w_4 = 0.10$ |
| **ALT** | Latency Target Score | $\min\left(100, \frac{\text{Target Latency P95}}{\text{Actual Latency P95}} \times 100\right)$ | $w_5 = 0.10$ |

---

## 4. Technical Data Structures & Schemas

### 4.1 Agent Review Report Interface (TypeScript)

```typescript
export interface AgentPerformanceReport {
  reviewId: string; // Format: "APR-YYYYMMDD-XXXX"
  agentId: string;
  agentRole: string; // e.g., "agent_software_engineer"
  evaluationPeriod: {
    startTime: string;
    endTime: string;
    totalTasksEvaluated: number;
  };
  metricScores: {
    taskSuccessRate: number;
    verificationPassRate: number;
    policyComplianceIndex: number;
    tokenBudgetEfficiency: number;
    latencyTargetScore: number;
  };
  compositeScore: number; // 0.0 to 100.0
  performanceTier: 'EXCELLENT' | 'GOOD' | 'NEEDS_IMPROVEMENT' | 'CRITICAL_UNDERPERFORM';
  governanceAction: 'NO_ACTION' | 'TRIGGER_PROMPT_TUNING' | 'LIMIT_CONCURRENCY' | 'SUSPEND_AGENT';
  improvementRecommendations: string[];
}
```

### 4.2 Agent Review Report Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentPerformanceReport",
  "type": "object",
  "required": [
    "reviewId",
    "agentId",
    "agentRole",
    "evaluationPeriod",
    "metricScores",
    "compositeScore",
    "performanceTier",
    "governanceAction"
  ],
  "properties": {
    "reviewId": { "type": "string", "pattern": "^APR-[0-9]{8}-[A-Z0-9]{6}$" },
    "agentId": { "type": "string" },
    "agentRole": { "type": "string" },
    "evaluationPeriod": {
      "type": "object",
      "required": ["startTime", "endTime", "totalTasksEvaluated"],
      "properties": {
        "startTime": { "type": "string", "format": "date-time" },
        "endTime": { "type": "string", "format": "date-time" },
        "totalTasksEvaluated": { "type": "integer" }
      }
    },
    "metricScores": {
      "type": "object",
      "required": ["taskSuccessRate", "verificationPassRate", "policyComplianceIndex", "tokenBudgetEfficiency", "latencyTargetScore"],
      "properties": {
        "taskSuccessRate": { "type": "number", "minimum": 0, "maximum": 100 },
        "verificationPassRate": { "type": "number", "minimum": 0, "maximum": 100 },
        "policyComplianceIndex": { "type": "number", "minimum": 0, "maximum": 100 },
        "tokenBudgetEfficiency": { "type": "number", "minimum": 0, "maximum": 100 },
        "latencyTargetScore": { "type": "number", "minimum": 0, "maximum": 100 }
      }
    },
    "compositeScore": { "type": "number", "minimum": 0, "maximum": 100 },
    "performanceTier": {
      "type": "string",
      "enum": ["EXCELLENT", "GOOD", "NEEDS_IMPROVEMENT", "CRITICAL_UNDERPERFORM"]
    },
    "governanceAction": {
      "type": "string",
      "enum": ["NO_ACTION", "TRIGGER_PROMPT_TUNING", "LIMIT_CONCURRENCY", "SUSPEND_AGENT"]
    }
  }
}
```

---

## 5. Governance Action Escalation Matrix

```text
IF CompositeScore >= 90.0:
    Tier = EXCELLENT --> GovernanceAction = NO_ACTION (Eligible for expanded task concurrency)

IF 80.0 <= CompositeScore < 90.0:
    Tier = GOOD --> GovernanceAction = NO_ACTION

IF 70.0 <= CompositeScore < 80.0:
    Tier = NEEDS_IMPROVEMENT --> GovernanceAction = TRIGGER_PROMPT_TUNING

IF CompositeScore < 70.0:
    Tier = CRITICAL_UNDERPERFORM --> GovernanceAction = SUSPEND_AGENT
    Emit AgentSuspendedEvent; route incoming agent tasks to backup/fallback agent role.
```

---

## 6. System Configuration

```yaml
agent_performance_review:
  evaluation_frequency_days: 7
  min_eval_tasks: 10
  tier_thresholds:
    excellent: 90.0
    good: 80.0
    needs_improvement: 70.0
  governance:
    auto_suspension_enabled: true
    fallback_routing_enabled: true
```

---

## 7. Verification & Audit Criteria

- **Automated Score Verification**: 100% of generated review scores must match baseline recalculation within 0.01 precision.
- **Suspension Safety Gate**: Verify that `AgentSuspendedEvent` correctly redirects 100% of subsequent task assignments to designated fallback agent roles.
