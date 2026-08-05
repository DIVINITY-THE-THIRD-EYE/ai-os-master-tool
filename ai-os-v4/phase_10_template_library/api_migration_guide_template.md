# API Version Migration Guide: v{{OLD_VERSION}} to v{{NEW_VERSION}}

> **Document Type**: Developer API Migration Guide  
> **API Name**: {{API_NAME}}  
> **Target Audience**: External & Internal API Consumers  
> **Target Sunset Date for v{{OLD_VERSION}}**: {{SUNSET_DATE}}  
> **Author**: {{DOCUMENT_AUTHOR}}  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Overview & Important Timeline

*Instruction: Provide a summary of structural changes, field renames, and performance improvements in API v{{NEW_VERSION}} compared to v{{OLD_VERSION}}.*

- **v{{OLD_VERSION}} Deprecation Date**: {{DEPRECATION_DATE}}
- **v{{OLD_VERSION}} Final Sunset Date**: {{SUNSET_DATE}} (Requests will return HTTP 410 Gone)

---

## 2. Summary of Breaking Changes

| Change Type | Affected Endpoint / Field | Old Behavior (v{{OLD_VERSION}}) | New Behavior (v{{NEW_VERSION}}) | Action Required by Consumer |
| :--- | :--- | :--- | :--- | :--- |
| Endpoint Rename | `POST /v1/user` | Returned `user_id` as String | Path: `POST /v2/users`, returns `id` as UUID | Update endpoint path & payload mapping |
| Field Removed | `GET /v1/orders` | Included `legacy_status_code` | Field removed entirely | Use `status` enum field |
| Header Requirement | All Endpoints | Optional `X-Correlation-ID` | Mandatory `X-Correlation-ID` header | Include UUID header in requests |

---

## 3. Code Migration Examples

### 3.1 Request Payload Migration

#### Legacy Request (v{{OLD_VERSION}})
```http
POST /api/v1/user
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Doe"
}
```

#### Upgraded Request (v{{NEW_VERSION}})
```http
POST /api/v2/users
Content-Type: application/json
X-Correlation-ID: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d

{
  "name": {
    "givenName": "Jane",
    "familyName": "Doe"
  }
}
```

---

## 4. Testing & Verification Sandbox

- **Sandbox Base URL**: `https://sandbox-api.{{DOMAIN}}/v{{NEW_VERSION}}`
- **Migration Support Email**: `api-support@{{DOMAIN}}`
