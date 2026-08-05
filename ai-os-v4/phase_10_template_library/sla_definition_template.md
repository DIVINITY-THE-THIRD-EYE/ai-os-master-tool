# Service Level Agreement (SLA) Definition: {{SERVICE_NAME}}

> **Document Type**: Service Level Agreement & Service Level Objectives  
> **Status**: {{DOCUMENT_STATUS}}  
> **Service Provider**: {{SERVICE_PROVIDER_TEAM}}  
> **Service Consumer / Client**: {{SERVICE_CONSUMER_TEAM}}  
> **Effective Date**: {{EFFECTIVE_DATE}}  
> **Review Date**: {{REVIEW_DATE}}  
> **Version**: {{DOCUMENT_VERSION}}  

---

## 1. Executive Summary & Service Scope

### 1.1 Purpose
*Instruction: Specify the service boundary, availability commitments, performance benchmarks, and support commitments for {{SERVICE_NAME}}.*

### 1.2 In-Scope Services
- Primary API endpoints: `https://api.{{DOMAIN}}/*`
- User Dashboard Application: `https://app.{{DOMAIN}}`
- Core Data Pipeline & Storage Services

---

## 2. Service Level Objectives (SLOs) & Targets

| Metric | Target (SLO) | Measurement Window | Calculation Formula | Breach Threshold (SLA) |
| :--- | :--- | :--- | :--- | :--- |
| Uptime / Availability | 99.9% | Monthly | `(Total Minutes - Downtime) / Total Minutes * 100` | < 99.5% |
| Latency (p95) | < 200 ms | 7-day Rolling | 95th percentile HTTP response time | > 500 ms |
| Latency (p99) | < 500 ms | 7-day Rolling | 99th percentile HTTP response time | > 1000 ms |
| Error Rate | < 0.1% | Monthly | `(HTTP 5xx Errors / Total Requests) * 100` | > 1.0% |

---

## 3. Incident Response Times & Priority Matrix

| Priority | Incident Severity Definition | Target Acknowledgment Time | Target Resolution Time (SLA) | Escalation Contact |
| :--- | :--- | :--- | :--- | :--- |
| P0 - Critical | Full outage affecting > 50% users, data loss risk | <= 15 minutes | <= 2 hours | {{P0_ESCALATION_CONTACT}} |
| P1 - High | Partial service degradation, key feature down | <= 30 minutes | <= 4 hours | {{P1_ESCALATION_CONTACT}} |
| P2 - Medium | Non-critical bug, minor feature impacted | <= 2 hours | <= 24 hours | {{P2_ESCALATION_CONTACT}} |
| P3 - Low | General cosmetic bug or minor inquiry | <= 8 hours | <= 5 business days | {{P3_ESCALATION_CONTACT}} |

---

## 4. Maintenance Windows & Exclusions

### 4.1 Scheduled Maintenance
- Scheduled maintenance windows (up to 4 hours per month) executed during off-peak hours (Sunday 01:00-05:00 UTC) are excluded from availability calculations.

### 4.2 Exclusions
The following conditions are excluded from SLA calculations:
- Force Majeure events beyond reasonable control.
- Failure of client-side ISP or third-party DNS routing issues.
- Unauthorized client modification or misuse of service APIs.

---

## 5. Service Credits & Penalties

| Monthly Availability Metric achieved | Service Credit Percentage (% of monthly bill) |
| :--- | :--- |
| 99.0% - 99.49% | 10% credit |
| 95.0% - 98.99% | 25% credit |
| < 95.0% | 50% credit |
