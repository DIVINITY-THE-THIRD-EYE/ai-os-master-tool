# Phase 09 — Verification Platform
## Specification 09.06: Security Checker Architecture (`security_checker.md`)

| Metadata Attribute | Specification Details |
| :--- | :--- |
| **Specification ID** | `SPEC-09-06` |
| **Title** | Security Checker & STRIDE Threat Scanner Specification |
| **Phase** | `Phase 09 — Verification Platform` |
| **Status** | `APPROVED` |
| **Version** | `4.0.0` |
| **Owner Subsystem** | `Platform Core — Security & Sandbox Defense` |
| **Dependencies** | `SPEC-09-01 (Verification Engine)`, `Volume 4 (STRIDE Threat Model)` |

---

## 1. Executive Summary

The **Security Checker** performs static application security testing (SAST), prompt injection defense analysis, secret exposure scanning, privilege escalation detection, and PII/sensitive data leakage checks on all system artifacts. Grounded in the **STRIDE Threat Model** specified in **Volume 4 (Security, Threat Model & Compliance)**, the Security Checker acts as an unbypassable shield preventing compromised outputs or unauthorized system access.

---

## 2. STRIDE Threat Rules & Vulnerability Catalog

| Rule ID | STRIDE Category | Security Rule & Threat Signature | Severity |
| :--- | :--- | :--- | :--- |
| `SEC-RULE-001` | **Tampering / Injection** | **Prompt Injection Payload Scanner**: Detects adversarial injection strings (e.g., "ignore previous instructions", system prompt override attempts). | `FATAL` |
| `SEC-RULE-002` | **Information Disclosure** | **Hardcoded Secrets & API Key Scanner**: Entropy scanner detecting AWS keys, private RSA keys, JWT tokens, DB passwords in code/configs. | `FATAL` |
| `SEC-RULE-003` | **Elevation of Privilege** | **Unauthorized Privilege Access**: Detects code attempting `sudo`, `eval()`, direct shell sub-process spawning, or sandbox escape APIs. | `FATAL` |
| `SEC-RULE-004` | **Information Disclosure** | **PII & Data Leakage Scanner**: Regex & Named Entity Recognition (NER) scanner for SSN, credit cards, email lists in outputs. | `CRITICAL` |
| `SEC-RULE-005` | **Tampering** | **OWASP Top 10 SAST**: Detects SQL Injection, Cross-Site Scripting (XSS), Insecure Deserialization, Path Traversal patterns in AST. | `CRITICAL` |

---

## 3. Multi-Layer Security Scanning Pipeline

```text
                  +----------------------------------------------+
                  |  Artifact Code / Prompt / Output Ingestion   |
                  +----------------------+-----------------------+
                                         |
                                         v
+----------------------------------------+----------------------------------------+
|                                        |                                        |
v                                        v                                        v
+-----------------------+  +-----------------------+  +-----------------------+
| High-Entropy Secret & |  | Adversarial Prompt    |  | AST Code Injection    |
| PII Regex Scanner     |  | Injection Detector    |  | & Privilege Analyzer  |
+-----------------------+  +-----------------------+  +-----------------------+
|                                        |                                        |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
                  +----------------------+-----------------------+
                  |  STRIDE Threat Vector Synthesis & Findings   |
                  +----------------------------------------------+
```

---

## 4. Technical Data Structures & Schemas

### 4.1 Security Check Result Payload Interface (TypeScript)

```typescript
export interface SecurityCheckResult {
  checkerId: 'CHECKER-SECURITY';
  artifactId: string;
  timestamp: string;
  passed: boolean;
  threatSummary: {
    strideCategoryCounts: {
      spoofing: number;
      tampering: number;
      repudiation: number;
      informationDisclosure: number;
      denialOfService: number;
      elevationOfPrivilege: number;
    };
    totalVulnerabilitiesFound: number;
  };
  vulnerabilities: Array<{
    ruleId: 'SEC-RULE-001' | 'SEC-RULE-002' | 'SEC-RULE-003' | 'SEC-RULE-004' | 'SEC-RULE-005';
    severity: 'FATAL' | 'CRITICAL' | 'MAJOR';
    location: {
      filePath: string;
      startLine?: number;
      endLine?: number;
    };
    vulnerabilityType: string;
    description: string;
    sanitizedSnippet: string; // Redacted snippet for audit trail
    remediationAction: string;
  }>;
}
```

### 4.2 Security Check Result Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SecurityCheckResult",
  "type": "object",
  "required": [
    "checkerId",
    "artifactId",
    "timestamp",
    "passed",
    "threatSummary",
    "vulnerabilities"
  ],
  "properties": {
    "checkerId": { "type": "string", "enum": ["CHECKER-SECURITY"] },
    "artifactId": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "passed": { "type": "boolean" },
    "threatSummary": {
      "type": "object",
      "required": ["strideCategoryCounts", "totalVulnerabilitiesFound"],
      "properties": {
        "strideCategoryCounts": { "type": "object" },
        "totalVulnerabilitiesFound": { "type": "integer" }
      }
    },
    "vulnerabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["ruleId", "severity", "location", "vulnerabilityType", "description"],
        "properties": {
          "ruleId": {
            "type": "string",
            "enum": ["SEC-RULE-001", "SEC-RULE-002", "SEC-RULE-003", "SEC-RULE-004", "SEC-RULE-005"]
          },
          "severity": { "type": "string", "enum": ["FATAL", "CRITICAL", "MAJOR"] },
          "vulnerabilityType": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 5. System Configuration

```yaml
security_checker:
  enabled: true
  entropy_threshold: 4.5 # Shannon entropy threshold for secret scanning
  pii_detection:
    scrub_in_reports: true
    detector_model: "ner_pii_v2"
  prompt_injection_detector:
    confidence_threshold: 0.85
  blocked_functions: ["eval", "exec", "child_process", "system", "fs.unlinkSync"]
```

---

## 6. Verification & Safety Criteria

- **Zero Exposure**: 100% detection of hardcoded AWS/GitHub API keys in code or configuration files.
- **Prompt Injection Defense**: Must catch 100% of benchmark injection vectors (Jailbreak, Persona Switch, System Prompt Override).
