# Blameless Post-Mortem Report: {{INCIDENT_TITLE}}

> **Post-Mortem ID**: PM-{{INCIDENT_NUMBER}}  
> **Status**: {{POST_MORTEM_STATUS}} (Draft / In Review / Final)  
> **Incident Lead**: {{INCIDENT_LEAD}}  
> **Facilitator**: {{FACILITATOR_NAME}}  
> **Date of Incident**: {{INCIDENT_DATE}}  
> **Date of Post-Mortem Meeting**: {{POST_MORTEM_MEETING_DATE}}  

---

## 1. Executive Summary & Impact Narrative

### 1.1 Overview
*Instruction: Provide a blameless, factual account of what went wrong, what the impact was, how it was resolved, and what systemic lessons were learned.*

{{EXECUTIVE_SUMMARY_TEXT}}

### 1.2 Quantitative Metrics
- **Duration**: {{DURATION_MINUTES}} minutes
- **Downtime**: {{DOWNTIME_MINUTES}} minutes
- **Impacted Requests**: {{IMPACTED_REQUEST_COUNT}}
- **Mean Time to Detect (MTTD)**: {{MTTD_MINUTES}} minutes
- **Mean Time to Resolve (MTTR)**: {{MTTR_MINUTES}} minutes

---

## 2. Chronological Timeline

| Time (UTC) | Description of Events | Observed Impact |
| :--- | :--- | :--- |
| {{T0_TIME}} | Deployment v{{VERSION}} executed | Initial change applied |
| {{T1_TIME}} | Metric anomaly: Memory usage spiked to 98% | Alert triggered |
| {{T2_TIME}} | War room assembled; rollback initiated | Mitigation started |
| {{T3_TIME}} | Traffic stabilized; metrics returned to normal | Service restored |

---

## 3. What Went Well, What Went Poorly, & Where We Got Lucky

### 3.1 What Went Well
- Automated alerts fired within {{ALERT_LATENCY_SECONDS}} seconds.
- Team responded quickly in war room channel `#incident-war-room`.

### 3.2 What Went Poorly
- Diagnostic logs were missing correlation IDs, delaying root cause pinpointing.
- Staging environment did not replicate production dataset scale.

### 3.3 Where We Got Lucky
- Outage occurred outside peak business hours, reducing financial impact.

---

## 4. Action Items & Lessons Learned

| Item ID | Action Description | Category | Owner | Target Date | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ACT-01 | Add load test step in CI pipeline matching 2x prod traffic | Prevention | {{OWNER_1}} | {{DUE_DATE_1}} | Open |
| ACT-02 | Implement distributed tracing correlation headers across microservices | Detection | {{OWNER_2}} | {{DUE_DATE_2}} | Open |
