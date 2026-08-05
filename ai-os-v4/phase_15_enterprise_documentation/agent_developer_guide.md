# AI OS v4 — Agent Developer Guide

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Agent Specification & Development Standard  
**Status:** Frozen / Production Standard  

---

## 1. Overview & Mandatory 11-Section Agent Mandate

This guide details how AI engineers create, test, and register new specialized agents in AI OS v4.

> **MANDATORY INVARIANT:** Every agent specification in AI OS v4 MUST contain all 11 required sections:
> 1. Role Definition
> 2. Mission Statement
> 3. Authority Level & Boundaries
> 4. Responsibilities List
> 5. Expected Inputs
> 6. Output Format Contracts
> 7. Decision Rules & Logic
> 8. Escalation Rules
> 9. Quality Metrics & SLAs
> 10. System & Execution Prompts
> 11. Concrete Examples

---

## 2. Canonical Agent Specification Structure

```markdown
# Agent Specification: [Agent Name]

## 1. Role Definition
[Detailed description of agent archetype and classification]

## 2. Mission Statement
[One-sentence clear mission statement]

## 3. Authority Level & Boundaries
- Allowed Actions: [...]
- Prohibited Actions: [...]
- Resource Limits: [...]

## 4. Responsibilities List
1. [...]
2. [...]

## 5. Expected Inputs
- Input Schema: [...]

## 6. Output Format Contracts
- Output Schema: [...]

## 7. Decision Rules & Logic
IF [condition] THEN [action] ELSE [fallback]

## 8. Escalation Rules
- Trigger: [...] Target: [...]

## 9. Quality Metrics & SLAs
- Target Latency: [...]
- Accuracy SLA: [...]

## 10. System & Execution Prompts
```system
[Full 200+ word system prompt]
```

## 11. Concrete Examples
### Example 1: Standard Input/Output Pair
[...]
```

---

## 3. Agent Lifecycle & Event Handlers

Agents extend the base SDK class `BaseAgent` and implement standard lifecycle event hooks:

```typescript
import { BaseAgent, AgentContext, TaskResult } from "@aios/sdk";

export class SecurityReviewerAgent extends BaseAgent {
  public async onInitialize(context: AgentContext): Promise<void> {
    this.logger.info("Initializing Security Reviewer Agent...");
    await this.registerToolSubscriptions(["com.aios.system.sast_scanner"]);
  }

  public async executeTask(context: AgentContext): Promise<TaskResult> {
    const inputCode = context.getInput<string>("source_code");
    
    // Perform verification step
    const scanResult = await this.invokeTool("com.aios.system.sast_scanner", { code: inputCode });
    
    if (scanResult.vulnerabilities.length > 0) {
      return this.rejectWithRework("Security vulnerabilities detected.", scanResult.vulnerabilities);
    }
    
    return this.completeWithSuccess({ status: "PASSED", proof_id: scanResult.proof_id });
  }
}
```

---

## 4. Summary Checklist for Agent Developer Guide Compliance

- [x] Mandatory 11-section agent specification structure detailed.
- [x] Full markdown specification layout template provided.
- [x] TypeScript `BaseAgent` class extension code sample included.
- [x] Verification and rework feedback workflow documented.
