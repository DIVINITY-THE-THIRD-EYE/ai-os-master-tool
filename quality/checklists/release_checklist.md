# Release Checklist (Gate 6)

**Responsible Agent:** A10 (Release & Deployment Agent)
**Gate:** Gate 6 (Release Gate)

## Pre-Release Verification
- [ ] Approval confirmed in Audit Log with artifact version — **Blocking**
- [ ] Human approval obtained if risk level is HIGH or CRITICAL — **Blocking**
- [ ] All release policies satisfied (release_policies.yaml) — **Blocking**
- [ ] No unresolved critical findings — **Blocking**
- [ ] Rollback plan documented and tested — **Blocking**

## Release Package
- [ ] All artifacts bundled in versioned release package — **Blocking**
- [ ] Release package signed with release ID and timestamp — **Blocking**
- [ ] Package manifest recorded in Version Manager — **Blocking**
- [ ] Release notes complete — **Blocking**

## Deployment
- [ ] Target environment configuration validated — **Blocking**
- [ ] Deployment strategy selected based on risk level — **Blocking**
- [ ] Monitoring and alerting active for target environment — **Blocking**
- [ ] Health checks defined and ready — **Blocking**
- [ ] release.started event published — **Blocking**

## Post-Deployment
- [ ] All health checks passed — **Blocking**
- [ ] Post-deployment validation suite passed — **Blocking**
- [ ] Key metrics within baseline range — **Blocking**
- [ ] Rollback path confirmed available — **Blocking**
- [ ] release.completed event published — **Blocking**
- [ ] Audit log entry recorded — **Blocking**
