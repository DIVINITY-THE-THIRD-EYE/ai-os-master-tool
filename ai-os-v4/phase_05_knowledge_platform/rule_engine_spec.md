# Declarative Rule Engine Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-RE-004  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Pattern Matching Architecture

The Rule Engine evaluates business logic, security policies, coding standards, and architectural invariants across the AI OS v4 execution lifecycle. It uses a high-performance Rete-based pattern matching algorithm capable of evaluating tens of thousands of declarative rules per second.

```text
[Fact Working Memory] ──► [Rete Alpha & Beta Network] ◄── [Rule Definitions Store]
                                   │
                                   ▼
                       [Agenda / Conflict Resolver]
                       (Salience ➔ Recency ➔ Specificity)
                                   │
                                   ▼
                       [Rule Action Execution Engine]
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
          [Mutate Working State]       [Emit Audit Event Log]
```

---

## 2. Rule DSL Syntax & Declarative Schema

Rules are declared in YAML or JSON format using structured boolean predicate logic.

```yaml
rule_id: R-SEC-0042
name: ProhibitUnsanitizedSQLQuery
description: Blocks code generation containing string-concatenated SQL queries in database modules.
domain: Security
priority: 95
status: ACTIVE
salience: 100

when:
  all:
    - fact: CodeArtifact.language
      operator: equal_to
      value: "TypeScript"
    - fact: CodeArtifact.module_type
      operator: equal_to
      value: "DatabaseRepository"
    - fact: CodeArtifact.ast_nodes
      operator: contains_pattern
      value: "SELECT * FROM + variable"

then:
  - action: RAISE_SECURITY_VIOLATION
    parameters:
      severity: CRITICAL
      error_code: ERR-SEC-5001
      message: "Unsanitized SQL concatenation detected. Use parameterized queries."
  - action: BLOCK_PIPELINE_EXECUTION
```

---

## 3. JSON Schema for Rule Definitions

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RuleDefinition",
  "type": "object",
  "properties": {
    "rule_id": { "type": "string", "pattern": "^R-[A-Z0-9-]+$" },
    "name": { "type": "string" },
    "domain": { "type": "string" },
    "salience": { "type": "integer", "minimum": 0, "maximum": 1000 },
    "when": {
      "type": "object",
      "properties": {
        "all": { "type": "array" },
        "any": { "type": "array" }
      }
    },
    "then": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "action": { "type": "string" },
          "parameters": { "type": "object" }
        },
        "required": ["action"]
      }
    }
  },
  "required": ["rule_id", "name", "domain", "when", "then"]
}
```

---

## 4. Conflict Resolution & Execution Agenda

When multiple rules match the current working memory state, the Conflict Resolver orders execution using a 3-tier deterministic strategy:

1. **Salience Score:** Rules with higher numerical salience (priority) execute first.
2. **Specificity:** Rules matching more specific condition clauses take precedence over general fallback rules.
3. **Recency:** Rules whose facts were asserted or updated most recently fire first.

---

## 5. Standard Enterprise Policy Rulebook

| Rule ID | Category | Target Trigger | Action |
| :--- | :--- | :--- | :--- |
| `R-INV-0001` | Architecture | Direct write to Knowledge Graph | Block transaction, raise `ERR-4004` |
| `R-SEC-0012` | Security | API Token hardcoded in output | Scrub token, quarantine artifact |
| `R-MEM-0089` | Memory | Token usage > 80% context budget | Trigger `context_compression_engine` |
| `R-QUAL-0105` | QA | Code coverage < 85% on target | Fail Quality Gate, request test generation |

---

## 6. Performance Benchmarks & Audit Logs

- **Pattern Matching Latency:** P95 < 5 ms for 10,000 active rules against 1,000 asserted facts.
- **Rete Node Memory Overhead:** < 120 MB per 10,000 rules.
- **Audit Serialization:** Every rule trigger emits a structured `RuleFiredEvent` to Kafka for compliance reporting.
