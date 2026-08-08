# Recovery Workflow (SOP-009: Failure, Retry, Recovery & Rollback)

## Purpose
Defines the standard procedure for handling failures, retries, recovery, and rollback across all agent tasks.

## Trigger
- Any task reaching a FAILED, BLOCKED, TIMEOUT, or RETRYING state
- Any `security.violation.detected` or `policy.violation.detected` event

## Step-by-Step Procedure

### Step 1: Detect Failure
- A04 (Scheduler) or A11 (Observability) detects failure condition
- Classify failure type immediately (see decision tree below)

### Step 2: Classify Failure Type

#### Transient Error
- Condition: Network timeout, rate limit, temporary service unavailability
- Action: Retry with exponential backoff
- Max retries: 3
- Backoff schedule: 1min → 5min → 15min

#### Dependency Failure
- Condition: Required artifact or service unavailable
- Action: Mark as WAITING_DEPENDENCY
- If dependency recovers within SLA: resume automatically
- If dependency does not recover: escalate to A00

#### Timeout
- Condition: Task exceeded time_budget_minutes_per_task
- Action: Check if retry budget available
- If retry allowed: retry with exponential backoff
- If retry budget exhausted: cancel or escalate

#### Policy Violation
- Condition: A08 detected policy rule violation
- Action: HALT immediately
- Action: Escalate to A08 (Policy Agent) and A00
- No retry permitted for policy violations

#### Security Violation
- Condition: A09 detected security issue
- Action: HALT ALL RELATED TASKS immediately
- Action: Escalate to Sev-1 — incident owner, A09, A05-SEC
- No retry permitted — human review required

#### Invalid Code or Artifact
- Condition: Self-validation or verification found unacceptable output
- Action: Send required fixes to A06
- If fixes applied and resubmitted: re-run verification
- If fixes rejected twice: reject task, escalate to Domain Authority

### Step 3: Resume from Checkpoint
- If checkpoint exists for the failed task: reload state from checkpoint
- Resume execution from last valid checkpoint
- Publish resumed execution events

### Step 4: Rollback (if needed)
- Identify all changes made by the failed task
- Reverse changes in reverse dependency order
- Validate rollback success (check system state matches pre-task state)
- Publish `release.failed` if deployment was in progress
- Generate rollback report

### Step 5: Publish Recovery Events
- Publish `retry.requested`, `escalation.raised`, or `release.failed` as appropriate
- Update task state in orchestrator

### Step 6: Generate Incident Report
- Document: failure type, root cause, impact, recovery actions, outcome
- Store in Artifact Store
- Feed to A12 (Learning Agent) for pattern analysis

## Exit Criteria
- Task is recovered (retry succeeds), cancelled, escalated, or rolled back
- Root cause captured in incident report
- All recovery events published to Event Bus

## Quality Gate
- No task may remain in BLOCKED or FAILED state without an active recovery action
