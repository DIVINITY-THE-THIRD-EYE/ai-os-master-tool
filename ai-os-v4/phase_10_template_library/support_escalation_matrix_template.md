# Technical Support & Incident Escalation Matrix: {{SERVICE_NAME}}

> **Document Type**: Escalation Matrix & Contact Protocol  
> **Status**: {{DOCUMENT_STATUS}}  
> **Service Name**: {{SERVICE_NAME}}  
> **Support Tier Scope**: L1 Support to Executive Leadership  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Incident Severity Definitions

- **SEV-1 (Critical Outage)**: System completely unavailable to external users. Immediate business loss.
- **SEV-2 (Major Degradation)**: Core functionality impaired for a significant subset of users.
- **SEV-3 (Minor Defect)**: Non-critical feature bug with acceptable operational workaround.

---

## 2. Multi-Level Escalation Matrix

| Support Level | Role / Team Name | Contact Channel / Email | Target Response SLA | Target Resolution SLA | Escalation Trigger |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (L1)** | Global Service Desk | `support@{{DOMAIN}}` | <= 15 Mins | <= 2 Hours | Initial ticket intake & basic triage |
| **Tier 2 (L2)** | On-Call Application Support | `#oncall-{{SERVICE_NAME}}` / PagerDuty | <= 15 Mins | <= 4 Hours | Unresolved by L1 in 30 mins or SEV-2 declared |
| **Tier 3 (L3)** | Core Engineering & Architecture | `dev-leads@{{DOMAIN}}` | <= 15 Mins | <= 2 Hours | Code bug / complex DB/Infra fix required |
| **Executive** | VP of Eng & Incident Commander | Direct Phone / Crisis Room | Immediate | N/A | SEV-1 outage > 1 hour |

---

## 3. Contact Roster & Emergency Hotline

| Role | Primary Contact Name | Phone / SMS Number | Email | Secondary Backup |
| :--- | :--- | :--- | :--- | :--- |
| Primary On-Call Engineer | {{PRIMARY_ONCALL}} | {{PRIMARY_PHONE}} | {{PRIMARY_EMAIL}} | {{BACKUP_ONCALL}} |
| Lead DevOps Engineer | {{DEVOPS_LEAD}} | {{DEVOPS_PHONE}} | {{DEVOPS_EMAIL}} | {{DEVOPS_BACKUP}} |
| Incident Commander | {{INCIDENT_COMMANDER}} | {{COMMANDER_PHONE}} | {{COMMANDER_EMAIL}} | {{COMMANDER_BACKUP}} |

---

## 4. Bridge & Crisis Communication Channels

- **PagerDuty Escalation Policy**: `https://pagerduty.{{DOMAIN}}/escalations/{{POLICY_ID}}`
- **Emergency War Room Zoom**: `https://zoom.{{DOMAIN}}/j/war-room-1`
- **Customer Communications Lead**: {{COMMUNICATIONS_LEAD}}
