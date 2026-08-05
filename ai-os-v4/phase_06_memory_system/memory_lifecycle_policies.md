# Memory Lifecycle & Governance Policies Specification

> **Subsystem:** Phase 06 — Memory System  
> **Document ID:** SPEC-06-MLP-010  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. Enterprise Memory Retention & Tiering Governance

This specification defines automated retention, tiering, archiving, and deletion policies across all 5 memory types (Working, Session, Persistent, Project, Agent) in compliance with SOC2, GDPR, and enterprise data governance.

```text
[Memory Creation] ──► Active Usage (Hot) ──► Inactivity / Age Trigger ──► Transition to Warm
                                                                                 │
                                                                                 ▼
[Permanent Hard Delete] ◄── Expiration / GDPR Scrub ◄── Transition to Cold Tier
```

---

## 2. Policy Matrix by Memory Type

| Memory Subsystem | Hot Retention | Warm Retention | Cold Archival | Hard Deletion / Purge Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Working Memory** | Duration of task execution | N/A | N/A | Flushed immediately upon task finish / GC |
| **Session Memory** | Active session (1 - 24 hrs) | 7 days (summarized) | 30 days | Hard purged after 30 days |
| **Persistent Memory** | 30 days | 365 days | 7 years | Retained per compliance rules |
| **Project Memory** | Active project lifecycle | 180 days post-release | 3 years | Archived upon project deprecation |
| **Agent Memory** | Continuous active profile | N/A | N/A | Retained while agent role exists |

---

## 3. GDPR & Right-to-Be-Forgotten Compliance Protocol

When a user or tenant requests account deletion:
1. `UserDeletionRequestedEvent` published to Event Bus.
2. Memory Sanitizer scans Session, Persistent, Project, and Experience stores.
3. All entries tagged with target `user_id` are hard-deleted.
4. Cryptographic deletion attestation log entry emitted to Immutable Audit Store.

---

## 4. Quota & Capacity Management Under Disk Pressure

When total persistent memory disk usage exceeds 85% capacity:
1. Low-quality experience runs (`quality_score < 0.70`) are purged immediately.
2. Cold storage logs older than 180 days are compressed and moved to Glacier S3 storage.
3. High-priority project memories and accepted ADR records are strictly protected from capacity purging.
