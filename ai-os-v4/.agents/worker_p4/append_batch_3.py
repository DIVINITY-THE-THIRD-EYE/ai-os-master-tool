import os

TARGET_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_04_workflow_library"

def write_wf(filename, title, purpose, prereqs, trigger, roles, steps, gates, failures, artifact_standard):
    path = os.path.join(TARGET_DIR, filename)
    content = f"# {title} Specification\n\n"
    content += f"## 1. Purpose & Objective\n{purpose}\n\n"
    content += f"## 2. Prerequisites & Trigger Conditions\n"
    content += f"- **Prerequisites**: {prereqs}\n"
    content += f"- **Trigger Conditions**: {trigger}\n\n"
    content += f"## 3. Participating Agent Roles & Responsibilities\n"
    for rname, rdesc in roles:
        content += f"- **{rname}**: {rdesc}\n"
    content += f"\n## 4. Step-by-Step Execution Sequence\n\n"
    for i, (sname, sinp, sact, sout, sver) in enumerate(steps, 1):
        content += f"### Step {i}: {sname}\n"
        content += f"- **Inputs**: {sinp}\n"
        content += f"- **Actions**: {sact}\n"
        content += f"- **Outputs**: {sout}\n"
        content += f"- **Verification**: {sver}\n\n"
    content += f"## 5. Decision Gates & Branching Rules\n"
    for g in gates:
        content += f"- {g}\n"
    content += f"\n## 6. Failure Modes & Fallback/Recovery Procedures\n"
    for f in failures:
        content += f"- {f}\n"
    content += f"\n## 7. Artifact Delivery & Output Standard\n{artifact_standard}\n"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename}")

