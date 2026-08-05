# Technical Troubleshooting Guide: {{SYSTEM_NAME}}

> **Document Type**: Incident Resolution & Troubleshooting Guide  
> **Status**: {{DOCUMENT_STATUS}}  
> **System/Component**: {{SYSTEM_NAME}}  
> **Target Audience**: Support Engineers / DevOps / On-Call Engineers  
> **Author**: {{DOCUMENT_AUTHOR}}  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Quick Triage Flowchart

```
[ Alarm Triggered ]
         |
         v
Check API Health Endpoint -> (Failing?) ---> Jump to Section 2.1 (Service Outage)
         |
      (Passing)
         v
Check High Latency / Queue Lag -------------> Jump to Section 2.2 (Performance Degradation)
```

---

## 2. Common Failure Scenarios & Step-by-Step Diagnostic Remedies

### 2.1 Symptom 1: HTTP 504 Gateway Timeout Errors

- **Root Causes**: Downstream database pool exhaustion, external vendor API hang, or thread deadlock.
- **Diagnostic Steps**:
  1. Inspect pod logs for timeout errors:
     ```bash
     kubectl logs -n {{NAMESPACE}} -l app={{SERVICE_NAME}} --tail=200 | grep "TimeoutException"
     ```
  2. Inspect database active connection count:
     ```sql
     SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
     ```
- **Remediation Action**:
  - Scale up replica pods: `kubectl scale deployment {{SERVICE_NAME}} --replicas=10 -n {{NAMESPACE}}`
  - Flush stale connection pool if necessary.

---

### 2.2 Symptom 2: High Memory Utilization & Out-of-Memory (OOM) Kills

- **Root Causes**: Heap memory leak, unexpected un-paginated payload query.
- **Diagnostic Steps**:
  1. Check OOM kill event history in Kubernetes:
     ```bash
     kubectl get events -n {{NAMESPACE}} --field-selector reason=OOMKilled
     ```
- **Remediation Action**:
  - Trigger heap dump analysis: `jcmd 1 GC.heap_dump /tmp/heapdump.hprof`
  - Temporarily bump container memory limit in deployment manifest.

---

## 3. Diagnostic Commands Reference Sheet

```bash
# Check pod restart count
kubectl get pods -n {{NAMESPACE}} -o wide --sort-by='.status.containerStatuses[0].restartCount'

# Inspect ingress controller routing
kubectl describe ingress {{INGRESS_NAME}} -n {{NAMESPACE}}

# Test network latency between pods
kubectl exec -it {{POD_NAME}} -n {{NAMESPACE}} -- curl -iv https://{{INTERNAL_SERVICE_HOST}}/health
```

---

## 4. Emergency Support & Escalation Path

- **Primary On-Call PagerDuty**: `https://pagerduty.{{DOMAIN}}/service/{{SERVICE_ID}}`
- **Internal Slack Channel**: `#support-escalations`
