# Execution Workflow (SOP-004: Parallel Execution)

## Purpose
Defines the standard parallel execution procedure for Worker Agents (A06) once the Scheduler (A04) has assigned tasks.

## Trigger
- Event: `task.assigned` received by Worker Agent
- Precondition: Execution plan approved, context ready, budgets available

## Prerequisites
- Worker Agent is in READY state in Agent Registry
- Worker context loaded from A02
- Task assignment contains: task_id, acceptance_criteria, tool_permissions, dependencies
- All upstream dependency artifacts are available in Artifact Store

## Step-by-Step Procedure

### Step 1: Load Context
- Worker receives `task.assigned` event
- Worker requests worker context package from A02
- Verify context is permission-checked and within token budget
- State transition: Assigned → Context Loaded

### Step 2: Review Acceptance Criteria
- Worker reads all acceptance criteria from task charter
- Worker identifies which verification module each criterion maps to
- Worker plans execution approach to satisfy all criteria
- State transition: Context Loaded → Planning

### Step 3: Research (if needed)
- Query A03 for relevant rules, standards, and best practices
- Retrieve any reusable components from Experience Repository
- State transition: Planning → Researching → Executing

### Step 4: Execute Work
- Perform assigned task according to worker type:
  - Code Worker: Write code following coding standards
  - Test Worker: Write and run test suites
  - Documentation Worker: Produce structured documentation
  - Analysis Worker: Produce research or analysis reports
  - Infrastructure Worker: Produce IaC configs and deployment manifests
- Publish `execution.started` event at start of work
- Publish progress events at significant milestones
- State transition: Executing → Collaborating (if needed) → Generating Artifacts

### Step 5: Collaborate (if needed)
- If another worker's output is needed, request via Event Bus
- Publish `dependency.blocked` if blocking dependency unavailable
- Resume execution when dependency artifact becomes available

### Step 6: Generate Artifacts
- Produce all required output artifacts
- Attach complete metadata: artifact_id, type, version, trace_id, task_id
- Store in Artifact Store immediately upon creation
- Publish `artifact.generated` for each artifact created

### Step 7: Self-Validation
- Check output against all acceptance criteria
- Run linting (zero errors required)
- Run applicable unit tests
- Scan for secrets and sensitive data
- Verify documentation completeness
- Produce self-validation report
- Publish `self_validation.completed`
- State transition: Generating Artifacts → Self Validation → Submitted

## Parallel Execution Management
- A04 identifies independent branches in the DAG
- Each branch executes concurrently up to max_parallel_workers_per_task (5)
- Budget consumption monitored per branch
- Branch exceeding budget is throttled immediately
- Artifacts merged only after all branch verifications pass
- Integration verification runs after merge

## Exit Criteria
- All assigned tasks completed or explicitly blocked with reason
- All artifacts submitted to Artifact Store with complete metadata
- Self-validation report produced for each artifact
- All progress events published to Event Bus
- No secrets present in any output

## Failure Handling
- If self-validation fails: retry up to 2 times before escalating
- If dependency unavailable: publish `dependency.blocked`, notify A04
- If security violation detected: stop immediately, publish `security.violation.detected`
- If budget exceeded: publish `budget.exceeded`, await scheduler decision

## Related Agents
- A04 (Scheduler): assigns tasks and monitors budget
- A02 (Context Agent): provides worker context
- A03 (Knowledge Agent): provides rules and best practices
- A07 (Verification Agent): receives submitted artifacts

## Events Published
- `execution.started`, `artifact.generated`, `self_validation.completed`, `task.blocked`, `budget.exceeded`

## Quality Gate
- Gate 3: Worker Self-Validation Gate
