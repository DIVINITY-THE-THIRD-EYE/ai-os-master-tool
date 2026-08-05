# User Acceptance Testing (UAT) Report: {{PROJECT_NAME}} v{{VERSION}}

> **Document Type**: User Acceptance Testing (UAT) Final Report  
> **Status**: {{DOCUMENT_STATUS}} (Passed / Passed with Caveats / Failed)  
> **UAT Lead**: {{UAT_LEAD}}  
> **Product Owner**: {{PRODUCT_OWNER}}  
> **Testing Window**: {{UAT_START_DATE}} to {{UAT_END_DATE}}  

---

## 1. Executive Summary & Acceptance Decision

### 1.1 Final Recommendation
- [x] **ACCEPTED FOR PRODUCTION DEPLOYMENT**
- [ ] **REJECTED - REMEDIATION REQUIRED**

### 1.2 Summary Statement
*Instruction: Provide a brief summary of UAT execution results, business scenario coverage, and overall user satisfaction.*

{{UAT_SUMMARY_STATEMENT}}

---

## 2. Test Execution Summary & Metrics

| Metric | Target | Actual Result | Status |
| :--- | :--- | :--- | :--- |
| Planned Business Scenarios | 100% | {{EXECUTED_SCENARIOS}} Scenarios | Complete |
| Overall Pass Rate | >= 95% | {{PASS_RATE}}% | Met |
| Critical (P0) Open Defects | 0 | {{OPEN_P0_COUNT}} | Met |
| High (P1) Open Defects | 0 | {{OPEN_P1_COUNT}} | Met |

---

## 3. Business Scenario Results Breakdown

| Scenario ID | User Workflow Description | Business Persona | Executed By | Result (Pass/Fail) | Notes / Observations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| UAT-SC-01 | Create and authorize new enterprise account | Admin User | {{TESTER_1}} | Pass | Workflow smooth |
| UAT-SC-02 | Generate quarterly financial tax report | Finance Manager | {{TESTER_2}} | Pass | Export completed in 3s |
| UAT-SC-03 | Bulk import 5,000 customer records | Ops Specialist | {{TESTER_3}} | Pass | Progress bar accurate |

---

## 4. Defect Log & Deferred Issues

| Defect ID | Description | Severity | Workaround Available? | Action Plan |
| :--- | :--- | :--- | :--- | :--- |
| DEF-01 | UI alignment offset on mobile Safari | P3 - Low | Yes (Use Desktop browser) | Fix in sprint v{{NEXT_VERSION}} |

---

## 5. Stakeholder Sign-off & Acceptance Approval

| Role | Name | Signature / Approval | Date |
| :--- | :--- | :--- | :--- |
| Business Sponsor | {{BUSINESS_SPONSOR}} | Approved | {{APPROVAL_DATE_1}} |
| Product Manager | {{PRODUCT_OWNER}} | Approved | {{APPROVAL_DATE_2}} |
| QA Manager | {{QA_LEAD}} | Approved | {{APPROVAL_DATE_3}} |
