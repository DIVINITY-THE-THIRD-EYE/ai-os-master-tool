---
title: Inter-Agent Channel Specification
document_id: SPEC-P01-MSG-016
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Agent Messaging Protocol Group
last_updated: 2026-08-05
---

# Inter-Agent Channel Specification

## Executive Summary
This document specifies Inter-Agent Channels (`inter_agent_channel`), providing direct peer-to-peer (P2P) and group broadcast communication channels between collaborating agents in AI OS v4.

---

## 1. Inter-Agent Channel Architecture

```text
+-------------------------------------------------------------------------+
|                         INTER-AGENT CHANNEL ENGINE                      |
+-------------------------------------------------------------------------+
    │                                                                  │
    ▼ Direct Channel (P2P)                                             ▼ Group Channel (Broadcast)
[ Agent A ] <===================> [ Agent B ]         [ Lead Agent ] ──> Broadcast Group
                                                         ├──> Worker Agent 1
                                                         ├──> Worker Agent 2
                                                         └──> QA Agent
```

---

## 2. Channel API Interface Contract

```typescript
export interface ChannelDescriptor {
  readonly channelId: string;
  readonly type: "P2P" | "BROADCAST" | "TOPIC";
  readonly creatorAgentId: string;
  readonly participantAgentIds: string[];
  readonly maxParticipants: number;
  readonly isEncrypted: boolean;
}

export interface IInterAgentChannel {
  createChannel(type: "P2P" | "BROADCAST", participants: string[]): Promise<ChannelDescriptor>;
  sendMessage(channelId: string, messageText: string, metadata?: Record<string, unknown>): Promise<string>;
  readMessages(channelId: string, limit?: number): Promise<Array<{ senderId: string; body: string; timestamp: string }>>;
  closeChannel(channelId: string): Promise<void>;
}
```

---

## 3. Security & Access Rules

1. **Explicit Channel Joining**: Agents CANNOT inject messages into a channel without being explicitly added to `participantAgentIds`.
2. **Channel Cryptographic Isolation**: Channels inherit session secret keys to encrypt payloads in transit using AES-256-GCM.

---

## 4. Verification Protocol

```bash
agy verify-inter-agent-channel --test-p2p --test-broadcast
```
Tests P2P message delivery, validates group broadcast propagation, and checks channel encryption.
