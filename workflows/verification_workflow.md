# Verification Workflow (SOP-006: Verification & Policy Validation)

## Purpose
Defines the standard procedure for independently verifying artifacts and generating governance-aware decisions.

## Trigger
- Event: `self_validation.completed` from Worker Agent (A06)
- Or: `verification.requested` from Orchestrator (A00)

## Prerequisites
- Artifact submitted to Artifact Store with complete metadata
- Self-validation report available
- Verification context package available from A02
- All 10 verification modules configured and ready

## Step-by-Step Procedure

### Step 1: Receive Artifact
- A07 receives `verification.requested` event
- Load artifact and verification context from A02
- Load acceptance criteria from task charter
- State transition: Submitted → Under Review

### Step 2: Run Verification Modules
Run all 10 modules in parallel where possible:
1. **Accuracy Verifier**: Cross-reference facts with knowledge base
2. **Standards Verifier**: Check against coding, architecture, and documentation standards
3. **Dependency Verifier**: Validate all declared dependencies
4. **Completeness Verifier**: Check all acceptance criteria are addressed
5. **Risk Verifier**: Verify risks are documented with mitigations
6. **Consistency Verifier**: Check internal consistency and cross-artifact consistency
7. **Conflict Detector**: Detect conflicts with existing approved artifacts
8. **Security Verifier**: Scan for secrets, vulnerabilities, unauthorized access
9. **Performance Verifier**: Validate performance expectations are addressed
10. **Compliance Verifier**: Check regulatory and policy compliance
- State transition: Under Review → Verification Running

### Step 3: Calculate Scores
- Quality Score (0.0–1.0): Weighted aggregate of module pass rates
- Confidence Score (0.0–1.0): Based on evidence completeness and source authority
- Risk Score (low/medium/high/critical): Based on findings severity and impact
- State transition: Verification Running → Quality Scoring

### Step 4: Policy Validation
- Send verification report to A08 (Policy Agent)
- A08 evaluates all 10 policy categories
- A08 generates final decision
- State transition: Quality Scoring → Policy Validation → Decision Generated

### Step 5: Generate Verification Report
- Compile all module results, scores, findings, and evidence
- Generate required fixes list (if any)
- Generate recommendations list
- Produce approval status recommendation
- Publish `verification.completed`

## Decision Outcomes
| Outcome | Condition | Next Action |
|---|---|---|
| Approved | All scores pass, no critical findings | Proceed to release |
| Conditionally Approved | Minor gaps, fixable issues | Return required fixes to A06 |
| Rejected | Score thresholds not met, critical findings | Generate rejection report |
| Escalated | Policy conflict or risk exceeds threshold | Route to A13 for human approval |

## Exit Criteria
- All 10 verification modules executed
- Quality score >= 0.85
- Confidence score >= 0.80
- Risk score <= medium
- Zero critical or high security findings
- Verification report published
- Decision recommendation sent to A08

## Failure Handling
- Missing evidence: Request from A03, escalate to A00 if unavailable
- Security finding: Immediate escalation to A09
- Compliance failure: Immediate escalation to A05-DATA and A05-GOV

## Quality Gate
- Gate 4: Verification Gate
