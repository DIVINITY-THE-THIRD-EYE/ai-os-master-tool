# Enterprise Best Practices Library Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-BPL-012  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Guideline Catalog

The Best Practices Library maintains formal, standardized guidelines across software development, AI model prompting, cloud infrastructure deployment, security compliance, and testing methodologies.

---

## 2. Best Practice Entry Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BestPracticeEntry",
  "type": "object",
  "properties": {
    "bp_id": { "type": "string", "pattern": "^BP-[A-Z]+-[0-9]{3}$" },
    "title": { "type": "string" },
    "domain_category": { 
      "type": "string", 
      "enum": ["FRONTEND", "BACKEND", "DEVOPS", "SECURITY", "AI_PROMPTING", "DATA_ENGINEERING"] 
    },
    "guideline_statement": { "type": "string" },
    "rationale": { "type": "string" },
    "good_example": { "type": "string" },
    "bad_example": { "type": "string" },
    "automated_checker_rule_ref": { "type": "string" }
  },
  "required": ["bp_id", "title", "domain_category", "guideline_statement", "good_example", "bad_example"]
}
```

---

## 3. Catalog Sample: Backend API Security Best Practice

```yaml
bp_id: BP-SEC-004
title: Mandatory JWT Signature Verification on API Boundaries
domain_category: SECURITY

guideline_statement: >
  All API endpoints accepting Bearer tokens must perform cryptographic signature verification
  using public keys fetched from the trusted Identity Provider JWKS endpoint prior to processing payload data.

good_example: |
  const verifier = new JwtVerifier({ jwksUri: 'https://auth.internal/jwks' });
  const payload = await verifier.verify(token);

bad_example: |
  const payload = jwt.decode(token); // Vulnerable to signature forgery

automated_checker_rule_ref: R-SEC-0042
```

---

## 4. Automated Compliance Verification

Every best practice entry is linked to an automated checker rule in the Verification Engine (`phase_09_verification_platform`). When code or configurations violate a best practice, the linter emits a warning or error during Quality Gate checks.
