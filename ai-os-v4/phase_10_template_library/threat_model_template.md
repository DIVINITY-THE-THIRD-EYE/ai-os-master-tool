# Security Threat Model: {{SYSTEM_NAME}}

> **Document Type**: Security Threat Model & Risk Analysis  
> **Status**: {{DOCUMENT_STATUS}}  
> **Threat Modeling Lead**: {{SECURITY_LEAD}}  
> **System Architect**: {{LEAD_ARCHITECT}}  
> **Framework Used**: STRIDE (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege)  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. System Context & Data Flow Diagram (DFD)

```
[ External User ] --(1. TLS Auth)--> [ Ingress Gateway ] --(2. Internal JWT)--> [ Business Logic ]
                                                                                      |
                                                                              (3. Encrypted Query)
                                                                                      v
                                                                             [ Primary Database Store ]
```

### 1.1 Assets & Data Classifications
- **Asset 1**: User Credentials & JWT Signing Keys (Classification: Critical)
- **Asset 2**: Customer PII & Transaction History (Classification: High)
- **Asset 3**: Public Product Catalog Metadata (Classification: Low)

---

## 2. Threat Analysis (STRIDE Matrix)

| Threat ID | Category | Threat Description | Affected Asset | Risk Score | Mitigation Strategy | Mitigation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| THR-01 | Spoofing | Adversary crafts forged JWT token | JWT Auth | High | Validate cryptographic signature against KMS public key | Implemented |
| THR-02 | Tampering | SQL Injection via unvalidated API parameter | Database | Critical | Use parameterized ORM queries exclusively | Implemented |
| THR-03 | Repudiation | User denies initiating wire transfer | Transaction Log | Medium | Enforce immutable audit logging with timestamp signatures | Implemented |
| THR-04 | Info Disclosure| Unencrypted database backup leaked | DB Backup | High | Enforce AWS KMS AES-256 backup encryption | Implemented |
| THR-05 | Denial of Service | API flooded with HTTP requests | API Gateway | High | Configure Rate Limiting & Cloudflare DDoS Shield | Implemented |
| THR-06 | Elevation of Privilege | Vertical privilege escalation via parameter tampering | Admin Service | Critical | Enforce strict RBAC middleware checks on server side | Implemented |

---

## 3. Trust Boundaries & Attack Vectors

- **Trust Boundary 1**: Internet Client to Ingress API Gateway (Untrusted to Semi-Trusted)
- **Trust Boundary 2**: API Gateway to Internal Service Mesh (Semi-Trusted to Trusted)
- **Trust Boundary 3**: Service Mesh to Database Layer (Trusted Storage)

---

## 4. Security Action Items & Residual Risk

- **Residual Risk Assessment**: Accepted low residual risk after Cloudflare DDoS and WAF deployment.
- **Action Item**: Perform bi-annual penetration test to re-validate threat assumptions.
