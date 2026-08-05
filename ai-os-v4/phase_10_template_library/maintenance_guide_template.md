# System Maintenance Guide: {{SYSTEM_NAME}}

> **Document Type**: Scheduled System Maintenance Guide  
> **Status**: {{DOCUMENT_STATUS}}  
> **System Owner**: {{SYSTEM_OWNER_TEAM}}  
> **Maintenance Window**: {{MAINTENANCE_SCHEDULE}} (e.g., Every Sunday 02:00 UTC - 04:00 UTC)  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Scope of Maintenance Tasks

| Task ID | Maintenance Activity | Frequency | Target Components | Impact / Downtime |
| :--- | :--- | :--- | :--- | :--- |
| MNT-01 | Database Index Rebuild & Vacuum | Weekly | Primary Database Cluster | None (Online rebuild) |
| MNT-02 | OS Patching & Kernel Upgrades | Monthly | Compute Nodes / Kubernetes | Rolling Reboot |
| MNT-03 | SSL/TLS Certificate Renewal | Every 90 Days | Ingress Controller / Domain | Zero Downtime |
| MNT-04 | Cold Storage Archival & Log Cleanup | Weekly | S3 / Log Storage | None |

---

## 2. Maintenance Procedures

### Procedure 1: Database Vacuum & Optimization
```sql
-- Rebuild fragmented indexes and re-evaluate statistics
VACUUM ANALYZE VERBOSE {{PRIMARY_TABLE_NAME}};
REINDEX TABLE CONCURRENTLY {{PRIMARY_TABLE_NAME}};
```

### Procedure 2: Log Archival & Disk Cleanup
```bash
-- Rotate logs and purge files older than 30 days
find /var/log/{{SERVICE_NAME}}/ -type f -name "*.log" -mtime +30 -exec rm -f {} \;
```

---

## 3. Maintenance Window Communication Checklist

- [ ] Send advance maintenance notification email to users 48 hours prior.
- [ ] Post banner notification on main web application UI.
- [ ] Set status page (`https://status.{{DOMAIN}}`) to "Scheduled Maintenance".
- [ ] Notify Customer Support team before start of maintenance.

---

## 4. Emergency Abort & Recovery Procedures

If maintenance exceeds allotted time window or encounters unexpected failure:
1. Revert node state to pre-maintenance snapshot.
2. Un-drain compute nodes and verify application connectivity.
3. Post update to status page explaining window extension or rescheduled date.
