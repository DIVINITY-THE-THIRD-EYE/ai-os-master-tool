---
title: Agent Communication Protocol (ACP) Specification
document_id: SPEC-P01-MSG-011
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Messaging & Inter-Agent Protocol Team
last_updated: 2026-08-05
---

# Agent Communication Protocol (ACP) Specification

## Executive Summary
This document specifies the Agent Communication Protocol (ACP v1.0), defining message frame layout, header metadata, request-response RPC, publish-subscribe events, conversation tracking, and serialization standards for inter-agent messaging in AI OS v4.

---

## 1. ACP Message Frame Envelope Architecture

```json
{
  "acpVersion": "1.0.0",
  "messageId": "msg-9021-f8a7",
  "correlationId": "corr-wf-7721",
  "conversationId": "conv-session-0912",
  "sender": {
    "agentId": "agent-orchestrator-main",
    "role": "orchestrator",
    "nodeId": "node-prod-east-01"
  },
  "recipient": {
    "agentId": "agent-swe-arch-001",
    "role": "architect",
    "channel": "direct"
  },
  "messageType": "REQUEST", // REQUEST | RESPONSE | EVENT | HANDOFF | HEARTBEAT
  "priority": "HIGH", // CRITICAL | HIGH | NORMAL | LOW
  "timestamp": "2026-08-05T15:50:00Z",
  "ttlMs": 30000,
  "payload": {
    "action": "SYNTHESIZE_SYSTEM_DESIGN",
    "parameters": {}
  },
  "signature": "sha256-hmac-signature-string"
}
```

---

## 2. Protocol Message Patterns

```text
[ REQUEST / RESPONSE RPC ]
  Sender Agent ──(ACP REQUEST Frame)──> Recipient Agent
  Sender Agent <──(ACP RESPONSE Frame)── Recipient Agent

[ EVENT BROADCAST ]
  Publisher Agent ──(ACP EVENT Frame)──> Event Bus ──> Subscriber Agents

[ HANDOFF DELEGATION ]
  Parent Agent ──(ACP HANDOFF Frame with Context)──> Subagent
```

---

## 3. Protocol Invariants & Rules

1. **Mandatory Correlation IDs**: Every response frame MUST carry the `correlationId` matching the request `messageId`.
2. **Cryptographic Header Verification**: All inter-agent ACP frames MUST include valid HMAC signatures signed using session secret keys.
3. **Payload Limit**: ACP message frames MUST NOT exceed 10 MB. Large artifacts route via storage URI reference pointers.

---

## 4. Verification Protocol

```bash
agy verify-acp-protocol --test-frames ./test/fixtures/acp_frames.json
```
Validates ACP envelope parsing, header HMAC signatures, correlation matching, and TTL expiration logic.
