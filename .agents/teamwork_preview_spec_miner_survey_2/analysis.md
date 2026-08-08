# AI OS Master Tool — Agents, Workflows & Policies Specification Survey (Survey 2)

**Report Date**: 2026-08-08  
**Surveyor**: Specification Miner (Survey 2)  
**Target Repository**: `ai-os-v4/ai-os-multi-agent-skill/` and root repository `c:\Users\PC\OneDrive\Documents\Master tool`

---

## 1. Executive Summary & Mining Scope

This specification survey presents an exhaustive, evidence-backed inspection of the **13 Specialized Agents (A01–A13)**, **6 Core Workflow Specifications**, **6 Policy Frameworks**, **8 Quality Gates**, **10 Verification Modules**, **31 Event Topics**, and **2 JSON Schemas** within the AI OS Master Tool repository.

All findings are mapped directly to concrete code locations (`runtime/*.py`, `api/index.py`, `tools/*.py`) or specification files (`agents/active/*.md`, `workflows/`, `policies/`, `quality/`, `events/`).

---

## 2. 13-Agent System Inventory (A01–A13)

| # | Agent ID | Agent Name | Primary Role | Trigger Events / Prompts | Key Capabilities | Code & Spec Backing | Implementation Status |
|---|---|---|---|---|---|---|---|
| 1 | **A01** | Intake & Requirements Agent | Converts raw user prompts/payloads into structured task charters with risk classification & acceptance criteria. | `task.created` | `task_intake`, `requirements_analysis`, risk classification, missing field detection | `agents/active/A01_intake_requirements_agent.md`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-1.5-pro`) | ✅ Implemented |
| 2 | **A02** | Context & Memory Agent | Assembles, compresses, ranks, filters, and publishes permissioned context snapshots for agents. | `task.intake.completed`, `knowledge.retrieved` | `context_retrieval`, `working_memory`, token budget optimization, sensitive data filtering | `agents/active/A02_context_memory_agent.md`, `runtime/memory_manager.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-2.0-flash`) | ✅ Implemented |
| 3 | **A03** | Knowledge Graph & Research Agent | Queries ontology, rules, SOPs, lessons learned, and anti-patterns; provides citations & evidence. | Context assembly queries, candidate knowledge from A12 | `knowledge_graph`, `ontology_mapping`, rule lookup, citation generation | `agents/active/A03_knowledge_graph_agent.md`, `runtime/memory_manager.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-1.5-pro`) | ✅ Implemented |
| 4 | **A04** | Scheduler, Dependency & Resource Agent | Builds DAGs, detects circular dependencies, allocates budgets, manages priority queues & retries. | `plan.proposed`, `dependency.blocked`, progress events | `dag_scheduling`, `workflow_planning`, worker pool allocation, exponential backoff | `agents/active/A04_scheduler_agent.md`, `runtime/workflow_executor.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-2.0-flash`) | ✅ Implemented |
| 5 | **A05** | Domain Authority Agent Family | Specialized expert authority enforcing domain standards, architecture rules, and approving domain work (9 sub-authorities). | Domain-relevant event signals, worker draft submissions | `architecture_design`, `domain_governance`, domain standards enforcement (Product, FE, BE, AI, QA, SEC, DATA, OPS, GOV) | `agents/active/A05_domain_authority_agent.md`, `runtime/agent_registry.py`, `api/index.py` (registered as `A05`), `runtime/llm_router.py` (`gpt-4o`) | 🟡 Partial / Experimental (Family spec defined for 9 sub-authorities; core `A05` registered in runtime) |
| 6 | **A06** | Execution Worker Agent | Performs actual task execution (code, tests, docs, analysis, IaC, data, prompts) & self-validation. | `task.assigned`, `verification.completed` (fix request) | `code_generation`, `task_execution`, multi-worker specialization, self-validation | `agents/active/A06_worker_agent.md`, `runtime/workflow_executor.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`claude-3-5-sonnet-20241022`) | ✅ Implemented |
| 7 | **A07** | Verification & Quality Agent | Independently checks accuracy, completeness, consistency, compliance, risk, security across 10 verifier modules. | `artifact.generated`, `verification.requested` | `quality_assurance`, `verification`, quality/confidence/risk scoring (0.0-1.0), required fix generation | `agents/active/A07_verification_agent.md`, `quality/verification_modules.yaml`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gpt-4o`) | ✅ Implemented |
| 8 | **A08** | Policy & Decision Intelligence Agent | Applies 10 policy categories to verification reports, evaluates conditions, and generates final governance decisions. | `verification.completed`, `plan.proposed` | `policy_evaluation`, `compliance_check`, approval status routing (Approved / Conditionally Approved / Rejected / Escalated) | `agents/active/A08_policy_decision_agent.md`, `policies/*.yaml`, `runtime/workflow_executor.py` (`ConditionEvaluator`), `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gpt-4o`) | ✅ Implemented |
| 9 | **A09** | Security & Compliance Agent | Enforces least privilege, RBAC, secret scanning, sandboxing high-risk tools, and audit logging. | Real-time tool calls, secret scanning triggers, permission checks | `security_audit`, `vulnerability_scan`, deny-by-default enforcement, secret leak detection | `agents/active/A09_security_compliance_agent.md`, `policies/security_policies.yaml`, `runtime/plugin_registry.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gpt-4o`) | ✅ Implemented |
| 10 | **A10** | Release & Deployment Agent | Manages release packaging, environment promotion, health validation, canary/blue-green rollouts, and rollbacks. | `decision.generated` (Approved) | `release_management`, `deployment`, rollback execution, release notes generation | `agents/active/A10_release_deployment_agent.md`, `policies/release_policies.yaml`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-2.0-flash`) | ✅ Implemented |
| 11 | **A11** | Observability & Operations Agent | Monitors system health, token usage, costs, queue depths, SLA compliance, and distributed tracing. | Continuous event bus telemetry, metric threshold checks | `monitoring`, `telemetry`, predictive SLA breach warning, disaster recovery trigger | `agents/active/A11_observability_operations_agent.md`, `runtime/managers/metrics_manager.py`, `runtime/managers/health_monitor.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-2.0-flash`) | ✅ Implemented |
| 12 | **A12** | Learning & Knowledge Publication Agent | Extracts lessons, anti-patterns, prompt optimizations from completed tasks and routes approved knowledge to graph. | Task completion, `verification.completed`, human feedback | `reflection`, `learning_opt`, candidate knowledge generation, knowledge publication pipeline | `agents/active/A12_learning_agent.md`, `quality/quality_gates.yaml` (Gate 7), `runtime/memory_manager.py`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`claude-3-5-sonnet-20241022`) | ✅ Implemented |
| 13 | **A13** | Human Collaboration Agent | Manages human approval/review queues, escalations, notifications, manual overrides, and approver SLA tracking. | `escalation.raised`, `human.approval.requested`, high-risk task triggers | `human_escalation`, `approval_gates`, approver SLA tracking, rationale logging | `agents/active/A13_human_collaboration_agent.md`, `workflows/canonical_workflow.yaml` (Gate 1 & 2), `policies/approval_policies.yaml`, `runtime/agent_registry.py`, `api/index.py`, `runtime/llm_router.py` (`gemini-1.5-pro`) | ✅ Implemented |

---

## 3. Workflow System Survey

The system defines 6 core workflows in `ai-os-v4/ai-os-multi-agent-skill/workflows/`:

### 3.1. Canonical Workflow (`canonical_workflow.yaml`)
- **Type**: Master 16-Step DAG Workflow
- **Triggers**: `task.created` via API (`POST /v1/tasks`) or CLI runner
- **Agent Coordination Pattern**: Sequenced DAG with parallel execution levels (`context_assembly` and `knowledge_retrieval` run in parallel; multi-worker execution runs in parallel under `A06`).
- **Key Steps & Branching**:
  1. `request_received` (Trigger)
  2. `intake` (A01) → Emits `task.intake.completed`
  3. `context_assembly` (A02) & `knowledge_retrieval` (A03) (Parallel)
  4. `planning` (A04) → Emits `plan.proposed`
  5. `policy_precheck` (A08) → Emits `plan.approved`
  6. `human_approval_gate_1` (A13) (Conditional: `risk_classification IN [high, critical]`)
  7. `scheduling` (A04) → Emits `task.scheduled`, `task.assigned`
  8. `parallel_execution` (A06) (Parallel worker threads: code, test, docs, analysis, infra)
  9. `verification` (A07) → Emits `verification.completed` (10 verifier modules)
  10. `policy_decision` (A08) → Emits `decision.generated` with branches:
      - `approved` → proceeds to `release`
      - `conditionally_approved` → loops back to `parallel_execution`
      - `rejected` → routes to `failure_report`
      - `escalated` → routes to `human_approval_gate_2`
  11. `human_approval_gate_2` (A13) (Conditional: `approval_status == escalated`)
  12. `release` (A10) → Emits `release.started`, `release.completed`
  13. `observability` (A11) → Emits `metrics.alert`, `sla.breach`
  14. `learning` (A12) → Emits `learning.candidate.generated`, `knowledge.published`
- **Implementation Status**: ✅ Implemented in `runtime/workflow_executor.py` and validated by `tools/validate_repository.py`.

### 3.2. Execution Workflow (`execution_workflow.md`)
- **Type**: Worker Task Execution Sub-Workflow
- **Triggers**: `task.assigned` event from A04 Scheduler
- **Coordination Pattern**: Parallel worker execution via `ThreadPoolExecutor` (max 5 parallel workers per `skill.yaml`).
- **Phases**: Load worker context → Review acceptance criteria → Perform work → Self-validation (Gate 3) → Submit artifacts to A07.
- **Retry Mechanism**: Exponential backoff schedule `[60s, 300s, 900s]` (1 min, 5 min, 15 min).
- **Implementation Status**: ✅ Implemented in `WorkflowExecutor._execute_with_retry`.

### 3.3. Verification Workflow (`verification_workflow.md`)
- **Type**: Quality Verification Sub-Workflow
- **Triggers**: `artifact.generated` or `verification.requested`
- **Coordination Pattern**: Pipeline execution across 10 verification modules (Accuracy, Standards, Dependency, Completeness, Risk, Consistency, Conflict, Security, Performance, Compliance).
- **Outputs**: Structured verification report, quality score (threshold >= 0.85), confidence score (threshold >= 0.80), risk score (max medium), required fixes list.
- **Implementation Status**: ✅ Implemented in `quality/verification_modules.yaml` and `WorkflowExecutor`.

### 3.4. Release Workflow (`release_workflow.md`)
- **Type**: Release & Deployment Sub-Workflow
- **Triggers**: `decision.generated` with status `approved`
- **Coordination Pattern**: Gate 6 check → Release packaging → Strategy selection (Canary 5%-25%-100%, Blue/Green, or Direct) → Environment promotion → Health check execution → Automatic rollback on failure.
- **Implementation Status**: ✅ Implemented in `policies/release_policies.yaml` and runtime persistence.

### 3.5. Recovery Workflow (`recovery_workflow.md`)
- **Type**: Resilience & Recovery Sub-Workflow
- **Triggers**: `task.failed`, process termination, state corruption, or DR activation
- **Coordination Pattern**: Checkpoint lookup → Step resumption → State restoration from VRAM snapshot / SQLite DB → Retries with exponential backoff.
- **Implementation Status**: ✅ Implemented in `runtime/managers/recovery_manager.py` & `WorkflowExecutor.resume_from_checkpoint`.

### 3.6. Learning Workflow (`learning_workflow.md`)
- **Type**: Knowledge Extraction & Reflection Sub-Workflow
- **Triggers**: Workflow completion (`release.completed` or task finalization)
- **Coordination Pattern**: Data collection → Pattern/anti-pattern mining → Candidate knowledge generation → Validation check → Governance approval → Knowledge Graph & Prompt Library publication.
- **Implementation Status**: ✅ Implemented in `quality/quality_gates.yaml` (Gate 7) & `runtime/memory_manager.py`.

---

## 4. Policies, Quality Gates, Schemas & Events Inventory

### 4.1. Policy Frameworks (`policies/`)

| Policy File | Policy ID | Scope | Rules Enforced | Enforcement Level |
|---|---|---|---|---|
| `governance_policies.yaml` | GOV-POLICY-001 | All agents & tasks | GOV-001 to GOV-006, BUS-001 to BUS-002 | Blocking |
| `security_policies.yaml` | SEC-POLICY-001 | All agents, artifacts, tools | SEC-001 to SEC-008 (Zero secrets, RBAC, least privilege, sandboxing) | Blocking |
| `compliance_policies.yaml` | CMP-POLICY-001 | All data operations | CMP-001 to CMP-005 (GDPR, SOC2 Type 2, ISO 27001, PII classification, 72h incident reporting) | Blocking |
| `release_policies.yaml` | REL-POLICY-001 | Release & deployment | REL-001 to REL-008 (Rollback plan required, human approval for high/critical risk, health check validation) | Blocking |
| `approval_policies.yaml` | APR-POLICY-001 | Approvals & escalations | APR-001 to APR-005 (Auto-approve low risk, human approval for high/critical/production/overrides, 30m approver SLA) | Blocking |
| `coding_policies.yaml` | COD-POLICY-001 | Code artifacts | COD-001 to COD-008 (Single responsibility, docstrings, no hardcoded secrets, >=80% test coverage, 0 lint errors) | Blocking |

### 4.2. Quality Gates (`quality/quality_gates.yaml`)

- **Gate 0: Task Registration Gate** (Phase: Intake | Agent: A01) — Clear objective, testable acceptance criteria, task taxonomy, risk assigned.
- **Gate 1: Planning Gate** (Phase: Planning | Agent: A04) — No circular dependencies in DAG, critical path identified, budgets allocated.
- **Gate 2: Policy Pre-Check Gate** (Phase: Pre-Execution | Agent: A08) — Governance, security, compliance policy pre-approval before work begins.
- **Gate 3: Worker Self-Validation Gate** (Phase: Execution | Agent: A06) — Linting pass, unit tests pass, no secrets, metadata complete.
- **Gate 4: Verification Gate** (Phase: Verification | Agent: A07) — All 10 verification modules execute, quality score >= 0.85, confidence >= 0.80, risk <= medium, 0 critical/high security findings.
- **Gate 5: Governance Decision Gate** (Phase: Governance | Agent: A08) — All 10 policy categories evaluated, rule IDs cited, human approval logged if required.
- **Gate 6: Release Gate** (Phase: Release | Agent: A10) — Approval confirmed, rollback plan tested, health checks defined, release notes complete.
- **Gate 7: Learning Gate** (Phase: Learning | Agent: A12) — Outcome recorded, candidate evidence-backed, approval received before publication.

### 4.3. 10 Verification Modules (`quality/verification_modules.yaml`)
1. **Accuracy Verifier**: Factual correctness against knowledge base.
2. **Standards Verifier**: Compliance with coding, architecture, docs standards.
3. **Dependency Verifier**: All dependencies exist, compatible, version-pinned.
4. **Completeness Verifier**: 100% of acceptance criteria met.
5. **Risk Verifier**: All risks documented with mitigations.
6. **Consistency Verifier**: Zero logical contradictions within/across artifacts.
7. **Conflict Detector**: Zero unresolved conflicts with approved artifacts.
8. **Security Verifier**: Zero secrets, zero critical/high vulnerabilities.
9. **Performance Verifier**: Performance benchmarks defined, no regressions.
10. **Compliance Verifier**: Regulatory frameworks (GDPR, SOC2, ISO) satisfied.

### 4.4. Numeric Scoring & Budget Thresholds (`quality/scoring_thresholds.yaml`)
- **Quality Score Min**: `0.85`
- **Confidence Score Min**: `0.80`
- **Max Allowed Risk**: `medium`
- **Min Test Coverage**: `0.80` (80%)
- **Max Lint Errors**: `0`
- **Token Budget per Task**: `100,000` tokens
- **Cost Budget per Task**: `$5.00` USD
- **Time Budget per Task**: `30` minutes
- **API Call Budget per Task**: `500` calls
- **Human Response SLA**: `30` minutes (auto-escalates on breach)

### 4.5. Event System & Schemas (`events/`)
- **Event Topics (`events/event_topics.yaml`)**: 31 registered topics including `task.created`, `task.intake.completed`, `context.ready`, `plan.proposed`, `plan.approved`, `task.scheduled`, `task.assigned`, `execution.started`, `artifact.generated`, `self_validation.completed`, `verification.requested`, `verification.completed`, `policy.violation.detected`, `security.violation.detected`, `budget.exceeded`, `dependency.blocked`, `retry.requested`, `escalation.raised`, `human.approval.requested`, `human.decision.received`, `decision.generated`, `release.started`, `release.completed`, `release.failed`, `learning.candidate.generated`, `knowledge.published`, `metrics.alert`, `sla.breach`, `bottleneck.detected`, `authority.review.completed`, `knowledge.retrieved`.
- **Event Payload Schema (`events/event_payload_schema.json`)**: Draft-07 JSON schema enforcing required fields: `event_id`, `trace_id`, `task_id`, `agent_id`, `event_type`, `timestamp`, `severity`.
- **Agent Handoff Schema (`events/handoff_schema.json`)**: Draft-07 JSON schema enforcing required fields: `handoff_id`, `trace_id`, `task_id`, `from_agent`, `to_agent`, `state`, `objective`, `acceptance_criteria`, `context_snapshot_id`, `required_decision`.

---

## 5. Runtime Architecture & Codebase Verification

The runtime implementation in `ai-os-v4/ai-os-multi-agent-skill/runtime/` provides python execution engines:

1. **`agent_registry.py` (`AgentRegistry`)**: Manages agent lifecycle (`registered` → `configured` → `ready` → `disabled` / `retired`), capacity filtering, health metrics, performance scoring.
2. **`capability_router.py` (`CapabilityRouter`)**: Thread-safe round-robin capability router matching task requirements to registered agents.
3. **`workflow_executor.py` (`WorkflowExecutor` & `ConditionEvaluator`)**: Executes DAG-based workflows, handles condition evaluation (`IN`, `==`, `!=`, `>=`, `<=`), manages `ThreadPoolExecutor` parallel steps, checkpointing, and exponential backoff retries.
4. **`llm_router.py` (`LLMRouter`)**: Multi-provider gateway for Gemini, OpenAI, and Anthropic Claude with deterministic mock fallback when API keys are absent. Features token and cost tracking.
5. **`event_bus.py` (`EventBus`)**: Pub-sub topic router with optional event history persistence and task ID filtering.
6. **`memory_manager.py` (`MemoryManager`)**: Manages working memory, persistent memory, and knowledge graph node/edge traversal.
7. **`bootstrap.py` & `persistence_coordinator.py`**: Composition root initializing SQLite database, Supabase configuration, VRAM memory image, snapshot engine, journal manager, and backup manager.
8. **`api_server.py` & `api/index.py`**: FastAPI server exposing endpoints `/v1/health`, `/v1/tasks`, `/v1/tasks/{task_id}`, `/v1/agents`, `/v1/events`, `/v1/usage`, mounted for serverless deployment on Vercel.

---

## 6. Discovered Features & Edge Cases

### Discovered Features
| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|---|---|---|---|---|---|---|
| 1 | Runtime | Deterministic LLM Mock Fallback | Allows offline testing without API keys | Any agent prompt | Pre-structured JSON response | Graceful fallback to mock response | `runtime/llm_router.py` |
| 2 | Runtime | Thread-Safe Round-Robin Routing | Concurrent safety for multi-threaded capability routing | Requested capability | Selected AgentRecord | Escalate to orchestrator if none available | `runtime/capability_router.py` |
| 3 | Runtime | VRAM Image Disk Flushing | In-memory database image flushed to disk on workflow finish | Workflow ID | Saved `.db` image | Log error, preserve runtime memory | `runtime/bootstrap.py`, `runtime/workflow_executor.py` |
| 4 | Security | Deny-by-Default Tool Whitelisting | Restricts agent tool invocations | Tool ID, agent ID, operation | `(allowed, reason)` | Reject unauthorized operations with audit log entry | `runtime/plugin_registry.py` |

### Edge Cases
| # | Feature | Input | Observed Behavior |
|---|---|---|---|
| 1 | Workflow Condition Evaluator | Missing key in condition evaluation string (e.g. `unknown_key == value`) | Defaults to `True` with warning log to prevent workflow deadlocks. |
| 2 | LLM Provider Fallback | Missing or invalid API key for primary model | Automatically cascades through Gemini → OpenAI → Anthropic → Mock without throwing unhandled exceptions. |
| 3 | DAG Dependency Resolution | Circular dependency declared in workflow steps (e.g. A depends on B, B depends on A) | `WorkflowExecutor._validate_dag` detects cycle via DFS and raises explicit `ValueError("Circular dependency detected")`. |
| 4 | Approver SLA Breach | Approver fails to respond within 30 minutes | Automatically triggers escalation to alternate approver via `APR-004` rule. |

---
*End of Survey 2 Report.*
