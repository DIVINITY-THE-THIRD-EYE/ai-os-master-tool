# AI OS v4 Lessons Learned & Post-Mortem Template (`lessons_template.md`)

## 1. Overview & Framework Purpose

The Lessons Learned Framework captures institutional knowledge from incident post-mortems, verification failures, prompt regressions, and operational bottlenecks. Captured lessons are ingested directly into the AI OS Knowledge Engine to update prompt guidelines, rule predicates, and anti-pattern databases automatically.

---

## 2. Incident Classification Taxonomy

- **Severity Level**:
  - `P0 - CRITICAL`: Total system outage, security breach, or production data corruption.
  - `P1 - HIGH`: Partial workflow blockage, major component degradation, SLA breach.
  - `P2 - MEDIUM`: Non-critical verification failure, recoverable agent retry loop.
  - `P3 - LOW`: Minor documentation mismatch, non-blocking warning.
- **Incident Category**:
  - `SECURITY`: Unauthorized access, prompt injection, credential exposure.
  - `LOGIC_BUG`: Incorrect code generation, state machine lockup, schema mismatch.
  - `PERFORMANCE`: High latency, token budget exhaustion, API rate limit.
  - `GOVERNANCE`: Policy violation, missing sign-off, un-audited handoff.

---

## 3. Post-Mortem Document Template

```markdown
# INCIDENT POST-MORTEM REPORT

## 1. Executive Incident Summary
- **Incident ID**: INC-2026-XXXX
- **Title**: [Short descriptive title of incident]
- **Date / Time of Incident**: YYYY-MM-DDTHH:MM:SSZ
- **Severity**: [P0 | P1 | P2 | P3]
- **Category**: [SECURITY | LOGIC_BUG | PERFORMANCE | GOVERNANCE]
- **Lead Investigator**: [Agent ID / Human Role]
- **Incident Status**: [RESOLVED | MONITORING | IN_PROGRESS]

---

## 2. Impact & SLA Metrics
- **Downtime / Delay Duration**: [e.g., 45 minutes]
- **Affected Workflows**: [e.g., WF-001 Software Development Workflow]
- **Affected Tenants / Agents**: [e.g., Agent A05, Agent A06]
- **Financial / Token Cost Impact**: [e.g., $14.50 USD / 3,200,000 extra tokens]

---

## 3. Incident Timeline (UTC)
| Timestamp | Event Source | Description |
|---|---|---|
| HH:MM:SS | Runtime Manager | Task execution initiated for TSK-881. |
| HH:MM:SS | Agent A05 | Generated code modification containing syntax error. |
| HH:MM:SS | Agent A06 | Verification failed; retry loop 1 initiated. |
| HH:MM:SS | System Router | Retry loop exhausted after 3 attempts; escalation triggered. |
| HH:MM:SS | Agent A11 | Incident Responder isolated context and initiated rollback. |

---

## 4. Root Cause Analysis (5 Whys Method)
1. **Why did the workflow fail?** 
   - Agent A05 generated TypeScript code that failed compilation.
2. **Why did the generated code fail compilation?**
   - The code imported a non-existent utility module `utils/formatters`.
3. **Why did the agent import a non-existent module?**
   - The prompt template lacked updated knowledge of available project modules.
4. **Why was the prompt template out of date?**
   - Recent refactoring moved `utils/formatters` to `@core/formatters` without updating prompt context.
5. **Why was prompt context not updated during refactoring?**
   - Refactoring workflow did not mandate an automated Knowledge Base refresh step.

---

## 5. Corrective & Preventative Actions (CAPA Matrix)

| ID | Action Item Description | Action Type | Assignee | Target Date | Status |
|---|---|---|---|---|---|
| CAPA-01 | Update prompt template `PROMPT_A05_CODE_GEN` with new module paths | Corrective | A13 (Knowledge Eng) | Immediate | COMPLETED |
| CAPA-02 | Add automated lint check for prompt module imports | Preventative | A07 (Security) | 2026-08-10 | PENDING |
| CAPA-03 | Ingest anti-pattern AP-011 into Knowledge Base | Preventative | A13 (Knowledge Eng) | 2026-08-07 | IN_PROGRESS |

---

## 6. Knowledge Graph Ingestion Protocol
Upon completion of this post-mortem report, execute the following ingestion command to update system memory:

```bash
aios-knowledge-tool ingest-lesson \
  --file=INC-2026-XXXX_post_mortem.md \
  --target-graph=knowledge/ontology/ \
  --update-rules=true
```
```
