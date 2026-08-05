# Observability Metric Dashboard Specification: {{DASHBOARD_NAME}}

> **Document Type**: Metric & Monitoring Dashboard Design Spec  
> **Status**: {{DOCUMENT_STATUS}}  
> **Target Platform**: Grafana / Datadog / New Relic  
> **Dashboard Owner**: {{DASHBOARD_OWNER_TEAM}}  
> **Target Service**: {{SERVICE_NAME}}  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Dashboard Purpose & Target Audience

*Instruction: Specify the purpose of this dashboard (e.g., Incident Triage / Executive Overview / SLA Monitoring) and core SLIs tracked.*

---

## 2. Dashboard Layout & Panel Definitions

```
+-----------------------------------------------------------------------+
| Panel 1: Throughput (RPS)       | Panel 2: HTTP Error Rates (5xx)     |
+---------------------------------+-------------------------------------+
| Panel 3: Latency Distribution   | Panel 4: Resource Usage (CPU/RAM)   |
| (p50, p95, p99)                 |                                     |
+-----------------------------------------------------------------------+
```

### 2.1 Panel 1: Request Rate (Throughput)
- **Visualization Type**: Time-series Line Graph
- **PromQL Query**:
  ```promql
  sum(rate(http_requests_total{service="{{SERVICE_NAME}}"}[5m])) by (status_code)
  ```
- **Unit**: Requests / Sec (RPS)

### 2.2 Panel 2: Latency Percentiles (SLO Monitoring)
- **Visualization Type**: Time-series Line Graph
- **PromQL Query**:
  ```promql
  histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service="{{SERVICE_NAME}}"}[5m])) by (le))
  ```
- **Alert Threshold**: Line turns RED if p95 > 200 ms for 3 minutes.

### 2.3 Panel 3: Error Rate Percentage
- **PromQL Query**:
  ```promql
  (sum(rate(http_requests_total{service="{{SERVICE_NAME}}", status=~"5.."}[5m])) / sum(rate(http_requests_total{service="{{SERVICE_NAME}}"}[5m]))) * 100
  ```

---

## 3. Automated Alert Integration

| Alert Rule Name | Evaluation Window | Critical Threshold | Warning Threshold | Notification Destination |
| :--- | :--- | :--- | :--- | :--- |
| `HighErrorRate` | 3 Mins | Error Rate > 1.0% | Error Rate > 0.1% | PagerDuty & Slack `#alerts-prod` |
| `HighLatencyP95` | 5 Mins | p95 > 500 ms | p95 > 250 ms | Slack `#alerts-prod` |
