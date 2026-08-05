# Release Workflow (SOP-008: Release & Deployment)

## Purpose
Defines the standard release and deployment procedure for approved artifacts.

## Trigger
- Event: `decision.generated` with approval_status = approved
- Precondition: Human approval obtained (if risk level requires it)

## Prerequisites
- Artifact approved by A08
- Rollback plan documented and validated
- Environment configuration available
- Health checks defined
- Monitoring active

## Step-by-Step Procedure

### Step 1: Confirm Approval
- Verify approval recorded in Audit Log with artifact version reference
- Confirm rollback plan exists and has been tested
- Verify human approval obtained if risk level is HIGH or CRITICAL

### Step 2: Package Artifacts
- Bundle all approved artifacts into versioned release package
- Sign release package with release ID and timestamp
- Record package manifest in Version Manager

### Step 3: Validate Release Readiness
- Check all policies in policies/release_policies.yaml pass
- Verify no unresolved critical findings exist
- Confirm monitoring and alerting are active for target environment
- Generate release readiness report

### Step 4: Select Deployment Strategy
| Risk Level | Strategy |
|---|---|
| Low | Direct deployment after automated approval |
| Medium | Canary rollout (5% → 25% → 100%) |
| High | Blue/Green with human approval at each stage |
| Critical | Blue/Green with multiple human approvals |

### Step 5: Deploy
- Publish `release.started`
- Execute deployment to target environment
- Monitor deployment events in real-time
- A11 tracks all deployment metrics

### Step 6: Run Health Checks
- Execute all defined health checks immediately post-deployment
- Health checks must all pass before declaring release complete
- If any health check fails: trigger rollback automatically

### Step 7: Validate Release
- Run post-deployment validation suite
- Verify all acceptance criteria still met in production environment
- Compare key metrics against pre-deployment baseline

### Step 8: Publish Release Report
- Generate release notes with: scope, risks, rollback, and validation results
- Record release audit log entry
- Publish `release.completed` event
- Activate ongoing monitoring via A11

## Exit Criteria
- Release successfully deployed
- All health checks passed
- Release validated
- Monitoring active
- Rollback path confirmed available
- Release notes complete
- Audit log entry recorded

## Failure Handling
- Health check failure: Trigger automatic rollback
- Rollback failure: Escalate to A11 and human incident owner at Sev-1
- Validation failure: Rollback, generate incident report

## Quality Gate
- Gate 6: Release Gate
