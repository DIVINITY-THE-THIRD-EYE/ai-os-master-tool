# AI OS v4 Multi-Agent Business Rules (`business_rules.md`)

## 1. Executive Summary

Business rules encapsulate domain logic, service level agreements (SLAs), operational constraints, financial limits, customer entitlements, and workflow priority handling within the AI OS v4 platform. All autonomous agents must validate and respect these rules during plan generation, workflow execution, and artifact delivery.

---

## 2. Business Rule Specifications

### Rule BUS-001: Execution SLA Limits by Task Severity
- **Rule ID**: `BUS-001`
- **Severity**: `HIGH`
- **Scope**: Task Scheduler & Orchestrator (A01)
- **Description**: Tasks must complete within declared SLA duration bounds based on priority tier.
- **SLA Bounds Table**:
  | Priority Tier | Target SLA | Max Timeout | Max Retry Attempts | Escalation Trigger |
  |---|---|---|---|---|
  | `P0_CRITICAL` | 5 minutes | 15 minutes | 3 retries | Immediate notification to Lead Engineer & Master |
  | `P1_HIGH` | 30 minutes | 2 hours | 2 retries | Escalate to Lead Engineer on 2nd failure |
  | `P2_MEDIUM` | 4 hours | 12 hours | 2 retries | Escalate on 2nd failure |
  | `P3_LOW` | 24 hours | 72 hours | 1 retry | Log failure to task report |

### Rule BUS-002: Feature Flag & Capability Gating
- **Rule ID**: `BUS-002`
- **Severity**: `HIGH`
- **Scope**: All Agents & Workflows
- **Description**: Agents must verify that a requested capability or feature module is explicitly enabled in `platform/feature_flags.yaml` before initiating execution.
- **Validation Protocol**:
  ```python
  def is_feature_enabled(feature_key: str, tenant_context: dict) -> bool:
      if not feature_flags.get(feature_key, False):
          raise FeatureGatedException(f"Feature '{feature_key}' is disabled for tenant '{tenant_context.get('tenant_id')}'")
      return True
  ```

### Rule BUS-003: Operational Cost & Token Budget Caps
- **Rule ID**: `BUS-003`
- **Severity**: `CRITICAL`
- **Scope**: All Task Execution Engines
- **Description**: Every workflow execution is assigned a maximum cost ceiling (USD/Tokens). If cumulative cost reaches 90% of the ceiling, warning `EVT_BUS_BUDGET_WARNING` is emitted. If 100% is reached, execution halts for approval.
- **Cost Allocation Budget**:
  - `Standard Development Workflow`: $2.50 USD / 2,500,000 tokens
  - `Deep Research & Architecture Workflow`: $10.00 USD / 10,000,000 tokens
  - `Emergency Incident Fix`: $5.00 USD / 5,000,000 tokens

### Rule BUS-004: Tenant Data Isolation & Boundary Safeguards
- **Rule ID**: `BUS-004`
- **Severity**: `CRITICAL`
- **Scope**: Memory Engine & Knowledge Graph
- **Description**: Cross-tenant data contamination is strictly prohibited. Agent memory, persistent storage, and intermediate prompt context must be segmented by `tenant_id`.
- **Validation**: Queries to the Knowledge Base MUST include `WHERE tenant_id = :active_tenant`.

### Rule BUS-005: Minimum Artifact Quality Standard for Delivery
- **Rule ID**: `BUS-005`
- **Severity**: `HIGH`
- **Scope**: Quality Assurance Agent (A06), Release Manager (A10)
- **Description**: Artifacts delivered to end users must pass minimum quality metrics:
  - Code test coverage $\ge 85\%$
  - Zero `CRITICAL` or `HIGH` static security vulnerabilities.
  - Zero syntax/formatting errors in generated documentation.

### Rule BUS-006: Operational Error Budget Handling
- **Rule ID**: `BUS-006`
- **Severity**: `MEDIUM`
- **Scope**: Release Workflow & Deployment Gates
- **Description**: If the rolling 30-day error rate for production workflows exceeds `0.5%`, automated deployments are locked (`STRICT_DEPLOYMENT_FREEZE`) until root cause remediation is validated by `A11 (Incident Responder)`.

### Rule BUS-007: Mandatory Change Window Constraints
- **Rule ID**: `BUS-007`
- **Severity**: `HIGH`
- **Scope**: Production Release Workflow
- **Description**: Production releases must occur within approved deployment windows unless classified as a `P0_CRITICAL` emergency patch.
- **Standard Windows**: Monday–Thursday, 02:00 UTC to 06:00 UTC. Blackout on Fridays, weekends, and statutory holidays.

### Rule BUS-008: Depreciation & Backward Compatibility SLA
- **Rule ID**: `BUS-008`
- **Severity**: `MEDIUM`
- **Scope**: System Architect (A03), API Design
- **Description**: Any public API endpoint or schema property marked `@deprecated` must remain functional and supported for a minimum of 180 days (6 months) before complete sunset.

### Rule BUS-009: Data Retention & Automated Purge Rules
- **Rule ID**: `BUS-009`
- **Severity**: `HIGH`
- **Scope**: Session & Persistent Memory
- **Description**: Transient execution logs, intermediate token caches, and raw prompt context must be purged after 90 days. Audit trails and final verification attestations are retained for 7 years.

### Rule BUS-010: Third-Party Service Dependency Validation
- **Rule ID**: `BUS-010`
- **Severity**: `HIGH`
- **Scope**: Execution Engine & Sandbox
- **Description**: Before starting a workflow that relies on external REST/gRPC endpoints, the Runtime Manager must perform a health check ping. If external uptime is $< 99.0\%$, the workflow enters a `WAIT_DEPENDENCY` backoff state.
