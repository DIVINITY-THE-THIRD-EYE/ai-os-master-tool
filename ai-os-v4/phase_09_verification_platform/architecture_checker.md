# Phase 09 — Verification Platform
## Specification 09.04: Architecture Checker Architecture (`architecture_checker.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-04` |
| **Title** | Architecture Conformance Checker & Invariant Verifier |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Architecture Governance` |
| **Dependencies** | `SPEC-09-01 (Verification Engine)`, `Volume 1 (Architecture Invariants)` |

---

## 1. Executive Summary

The **Architecture Checker** enforces non-negotiable enterprise architecture rules, layer boundary isolation, circular dependency prevention, and architectural invariants across all system components. In compliance with **Volume 1 Section 1 (Non-Negotiable Architecture Conformance Rules)**, this checker statically inspects dependency import graphs, package boundaries, memory commit protocols, and state machine transitions to guarantee architectural integrity.

---

## 2. Architecture Invariant Enforcement Rules

| Rule ID | Targeted Architectural Invariant | Enforced Constraint & Verification Method | Severity |
| :--- | :--- | :--- | :--- |
| `ARC-INV-001` | **Invariant 1: No Direct Writes to EKG** | Scan codebase for direct DB write calls targeting Knowledge Graph tables from worker agent modules. Must route via KUP (`SPEC-08-06`). | `FATAL` |
| `ARC-INV-002` | **Invariant 2: Selective Deployment Gate** | Verify no agent initialization code bypasses `deploy_agents_for_goal()` kernel call. | `CRITICAL` |
| `ARC-INV-003` | **Invariant 3: Decoupled Communication** | Verify inter-subsystem calls use Event Bus or Kernel APIs. Block direct module mutation. | `FATAL` |
| `ARC-INV-004` | **Invariant 4: Artifact Lineage Metadata** | Verify every generated artifact header contains SHA256 checksum, author ID, and parent IDs. | `MAJOR` |
| `ARC-INV-005` | **Invariant 5: Stateful Operation Checkpoints** | Verify long-running operations (> 5 sec) implement state serialization & checkpoint hooks. | `CRITICAL` |
| `ARC-INV-006` | **Layer Boundaries** | Check import dependency graph for illegal cross-layer imports (e.g., UI importing DB drivers). | `CRITICAL` |
| `ARC-INV-007` | **Circular Dependencies** | Run Tarjan's Strongly Connected Components algorithm to verify 0 circular module dependencies. | `FATAL` |

---

## 3. Structural Dependency Graph Verification Workflow

```text
                  +----------------------------------------------+
                  | Module Import Graph Harvester & AST Analysis |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Dependency Matrix Construction & Directed Graph|
                  +----------------------+-----------------------+
                                         |
                                         v
+----------------------------------------+----------------------------------------+
|                                        |                                        |
v                                        v                                        v
+-----------------------+  +-----------------------+  +-----------------------+
| Invariants 1-5 Rule   |  | Tarjan SCC Circular   |  | Modularity & Layer    |
| Verifier              |  | Dependency Detector   |  | Boundary Evaluator    |
+-----------------------+  +-----------------------+  +-----------------------+
|                                        |                                        |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  | Aggregated Architectural Finding Dispatch    |
                  +----------------------------------------------+
```

---

## 4. Technical Data Structures & Schemas

### 4.1 Architecture Conformance Payload Interface (TypeScript)

```typescript
export interface ArchitectureCheckResult {
  checkerId: 'CHECKER-ARCHITECTURE';
  artifactId: string;
  timestamp: string;
  passed: boolean;
  modularityScore: number; // 0.0 to 100.0
  invariantViolations: Array<{
    ruleId: 'ARC-INV-001' | 'ARC-INV-002' | 'ARC-INV-003' | 'ARC-INV-004' | 'ARC-INV-005' | 'ARC-INV-006' | 'ARC-INV-007';
    severity: 'FATAL' | 'CRITICAL' | 'MAJOR';
    violatingModulePath: string;
    targetReferencePath?: string;
    description: string;
    admittedByAdr: boolean; // Flag if violation is explicitly granted by an ADR
  }>;
  circularDependencyCycles: Array<{
    cycleId: string;
    modulePathChain: string[]; // e.g., ["moduleA", "moduleB", "moduleC", "moduleA"]
  }>;
}
```

### 4.2 Architecture Check Result Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ArchitectureCheckResult",
  "type": "object",
  "required": [
    "checkerId",
    "artifactId",
    "timestamp",
    "passed",
    "modularityScore",
    "invariantViolations",
    "circularDependencyCycles"
  ],
  "properties": {
    "checkerId": { "type": "string", "enum": ["CHECKER-ARCHITECTURE"] },
    "artifactId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "passed": { "type": "boolean" },
    "modularityScore": { "type": "number", "minimum": 0, "maximum": 100 },
    "invariantViolations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ruleId", "severity", "violatingModulePath", "description"],
        "properties": {
          "ruleId": {
            "type": "string",
            "enum": ["ARC-INV-001", "ARC-INV-002", "ARC-INV-003", "ARC-INV-004", "ARC-INV-005", "ARC-INV-006", "ARC-INV-007"]
          },
          "severity": { "type": "string", "enum": ["FATAL", "CRITICAL", "MAJOR"] },
          "violatingModulePath": { "type": "string" },
          "description": { "type": "string" },
          "admittedByAdr": { "type": "boolean" }
        }
      }
    },
    "circularDependencyCycles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["cycleId", "modulePathChain"],
        "properties": {
          "cycleId": { "type": "string" },
          "modulePathChain": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

---

## 5. Modularity Scoring Formula

$$\text{ModularityScore} = 100 - \left(15 \times N_{\text{CircularCycles}}\right) - \left(20 \times N_{\text{InvariantViolations}}\right) - \left(5 \times N_{\text{LayerBoundaryBreaches}}\right)$$

---

## 6. Verification Criteria

- **Invariant Enforcement Precision**: 100% detection of direct Knowledge Graph writes or unauthorized event bypasses.
- **Zero Cycle Tolerance**: Any circular dependency chain immediately marks `passed = false` with `FATAL` severity.
