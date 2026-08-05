# API Specification: {{API_NAME}}

> **Document Type**: REST / gRPC API Specification Specification  
> **Status**: {{DOCUMENT_STATUS}}  
> **Base URL**: `https://{{API_DOMAIN}}/api/v{{API_VERSION}}`  
> **Owner**: {{API_OWNER_TEAM}}  
> **Author(s)**: {{DOCUMENT_AUTHOR}}  
> **Last Updated**: {{LAST_UPDATED}}  
> **Version**: {{API_VERSION}}  

---

## 1. Document Control & Revision History

| Version | Date | Author | Summary of Changes |
| :--- | :--- | :--- | :--- |
| {{API_VERSION}} | {{LAST_UPDATED}} | {{DOCUMENT_AUTHOR}} | Initial API specification release |

---

## 2. Overview & Authentication

### 2.1 API Purpose
*Instruction: Describe the service capabilities, intended clients, and core workflows exposed by {{API_NAME}}.*

### 2.2 Authentication & Authorization
All API requests require a Bearer token in the HTTP Authorization header:
```http
Authorization: Bearer <JWT_ACCESS_TOKEN>
```
- **Token Issuer**: `https://auth.{{DOMAIN}}`
- **Supported Scopes**: `{{API_SCOPE_READ}}`, `{{API_SCOPE_WRITE}}`, `{{API_SCOPE_ADMIN}}`

### 2.3 Common Request Headers
| Header Name | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | String | Yes | Bearer JWT token |
| `Content-Type` | String | Yes | `application/json` |
| `X-Correlation-ID` | UUID | Recommended | Unique tracing ID for cross-service request tracking |

---

## 3. Standard Response Wrapper & Status Codes

### 3.1 Response Structure
```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "requestId": "req_123456789",
    "timestamp": "2026-08-05T12:00:00Z"
  }
}
```

### 3.2 Standard HTTP Status Codes
- `200 OK`: Request succeeded.
- `201 Created`: Resource successfully created.
- `400 Bad Request`: Validation error or invalid request payload.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Requested resource does not exist.
- `429 Too Many Requests`: Rate limit exceeded.
- `500 Internal Server Error`: Server error.

---

## 4. Endpoint Definitions

### Endpoint 1: {{ENDPOINT_1_NAME}}

- **HTTP Method**: `POST`
- **Path**: `/{{RESOURCE_NAME}}`
- **Summary**: {{ENDPOINT_1_SUMMARY}}

#### Request Body
```json
{
  "name": "{{SAMPLE_NAME}}",
  "category": "{{SAMPLE_CATEGORY}}",
  "enabled": true
}
```

#### Field Validation Rules
| Field | Type | Required | Constraints / Description |
| :--- | :--- | :--- | :--- |
| `name` | String | Yes | Max 100 chars, alphanumeric |
| `category` | String | Yes | Enum: [`OPTION_A`, `OPTION_B`] |
| `enabled` | Boolean | No | Default: `true` |

#### Response (`201 Created`)
```json
{
  "success": true,
  "data": {
    "id": "res_99887766",
    "name": "{{SAMPLE_NAME}}",
    "category": "{{SAMPLE_CATEGORY}}",
    "enabled": true,
    "createdAt": "2026-08-05T12:00:00Z"
  },
  "error": null,
  "meta": {
    "requestId": "req_123456789",
    "timestamp": "2026-08-05T12:00:00Z"
  }
}
```

---

### Endpoint 2: {{ENDPOINT_2_NAME}}

- **HTTP Method**: `GET`
- **Path**: `/{{RESOURCE_NAME}}/{id}`
- **Summary**: Retrieve details of a specific {{RESOURCE_NAME}}

#### Path Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | String | Yes | Unique ID of the resource |

#### Response (`200 OK`)
```json
{
  "success": true,
  "data": {
    "id": "res_99887766",
    "name": "{{SAMPLE_NAME}}",
    "status": "ACTIVE"
  },
  "error": null,
  "meta": {
    "requestId": "req_987654321",
    "timestamp": "2026-08-05T12:05:00Z"
  }
}
```

---

## 5. Rate Limiting & Throttling

| Tier | Rate Limit (Requests/Min) | Burst Allowance |
| :--- | :--- | :--- |
| Standard | 100 req/min | 150 |
| Premium / Internal | 1000 req/min | 1500 |

Rate limit headers returned in all responses:
- `X-RateLimit-Limit`: Maximum allowed requests per window
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: UTC epoch seconds when window resets

---

## 6. Deprecation Policy
- Deprecated endpoints will include `Warning: 299 - "Deprecated API"` response header.
- Minimum notice period before endpoint removal: 6 months.
