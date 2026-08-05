# AI OS v4 — Troubleshooting & Operations Manual

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Operational Incident Runbook & Diagnostic Guide  
**Status:** Frozen / Production Standard  

---

## 1. Overview & Incident Triage Protocol

This manual provides diagnostic procedures, decision trees, and step-by-step incident runbooks for operators managing AI OS v4 clusters under failure conditions.

```
                                 [ALERT TRIGGERED]
                                         │
                                         v
                         [Step 1: Check Severity Level]
                                         │
         +-------------------------------+-------------------------------+
         |                               |                               |
         v                               v                               v
[CRITICAL: Outage / Escapes]     [HIGH: Latency SLA Breach]     [MEDIUM: Rate Throttling]
  - Execute Emergency Freeze       - Check Redis L2 PDP Cache     - Scale Out Token Buckets
  - Run Diagnostic Script          - Scale Worker Replicas        - Inspect Downstream Provider
         │                               |                               |
         v                               v                               v
  [Runbook INC-001]               [Runbook INC-002]               [Runbook INC-003]
```

---

## 2. Emergency Operational Runbooks

### Runbook INC-001: 2PC Memory Deadlock / Transaction Lock Timeout

- **Symptom:** Tasks stuck in `UNDER_REVIEW` state; logs report `ERR_2PC_PREPARE_TIMEOUT`.
- **Root Cause:** A worker node crashed after acquiring 2PC memory locks without emitting `COMMIT` or `ABORT`.
- **Diagnostic Command:**
  ```bash
  aios-admin memory locks list --tenant-id tenant_enterprise_alpha
  ```
- **Remediation Steps:**
  1. Force release orphaned transaction locks older than 60 seconds:
     ```bash
     aios-admin memory locks purge-orphaned --max-age-seconds 60
     ```
  2. Verify PostgreSQL database connection pool health.
  3. Restart affected Memory Coordinator pod instance if lock release fails.

---

### Runbook INC-002: Sandbox Container Escape Alert

- **Symptom:** Security Supervisor raises `SECURITY_ALERT_SANDBOX_BREACH`.
- **Root Cause:** A tool process attempted unauthorized system call or host filesystem access outside sandbox bounds.
- **Remediation Steps:**
  1. **EXECUTE IMMEDIATE SYSTEM FREEZE:**
     ```bash
     aios-admin security freeze-cluster --reason "Sandbox breach investigation"
     ```
  2. Revoke agent security token and isolate pod instance via Kubernetes network policy.
  3. Export cryptographic audit log block for forensic analysis.
  4. Decommission compromised tool plugin from Tool Registry.

---

### Runbook INC-003: Cascade Rate Limit Throttling (HTTP 429 Storm)

- **Symptom:** Tasks failing with `ERR_RATE_LIMIT_EXCEEDED` across multiple agent roles.
- **Root Cause:** Upstream LLM provider (OpenAI / Anthropic) quota exhausted.
- **Remediation Steps:**
  1. Trigger dynamic model degradation fallback pathway:
     ```bash
     aios-admin router set-fallback --from "gpt-4o" --to "claude-3-5-sonnet"
     ```
  2. Enable temporary Token Bucket burst overcommit (+20%) for priority queue 0.

---

## 3. High-Value Diagnostic CLI Triage Commands

```bash
# Check Overall Health of All Subsystems
aios-admin status --all

# Trace Specific Task Execution Lifecycle
aios-admin tasks trace --task-id tsk_00192a831

# Verify Merkle Audit Log Integrity
aios-admin audit verify-chain --sequence-start 1000 --sequence-end 2000

# Inspect Active Rate Limit Counters in Redis
aios-admin ratelimit inspect --group fs_read_ops
```

---

## 4. Summary Checklist for Troubleshooting Manual Compliance

- [x] Incident triage flowcharts and severity levels established.
- [x] Concrete runbooks for 2PC Memory Deadlocks (INC-001), Sandbox Escapes (INC-002), and Rate Limit Storms (INC-003) written.
- [x] High-value diagnostic CLI commands documented.
- [x] Emergency system freeze procedures locked.
