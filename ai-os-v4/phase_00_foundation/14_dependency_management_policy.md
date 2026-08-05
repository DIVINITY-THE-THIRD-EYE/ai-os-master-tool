---
title: Dependency Management Policy & Verification Standard
document_id: SPEC-P00-DEP-014
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Security & Supply Chain Working Group
last_updated: 2026-08-05
---

# Dependency Management Policy & Verification Standard

## Executive Summary
This document specifies the software supply chain security rules, dependency pinning, vulnerability scanning standards, package manager conventions, and SBOM (Software Bill of Materials) requirements for AI OS v4.

---

## 1. Supply Chain Architecture & Invariants

```text
[ External Package Registry (npm / PyPI / Crates) ]
                         │
                         ▼
[ Automated Vulnerability & License Scanner (Snyk / Trivy) ]
                         │
                         ▼
[ Internal Lockfile Pinning (package-lock.json / poetry.lock) ]
                         │
                         ▼
[ Verified Reproducible Container Build ]
```

---

## 2. Mandatory Dependency Rules

1. **Exact Version Pinning**: All third-party library dependencies MUST be pinned to exact versions in lockfiles. Wildcard or fuzzy version ranges (`^1.2.0`, `~2.0`, `*`) are strictly prohibited in production releases.
2. **Zero High/Critical Vulnerabilities**: Continuous Integration (CI) builds MUST fail if dependencies contain unmitigated CVEs rated High or Critical.
3. **Software Bill of Materials (SBOM)**: Every build release MUST generate a CycloneDX-formatted SBOM (`sbom.json`).
4. **Private Registry Proxy**: External packages route through an enterprise artifact repository proxy (Nexus / Artifactory) with package hash validation.

---

## 3. Package Management Matrix

| Language | Primary Package Manager | Lockfile | SBOM Generator |
| :--- | :--- | :--- | :--- |
| **Node.js / TypeScript** | `pnpm` / `npm` | `pnpm-lock.yaml` | `@cyclonedx/cyclonedx-npm` |
| **Python** | `poetry` / `pip` | `poetry.lock` | `cyclonedx-py` |
| **Go** | `go modules` | `go.sum` | `cyclonedx-gobom` |

---

## 4. Verification Protocol

Run dependency scan and audit:
```bash
agy audit-deps --strict --sbom ./sbom.json
```
Validates zero CVE violations, valid lockfiles, exact version pins, and approved package licenses.
