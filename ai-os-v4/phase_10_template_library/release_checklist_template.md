# Production Release Gate & Verification Checklist: v{{RELEASE_VERSION}}

> **Document Type**: Release Gate Quality Checklist  
> **Release Target**: {{PROJECT_NAME}} v{{RELEASE_VERSION}}  
> **Release Manager**: {{RELEASE_MANAGER}}  
> **Target Environment**: Production ({{PROD_CLUSTER}})  
> **Planned Release Date**: {{PLANNED_DATE}}  

---

## 1. Quality & Test Gate Criteria

- [ ] **Unit Tests**: 100% passing across all repos (Coverage: {{UNIT_COVERAGE}}%).
- [ ] **Integration Tests**: Staging regression suite passed with zero errors.
- [ ] **Security Scans**: Container scan clean (0 Critical, 0 High vulnerabilities).
- [ ] **Performance Validation**: Load test signed off by Performance Lead.

---

## 2. Release Readiness Sign-offs

| Verification Area | Responsible Approver | Sign-off Status (Approved/Pending) | Timestamp / Date |
| :--- | :--- | :--- | :--- |
| Product & Features | {{PRODUCT_OWNER}} | Approved | {{APPROVAL_TIME_1}} |
| QA & Regression | {{QA_LEAD}} | Approved | {{APPROVAL_TIME_2}} |
| Security & Compliance | {{SECURITY_LEAD}} | Approved | {{APPROVAL_TIME_3}} |
| Infrastructure & Ops | {{DEVOPS_LEAD}} | Approved | {{APPROVAL_TIME_4}} |

---

## 3. Go-Live Execution Timeline & Task Verification

- [ ] **T-2 Hours**: Publish maintenance announcement banner on web portal.
- [ ] **T-1 Hour**: Final staging environment verification check.
- [ ] **T-15 Mins**: Take database snapshot `pre-release-v{{RELEASE_VERSION}}`.
- [ ] **T-0 Mins**: Deploy Helm release to production cluster.
- [ ] **T+15 Mins**: Run post-deployment smoke test suite.
- [ ] **T+30 Mins**: Monitor Grafana error dashboards (`HTTP 5xx rate = 0%`).

---

## 4. Rollback Verification Protocol

- [ ] Rollback Helm command verified: `helm rollback {{SERVICE_NAME}} -n {{NAMESPACE}}`.
- [ ] Rollback database script staged and ready if required.
