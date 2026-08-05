# Code Review Workflow Specification

## 1. Purpose & Objective
Inspect pull request diffs for logic bugs, security vulnerabilities, performance flaws, test coverage, and code style compliance.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Open Pull Request (PR), automated CI status checks (passing), static analysis report.
- **Trigger Conditions**: Developer submission of PR for peer review.

## 3. Participating Agent Roles & Responsibilities
- **Code Reviewer**: Inspects PR diff, evaluates design patterns, requests changes or approves PR.
- **Security Analyst**: Validates input sanitization, authentication checks, and dependency security.
- **QA Specialist**: Verifies PR includes appropriate unit/integration tests for modified functionality.

## 4. Step-by-Step Execution Sequence

### Step 1: Automated Pre-Check Verification
- **Inputs**: PR metadata, CI build status, linter output.
- **Actions**: Verify CI build status is green, confirm no merge conflicts exist, check linter and coverage reports.
- **Outputs**: Pre-Review Status Verification Log.
- **Verification**: CI build green and minimum 80% diff line coverage.

### Step 2: Structural & Design Pattern Inspection
- **Inputs**: PR code diff, codebase architectural guidelines.
- **Actions**: Inspect modularity, naming conventions, separation of concerns, DRY principles, and abstraction layers.
- **Outputs**: Code Review Comments (Line-by-Line).
- **Verification**: Zero architectural violations identified in diff.

### Step 3: Logic & Edge Case Validation
- **Inputs**: PR code diff, feature specification.
- **Actions**: Verify handling of null/empty inputs, boundary conditions, error handling, and concurrency locks.
- **Outputs**: Logic Verification Notes.
- **Verification**: All edge cases properly handled with defensive code checks.

### Step 4: Security & Performance Audit
- **Inputs**: PR code diff, OWASP guidelines, database queries.
- **Actions**: Audit SQL queries for injection risk, inspect memory allocation, verify auth checks on new endpoints.
- **Outputs**: Security & Performance Audit Notes.
- **Verification**: Zero security flaws or N+1 database query patterns.

### Step 5: Approval Sign-Off & PR Merge Clearance
- **Inputs**: Resolved reviewer comments, updated PR branch.
- **Actions**: Confirm all reviewer comments resolved, verify final green CI build, approve PR for merge.
- **Outputs**: PR Approval Status & Merge Authorization.
- **Verification**: Minimum 2 peer approvals recorded on Git host.

## 5. Decision Gates & Branching Rules
- Gate 1: CI status check must be 100% green before peer reviewer opens PR.
- Gate 2: All reviewer requested changes must be resolved before PR approval.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: PR diff too large (> 500 lines) -> Action: Request author split PR into smaller, atomic pull requests.
- Failure Mode 2: Unresolved comment dispute -> Action: Escalate to Tech Lead for final arbitration.

## 7. Artifact Delivery & Output Standard
Git Pull Request Thread, Resolved Review Comments, CI Status Check Logs, and Merged PR Commit Record.
