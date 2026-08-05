---
title: Open Source License Compliance & Governance Policy
document_id: SPEC-P00-LIC-015
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Legal & Open Source Compliance Committee
last_updated: 2026-08-05
---

# Open Source License Compliance & Governance Policy

## Executive Summary
This document specifies legal compliance rules, allowed open-source licenses, prohibited copyleft licenses, attribution requirements, and automated compliance auditing procedures for AI OS v4.

---

## 1. License Classification Matrix

All dependencies integrated into AI OS v4 must fall into pre-approved license categories:

```text
ALLOWED (Permissive)       CONDITIONALLY ALLOWED      PROHIBITED (Strong Copyleft)
├── Apache-2.0             ├── LGPL-2.1 / LGPL-3.0    ├── GPL-2.0 / GPL-3.0
├── MIT                    ├── MPL-2.0               ├── AGPL-3.0
├── BSD-2-Clause / BSD-3   └── CDDL-1.0              └── SSPL / BUSL
└── ISC
```

---

## 2. Governance Rules & Invariants

1. **Strict AGPL / GPL Ban**: Dependencies under AGPL-3.0 or GPL-3.0 are strictly forbidden in core platform runtime packages to prevent license contamination.
2. **Apache-2.0 Header Requirement**: All proprietary and open specification files created under AI OS v4 MUST include standard copyright headers.
3. **Automated License Audit Gate**: Pull Requests introducing dependencies with unclassified or copyleft licenses will be automatically blocked by CI.
4. **Third-Party Attribution File**: Every release MUST include a `THIRD_PARTY_LICENSES.md` file aggregating notices and copyright statements from all vendor libraries.

---

## 3. License Audit Workflow

```text
[ Developer Submits PR ] ──> [ CI License Scanner (FOSSology / LicenseFinder) ]
                                            │
               ┌────────────────────────────┴────────────────────────────┐
               ▼ (Approved Permissive)                                   ▼ (Flagged Copyleft)
     [ Merge Approved ]                                     [ PR Blocked & Escalated ]
```

---

## 4. Verification Protocol

Verify open-source license compliance:
```bash
agy verify-licenses --root ./ai-os-v4
```
Scans all direct and transitive dependencies and validates against approved license matrix.
