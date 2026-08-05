# Phase 08 — Reflection and Learning
## Specification 08.03: Root Cause Analysis Specification (`root_cause_analysis_spec.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-08-03` |
| **Title** | Automated Root Cause Analysis (RCA) Specification & Causal Graphs |
| **Phase** | `Phase 08 — Reflection and Learning` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Meta-Diagnostics & Governance` |
| **Dependencies** | `SPEC-08-01 (Reflection Engine)`, `SPEC-08-02 (Failure Analysis Engine)`, `SPEC-05-01 (Knowledge Graph)` |

---

## 1. Executive Summary

The **Root Cause Analysis (RCA) Engine** performs deep structural and causal investigations into critical or recurring system failures. Moving beyond immediate symptom detection, the RCA Engine applies an automated **5-Whys Causal Chain Algorithm** combined with **Temporal Trace Reconstruction** and **Causal Dependency Graph Mining**. It isolates the underlying systemic origin of defects—such as flawed prompt templates, missing schema definitions, improper DAG dependencies, or latent resource bottlenecks—and generates formal, immutable RCA Artifacts.

---

## 2. Architectural Overview & Workflow

```text
                  +----------------------------------------------+
                  |    Failure Diagnostic Event (from FAE)       |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Temporal Execution Trace Reconstructor       |
                  |  (Stitches Multi-Agent Event Timelines)      |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Causal Dependency Graph (CDG) Builder       |
                  |  (Nodes: Events/States; Edges: Causality)    |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Automated 5-Whys Reasoning Traversal Engine |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  Root Cause Isolation & Countermeasure Synthesizer |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |   Formal RCA Artifact Schema Generation      |
                  +----------------------------------------------+
```

---

## 3. The 5-Whys Causal Traversal Algorithm

The RCA Engine implements an automated 5-Whys expansion loop using structured prompts over the temporal trace:

```text
Level 1 (Symptom): Why did Task X fail?
  --> Output: Agent Y produced malformed JSON output at Step 4.

Level 2 (Direct Cause): Why was the output malformed?
  --> Output: Agent Y used tool 'bash_exec' which returned an unexpected error string containing unescaped quotes.

Level 3 (Contributing Factor): Why did the tool return unescaped quotes?
  --> Output: System script environment variable missing double-quote sanitizer.

Level 4 (Systemic Defect): Why was the sanitizer missing?
  --> Output: Prompt template for Agent Y lacked explicit formatting instructions for bash tool payload handling.

Level 5 (Root Cause): Why was the prompt template lacking these instructions?
  --> Output: Prompt design specification SPEC-03-88 was not updated when bash tool version 2.4 was deployed.
```

---

## 4. Technical Data Structures & Schemas

### 4.1 Causal Graph Node & Edge Data Structures (TypeScript)

```typescript
export interface CausalNode {
  id: string; // Event ID or State Change ID
  timestamp: string;
  subsystem: string;
  actor: string; // Agent ID or Service Name
  action: string;
  stateDelta: Record<string, unknown>;
}

export interface CausalEdge {
  sourceNodeId: string;
  targetNodeId: string;
  relationshipType: 'TRIGGERED_BY' | 'DEPENDS_ON' | 'MODIFIED_STATE' | 'TRANSMITTED_ERROR';
  causalWeight: number; // 0.0 to 1.0 confidence
}

export interface CausalDependencyGraph {
  graphId: string;
  rootFailureNodeId: string;
  nodes: CausalNode[];
  edges: CausalEdge[];
}
```

### 4.2 Formal RCA Artifact Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RootCauseAnalysisArtifact",
  "type": "object",
  "required": [
    "rcaId",
    "incidentId",
    "timestamp",
    "symptomSummary",
    "rootCauseSummary",
    "fiveWhysChain",
    "isolatedSystemicDefect",
    "preventativeCountermeasures"
  ],
  "properties": {
    "rcaId": { "type": "string", "pattern": "^RCA-[0-9]{8}-[A-Z0-9]{6}$" },
    "incidentId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "symptomSummary": { "type": "string" },
    "rootCauseSummary": { "type": "string" },
    "fiveWhysChain": {
      "type": "array",
      "minItems": 3,
      "maxItems": 5,
      "items": {
        "type": "object",
        "required": ["level", "question", "answer", "evidenceEventId"],
        "properties": {
          "level": { "type": "integer", "minimum": 1, "maximum": 5 },
          "question": { "type": "string" },
          "answer": { "type": "string" },
          "evidenceEventId": { "type": "string" }
        }
      }
    },
    "isolatedSystemicDefect": {
      "type": "object",
      "required": ["componentType", "componentId", "description"],
      "properties": {
        "componentType": { "type": "string", "enum": ["PROMPT_TEMPLATE", "WORKFLOW_DAG", "TOOL_WRAPPER", "SCHEMA_DEFINITION", "RESOURCE_POLICY"] },
        "componentId": { "type": "string" },
        "description": { "type": "string" }
      }
    },
    "preventativeCountermeasures": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["countermeasureId", "targetSubsystem", "actionPlan", "automatedPatchAvailable"],
        "properties": {
          "countermeasureId": { "type": "string" },
          "targetSubsystem": { "type": "string" },
          "actionPlan": { "type": "string" },
          "automatedPatchAvailable": { "type": "boolean" }
        }
      }
    }
  }
}
```

---

## 5. Event Integration Points

- **Consumes**: `FailureDiagnosticReportGeneratedEvent` (from FAE).
- **Publishes**:
  - `RCASignoffRequestedEvent`: Triggers human/governance approval for major systemic findings.
  - `RootCauseIsolatedEvent`: Notifies `improvement_suggestion_engine.md` to auto-generate patches.

```json
{
  "eventId": "EVT-RCA-ISOL-7712",
  "eventType": "RootCauseIsolatedEvent",
  "timestamp": "2026-08-05T21:16:00Z",
  "payload": {
    "rcaId": "RCA-20260805-XY7712",
    "isolatedComponent": "PROMPT_TEMPLATE",
    "componentId": "prompt_react_developer_v2",
    "rootCauseSummary": "Prompt lacks explicit escape rule for single quotes in JSON payloads."
  }
}
```

---

## 6. Verification & Quality Gates

- **Depth Gate**: Every generated RCA must achieve at least 3 levels in the 5-Whys chain with verified event evidence linked to each level.
- **Trace Reconstructability**: 100% of event references in the causal graph must match existing log IDs in the event store.
