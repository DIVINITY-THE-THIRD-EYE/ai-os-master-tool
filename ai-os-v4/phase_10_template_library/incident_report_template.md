# Major Incident Report: INC-{{INCIDENT_NUMBER}} - {{INCIDENT_TITLE}}

> **Incident ID**: INC-{{INCIDENT_NUMBER}}  
> **Severity Level**: {{SEVERITY_LEVEL}} (SEV-1 / SEV-2 / SEV-3)  
> **Incident Commander**: {{INCIDENT_COMMANDER}}  
> **Lead Investigator**: {{LEAD_INVESTIGATOR}}  
> **Impacted Services**: {{IMPACTED_SERVICES}}  
> **Incident Start Time**: {{INCIDENT_START_TIME}} UTC  
> **Incident Resolution Time**: {{INCIDENT_RESOLVED_TIME}} UTC  
> **Total Downtime / Duration**: {{TOTAL_DURATION}}  

---

## 1. Executive Summary & Impact Assessment

### 1.1 Summary
*Instruction: Provide a concise executive overview of what occurred, why it occurred, and how service was restored.*

{{EXECUTIVE_SUMMARY}}

### 1.2 Impact Metrics
- **Customer Impact**: {{CUSTOMER_IMPACT_COUNT}} users impacted ({{IMPACT_PERCENTAGE}}% of total active traffic)
- **Financial / Revenue Impact**: ${{ESTIMATED_REVENUE_IMPACT}}
- **Data Loss**: {{DATA_LOSS_STATUS}} (None / Partial / Complete)
- **SLA Breach**: {{SLA_BREACH_STATUS}} (Yes / No)

---

## 2. Incident Timeline (UTC)

| Timestamp (UTC) | Event / Action Taken | Actor / Team |
| :--- | :--- | :--- |
| {{T0_TIME}} | Automated PagerDuty alert triggered for High Latency | Monitoring |
| {{T1_TIME}} | Incident Commander declared SEV-1 and assembled war room | {{INCIDENT_COMMANDER}} |
| {{T2_TIME}} | Root cause identified as database connection pool exhaustion | {{LEAD_INVESTIGATOR}} |
| {{T3_TIME}} | Applied hotfix patch and restarted DB pool instances | DevOps Team |
| {{T4_TIME}} | Service metrics restored to normal baseline | Monitoring |
| {{T5_TIME}} | Incident officially closed | {{INCIDENT_COMMANDER}} |

---

## 3. Root Cause Analysis (5 Whys)

1. **Why did service fail?**: {{WHY_1}}
2. **Why did that happen?**: {{WHY_2}}
3. **Why was it not caught earlier?**: {{WHY_3}}
4. **Why did safeguards fail?**: {{WHY_4}}
5. **Root Cause**: {{ROOT_CAUSE_FINAL}}

---

## 4. Corrective & Preventive Action Items (CAPA)

| Action Item ID | Preventive Action Description | Priority | Owner | Target Due Date | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CAPA-01 | Increase connection pool limits and configure autoscaling alerts | P0 | {{CAPA_OWNER_1}} | {{CAPA_DATE_1}} | Open |
| CAPA-02 | Add synthetic monitoring test for DB health | P1 | {{CAPA_OWNER_2}} | {{CAPA_DATE_2}} | Open |
