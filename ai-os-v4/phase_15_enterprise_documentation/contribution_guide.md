# AI OS v4 — Open-Source & Enterprise Contribution Guide

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Open Source & Internal Governance Standard  
**Status:** Frozen / Production Standard  

---

## 1. Overview & Code of Conduct

We welcome contributions to AI OS v4! All contributors, maintainers, and community members MUST adhere to the enterprise **Contributor Covenant Code of Conduct v2.1**.

---

## 2. Git Branching Strategy & Pull Request Workflow

AI OS v4 utilizes a **Trunk-Based Development** model with short-lived feature branches:

```
[main] ─────────────────────────────────────────────────────────► (Release Ready)
         │                                               ▲
         └──► [feat/add-new-tool-registry] ──(PR/CI)─────┤ (Merged via Squash)
```

### 2.1 Commit Message Convention (Conventional Commits v1.0)

All commit messages MUST adhere to Conventional Commits:

```text
feat(plugin): add WASM Tier 1 sandbox runtime loader
fix(memory): resolve 2PC deadlock during vector store compaction
docs(api): update OpenAPI spec for task creation endpoint
test(security): add prompt injection regression test cases
```

---

## 3. Pull Request (PR) Requirements & Checklist

Every PR submitted to `main` MUST satisfy the following automated and peer-review gates:

- [x] **Automated Build & Test:** `make test-all` passes with 0 failures.
- [x] **Code Coverage:** Code coverage is $\ge 85\%$ on newly added lines.
- [x] **Architecture Review:** No violations of the 5 core system invariants.
- [x] **Documentation Updated:** Corresponding specs in `phase_15_enterprise_documentation` updated.
- [x] **Sign-off (CLA):** Developer Certificate of Origin (DCO) or Contributor License Agreement signed.

---

## 4. Summary Checklist for Contribution Guide Compliance

- [x] Contributor Covenant Code of Conduct adoption defined.
- [x] Trunk-based development and Conventional Commits workflow specified.
- [x] 5-point automated PR acceptance gate checklist locked.
