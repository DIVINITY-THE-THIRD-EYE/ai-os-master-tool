# AI OS v4 — Rate Limit Policy Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** Enterprise System Resilience Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Multi-Tier Rate Limiting Architecture

The **Rate Limit Engine** protects system stability, prevents resource exhaustion, manages external API costs (such as LLM inference endpoints), and ensures fair multi-tenant resource sharing. Rate limiting operates across five hierarchical layers:

```
+-----------------------------------------------------------------------------------+
|                           GLOBAL EDGE LIMITER (Layer 1)                           |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                          TENANT TIER LIMITER (Layer 2)                            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           AGENT ROLE LIMITER (Layer 3)                            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           TOOL GROUP LIMITER (Layer 4)                            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        UPSTREAM API PROVIDER (Layer 5)                            |
|             (Token Buckets for OpenAI / Anthropic / Local Clusters)               |
+-----------------------------------------------------------------------------------+
```

---

## 2. Rate Limiting Algorithms & Mathematical Formulation

### 2.1 Sliding Window Counter Algorithm

For precise, burst-resilient rate control without window boundary spikes, AI OS v4 utilizes the Sliding Window Counter algorithm:

$$\text{Count} = \text{Count}_{\text{current}} + \text{Count}_{\text{previous}} \times \left(1 - \frac{t - t_{\text{window\_start}}}{\text{WindowSize}}\right)$$

If $\text{Count} \ge \text{Limit}$, execution requests are instantly throttled or queued.

### 2.2 Token Bucket for Token-based Consumption (LLMs)

For LLM inference limits measured in Tokens Per Minute (TPM) and Requests Per Minute (RPM):

- **Capacity ($B$):** Max token bucket capacity (burst allowance).
- **Refill Rate ($R$):** Tokens added per second.
- **Cost ($C$):** Actual prompt + completion tokens consumed.

---

## 3. Rate Limit Configuration Schema

Rate limit policies are declared per tenant, agent group, or tool category using standard JSON schemas:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RateLimitPolicyDefinition",
  "type": "object",
  "required": ["policy_id", "scope", "target_id", "rules"],
  "properties": {
    "policy_id": { "type": "string" },
    "scope": {
      "type": "string",
      "enum": ["GLOBAL", "TENANT", "AGENT", "TOOL_GROUP", "UPSTREAM_PROVIDER"]
    },
    "target_id": { "type": "string" },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["metric", "limit", "window_seconds", "action_on_exceed"],
        "properties": {
          "metric": {
            "type": "string",
            "enum": ["REQUEST_COUNT", "LLM_TOKENS", "EXECUTION_TIME_MS", "NETWORK_BYTES"]
          },
          "limit": { "type": "integer" },
          "window_seconds": { "type": "integer" },
          "action_on_exceed": {
            "type": "string",
            "enum": ["REJECT_IMMEDIATE", "QUEUE_AND_DELAY", "DEGRADE_PRIORITY"]
          },
          "max_queue_wait_ms": { "type": "integer", "default": 5000 }
        }
      }
    }
  }
}
```

---

## 4. Distributed Rate Counter Engine (Redis Cluster)

To maintain rate limits across distributed cluster nodes, counter states are maintained in a high-performance Redis cluster using Lua scripts to guarantee atomic check-and-increment operations.

```lua
-- Atomic Redis Sliding Window Rate Limiter Script
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local clearBefore = now - window

redis.call('ZREMRANGEBYSCORE', key, 0, clearBefore)
local currentRequests = redis.call('ZCARD', key)

if currentRequests < limit then
    redis.call('ZADD', key, now, now)
    redis.call('EXPIRE', key, math.ceil(window / 1000))
    return 1 -- ALLOWED
else
    return 0 -- LIMITED
end
```

---

## 5. Dynamic Backpressure & Priority Queuing

When limits are reached, low-priority tasks are suspended or queued, while high-priority emergency tasks (such as security monitoring or incident recovery) bypass soft limits.

| Priority Tier | Queue Allocation | Limit Overcommit Allowance | Throttling Action |
| :--- | :--- | :--- | :--- |
| **Emergency / Kernel** | Priority Queue 0 | +50% Overcommit | Never throttled |
| **Production Task** | Priority Queue 1 | +10% Overcommit | Queued up to 10s |
| **Batch / Background** | Priority Queue 2 | +0% Overcommit | Immediate delay / 429 |
| **Untrusted Sandbox** | Priority Queue 3 | +0% Overcommit | Instant rejection |

---

## 6. Overlimit Response Headers & Error Payload

When a request exceeds rate limits, the system returns standard RFC-6585 compliance payloads:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 15
X-RateLimit-Limit-Requests: 1000
X-RateLimit-Remaining-Requests: 0
X-RateLimit-Reset: 1770144015

{
  "error_code": "ERR_RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded for tool group 'fs_read_ops'.",
  "limit": 1000,
  "window_seconds": 60,
  "retry_after_seconds": 15
}
```

---

## 7. Summary Checklist for Rate Limit Policy Compliance

- [x] 5-layer rate limit hierarchy (Global down to Upstream Provider) established.
- [x] Sliding Window Counter & Token Bucket algorithm formulations verified.
- [x] Redis Lua atomic check-and-increment implementation provided.
- [x] Priority-tiered dynamic backpressure queuing rules defined.
- [x] Standard RFC-6585 headers and HTTP 429 payload formats locked.
