---
title: Token & API Rate Limiter Specification
document_id: SPEC-P01-SCHED-029
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Platform Infrastructure Team
last_updated: 2026-08-05
---

# Token & API Rate Limiter Specification

## Executive Summary
This document specifies the Rate Limiter (`rate_limiter`), managing LLM API request throttling, token-per-minute (TPM) limits, requests-per-minute (RPM) limits, sliding window token bucket algorithms, and provider quota protection across AI OS v4.

---

## 1. Rate Limiter Token Bucket Architecture

```text
[ INCOMING LLM REQUEST ] ──> AcquireTokens(count: 2500)
                                      │
                                      ▼
+-----------------------------------------------------------------+
| RATE LIMITER ENGINE (Redis Token Bucket / Leaky Bucket)         |
|  - Provider Bucket: OpenAI (60,000 TPM / 500 RPM)               |
|  - Provider Bucket: Anthropic (40,000 TPM / 300 RPM)            |
+-----------------------------------------------------------------+
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼ (Tokens Available)                          ▼ (Rate Limit Exceeded)
    [ CONSUME TOKENS & FORWARD ]                [ THROTTLE & ENQUEUE BACKOFF ]
```

---

## 2. Rate Limiter Interface Contract

```typescript
export interface RateLimitQuota {
  readonly provider: string;
  readonly maxTokensPerMinute: number;
  readonly maxRequestsPerMinute: number;
}

export interface IRateLimiter {
  acquireQuota(provider: string, estimatedTokens: number): Promise<{ granted: boolean; retryAfterMs: number }>;
  recordActualUsage(provider: string, tokensUsed: number): Promise<void>;
  getProviderStatus(provider: string): Promise<{ remainingTokens: number; remainingRequests: number }>;
}
```

---

## 3. Rate Limiting Invariants & Rules

1. **Sliding Window Accuracy**: Evaluates token consumption over 60-second sliding windows to prevent boundary burst spikes.
2. **Provider Failover Trigger**: When a primary LLM provider hits 95% quota utilization, Rate Limiter notifies Context Router to switch to secondary provider endpoints.

---

## 4. Verification Protocol

```bash
agy verify-rate-limiter --provider openai --test-burst
```
Simulates high-frequency token requests, validates sliding window rate limiting, and tests provider failover triggers.
