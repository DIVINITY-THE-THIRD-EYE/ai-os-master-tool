# Security Checklist (Gate 4 & Gate 5)

**Responsible Agent:** A09 (Security Agent), A07 (Verification Agent)
**Gate:** Gate 4 (Verification Gate), Gate 5 (Governance Decision Gate)

## Secret & Credential Security
- [ ] Zero secrets, tokens, or credentials in code — **Blocking**
- [ ] Zero secrets in configuration files — **Blocking**
- [ ] Zero secrets in logs, reports, or artifacts — **Blocking**
- [ ] All secrets stored in approved Secret Manager — **Blocking**
- [ ] Secret rotation policy defined — **Blocking**

## Access Control
- [ ] All operations use least-privilege principle — **Blocking**
- [ ] RBAC defined and enforced — **Blocking**
- [ ] All tool calls are permissioned — **Blocking**
- [ ] Sandbox enforced for high-risk tool execution — **Blocking**
- [ ] No agent can act outside registered capabilities — **Blocking**

## Data Security
- [ ] All sensitive data classified by level — **Blocking**
- [ ] Encryption in transit (TLS 1.2+) enforced — **Blocking**
- [ ] Encryption at rest enforced for sensitive data — **Blocking**
- [ ] PII fields identified and protected — **Blocking**
- [ ] Data retention policy applied — **Blocking**

## Vulnerability Scanning
- [ ] Static analysis security scan passed — **Blocking**
- [ ] Dependency vulnerability scan passed — **Blocking**
- [ ] Zero critical findings — **Blocking**
- [ ] Zero high findings — **Blocking**
- [ ] OWASP Top 10 checks completed for web surfaces — **Blocking**

## Audit Trail
- [ ] All sensitive operations logged immutably — **Blocking**
- [ ] Audit logs include: who, what, when, result — **Blocking**
- [ ] Logs are tamper-evident — **Blocking**
