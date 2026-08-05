# Root Cause Analysis (RCA): RCA-{{RCA_NUMBER}} - {{RCA_TITLE}}

> **RCA Document ID**: RCA-{{RCA_NUMBER}}  
> **Status**: {{RCA_STATUS}}  
> **Investigator**: {{LEAD_INVESTIGATOR}}  
> **System/Component**: {{SYSTEM_NAME}}  
> **Date of Occurrence**: {{EVENT_DATE}}  
> **Related Incident Ticket**: INC-{{INCIDENT_NUMBER}}  

---

## 1. Problem Statement

*Instruction: Formulate a precise, factual problem statement detailing what failed, when it failed, and what symptoms were observed.*

{{PROBLEM_STATEMENT}}

---

## 2. Methodology & Cause Tree Analysis

### 2.1 The 5 Whys Methodology
1. **Why did the system experience outage?**
   - {{WHY_1}}
2. **Why did {{WHY_1}} occur?**
   - {{WHY_2}}
3. **Why did {{WHY_2}} occur?**
   - {{WHY_3}}
4. **Why was {{WHY_3}} not detected by automated tests?**
   - {{WHY_4}}
5. **Why was there no automated fallback mechanism?**
   - {{WHY_5}}

### 2.2 Root Cause Summary
- **Primary Root Cause**: {{PRIMARY_ROOT_CAUSE}}
- **Contributing Factors**:
  - {{CONTRIBUTING_FACTOR_1}}
  - {{CONTRIBUTING_FACTOR_2}}

---

## 3. Barrier & Safeguard Analysis

| Existing Safeguard / Control | Status During Event (Failed / Bypassed / Absent) | Reason for Safeguard Breakdown | Recommended Improvement |
| :--- | :--- | :--- | :--- |
| Database Connection Timeout | Failed | Timeout threshold set too high (60s) | Reduce timeout to 5s |
| Circuit Breaker Middleware | Absent | Circuit breaker not implemented on legacy client | Implement Resilience4j circuit breaker |

---

## 4. Corrective Actions & Implementation Schedule

| Action ID | Corrective Action Description | Target Component | Owner | Target Date | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CA-01 | {{CORRECTIVE_ACTION_1}} | {{COMPONENT_1}} | {{OWNER_1}} | {{TARGET_DATE_1}} | Open |
| CA-02 | {{CORRECTIVE_ACTION_2}} | {{COMPONENT_2}} | {{OWNER_2}} | {{TARGET_DATE_2}} | Open |
