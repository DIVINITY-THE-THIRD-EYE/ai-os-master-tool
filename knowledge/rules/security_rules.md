# AI OS v4 Multi-Agent System Security Rules (`security_rules.md`)

## 1. Zero-Trust Security Paradigm

AI OS v4 operates under a strict **Zero-Trust Security Architecture**. No agent, workflow, user prompt, or third-party integration is intrinsically trusted. All inter-agent messages, file access attempts, tool invocations, and code generations must be authenticated, authorized, sanitized, and audited.

---

## 2. Security Rule Specifications

### Rule SEC-001: Absolute Prohibition of Hardcoded Credentials
- **Rule ID**: `SEC-001`
- **Severity**: `CRITICAL`
- **Scope**: All Source Code, Prompts, Artifacts, Configs, Logs
- **Description**: Plaintext API keys, passwords, private keys, database credentials, or secret tokens MUST NEVER be present in source files, prompts, or commits.
- **Enforcement**: Mandatory pre-commit static scan using regex patterns for high-entropy strings, AWS keys, JWTs, and RSA keys.
- **Remediation**: Violations fail verification immediately and trigger secret rotation procedures.

### Rule SEC-002: Defense-in-Depth Prompt Injection Prevention
- **Rule ID**: `SEC-002`
- **Severity**: `CRITICAL`
- **Scope**: All Inbound Prompts & External Inputs
- **Description**: All user inputs and untrusted data sources must pass through multi-layer prompt injection detection filters before reaching LLM execution contexts.
- **Validation Pipeline**:
  ```python
  def sanitize_input_prompt(raw_prompt: str) -> str:
      # Step 1: Detect system prompt override attempts
      injection_patterns = [
          r"ignore previous instructions",
          r"system prompt override",
          r"you are now DAN",
          r"reveal your system prompt"
      ]
      for pattern in injection_patterns:
          if re.search(pattern, raw_prompt, re.IGNORECASE):
              raise PromptInjectionException(f"Prompt injection pattern detected: {pattern}")
      
      # Step 2: Escape delimiter tokens
      sanitized = raw_prompt.replace("<|im_start|>", "").replace("<|im_end|>", "")
      return sanitized
  ```

### Rule SEC-003: Cryptographic Standards & Key Management
- **Rule ID**: `SEC-003`
- **Severity**: `CRITICAL`
- **Scope**: Data Encryption at Rest & In Transit
- **Description**: All cryptographic operations must adhere to approved algorithms. Deprecated cipher suites are rejected.
- **Approved Suite**:
  - Symmetric Encryption: `AES-256-GCM` or `ChaCha20-Poly1305`
  - Asymmetric Encryption / Signatures: `Ed25519` or `RSA-4096`
  - Hashing: `SHA-256`, `SHA-512`, `BLAKE3`
  - TLS Protocol: `TLS 1.3 mandatory`

### Rule SEC-004: Role-Based & Attribute-Based Access Control (RBAC/ABAC)
- **Rule ID**: `SEC-004`
- **Severity**: `CRITICAL`
- **Scope**: Tool Execution & Resource API Access
- **Description**: Agent permissions are validated dynamically using fine-grained RBAC/ABAC policies.
- **Policy Check Table**:
  | Agent Role | File Read | File Write | Code Execute | Network Access | Admin Ops |
  |---|---|---|---|---|---|
  | `A05 (CodeImplementer)` | Workspace Only | Targeted File | Sandbox Only | Local/Whitelisted | Prohibited |
  | `A07 (SecurityAuditor)`| Read-All | Audit Dir Only| Read-Only Scan | Whitelisted Scanners| Prohibited |
  | `A10 (ReleaseManager)` | Read-All | Dist/Build Dir| Build Tools Only | Deployment Endpoints | Conditional |

### Rule SEC-005: Sandboxed Code Execution Boundaries
- **Rule ID**: `SEC-005`
- **Severity**: `CRITICAL`
- **Scope**: Code Implementer (A05), QA (A06)
- **Description**: Generated code and tests MUST BE executed strictly within containerized, ephemeral sandboxes (e.g., Docker / gVisor / WebAssembly) with restricted resources:
  - Network isolation: No internet access during build/test unless explicitly whitelisted.
  - Storage isolation: Ephemeral tmpfs mounted read-only except designated workspace.
  - Timeout: Hard limit of 180 seconds per execution block.

### Rule SEC-006: Data Anonymization & PII Sanitization
- **Rule ID**: `SEC-006`
- **Severity**: `HIGH`
- **Scope**: Logging Engine, Telemetry, Memory System
- **Description**: Personally Identifiable Information (PII) including emails, IP addresses, full names, credit card numbers, and SSNs must be redacted or pseudonymized prior to persisting into log files or LLM context stores.

### Rule SEC-007: Supply Chain Dependency Vulnerability Scanning
- **Rule ID**: `SEC-007`
- **Severity**: `HIGH`
- **Scope**: Software Artifacts & Package Manifests
- **Description**: Any third-party dependency introduced by `A04` or `A05` must be scanned via vulnerability database lookup (CVE/GHSA).
- **Threshold**: Zero dependencies with `CVSS score >= 7.0` (High/Critical) are allowed into the build manifest.

### Rule SEC-008: Secure Inter-Agent Transport Security (mTLS)
- **Rule ID**: `SEC-008`
- **Severity**: `HIGH`
- **Scope**: Message Router & Event Bus
- **Description**: Remote or distributed agent communication channels must utilize mutual TLS (mTLS) with short-lived X.509 certificates to verify peer identity and encrypt payload traffic.

### Rule SEC-009: Least-Privilege Directory Workspace Scoping
- **Rule ID**: `SEC-009`
- **Severity**: `HIGH`
- **Scope**: File I/O Tools (`view_file`, `write_to_file`, `replace_file_content`)
- **Description**: Agents may only write to paths within their explicitly assigned working directory tree. Writing to system directories (`/etc`, `C:\Windows`, root paths outside workspace) is blocked by default.

### Rule SEC-010: Security Attestation & Signed Handoffs
- **Rule ID**: `SEC-010`
- **Severity**: `CRITICAL`
- **Scope**: All Handoff Reports (`handoff.md`)
- **Description**: Every agent handoff package must contain an cryptographic verification hash. The Security Auditor (A07) must sign off on high-risk handoffs prior to execution stage transition.
