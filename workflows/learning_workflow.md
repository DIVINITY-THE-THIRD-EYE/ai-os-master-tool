# Learning Workflow (SOP-010: Learning & Knowledge Publication)

## Purpose
Transforms execution experience into approved, reusable knowledge stored in the knowledge graph and prompt library.

## Trigger
- Event: `release.completed` or `decision.generated` (any outcome)
- Scheduled: End of each workflow cycle

## Prerequisites
- Complete task record available (outcomes, artifacts, metrics)
- Verification reports from A07 available
- Human feedback from A13 collected (if applicable)

## Step-by-Step Procedure

### Step 1: Collect Task Data
- A12 subscribes to `release.completed` or `decision.generated`
- Retrieve complete task record: outcomes, artifacts, verification reports, human feedback, metrics
- Retrieve execution metrics from A11

### Step 2: Extract Patterns
- Analyze task execution for recurring patterns
- Identify: what worked well, what failed, what could be optimized
- Compare with prior similar tasks in Experience Repository

### Step 3: Generate Lessons Learned
- Document specific lessons with evidence
- Format: context + observation + recommendation + evidence link
- Classify as: best_practice / anti_pattern / workflow_optimization / prompt_improvement

### Step 4: Propose Optimizations
- Prompt improvements: if prompt produced suboptimal output
- Skill improvements: if agent behavior was inefficient
- Workflow improvements: if DAG ordering was suboptimal

### Step 5: Submit Candidate Knowledge
- Create structured candidate knowledge entry
- Include: evidence, source task ID, classification, proposed change
- Submit to validation pipeline
- Publish `learning.candidate.generated`

### Step 6: Validation Pipeline
- A07 validates candidate for quality (evidence-backed, non-conflicting)
- A08 validates candidate for policy compliance
- If validation fails: archive candidate with failure reason

### Step 7: Approval Pipeline
- Route approved candidates to relevant Domain Authority (A05-*)
- For high-impact knowledge: route to A13 for human approval
- Record approval with approver identity and timestamp

### Step 8: Publish Approved Knowledge
- A03 updates knowledge graph with approved entries
- Version history maintained
- Prompt library updated if prompt improvements approved
- Publish `knowledge.published`

## Exit Criteria
- All lessons generated and classified
- Candidate knowledge submitted to validation pipeline
- Approved knowledge published to knowledge graph
- Version history updated
- `knowledge.published` event emitted

## Quality Gate
- Gate 7: Learning Gate
- No candidate may be published without passing validation and approval
