---
title: Agent Session Manager Specification
document_id: SPEC-P01-KERN-007
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Session & Security Architecture Group
last_updated: 2026-08-05
---

# Agent Session Manager Specification

## Executive Summary
This document specifies the Session Manager (`session_manager`), responsible for creating, tracking, authenticating, renewing, and terminating agent interactive sessions, state tokens, and multi-agent workspace sessions.

---

## 1. Session Architecture & State Lifecycle

```text
[ Session Start Request ] ──> CreateSession() ──> [ SESSION: ACTIVE ]
                                                         │
               ┌─────────────────────────────────────────┴─────────────────────────────────────────┐
               ▼ (Idle Timeout > 1800s)                                                            ▼ (Explicit Close)
     [ SESSION: EXPIRED ]                                                                 [ SESSION: TERMINATED ]
               │                                                                                   │
               └─────────────────────────> [ SESSION PURGED ] <────────────────────────────────────┘
```

---

## 2. Session Schema & Interface Contract

```typescript
export interface AgentSession {
  readonly sessionId: string;
  readonly parentTaskId: string;
  readonly primaryAgentId: string;
  readonly participatingAgentIds: string[];
  readonly createdAt: string;
  readonly expiresAt: string;
  readonly status: "ACTIVE" | "EXPIRED" | "TERMINATED";
  readonly sessionToken: string;
}

export interface ISessionManager {
  createSession(primaryAgentId: string, parentTaskId: string, ttlSeconds?: number): Promise<AgentSession>;
  getSession(sessionId: string): Promise<AgentSession | null>;
  addParticipant(sessionId: string, agentId: string): Promise<void>;
  validateSessionToken(sessionId: string, token: string): Promise<boolean>;
  terminateSession(sessionId: string): Promise<void>;
}
```

---

## 3. Operational Security & Timeout Rules

1. **Session Token Signatures**: Session tokens are cryptographically signed HMAC-SHA256 tokens carrying session metadata.
2. **Idle Expiration**: Sessions with zero inter-agent messages for 1800 seconds (30 minutes) expire automatically.
3. **Session Replay Protection**: Each message within a session must include an incrementing sequence number to block replay attacks.

---

## 4. Verification Protocol

```bash
agy verify-session-manager --test-security
```
Tests session token issuance, validates participant additions, checks idle timeout purging, and verifies replay protection.
