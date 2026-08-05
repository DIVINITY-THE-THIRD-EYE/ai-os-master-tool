# Lessons Learned Repository Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-LL-011  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Retrospective Learning

The Lessons Learned Repository stores structured post-mortem analyses, failure patterns, root cause classifications, and corrective actions derived from past task executions and platform incidents.

---

## 2. Lessons Learned Metadata Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LessonLearnedRecord",
  "type": "object",
  "properties": {
    "lesson_id": { "type": "string", "pattern": "^LL-[0-9]{5}$" },
    "incident_ref": { "type": "string" },
    "category": { "type": "string", "enum": ["PERFORMANCE", "SECURITY", "SYNTAX_ERROR", "DEADLOCK", "TOKEN_EXHAUSTION", "SPEC_AMBIGUITY"] },
    "summary": { "type": "string" },
    "root_cause_analysis": { "type": "string" },
    "trigger_conditions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "corrective_action": { "type": "string" },
    "preventive_policy_rule": { "type": "string" },
    "severity_impact": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"] }
  },
  "required": ["lesson_id", "category", "summary", "root_cause_analysis", "corrective_action", "preventive_policy_rule"]
}
```

---

## 3. Automated Context Warning Injection Pipeline

Before a Worker Agent begins executing a task, the Reflection and Learning system queries the Lessons Learned Repository:

```text
[Task Context] ──► Query Lessons Learned ──► Matches Trigger Conditions?
                                                      │
                                                      ├── YES ──► Inject Warning Prompt Box into Agent Prompt
                                                      └── NO  ──► Proceed normally
```

### Injected Warning Prompt Example

```text
[SYSTEM WARNING: HISTORICAL FAILURE RISK DETECTED]
Related Lesson: LL-00142 (Database Deadlock under High Concurrent Writes)
Trigger Condition: Batch updates exceeding 100 rows in PostgreSQL execution context.
Mandatory Action: Split batch transactions into chunks <= 25 rows and acquire row locks in deterministic ID order.
```

---

## 4. Governance & Review Workflow

1. **Candidate Extraction:** Reflection Engine automatically proposes candidate lessons after task failures (`outcome_status == FAILURE`).
2. **Authority Review:** Domain Authority Agent or Human Lead reviews and validates root cause accuracy.
3. **Policy Promotion:** Validated lessons are promoted into permanent Rule Engine policies (`rule_engine_spec.md`).
