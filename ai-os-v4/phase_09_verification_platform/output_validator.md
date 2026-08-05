# Phase 09 — Verification Platform
## Specification 09.11: Output Validator Architecture (`output_validator.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-11` |
| **Title** | Output Validator & Schema Integrity Scanner |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Schema & Output Validation` |
| **Dependencies** | `SPEC-09-01 (Verification Engine)`, `SPEC-11-01 (JSON Schemas)` |

---

## 1. Executive Summary

The **Output Validator** acts as the first line of defense in the Verification Platform. It validates the syntactic, structural, and schema integrity of raw agent outputs before any complex logic, security, or semantic checkers execute. Inspecting JSON, YAML, XML, Markdown, and source code outputs against the 40+ official system JSON schemas (`phase_11_schemas/`), it rejects malformed JSON, missing required fields, out-of-bounds numeric parameters, and invalid data types.

---

## 2. Structural & Schema Rules

| Rule ID | Format / Schema | Verification Description | Severity |
| :--- | :--- | :--- | :--- |
| `VAL-RULE-001` | **JSON Syntactic** | **JSON Syntax Integrity**: Validates payload is parseable JSON without unescaped characters or trailing commas. | `FATAL` |
| `VAL-RULE-002` | **JSON Schema** | **Phase 11 Schema Conformance**: Validates JSON output against target schema in `phase_11_schemas/` ($schema, title, type, properties). | `FATAL` |
| `VAL-RULE-003` | **YAML Syntactic** | **YAML Syntax Integrity**: Validates YAML specs (workflows, configs) for proper indentation and scalar types. | `FATAL` |
| `VAL-RULE-004` | **Regex & Type Range** | **Regex & Numeric Constraints**: Enforces regex patterns (e.g. UUID, ISO 8601 timestamps, semver) and min/max value bounds. | `CRITICAL` |
| `VAL-RULE-005` | **Artifact Hashing** | **Cryptographic Lineage Checksum**: Calculates SHA-256 hash of output payload and verifies matching header checksum. | `MAJOR` |

---

## 3. Technical Data Structures & Schemas

### 3.1 Output Validator Payload Interface (TypeScript)

```typescript
export interface OutputValidationResult {
  checkerId: 'CHECKER-OUTPUT-VALIDATOR';
  artifactId: string;
  timestamp: string;
  passed: boolean;
  targetSchemaUri?: string; // e.g., "phase_11_schemas/agent_schema.json"
  checksumSha256: string;
  syntaxFormat: 'JSON' | 'YAML' | 'XML' | 'MARKDOWN' | 'SOURCE_CODE';
  schemaErrors: Array<{
    ruleId: 'VAL-RULE-001' | 'VAL-RULE-002' | 'VAL-RULE-003' | 'VAL-RULE-004' | 'VAL-RULE-005';
    severity: 'FATAL' | 'CRITICAL' | 'MAJOR';
    dataPath: string; // JSONPointer e.g., "/properties/agentId"
    keyword: string; // e.g., "required", "pattern", "type"
    errorMessage: string;
  }>;
}
```

### 3.2 Output Validation Result Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OutputValidationResult",
  "type": "object",
  "required": [
    "checkerId",
    "artifactId",
    "timestamp",
    "passed",
    "checksumSha256",
    "syntaxFormat",
    "schemaErrors"
  ],
  "properties": {
    "checkerId": { "type": "string", "enum": ["CHECKER-OUTPUT-VALIDATOR"] },
    "artifactId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "passed": { "type": "boolean" },
    "targetSchemaUri": { "type": "string" },
    "checksumSha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "syntaxFormat": { "type": "string", "enum": ["JSON", "YAML", "XML", "MARKDOWN", "SOURCE_CODE"] },
    "schemaErrors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ruleId", "severity", "dataPath", "keyword", "errorMessage"],
        "properties": {
          "ruleId": {
            "type": "string",
            "enum": ["VAL-RULE-001", "VAL-RULE-002", "VAL-RULE-003", "VAL-RULE-004", "VAL-RULE-005"]
          },
          "severity": { "type": "string", "enum": ["FATAL", "CRITICAL", "MAJOR"] },
          "dataPath": { "type": "string" },
          "keyword": { "type": "string" },
          "errorMessage": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 4. System Configuration

```yaml
output_validator:
  enabled: true
  schema_validator_engine: "Ajv" # Fast JSON schema validator
  strict_additional_properties: true
  allow_partial_json_repair: false # Reject malformed JSON; do not auto-fix
  compute_sha256_checksums: true
```

---

## 5. Verification Criteria

- **Validation Speed**: Must complete schema validation in $< 15\text{ms}$ per JSON artifact.
- **Zero Tolerance**: 100% of malformed JSON payloads or missing required fields trigger immediate `FATAL` reject.
