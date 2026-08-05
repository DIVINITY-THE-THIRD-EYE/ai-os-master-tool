# Release Notes: {{PROJECT_NAME}} v{{RELEASE_VERSION}}

> **Release Version**: v{{RELEASE_VERSION}}  
> **Release Date**: {{RELEASE_DATE}}  
> **Environment**: {{ENVIRONMENT}} (e.g., Production / Staging)  
> **Release Manager**: {{RELEASE_MANAGER}}  

---

## 1. Release Summary

*Instruction: Provide a brief high-level summary of major features, enhancements, and critical fixes included in v{{RELEASE_VERSION}}.*

- **Highlights**: {{RELEASE_HIGHLIGHTS_SUMMARY}}
- **Deployment Type**: {{DEPLOYMENT_TYPE}} (e.g., Zero-downtime rolling update)

---

## 2. What's New (Features & Enhancements)

- **[Feature] {{FEATURE_1_TITLE}}**: {{FEATURE_1_DESC}} (`#{{TICKET_1}}`)
- **[Feature] {{FEATURE_2_TITLE}}**: {{FEATURE_2_DESC}} (`#{{TICKET_2}}`)
- **[Enhancement] {{ENHANCEMENT_1_TITLE}}**: {{ENHANCEMENT_1_DESC}} (`#{{TICKET_3}}`)

---

## 3. Bug Fixes

- **[Fix] {{FIX_1_TITLE}}**: {{FIX_1_DESC}} (`#{{TICKET_4}}`)
- **[Fix] {{FIX_2_TITLE}}**: {{FIX_2_DESC}} (`#{{TICKET_5}}`)

---

## 4. Breaking Changes & Deprecations

> **WARNING**: The following breaking changes require action prior to or immediately after upgrade:

- {{BREAKING_CHANGE_1_DESC}}
- {{DEPRECATION_1_DESC}}

---

## 5. Security Updates & Dependency Changes

- Upgraded `{{LIB_NAME}}` to version `{{LIB_VERSION}}` (Fixes CVE-{{CVE_ID}})
- Patched authentication token validation logic.

---

## 6. Migration & Deployment Instructions

1. Run database migration script:
   ```bash
   npm run db:migrate -- --version={{RELEASE_VERSION}}
   ```
2. Deploy artifacts via Helm:
   ```bash
   helm upgrade {{PROJECT_NAME}} ./charts/{{PROJECT_NAME}} --set image.tag={{RELEASE_VERSION}}
   ```
3. Verify endpoint health: `https://{{API_DOMAIN}}/health`
