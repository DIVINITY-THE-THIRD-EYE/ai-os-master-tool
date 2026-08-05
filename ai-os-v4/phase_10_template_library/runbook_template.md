# Service Operational Runbook: {{SERVICE_NAME}}

> **Document Type**: Operations & Incident Runbook  
> **Service Name**: {{SERVICE_NAME}}  
> **Service Tier**: {{SERVICE_TIER}} (Tier 1 - Critical / Tier 2 - Important / Tier 3 - Non-Critical)  
> **Primary On-Call Escalation**: {{ONCALL_TEAM}}  
> **Repository**: `https://github.com/{{ORG}}/{{SERVICE_NAME}}`  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Service Overview & Architecture

### 1.1 Summary
*Instruction: Describe what {{SERVICE_NAME}} does, its core dependencies, and critical health indicators.*

- **Dashboard Link**: `https://grafana.{{DOMAIN}}/d/{{SERVICE_NAME}}`
- **Alert Channel**: `#alerts-{{SERVICE_NAME}}`
- **Log Aggregator**: `https://logs.{{DOMAIN}}/app/kibana#/{{SERVICE_NAME}}`

---

## 2. Common Alert Conditions & Standard Remedies

### Alert 1: `{{ALERT_1_NAME}}` (e.g., High Error Rate > 5%)
- **Trigger Condition**: Error rate exceeds 5% for 3 consecutive minutes.
- **Impact**: End users experience HTTP 500 error responses.
- **Diagnosis Command**:
  ```bash
  kubectl logs -n {{NAMESPACE}} -l app={{SERVICE_NAME}} --tail=100 | grep ERROR
  ```
- **Remediation Steps**:
  1. Check downstream database connectivity.
  2. If memory leak suspected, perform rolling restart:
     ```bash
     kubectl rollout restart deployment/{{SERVICE_NAME}} -n {{NAMESPACE}}
     ```
  3. Verify status:
     ```bash
     kubectl rollout status deployment/{{SERVICE_NAME}} -n {{NAMESPACE}}
     ```

---

### Alert 2: `{{ALERT_2_NAME}}` (e.g., High CPU Utilization > 90%)
- **Trigger Condition**: Average CPU usage exceeds 90% across pod cluster.
- **Remediation Steps**:
  1. Scale deployment manually if HPA is insufficient:
     ```bash
     kubectl scale deployment/{{SERVICE_NAME}} --replicas={{DESIRED_REPLICAS}} -n {{NAMESPACE}}
     ```

---

## 3. Graceful Restart & Maintenance Procedures

1. **Drain Node / Stop Traffic**: Set load balancer readiness weight to 0.
2. **Execute Clean Maintenance**:
   ```bash
   ./scripts/maintenance_mode.sh --enable
   ```
3. **Resume Traffic**: Restore readiness checks and confirm metric recovery.

---

## 4. Escalation Contacts

| Level | Contact Role | Primary Contact | Secondary Contact | Phone / Page |
| :--- | :--- | :--- | :--- | :--- |
| L1 | Primary On-Call | {{L1_NAME}} | {{L1_BACKUP}} | {{L1_PHONE}} |
| L2 | Service Technical Lead | {{L2_NAME}} | {{L2_BACKUP}} | {{L2_PHONE}} |
| L3 | Engineering Director | {{L3_NAME}} | {{L3_BACKUP}} | {{L3_PHONE}} |
