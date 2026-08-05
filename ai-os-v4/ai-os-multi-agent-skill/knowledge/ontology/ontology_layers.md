# AI OS Knowledge Ontology Layers

## Layer 0: Core Primitives
Fundamental entities that all other layers build on.

| Entity | Description |
|---|---|
| Task | A unit of work with objective, criteria, and state |
| Agent | An autonomous agent instance with capabilities |
| Artifact | Any produced output (code, docs, configs, reports) |
| Workflow | An execution sequence of tasks with dependencies |
| Event | A named notification published to the Event Bus |
| Decision | A recorded governance decision with rationale |
| Knowledge | A validated, approved fact or rule entry |
| Policy | An enforceable rule with violation actions |

## Layer 1: Domain Entities
Entities specific to operational domains.

| Entity | Description | Relates To |
|---|---|---|
| Requirement | A business or functional need | Task, Project |
| Capability | A skill or function an agent provides | Agent, Task |
| Tool | An external integration or action | Agent, Permission |
| Risk | An identified threat with impact and likelihood | Task, Artifact |
| Finding | A security or quality issue | Artifact, Verification |
| Approval | A recorded human decision | Decision, Artifact |
| Release | A deployment event | Artifact, Environment |
| Incident | A production failure or breach | Task, Recovery |

## Layer 2: Relationship Types
Relationships between entities.

| Relationship | From | To | Meaning |
|---|---|---|---|
| produces | Agent | Artifact | Agent created this artifact |
| depends_on | Task | Task | Task cannot start until dependency complete |
| validates | Agent | Artifact | Verification agent checked this artifact |
| approves | Human/Agent | Decision | Entity approved this decision |
| resolves | Decision | Risk | Decision addresses this risk |
| triggers | Event | Workflow | Event initiates this workflow |
| references | Artifact | Knowledge | Artifact cites this knowledge entry |
| escalates_to | Event | Agent/Human | Event routes issue to this target |

## Layer 3: Rule Graph
Formal rules that govern entity behavior.

- Rules are versioned and approval-dated
- Each rule references its source policy document
- Rules have enforcement level: blocking | warning | informational
- Rules link to escalation actions on violation
- Rules are organized by category: GOV, SEC, CMP, ARC, COD, DOC, REL, ESC, APR

## Layer 4: Traceability Graph
Every artifact links to:
- The requirement it satisfies
- The rule it complies with
- The agent that produced it
- The decision that approved it
- The test that verified it
- The human who reviewed it
- The release that deployed it

## Layer 5: Experience Repository
- Success cases: patterns from completed successful tasks
- Failure cases: anti-patterns from failed tasks
- Lessons learned: extracted insights
- Best practices: approved reusable patterns
- Prompt improvements: tested prompt versions
- Workflow optimizations: tested workflow improvements
