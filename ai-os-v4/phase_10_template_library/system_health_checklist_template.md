# System Health & Routine Inspection Checklist: {{SYSTEM_NAME}}

> **Document Type**: Operational Health Checklist  
> **Status**: {{DOCUMENT_STATUS}}  
> **Inspector / Engineer**: {{INSPECTOR_NAME}}  
> **Inspection Frequency**: Daily / Weekly / Monthly  
> **Target Environment**: Production ({{ENVIRONMENT_NAME}})  
> **Date Executed**: {{CHECK_DATE}}  

---

## 1. Core Services & Endpoint Readiness

| Service Name | Health Check Endpoint | Expected HTTP Status | Checked Status (Pass/Fail) | Response Time (ms) |
| :--- | :--- | :--- | :--- | :--- |
| API Gateway | `https://api.{{DOMAIN}}/health` | 200 OK | Pass | 45 ms |
| Core Service | `https://core.{{DOMAIN}}/health/liveness` | 200 OK | Pass | 60 ms |
| Auth Service | `https://auth.{{DOMAIN}}/.well-known/openid-configuration` | 200 OK | Pass | 35 ms |

---

## 2. Infrastructure Metrics & Resource Utilization

- [ ] **CPU Utilization**: Cluster average < 70% (Current: {{CPU_PERCENTAGE}}%)
- [ ] **Memory Utilization**: Memory usage < 75% (Current: {{MEM_PERCENTAGE}}%)
- [ ] **Disk Usage**: PVC / EBS volumes < 80% capacity (Current: {{DISK_PERCENTAGE}}%)
- [ ] **Database Connection Pool**: Available connections > 30% (Current: {{CONN_PERCENTAGE}}%)

---

## 3. Observability & Log Health

- [ ] **Error Spikes**: Zero unexplained HTTP 5xx error spikes in last 24h.
- [ ] **Alert Channel**: No unacknowledged Critical/High alerts in `#alerts-prod`.
- [ ] **Log Ingestion Rate**: Log pipeline throughput normal (no backlog/lag in Kafka/Vector).

---

## 4. Security & Backup Health

- [ ] **Backup Job Status**: Nightly DB backup completed successfully at {{BACKUP_TIME}} UTC.
- [ ] **SSL Certificates**: Expiry date > 30 days out (Nearest expiry: {{SSL_EXPIRY_DATE}}).
- [ ] **Container Image Vulnerabilities**: Zero newly published CVE-Criticals reported.

---

## 5. Inspection Summary & Action Items

- **Overall Inspection Result**: {{HEALTH_RESULT}} (ALL CLEAR / ATTENTION REQUIRED)
- **Notes / Escalations**: {{INSPECTION_NOTES}}
