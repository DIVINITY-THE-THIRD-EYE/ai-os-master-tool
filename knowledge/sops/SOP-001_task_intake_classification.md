# SOP-001: Task Intake & Classification

**Purpose:** Standardize how raw user requests are converted into structured, executable task definitions.

**Responsible Agent:** A01 (Intake & Requirements Agent)

**Trigger:** `task.created` event received by A01

**Prerequisites:**
- User request or API payload received by Orchestrator (A00)
- Business vocabulary available from Knowledge Graph (A03)
- Risk classification rules available from governance_policies.yaml

**Step-by-Step Procedure:**

**Step 1: Parse Intent**
- Extract user's core objective from request text
- Identify task type (feature development, bug fix, research, analysis, deployment, etc.)
- Identify domain (software, finance, healthcare, etc.)

**Step 2: Identify Complexity**
- Estimate task complexity (Simple / Medium / Complex / Expert)
- Based on: number of systems affected, number of agents required, estimated duration

**Step 3: Identify Missing Information**
- List all missing fields required for a complete task charter
- Generate specific clarifying questions for each missing item
- Determine if clarification can be obtained from context or must be requested from human

**Step 4: Assign Risk Classification**
- Evaluate against risk criteria:
  - LOW: No production systems, no PII, no security implications
  - MEDIUM: Internal systems, limited data, reversible
  - HIGH: Production systems, PII involved, significant scope
  - CRITICAL: Irreversible, regulatory implications, financial impact

**Step 5: Extract Acceptance Criteria**
- Derive measurable, testable acceptance criteria from requirements
- Each criterion must be verifiable by A07
- Flag any subjective criteria and convert to measurable form

**Step 6: Produce Task Charter**
- Complete task charter JSON with all required fields
- Register with A00 (Master Orchestrator)
- Publish `task.intake.completed` event

**Exit Criteria:**
- Task charter produced with all required fields
- Risk level assigned
- Acceptance criteria are testable
- `task.intake.completed` published

**Failure Handling:**
- Missing information after one clarification cycle: escalate to human task owner via A13
- Conflicting requirements: escalate to Product Authority (A05-P)
- Risk classified as CRITICAL: immediately notify A00 and A08

**Events Published:** `task.intake.completed`

**Quality Gate:** Gate 0 (Task Registration Gate)