# Batch 3: Workflows 21 to 30
wf_list = [
    # 21
    ("knowledge_extraction_workflow.md", "Knowledge Extraction Workflow",
     "Automate unstructured document parsing, entity-relation extraction, vector indexing, graph node creation, and knowledge base enrichment.",
     "Raw document corpus (PDFs, Markdown, HTML), embedding model API, vector database (Milvus/Pinecone), graph DB (Neo4j).",
     "Ingestion trigger from document upload repository.",
     [("Knowledge Engineer", "Defines ontology schema, entity extraction taxonomy, and graph relationship rules."),
      ("NLP Specialist", "Configures chunking strategies, embedding pipeline, and NER models."),
      ("Information Architect", "Audits graph consistency, vector retrieval precision, and chunk deduplication.")],
     [("Document Parsing & Text Normalization", "Raw document corpus, OCR engine (Tesseract/Unstructured).", "Extract raw text, strip formatting noise, perform OCR on image tables, split into structural sections.", "Cleaned plain text / markdown files.", "Parsing validation check ensuring 0 empty pages or corrupted character encoding."),
      ("Semantic Chunking & Embedding Generation", "Normalized text files, tokenizer, embedding model (text-embedding-3-large).", "Apply recursive semantic chunking (500 tokens with 100 token overlap), generate dense vector embeddings.", "Chunk metadata records and vector arrays.", "Vector dimension audit matching target index configuration (e.g. 1536 dimensions)."),
      ("Named Entity & Relation Extraction (NER/RE)", "Semantic chunks, LLM extraction prompt / spaCy model, ontology schema.", "Extract domain entities (Concepts, Tools, APIs, Authors) and explicit relations (DEPENDS_ON, IMPLEMENTS, REQUIRES).", "JSON-LD Entity-Relation triples.", "Schema validation check verifying all extracted entity types conform to ontology."),
      ("Vector & Graph Database Ingestion", "Vector embeddings, E-R triples, Pinecone/Neo4j endpoints.", "Upsert vector embeddings with metadata into vector DB; merge nodes and edges into Neo4j graph DB.", "Ingested Vector Database index and Neo4j Graph DB update status.", "Database query confirmation verifying node count increase."),
      ("Retrieval Evaluation & Index Optimization", "Evaluation query set, ground truth answers, RAG Triad benchmark (Ragas).", "Run sample RAG queries, compute Context Precision, Context Recall, and Faithfulness metrics.", "Knowledge Extraction Benchmark Report.", "Context Precision >= 0.85 and Context Recall >= 0.80.")],
     ["Gate 1: Schema validation check must pass 100% of extracted triples before Neo4j insertion.",
      "Gate 2: Retrieval benchmark (Ragas precision >= 0.85) required before enabling production search index."],
     ["Failure Mode 1: PDF OCR failure on scanned table -> Action: Route document to vision LLM (GPT-4o) table parser fallback.",
      "Failure Mode 2: Vector embedding rate-limit exceeded -> Action: Implement exponential backoff queue with batch size reduction."],
     "Ingested Vector Index, Neo4j Knowledge Graph triples, Ragas Retrieval Benchmark Report, and Processed Corpus Manifest."),

    # 22
    ("prompt_engineering_workflow.md", "Prompt Engineering Workflow",
     "Iteratively design, benchmark, evaluate, optimize, and version control LLM system prompts for specialized agent tasks.",
     "Task specification, target LLM model endpoints, test prompt evaluation dataset, baseline system prompt.",
     "New agent deployment request or prompt accuracy degradation alert.",
     [("Prompt Engineer", "Drafts system prompts, few-shot examples, chain-of-thought instructions, and output formats."),
      ("AI Quality Auditor", "Executes automated benchmark evaluation, evaluates model output accuracy, and measures token usage."),
      ("Model Specialist", "Monitors token latency, context window utilization, and model parameter tuning.")],
     [("Task Breakdown & Initial Prompt Construction", "Agent specification document, output JSON schema.", "Define system role context, specify operational constraints, draft step-by-step reasoning steps, add 3-5 few-shot examples.", "Draft System Prompt v1.0.", "Prompt Engineer peer check on formatting and instructions."),
      ("Evaluation Dataset Curation", "Historical task inputs, edge-case scenarios, ground-truth outputs.", "Curate a golden dataset of 50-100 test cases covering standard inputs, edge cases, and adversarial prompt injection tests.", "Golden Evaluation Dataset (JSON lines format).", "AI Quality Auditor validation of ground-truth label correctness."),
      ("Automated Batch Benchmark Execution", "System Prompt v1.0, Golden Dataset, evaluation framework (Promptfoo / LangSmith).", "Run evaluation suite against target LLM models; record accuracy, JSON schema adherence, latency, and cost.", "Prompt Benchmark Results Matrix.", "Schema validation pass rate >= 95%."),
      ("Adversarial Robustness & Injection Testing", "Prompts under evaluation, jailbreak / injection test payloads.", "Execute prompt injection suites, verify system prompt boundary enforcement and refusal rules.", "Adversarial Test Report.", "100% rejection rate on prompt injection and system prompt extraction attacks."),
      ("Prompt Optimization & Version Publishing", "Benchmark results, token cost data, Git repository.", "Refactor prompt for token conciseness, freeze version (e.g. `v1.2.0`), commit to Prompt Library repository.", "Published Prompt YAML/Markdown file in central repository.", "Automated CI check verifying prompt file structure and metadata tags.")],
     ["Gate 1: System prompt must pass 100% of prompt injection defense tests before release approval.",
      "Gate 2: Golden dataset accuracy must reach >= 90% benchmark score prior to production tag."],
     ["Failure Mode 1: Model fails JSON schema output adherence -> Action: Add explicit XML tags or JSON enforcement mode, re-run benchmark.",
      "Failure Mode 2: High token consumption exceeding budget -> Action: Compress context instructions, remove redundant few-shot examples."],
     "Version-controlled Prompt Markdown/YAML file, Promptfoo Evaluation Matrix Report, and Adversarial Security Audit Log."),

    # 23
    ("documentation_generation_workflow.md", "Documentation Generation Workflow",
     "Automate source code parsing, docstring extraction, API reference generation, tutorial writing, and static documentation site compilation.",
     "Codebase repository, docstring standards (Google/NumPy style), TypeDoc/Sphinx/MkDocs configuration.",
     "Merge into main branch or product release tag.",
     [("Technical Writer", "Drafts overview guides, architecture tutorials, and API usage examples."),
      ("Documentation Engineer", "Maintains static site generators (MkDocs/Docusaurus) and CI documentation build scripts."),
      ("QA Auditor", "Runs broken link checkers, docstring coverage analyzers, and readability audits.")],
     [("Source Code AST Parsing & Docstring Audit", "Source code tree, docstring coverage tool (interrogate / TypeDoc).", "Parse code abstract syntax trees (AST), calculate docstring coverage percentage, identify undocumented functions/classes.", "Docstring Coverage Audit Report.", "Docstring coverage >= 90% across all exported public APIs."),
      ("API Reference Generation", "Source codebase, API doc generator (Sphinx / TypeDoc / Swagger).", "Extract inline docstrings, generate markdown/HTML API reference pages detailing parameters, types, returns, and exceptions.", "Generated API Reference Markdown files.", "Zero docstring parsing warnings during generation build."),
      ("Guides & Usage Example Drafting", "Feature specs, API reference, target user persona.", "Write getting-started guides, architecture overviews, code snippets, and common use-case tutorials.", "User Guides & Concept Documentation.", "Technical Writer verification of snippet runnable status."),
      ("Site Compilation & Broken Link Check", "Markdown docs tree, MkDocs / Docusaurus config, link checker tool (htmlproofer).", "Compile markdown files into responsive HTML site; execute internal/external broken link scanner.", "Compiled Static Site assets and Link Audit Log.", "Zero broken internal links and 0 compilation errors."),
      ("Deployment & CDN Publication", "Compiled static site, GitHub Pages / Vercel hosting target.", "Deploy documentation build to CDN hosting bucket; update version dropdown picker.", "Live Documentation URL.", "HTTP 200 verification on root site and key API reference pages.")],
     ["Gate 1: Docstring coverage must meet or exceed 90% threshold before generating API references.",
      "Gate 2: Broken link checker must report 0 broken links prior to deployment publication."],
     ["Failure Mode 1: Sphinx/TypeDoc build syntax error in docstring -> Action: Fix malformed JSDoc/reST formatting in source file, re-run build.",
      "Failure Mode 2: Broken external URL link -> Action: Update link to active destination or archive URL."],
     "Compiled static documentation site, Docstring Coverage Report, Link Checker Audit Log, and published CDN URL."),

    # 24
    ("testing_pipeline_workflow.md", "Testing Pipeline Workflow",
     "Structure comprehensive software quality assurance spanning unit, integration, system, regression, performance, and security testing.",
     "Source code repository, test framework configuration (pytest/jest/playwright), test database.",
     "Pull Request creation or CI pipeline trigger.",
     [("QA Lead", "Defines test strategy, coverage targets, and test environment architecture."),
      ("Automation Specialist", "Writes automated test scripts, mocks, and custom test assertions."),
      ("Test Engineer", "Analyzes test execution failures, triages bugs, and maintains test data fixtures.")],
     [("Unit Test Execution & Coverage Audit", "Source code, unit test suite, coverage tool (coverage.py/istanbul).", "Run fast unit tests in parallel, measure code line and branch coverage metrics.", "Unit Test Results XML & Coverage Report.", "100% unit test pass rate with minimum 80% line coverage."),
      ("Integration Test Execution", "Service build, database test container (Testcontainers), API integration tests.", "Spin up containerized dependencies, execute API integration tests against mock/local endpoints.", "Integration Test Results Log.", "100% pass rate on integration test suites."),
      ("End-to-End (E2E) & Regression Run", "Staging environment deployment, Playwright / Selenium test suite.", "Execute critical path user journey tests (login, checkout, search) across headless browser matrix.", "E2E Test Execution Video & Trace Artifacts.", "Zero regression failures on critical user flows."),
      ("Performance & Stress Testing", "Staging environment, k6 / Locust load scripts.", "Simulate target concurrent user load, measure request latency (p95, p99), throughput (RPS), and error rate.", "Performance Benchmark Summary.", "p95 latency < 300ms under 1000 concurrent user load."),
      ("Test Result Aggregation & Reporting", "All test logs (Unit, Integration, E2E, Performance).", "Aggregate results into unified JUnit XML / HTML report, update PR status check on Git host.", "Unified QA Test Summary Report.", "QA Lead sign-off on test pipeline execution.")],
     ["Gate 1: Unit coverage threshold (<80%) automatically blocks PR merge.",
      "Gate 2: Any E2E critical path failure halts release pipeline escalation."],
     ["Failure Mode 1: Flaky E2E test causing false pipeline failure -> Action: Quarantine flaky test, log bug ticket, re-run pipeline.",
      "Failure Mode 2: Performance test latency spike -> Action: Capture APM profile, escalate to performance engineer for query optimization."],
     "Unified JUnit XML test report, Code Coverage HTML report, E2E Playwright trace archives, and k6 performance report.")
]

# Write batch 3
for item in wf_list:
    write_wf(*item)

print("Batch 3 (21-24) written successfully.")
