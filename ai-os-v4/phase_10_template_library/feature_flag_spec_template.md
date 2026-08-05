# Feature Flag Specification & Rollout Plan: {{FLAG_KEY}}

> **Feature Flag Key**: `{{FLAG_KEY}}`  
> **Document Type**: Feature Toggle Specification  
> **Status**: {{FLAG_STATUS}} (Draft / Active / Sunset Pending / Retired)  
> **Feature Owner**: {{FEATURE_OWNER}}  
> **Target Release Version**: v{{RELEASE_VERSION}}  
> **Platform Provider**: LaunchDarkly / Unleash / Flagsmith  
> **Planned Retirement Date**: {{RETIREMENT_DATE}}  

---

## 1. Feature Flag Overview & Intent

### 1.1 Purpose
*Instruction: Describe the feature controlled by `{{FLAG_KEY}}`, target user segments, and intended business outcomes.*

- **Flag Type**: {{FLAG_TYPE}} (Boolean / Multivariate / Percentage Rollout)
- **Default Variation (Off)**: `false` (Legacy experience)
- **Target Variation (On)**: `true` (New experience)

---

## 2. Targeting Rules & Phased Rollout Schedule

```
Phase 1: Internal QA & Beta Testers (100% targeting for user.email ends with "@company.com")
Phase 2: Canary Release (5% of production users)
Phase 3: Broad Release (25% -> 50% -> 100% over 7 days)
```

| Phase | Rollout Percentage / Rule | Start Date | Success Criteria to Advance |
| :--- | :--- | :--- | :--- |
| Phase 1 | Internal Employees Only | {{DATE_1}} | Zero P0/P1 bugs reported in 48 hours |
| Phase 2 | 5% Production Users | {{DATE_2}} | Error rate change <= 0.00% |
| Phase 3 | 100% General Availability (GA) | {{DATE_3}} | p95 latency remains stable |

---

## 3. Code Implementation Snippet

```typescript
import { featureClient } from '../services/featureClient';

export async function processOrder(user: UserContext, payload: OrderPayload) {
  const isNewCheckoutEnabled = await featureClient.getVariation('{{FLAG_KEY}}', user, false);
  
  if (isNewCheckoutEnabled) {
    return executeNewCheckoutWorkflow(payload);
  } else {
    return executeLegacyCheckoutWorkflow(payload);
  }
}
```

---

## 4. Kill-Switch Procedure & Sunset Strategy

- **Kill-Switch Trigger**: If HTTP 5xx error rate spikes > 0.5% after flag activation, toggle `{{FLAG_KEY}}` to `OFF` in admin console immediately.
- **Cleanup Strategy**: Remove flag evaluation code and delete flag definition within 30 days of 100% GA rollout.
