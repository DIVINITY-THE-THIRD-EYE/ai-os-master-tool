# AI OS v4 — Production Deployment Guide

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Enterprise Cloud & Kubernetes Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Deployment Architecture Overview

This guide provides procedures for deploying AI OS v4 to production Kubernetes clusters (EKS, GKE, AKS, or bare-metal OKD) using Helm charts and Infrastructure-as-Code (Terraform).

```
+-----------------------------------------------------------------------------------+
|                           PRODUCTION INGRESS (AWS ALB / NGINX)                    |
|                   (TLS 1.3 Termination, WAF, DDoS Protection)                     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        KUBERNETES CLUSTER (AI OS NAMESPACE)                       |
|                                                                                   |
|  +--------------------+    +--------------------+    +-------------------------+  |
|  | Kernel Deployment  |    | PDP Policy Engine  |    | Verification Engine     |  |
|  | (Replicas: 3+)     |    | (Replicas: 5+)     |    | (Replicas: 3+)          |  |
|  +---------+----------+    +---------+----------+    +------------+------------+  |
|            |                         |                            |               |
|  +---------v----------+    +---------v----------+    +------------v------------+  |
|  | NATS JetStream     |    | Redis Enterprise   |    | PostgreSQL Cluster      |  |
|  | State Bus Cluster  |    | Cache Cluster      |    | (HA Patroni + Stolon)   |  |
|  +--------------------+    +--------------------+    +-------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Helm Deployment Specification

### 2.1 Standard Installation Command

```bash
# Add enterprise Helm repository
helm repo add aios https://charts.aios.enterprise.internal
helm repo update

# Install AI OS v4 in production namespace
helm install aios-v4 aios/ai-os-v4 \
  --namespace aios-system \
  --create-namespace \
  -f values-production.yaml
```

### 2.2 Production `values-production.yaml` Sample

```yaml
global:
  environment: production
  tenantMode: multi-tenant
  domain: aios.enterprise.internal

kernel:
  replicaCount: 3
  resources:
    limits:
      cpu: "4000m"
      memory: "8192Mi"
    requests:
      cpu: "1000m"
      memory: "2048Mi"
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

pdpEngine:
  replicaCount: 5
  l2Cache:
    enabled: true
    redisUrl: "redis://redis-cluster.aios-system.svc.cluster.local:6379"

security:
  mTLSEnabled: true
  vaultIntegration:
    address: "https://vault.enterprise.internal:8200"
    role: "aios-kernel-role"

persistence:
  postgresql:
    host: "postgres-ha.aios-system.svc.cluster.local"
    database: "aios_production"
  qdrant:
    endpoint: "http://qdrant.aios-system.svc.cluster.local:6333"
```

---

## 3. High Availability & Zero-Downtime Rolling Upgrades

1. **Pod Disruption Budgets (PDB):** Enforces `minAvailable: 2` across all core deployment microservices.
2. **Rolling Update Strategy:**
   ```yaml
   strategy:
     type: RollingUpdate
     rollingUpdate:
       maxSurge: 1
       maxUnavailable: 0
   ```
3. **Database Migrations:** Database migrations use Goose / Flyway pre-deploy jobs that execute schema additions without locking active tables.

---

## 4. Summary Checklist for Deployment Guide Compliance

- [x] Cloud-native Kubernetes deployment architecture defined.
- [x] Canonical Helm command and production `values.yaml` schema provided.
- [x] Pod Disruption Budgets and zero-downtime rolling update strategy locked.
- [x] Database schema migration procedures documented.
