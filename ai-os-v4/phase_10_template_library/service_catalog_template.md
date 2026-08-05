# Enterprise Service Catalog Entry: {{SERVICE_NAME}}

> **Service ID**: SVC-{{SERVICE_ID}}  
> **Service Name**: {{SERVICE_NAME}}  
> **Tier / Criticality**: {{SERVICE_TIER}} (Tier 1 / Tier 2 / Tier 3)  
> **Service Owner Team**: {{OWNER_TEAM}}  
> **Tech Lead**: {{TECH_LEAD}}  
> **Primary On-Call**: {{ONCALL_ROTATION}}  
> **Status**: {{SERVICE_STATUS}} (Production / Beta / Deprecated)  

---

## 1. Service Overview & Capabilities

### 1.1 Summary
*Instruction: Describe the primary business function, core responsibilities, and architectural scope of {{SERVICE_NAME}}.*

- **Repository**: `https://github.com/{{ORG}}/{{REPO_NAME}}`
- **Primary Programming Language**: {{PRIMARY_LANGUAGE}}
- **Deployment Platform**: Kubernetes (`{{CLUSTER_NAME}}` / Namespace: `{{NAMESPACE}}`)

---

## 2. API Endpoints & Interfaces Exposed

| Endpoint / Interface | Protocol | Description | Auth Required | SLO Latency (p95) |
| :--- | :--- | :--- | :--- | :--- |
| `POST /api/v1/resource` | REST / JSON | Creates new resource entity | Yes (JWT) | < 150 ms |
| `GET /api/v1/resource/{id}`| REST / JSON | Retrieves resource details | Yes (JWT) | < 50 ms |
| `events.resource.updated` | Kafka Event | Event broadcast on state change | Internal | N/A |

---

## 3. Dependency Map

### 3.1 Upstream Dependencies (Services that depend on this service)
- `{{UPSTREAM_SERVICE_1}}`
- `{{UPSTREAM_SERVICE_2}}`

### 3.2 Downstream Dependencies (Services this service calls)
- Database: `{{DOWNSTREAM_DB}}`
- Redis Cache Cluster
- Third-party API: `{{THIRD_PARTY_API}}`

---

## 4. Operational Telemetry & Links

- **Grafana Dashboard**: `https://grafana.{{DOMAIN}}/d/{{SERVICE_NAME}}`
- **Kibana Log Query**: `https://logs.{{DOMAIN}}/app/kibana#/{{SERVICE_NAME}}`
- **Runbook**: `https://wiki.{{DOMAIN}}/runbooks/{{SERVICE_NAME}}.md`
- **PagerDuty Service**: `https://pagerduty.{{DOMAIN}}/services/{{SERVICE_ID}}`
