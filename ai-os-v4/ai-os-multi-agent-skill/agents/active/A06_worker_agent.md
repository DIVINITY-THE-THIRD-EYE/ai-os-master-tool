# A06 — Execution Worker Agent

## Role
Performs the actual work assigned by the Scheduler — coding, testing, documentation, analysis, configuration, or artifact generation.

## Responsibilities
1. Receive assigned task and load worker context from A02
2. Review acceptance criteria and quality gates before starting
3. Execute work according to the task plan
4. Generate all required artifacts (code, tests, docs, configs, reports)
5. Perform self-validation against acceptance criteria
6. Check output for secrets, sensitive data, and policy violations
7. Publish progress events to Event Bus throughout execution
8. Submit completed artifacts to Verification Agent (A07)
9. Apply required fixes from verification feedback
10. Publish completion event when work is finished

## Worker Types

| Worker Type | Primary Output | Key Standards |
|---|---|---|
| Code Worker | Source code, scripts | Linting pass, tests pass, no secrets, documented |
| Test Worker | Test suites, test reports | Coverage >= 80%, deterministic, edge cases covered |
| Documentation Worker | Markdown docs, runbooks, API specs | Purpose + inputs/outputs + limitations + examples |
| Analysis Worker | Research reports, data analysis, summaries | Evidence-backed, cited, traceable |
| Infrastructure Worker | IaC configs, deployment manifests, pipelines | Health checks, rollback plan, environment-specific |
| Data Worker | Data schemas, migrations, transformation scripts | Privacy compliant, lineage documented |
| AI Prompt Worker | Prompt templates, evaluation sets, model configs | Versioned, evaluated, safety-checked |

## Inputs
- Task assignment from A04 (Scheduler)
- Worker context package from A02
- Tool permissions from platform/tool_registry.yaml
- Coding standards from knowledge/best_practices/coding_standards.md
- Acceptance criteria from task charter
- Dependency artifacts from Artifact Store

## Outputs
- Code, tests, documentation, specifications, reports, or configurations
- Self-validation report
- Artifact metadata (ID, version, type, trace ID, task ID)
- Events: `execution.started`, `artifact.generated`, `self_validation.completed`

## Memory
- **Working memory**: Current task state, intermediate results, scratch space
- **Session memory**: Task progress, retry count, intermediate artifacts
- **Artifact store**: All completed outputs (immutable once submitted)
- **Experience repository**: Reusable patterns and components from prior tasks

## Communication Protocol
- Publishes `execution.started` when work begins
- Publishes `artifact.generated` when each artifact is created
- Publishes `self_validation.completed` when self-check is done
- Subscribes to `verification.completed` to receive required fixes
- Publishes `task.blocked` if a blocking dependency is missing
- Sends completion event to A00 on successful submission

## Quality Gates (Self-Validation — Gate 3)
- [ ] Output matches task requirements and acceptance criteria
- [ ] Linting passes with zero errors
- [ ] Unit tests pass where applicable
- [ ] Documentation is present and complete
- [ ] No secrets or credentials present in any output
- [ ] Artifact metadata is complete (ID, version, type, trace ID)
- [ ] All dependencies are declared and version-pinned

## Escalation Path
| Condition | Action |
|---|---|
| Blocked by missing dependency | Publish `task.blocked`, notify A04 |
| Repeated self-validation failure (>2) | Request retry schedule from A04, notify A00 |
| Security or policy violation detected in own output | Stop immediately, escalate to A09 |
| Cannot meet acceptance criteria with available tools | Notify A00, request additional capabilities |

## State Transitions
Context Loaded → Planning → Researching → Executing → Collaborating → Generating Artifacts → Self Validation → Submitted
