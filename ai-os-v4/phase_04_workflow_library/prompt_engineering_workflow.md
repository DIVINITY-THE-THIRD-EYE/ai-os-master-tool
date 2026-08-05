# Prompt Engineering Workflow Specification

## 1. Purpose & Objective
Iteratively design, benchmark, evaluate, optimize, and version control LLM system prompts for specialized agent tasks.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Task specification, target LLM model endpoints, test prompt evaluation dataset, baseline system prompt.
- **Trigger Conditions**: New agent deployment request or prompt accuracy degradation alert.

## 3. Participating Agent Roles & Responsibilities
- **Prompt Engineer**: Drafts system prompts, few-shot examples, chain-of-thought instructions, and output formats.
- **AI Quality Auditor**: Executes automated benchmark evaluation, evaluates model output accuracy, and measures token usage.
- **Model Specialist**: Monitors token latency, context window utilization, and model parameter tuning.

## 4. Step-by-Step Execution Sequence

### Step 1: Task Breakdown & Initial Prompt Construction
- **Inputs**: Agent specification document, output JSON schema.
- **Actions**: Define system role context, specify operational constraints, draft step-by-step reasoning steps, add 3-5 few-shot examples.
- **Outputs**: Draft System Prompt v1.0.
- **Verification**: Prompt Engineer peer check on formatting and instructions.

### Step 2: Evaluation Dataset Curation
- **Inputs**: Historical task inputs, edge-case scenarios, ground-truth outputs.
- **Actions**: Curate a golden dataset of 50-100 test cases covering standard inputs, edge cases, and adversarial prompt injection tests.
- **Outputs**: Golden Evaluation Dataset (JSON lines format).
- **Verification**: AI Quality Auditor validation of ground-truth label correctness.

### Step 3: Automated Batch Benchmark Execution
- **Inputs**: System Prompt v1.0, Golden Dataset, evaluation framework (Promptfoo / LangSmith).
- **Actions**: Run evaluation suite against target LLM models; record accuracy, JSON schema adherence, latency, and cost.
- **Outputs**: Prompt Benchmark Results Matrix.
- **Verification**: Schema validation pass rate >= 95%.

### Step 4: Adversarial Robustness & Injection Testing
- **Inputs**: Prompts under evaluation, jailbreak / injection test payloads.
- **Actions**: Execute prompt injection suites, verify system prompt boundary enforcement and refusal rules.
- **Outputs**: Adversarial Test Report.
- **Verification**: 100% rejection rate on prompt injection and system prompt extraction attacks.

### Step 5: Prompt Optimization & Version Publishing
- **Inputs**: Benchmark results, token cost data, Git repository.
- **Actions**: Refactor prompt for token conciseness, freeze version (e.g. `v1.2.0`), commit to Prompt Library repository.
- **Outputs**: Published Prompt YAML/Markdown file in central repository.
- **Verification**: Automated CI check verifying prompt file structure and metadata tags.

## 5. Decision Gates & Branching Rules
- Gate 1: System prompt must pass 100% of prompt injection defense tests before release approval.
- Gate 2: Golden dataset accuracy must reach >= 90% benchmark score prior to production tag.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Model fails JSON schema output adherence -> Action: Add explicit XML tags or JSON enforcement mode, re-run benchmark.
- Failure Mode 2: High token consumption exceeding budget -> Action: Compress context instructions, remove redundant few-shot examples.

## 7. Artifact Delivery & Output Standard
Version-controlled Prompt Markdown/YAML file, Promptfoo Evaluation Matrix Report, and Adversarial Security Audit Log.
