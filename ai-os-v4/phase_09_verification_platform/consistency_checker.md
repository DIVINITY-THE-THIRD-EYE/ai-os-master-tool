# Phase 09 — Verification Platform
## Specification 09.03: Consistency Checker Architecture (`consistency_checker.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-03` |
| **Title** | Cross-Artifact Consistency Checker Specification |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Multi-Artifact Alignment Verification` |
| **Dependencies** | `SPEC-09-01 (Verification Engine)`, `SPEC-00-01 (Conventions)` |

---

## 1. Executive Summary

The **Consistency Checker** validates cross-artifact alignment across multi-file outputs. In a multi-agent system, an engineering task often produces multiple interdependent deliverables (e.g., OpenAPI Spec $\leftrightarrow$ Controller Code $\leftrightarrow$ Unit Test $\leftrightarrow$ User Documentation). The Consistency Checker performs semantic cross-validation to ensure parameter names, data types, system invariants, naming conventions, and schema contracts match perfectly across all generated files.

---

## 2. Cross-Artifact Verification Matrix

```text
+-----------------------+                         +-----------------------+
|  OpenAPI / API Spec   |<=======================>| Controller / Service  |
|  (spec.json / spec.yaml)                       | Code Implementation   |
+-----------+-----------+                         +-----------+-----------+
            ^                                                 ^
            |                                                 |
            |            Cross-Artifact Alignment             |
            v            Consistency Checker Matrix           v
+-----------+-----------+                         +-----------+-----------+
| Unit & Integration    |<=======================>| User & API Technical  |
| Test Suite Files      |                         | Documentation Docs    |
+-----------------------+                         +-----------------------+
```

---

## 3. Consistency Rule Catalog

| Rule ID | Alignment Dimension | Verification Description | Severity |
| :--- | :--- | :--- | :--- |
| `CNS-RULE-001` | **API Contract vs. Code** | Verifies exported route paths, request payload fields, and HTTP status codes match OpenAPI spec exactly. | `CRITICAL` |
| `CNS-RULE-002` | **Code vs. Test Coverage** | Verifies every public function in code artifact has a matching unit test signature in test suite. | `MAJOR` |
| `CNS-RULE-003` | **Code vs. Documentation** | Verifies function parameter names and types in docstrings match actual signature. | `MAJOR` |
| `CNS-RULE-004` | **Naming Conventions** | Enforces `CONVENTIONS.md` naming rules (snake_case vs camelCase vs PascalCase per file type). | `MINOR` |
| `CNS-RULE-005` | **Schema Alignment** | Checks JSON schema field types against DB migration scripts and TypeScript interfaces. | `CRITICAL` |

---

## 4. Technical Data Structures & Schemas

### 4.1 Cross-Artifact Alignment Payload Interface (TypeScript)

```typescript
export interface ArtifactRef {
  artifactId: string;
  filePath: string;
  artifactType: 'SPECIFICATION' | 'IMPLEMENTATION_CODE' | 'TEST_SUITE' | 'DOCUMENTATION';
}

export interface ConsistencyCheckResult {
  checkerId: 'CHECKER-CONSISTENCY';
  targetGroup: ArtifactRef[];
  timestamp: string;
  passed: boolean;
  mismatchFindings: Array<{
    ruleId: string;
    severity: 'CRITICAL' | 'MAJOR' | 'MINOR';
    sourceArtifact: ArtifactRef;
    targetArtifact: ArtifactRef;
    sourceElement: string; // e.g., "GET /api/v1/users payload field 'user_id'"
    targetElement: string; // e.g., "controller method argument 'userId'"
    mismatchDescription: string;
  }>;
}
```

### 4.2 Consistency Check Result Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ConsistencyCheckResult",
  "type": "object",
  "required": [
    "checkerId",
    "targetGroup",
    "timestamp",
    "passed",
    "mismatchFindings"
  ],
  "properties": {
    "checkerId": { "type": "string", "enum": ["CHECKER-CONSISTENCY"] },
    "targetGroup": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["artifactId", "filePath", "artifactType"],
        "properties": {
          "artifactId": { "type": "string" },
          "filePath": { "type": "string" },
          "artifactType": { "type": "string" }
        }
      }
    },
    "timestamp": { "type": "string", "format": "date-time" },
    "passed": { "type": "boolean" },
    "mismatchFindings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ruleId", "severity", "sourceArtifact", "targetArtifact", "mismatchDescription"],
        "properties": {
          "ruleId": { "type": "string" },
          "severity": { "type": "string", "enum": ["CRITICAL", "MAJOR", "MINOR"] },
          "mismatchDescription": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 5. Algorithmic Cross-Diff Protocol

```text
Step 1: Parse all input artifacts in current task artifact bundle.
Step 2: Build Symbol Dependency Graph (SDG) mapping route definitions, types, export functions.
Step 3: Execute pair-wise diff matching (Spec vs Code; Code vs Tests; Code vs Docs).
Step 4: Flag type mismatches, missing fields, or naming convention drift.
Step 5: Generate unified Consistency Verification Report.
```

---

## 6. Verification Criteria

- **Cross-Spec Precision**: 100% detection of parameter type mismatches between OpenAPI specs and controller code.
- **Convention Enforcement**: Zero unflagged violations of `CONVENTIONS.md` across verified bundles.
