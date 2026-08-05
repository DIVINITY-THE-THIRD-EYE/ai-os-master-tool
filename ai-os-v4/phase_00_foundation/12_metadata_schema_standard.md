---
title: Metadata Schema Standard & Extension Protocol
document_id: SPEC-P00-META-012
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Data Architecture Team
last_updated: 2026-08-05
---

# Metadata Schema Standard & Extension Protocol

## Executive Summary
This document specifies the global metadata structures, envelope definitions, provenance metadata, lineage tracking, and schema extension protocols for artifacts, tasks, agents, and workflows across AI OS v4.

---

## 1. Global Metadata Envelope Architecture

Every system entity (artifact, task, agent execution snapshot, memory node) MUST include a standardized metadata envelope:

```json
{
  "$schema": "https://ai-os.org/schemas/v1/metadata_envelope.schema.json",
  "entityId": "art-0982-arch-diagram",
  "entityType": "ARTIFACT",
  "createdAt": "2026-08-05T15:48:00Z",
  "updatedAt": "2026-08-05T15:48:00Z",
  "ownerAgentId": "agent-swe-arch-001",
  "executionId": "exec-wf-7712",
  "provenance": {
    "parentEntityIds": ["art-0981-raw-requirements"],
    "checksumSha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "generationPromptId": "prompt-arch-synthesis-v2",
    "modelIdentifier": "gpt-4o-2026-08"
  },
  "governance": {
    "classification": "CONFIDENTIAL",
    "retentionDays": 365,
    "legalHold": false
  },
  "customExtensions": {}
}
```

---

## 2. Provenance & Lineage Invariants

1. **Cryptographic Lineage Tracking**: Every created artifact MUST compute and embed the SHA-256 hash of its source content and link to its parent entity IDs.
2. **Immutable History**: Modifications to an entity create a new versioned envelope while preserving original `createdAt` and lineage chain references.
3. **Strict Validation**: Metadata headers are validated against JSON schema definitions before persisting to disk or vector memory.

---

## 3. Extension Protocol

Custom metadata fields MUST be scoped under the `customExtensions` namespace object using reverse-domain notation:

```json
{
  "customExtensions": {
    "org.enterprise.compliance": {
      "soc2Audited": true,
      "approvalSignoffBy": "user-qa-lead-01"
    }
  }
}
```

---

## 4. Verification Protocol

Validate entity metadata compliance:
```bash
agy validate-metadata --file ./artifacts/sample_artifact.json
```
Ensures required fields, valid ISO timestamps, SHA-256 formatting, and schema compatibility.
