# Anti-Patterns Catalog

This catalog documents known harmful patterns that AI OS agents must avoid.

## AP-001: Secret in Output
**Pattern:** Including API keys, passwords, tokens, or credentials in any artifact, prompt, log, or report.
**Risk:** Critical — immediate security breach.
**Detection:** Secret scanner in Verification Module 8 (Security Verifier).
**Mitigation:** Use Secret Manager. Reference secrets by name only. Never pass secrets as values.

## AP-002: Silent Swallowing of Errors
**Pattern:** Catching exceptions without logging or re-raising.
**Risk:** High — failures become invisible, leading to data corruption or silent wrong outputs.
**Detection:** Static analysis check in Standards Verifier.
**Mitigation:** Always log errors with context. Always re-raise or handle explicitly.

## AP-003: Scope Creep
**Pattern:** Task expanding beyond its defined boundaries without explicit approval.
**Risk:** High — uncontrolled changes, budget overruns, unexpected side effects.
**Detection:** Completeness Verifier checks against original acceptance criteria.
**Mitigation:** Any scope change requires A00 approval before work continues.

## AP-004: Skipping Self-Validation
**Pattern:** Worker Agent submitting artifacts without running self-validation checks.
**Risk:** High — poor quality artifacts reach verification, wasting cycles.
**Detection:** Verification Agent checks for self-validation report presence.
**Mitigation:** Self-validation is mandatory per Gate 3. No submission without report.

## AP-005: Bypassing Verification Gate
**Pattern:** Moving artifact to release without completing all 10 verification modules.
**Risk:** Critical — defective, insecure, or non-compliant artifacts reach production.
**Detection:** Release policies check for verification completion record.
**Mitigation:** Verification is always mandatory. No release path bypasses Gate 4.

## AP-006: Context Pollution
**Pattern:** Including sensitive data, irrelevant content, or another agent's private context in shared context.
**Risk:** High — data leakage, confusion, and incorrect agent behavior.
**Detection:** Context Agent (A02) enforces permission boundaries before publishing.
**Mitigation:** A02 filters all context through permission and sensitivity checks.

## AP-007: Undocumented Risk
**Pattern:** Worker producing output that introduces risk without documenting the risk or mitigation.
**Risk:** High — risks remain unknown until they cause failures.
**Detection:** Risk Verifier module in A07.
**Mitigation:** All HIGH and CRITICAL risks must be documented with mitigations in the artifact.

## AP-008: Deploying Without Rollback Plan
**Pattern:** Executing a production deployment without a tested, documented rollback plan.
**Risk:** Critical — if deployment fails, recovery path is undefined.
**Detection:** Release Gate 6 blocks deployment without rollback plan.
**Mitigation:** Rollback plan must be documented and tested before any production deployment.

## AP-009: Publishing Unvalidated Knowledge
**Pattern:** Adding a lesson or best practice to the knowledge graph without validation and approval.
**Risk:** High — unvalidated knowledge can corrupt future agent behavior.
**Detection:** Learning Gate 7 enforces validation pipeline before publication.
**Mitigation:** All candidate knowledge must pass A07 quality check, A08 policy check, and Domain Authority approval.

## AP-010: Assuming Agent Availability
**Pattern:** Task scheduling assumes agents will be available without checking health status first.
**Risk:** Medium — tasks assigned to unhealthy agents fail and require retry.
**Detection:** A04 checks agent health before assignment.
**Mitigation:** Always check agent health status from Agent Registry before assigning work.
