# Environment Setup & Infrastructure Guide: {{ENVIRONMENT_NAME}}

> **Document Type**: Environment Provisioning & Configuration Guide  
> **Environment**: {{ENVIRONMENT_NAME}} (e.g., Local Dev / Staging / Production)  
> **Infrastructure Platform**: AWS / Kubernetes / Terraform  
> **Maintainer Team**: Platform Engineering  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Environment Architecture & Topology

```
[ Ingress Controller ] ---> [ Service Mesh (Istio) ] ---> [ Application Pods ]
                                                                |
                                                                v
                                                     [ Managed Cloud Database ]
```

---

## 2. Infrastructure Provisioning via Terraform

### Step 1: Initialize Terraform Backend
```bash
cd infra/environments/{{ENVIRONMENT_NAME}}
terraform init -backend-config="bucket={{TF_STATE_BUCKET}}" -backend-config="key={{ENVIRONMENT_NAME}}/terraform.tfstate"
```

### Step 2: Plan Infrastructure Changes
```bash
terraform plan -out=tfplan.binary
```

### Step 3: Apply Provisioning
```bash
terraform apply tfplan.binary
```

---

## 3. Environment Variables & Secret Ingestion

| Variable Name | Description | Secret Source (Vault / KMS Path) | Mandatory? |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | Connection string for primary DB | `secret/{{ENVIRONMENT_NAME}}/db_url` | Yes |
| `REDIS_HOST` | Host address of Redis cluster | ConfigMap | Yes |
| `JWT_SECRET_KEY` | HMAC signing key for user tokens | `secret/{{ENVIRONMENT_NAME}}/jwt_key` | Yes |

---

## 4. Environment Verification & Health Tests

```bash
# Verify Kubernetes Nodes
kubectl get nodes -o wide

# Verify Secrets Sync
kubectl get secrets -n {{NAMESPACE}}

# Test Cluster Synthetic Ping
curl -k https://{{ENVIRONMENT_NAME}}-api.{{DOMAIN}}/health
```
