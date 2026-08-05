# Formal Deprecation Notice: {{DEPRECATED_ITEM_NAME}}

> **Notice ID**: DEP-NOTICE-{{NOTICE_NUMBER}}  
> **Deprecated Asset**: {{DEPRECATED_ITEM_NAME}} (e.g., API Endpoint / Service / CLI Tool)  
> **Current Status**: {{DEPRECATION_STATUS}} (Deprecated / End of Life / Sunset Completed)  
> **Announcement Date**: {{ANNOUNCEMENT_DATE}}  
> **Official Sunset / EOL Date**: {{SUNSET_DATE}}  
> **Owner Team**: {{OWNER_TEAM}}  

---

## 1. Executive Summary & Impact Statement

> **ATTENTION REQUIRED**: {{DEPRECATED_ITEM_NAME}} is officially deprecated as of {{ANNOUNCEMENT_DATE}}. Active support and bug fixes will cease on {{SUNSET_DATE}}.

### 1.1 Scope of Impact
*Instruction: Specify affected software versions, client integrations, and operational impacts resulting from this deprecation.*

---

## 2. Deprecation Schedule & Milestone Dates

```
[ Announcement Date ] --------------> [ Maintenance Only ] --------------> [ Hard Sunset / EOL ]
  ({{ANNOUNCEMENT_DATE}})                ({{MAINTENANCE_DATE}})                 ({{SUNSET_DATE}})
```

| Date | Milestone | Operational Status / Consequence |
| :--- | :--- | :--- |
| {{ANNOUNCEMENT_DATE}} | Initial Deprecation Announcement | Warning headers added to API responses |
| {{MAINTENANCE_DATE}} | Feature Freeze | No new feature enhancements; security fixes only |
| {{SUNSET_DATE}} | Hard Sunset / End-of-Life | Endpoint returns HTTP 410 Gone / Service terminated |

---

## 3. Migration Path & Recommended Alternative

Consumers must migrate to the recommended replacement asset prior to {{SUNSET_DATE}}:

- **Replacement Asset**: `{{REPLACEMENT_ITEM_NAME}}`
- **Migration Guide Link**: `https://docs.{{DOMAIN}}/migration/{{REPLACEMENT_GUIDE_SLUG}}`

---

## 4. Support Contacts & Escalation

- **Technical Support Channel**: `#deprecation-{{DEPRECATED_ITEM_NAME}}`
- **Contact Email**: `api-migration@{{DOMAIN}}`
