# Deployment Guide: {{SYSTEM_NAME}}

> **Document Type**: Production Deployment & Release Guide  
> **Status**: {{DOCUMENT_STATUS}}  
> **Target Release Version**: v{{RELEASE_VERSION}}  
> **Deployment Lead**: {{DEPLOYMENT_LEAD}}  
> **Target Environment**: {{TARGET_ENVIRONMENT}}  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Pre-Deployment Checklist

- [ ] All CI/CD pipeline tests passed successfully.
- [ ] Database migration scripts tested against staging sandbox.
- [ ] Rollback plan documented and verified.
- [ ] Stakeholders notified in `#announcements-deployments`.
- [ ] Maintenance window scheduled (if downtime required).

---

## 2. Infrastructure & Environment Requirements

- **Kubernetes Cluster**: `{{K8S_CLUSTER_NAME}}`
- **Namespace**: `{{NAMESPACE}}`
- **Required Secrets**: Configured in KMS / Vault at path `{{VAULT_SECRET_PATH}}`

---

## 3. Step-by-Step Deployment Procedure

### Step 1: Backup Operations
Execute database snapshot prior to schema migration:
```bash
pg_dump -h {{DB_HOST}} -U {{DB_USER}} -d {{DB_NAME}} -F c -f backup_v{{RELEASE_VERSION}}.dump
```

### Step 2: Database Migration
Apply schema updates:
```bash
flyway migrate -url=jdbc:postgresql://{{DB_HOST}}:5432/{{DB_NAME}} -user={{DB_USER}}
```

### Step 3: Application Deployment
Apply updated Kubernetes manifests or Helm values:
```bash
helm upgrade --install {{SERVICE_NAME}} ./helm-chart \
  --namespace {{NAMESPACE}} \
  --set image.tag=v{{RELEASE_VERSION}} \
  --values ./environments/{{TARGET_ENVIRONMENT}}/values.yaml
```

### Step 4: Verification & Smoke Testing
Run post-deployment smoke test suite:
```bash
npm run test:smoke -- --env={{TARGET_ENVIRONMENT}}
```

---

## 4. Rollback Plan

If post-deployment smoke tests fail or critical errors occur (HTTP 5xx rate > 1%):

1. **Revert Helm Release**:
   ```bash
   helm rollback {{SERVICE_NAME}} {{PREVIOUS_REVISION_NUMBER}} -n {{NAMESPACE}}
   ```
2. **Restore Database (if required)**:
   ```bash
   pg_restore -h {{DB_HOST}} -U {{DB_USER}} -d {{DB_NAME}} backup_v{{RELEASE_VERSION}}.dump
   ```
3. **Notify War Room**: Inform `#incident-room` of rollback completion.
