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

wf_list = [
    # 31
    ("code_refactoring_workflow.md", "Code Refactoring Workflow",
     "Improve code readability, maintainability, and structural design while strictly preserving existing functional behavior.",
     "Target codebase module, existing test suite with high coverage (>85%), static analysis report of code smells.",
     "High cyclomatic complexity alert, technical debt sprint task assignment.",
     [("Senior Refactoring Lead", "Identifies anti-patterns, defines target architectural design, and enforces zero-regression rule."),
      ("Software Engineer", "Applies design patterns, extracts modules, eliminates code duplicate blocks, and refactors methods."),
      ("QA Specialist", "Executes regression test suites and benchmarks execution latency to verify behavior parity.")],
     [("Code Smell Identification & Baseline Test Run", "Target source file, SonarQube complexity report, existing unit test suite.", "Identify high complexity functions, duplicate code blocks, tight coupling; execute baseline test suite.", "Refactoring Plan Document and Baseline Test Run Logs.", "100% baseline test pass rate established prior to code edits."),
      ("Modular Decomposition & Interface Extraction", "Target codebase, Refactoring Plan.", "Extract long methods into smaller functions, decouple class dependencies using interface abstractions.", "Refactored module skeleton.", "TypeScript/Python compiler passing with zero structural syntax errors."),
      ("Design Pattern Application", "Module skeleton, design pattern rules (Factory, Strategy, Observer).", "Apply appropriate design patterns to streamline control flow and eliminate conditional branching duplication.", "Refactored codebase implementation.", "Unit tests re-executed locally with 100% pass rate."),
      ("Regression Verification & Coverage Audit", "Refactored codebase, full integration test suite, coverage analyzer.", "Run full integration test suite, compare code coverage against baseline; verify no behavioral regressions.", "Coverage Comparison Report.", "Code coverage maintained at or above baseline (>85%), 0 broken tests."),
      ("Performance Diff & Code Review", "Refactored PR, benchmark scripts, SonarQube scanner.", "Measure memory and latency impact; execute SonarQube scanner to confirm cyclomatic complexity reduction.", "Refactoring Pull Request & SonarQube Summary.", "Cyclomatic complexity reduced by >= 30% with 0 functional regressions.")],
     ["Gate 1: Existing unit test suite must pass 100% before starting refactoring edits.",
      "Gate 2: Code coverage must not decrease as a result of the refactoring process."],
     ["Failure Mode 1: Refactoring breaks legacy edge-case behavior -> Action: Revert commit to previous green state, add missing unit test for edge-case, re-attempt refactoring.",
      "Failure Mode 2: Latency regression introduced -> Action: Profile execution trace, optimize memory allocation, re-benchmark."],
     "Refactored Code Pull Request, SonarQube Complexity Reduction Report, Baseline vs Post-Refactor Test Results."),

    # 32
    ("database_migration_workflow.md", "Database Migration Workflow",
     "Execute zero-downtime database schema updates, column migrations, and data transformations across production environments.",
     "Database migration scripts (up/down SQL), staging database snapshot, schema migration tool (Flyway/Prisma/Liquibase).",
     "Feature release requiring DB schema changes or table restructuring.",
     [("Database Administrator", "Reviews SQL migration scripts, locks table indices, and oversees execution safety."),
      ("Backend Engineer", "Writes ORM model migrations, backward-compatible data access code, and rollback scripts."),
      ("SRE Specialist", "Monitors DB connection pool, query execution latency, and replication lag during migration.")],
     [("Migration Script Authoring & Dry-Run Test", "Schema diff, ORM migration generator, local database instance.", "Write backward-compatible migration script (expand-contract pattern), draft rollback down-script.", "Validated SQL Migration Scripts (UP/DOWN).", "Dry-run execution against local test database succeeds."),
      ("Staging Environment Validation", "SQL migration scripts, staging database clone.", "Apply migration script to staging database; verify ORM queries against modified schema.", "Staging Migration Execution Log.", "Migration completes on staging with 0 query syntax errors and clean rollback test."),
      ("Pre-Migration Backup & Locking Audit", "Production DB instance, snapshot tool (AWS RDS Snapshots).", "Trigger manual DB snapshot, inspect active long-running queries, verify replication lag is zero.", "Pre-Migration Snapshot ID & Health Check Log.", "Snapshot completed and verified restored on sandbox instance."),
      ("Production Migration Execution", "Production DB credentials, migration runner, SRE monitoring.", "Apply migration script to production DB using expand-contract strategy; monitor locks and CPU utilization.", "Production Migration Execution Log.", "Migration runner exits with code 0 and table locks released."),
      ("Data Validation & Application Sync", "Production database, application servers, verification queries.", "Run data validation queries to check row counts and column constraints; deploy application code update.", "Post-Migration Data Verification Report.", "100% row count checksum match and 0 database query errors in application logs.")],
     ["Gate 1: Migration scripts must follow expand-contract pattern (no destructive drops in initial migration).",
      "Gate 2: Pre-migration snapshot verification must pass before executing scripts on production."],
     ["Failure Mode 1: Table lock timeout during schema migration -> Action: Abort migration, kill blocking query, re-run with explicit lock timeout parameters.",
      "Failure Mode 2: Data corruption during column transform -> Action: Execute down-script rollback or restore DB state from pre-migration snapshot."],
     "Tested SQL Migration Scripts, Pre-Migration Snapshot Verification, Production Execution Log, and Post-Migration Data Report."),

    # 33
    ("performance_tuning_workflow.md", "Performance Tuning Workflow",
     "Identify system bottlenecks, optimize database queries, adjust memory allocations, refine caching strategies, and verify latency improvements.",
     "APM monitoring data (Datadog/NewRelic), performance benchmark scripts (k6), system profile access.",
     "SLA latency threshold breach alert or high resource utilization alert.",
     [("Performance Engineer", "Conducts profiling analyses, identifies latency hotspots, and writes benchmark scripts."),
      ("DB Specialist", "Optimizes SQL queries, index structures, connection pooling, and cache invalidation."),
      ("System Architect", "Adjusts JVM/Node memory settings, thread pools, and distributed caching topology.")],
     [("Baseline Benchmarking & Bottleneck Profiling", "APM telemetry, target endpoints, k6 load testing suite.", "Execute baseline load test, capture flame graphs (cpu/memory/io), identify top 3 latency bottleneck methods/queries.", "Baseline Performance Report & Flame Graph Traces.", "Identified bottleneck contributing >= 40% to overall request latency."),
      ("Database & Query Optimization", "Slow query log, EXPLAIN ANALYZE traces, DB schema.", "Optimize slow SQL queries, add composite database indices, adjust ORM eager/lazy loading strategy.", "Optimized SQL Queries & Index Migration Scripts.", "EXPLAIN ANALYZE shows index scan replacing costly sequential table scan."),
      ("Caching Strategy Implementation", "Frequent query patterns, Redis / Memcached cluster.", "Implement multi-level caching (in-memory + Redis), configure TTLs and cache invalidation hooks.", "Caching Layer Integration Code.", "Cache hit ratio >= 85% verified under test load."),
      ("System & Memory Tuning", "Runtime config (JVM flags / Node heap / Worker counts), load generator.", "Tune thread pool sizes, garbage collection parameters, keep-alive connections, and memory allocation caps.", "Tuned System Configuration Files.", "Memory usage stabilized with zero full GC pause spikes under peak load."),
      ("Verification Load Test & SLA Audit", "Tuned environment, k6 load test script.", "Re-run identical k6 load test benchmark, compare throughput (RPS), p95/p99 latency against baseline.", "Final Performance Comparison Audit Report.", "p95 latency reduced by >= 40% and throughput increased by >= 50% vs baseline.")],
     ["Gate 1: Bottleneck root cause must be isolated via flame graph trace before code modification.",
      "Gate 2: Verification load test must prove >= 30% p95 latency reduction without introducing error rate spikes."],
     ["Failure Mode 1: Cache stampede under high load -> Action: Implement probabilistic early expiration / mutex lock on cache refresh.",
      "Failure Mode 2: Database index addition causes write slowdown -> Action: Evaluate partial/sparse index alternative."],
     "Baseline vs Post-Tuning Performance Report, Flame Graph Profiling Artifacts, Index Migration Scripts, and k6 Execution Logs."),

    # 34
    ("data_pipeline_workflow.md", "Data Pipeline Workflow",
     "Construct scalable Extract, Transform, Load (ETL/ELT) data pipelines, ensuring schema validation, data quality checks, and data warehouse ingestion.",
     "Raw data sources (Kafka/S3/SQL), target data warehouse (Snowflake/BigQuery), Airflow/dbt environment.",
     "New data source integration request or scheduled ETL pipeline trigger.",
     [("Data Engineer", "Author Airflow DAGs, Spark jobs, dbt transformation models, and pipeline code."),
      ("Analytics Specialist", "Defines data warehouse schemas, business metrics, and dimensional models (Kimball)."),
      ("Data Quality Auditor", "Configures Great Expectations data quality tests, anomaly detection, and schema drift checks.")],
     [("Data Source Discovery & Schema Mapping", "Raw data sample (JSON/CSV/Parquet), source API/DB specs.", "Analyze source data schema, define target staging/marts tables in data warehouse, outline ETL transformation steps.", "Data Architecture & Schema Mapping Spec.", "Analytics Specialist approval of dimensional model layout."),
      ("Pipeline & DAG Implementation", "Schema mapping, Apache Airflow / Prefect framework, PySpark / SQL scripts.", "Develop pipeline extraction scripts, transformation logic, and load handlers; construct Airflow DAG dependencies.", "Airflow DAG python code co-located with unit tests.", "Airflow DAG syntax check (`airflow dags test`) passing with zero errors."),
      ("Data Quality Check Configuration", "Transformed data models, Great Expectations framework.", "Define validation rules (non-null constraints, unique keys, range checks, foreign key integrity).", "Great Expectations Suite JSON config.", "Data Quality test suite passes against sample staging dataset."),
      ("Pipeline Integration & Staging Run", "Airflow environment, staging data warehouse dataset.", "Trigger DAG run on staging cluster, monitor task execution duration, inspect data loading efficiency.", "Staging Pipeline Execution Log & Audit Dashboard.", "100% task success rate in Airflow DAG execution."),
      ("Production Deployment & Telemetry Alerting", "Passed Airflow DAG, production Snowflake/BigQuery credentials.", "Deploy DAG to production Airflow scheduler; configure PagerDuty / Slack alerts for pipeline failures or SLA breaches.", "Production Pipeline Deployment Log.", "Successful initial production DAG run with verified table counts.")],
     ["Gate 1: Great Expectations data quality suite must pass 100% prior to pushing data to production marts.",
      "Gate 2: Pipeline execution time must meet target SLA window (e.g. completed before 06:00 AM UTC)."],
     ["Failure Mode 1: Source schema drift breaks ETL parser -> Action: Quarantine bad batch into dead-letter queue, notify Data Engineer, auto-adjust schema mapping.",
      "Failure Mode 2: Data warehouse loading out-of-memory -> Action: Optimize Spark partition sizing, adjust chunk load limits."],
     "Airflow DAG Python code, dbt transformation models, Great Expectations validation report, and Production Pipeline Run Logs."),

    # 35
    ("model_training_workflow.md", "Model Training Workflow",
     "Execute large-scale Machine Learning model training, hyperparameter optimization, distributed multi-GPU orchestration, and checkpoint verification.",
     "Cleaned dataset, ML framework (PyTorch/TensorFlow), GPU compute cluster, WandB / MLflow logging framework.",
     "Scheduled model retrain trigger or new model architecture experiment authorization.",
     [("ML Engineer", "Constructs distributed training pipeline, GPU cluster scripts, and model checkpointing."),
      ("Data Scientist", "Selects feature sets, loss functions, learning rate schedules, and optimization algorithms."),
      ("Systems Engineer", "Monitors GPU cluster memory utilization, CUDA driver compatibility, and node communication latency.")],
     [("Dataset Preparation & Pipeline Validation", "Raw dataset, feature store, target preprocessing scripts.", "Load features from feature store, execute data normalization, split dataset (80/10/10), verify batch loader performance.", "Processed Dataset Loaders & Validation Stats.", "Dataset loader pipeline achieves target GPU feed throughput (0 IO bottleneck)."),
      ("Training Script & Architecture Setup", "ML framework (PyTorch/Lightning), hyperparameter configuration file.", "Configure distributed data parallel (DDP) training loop, implement loss functions, set up automatic mixed-precision (AMP).", "Model Training Script (train.py).", "Single-batch training dry-run completes with loss value computation."),
      ("Distributed Multi-GPU Training Run", "Training script, Ray / Torchrun cluster configuration, WandB tracking.", "Launch distributed training job across GPU nodes; monitor GPU memory usage, loss convergence, and gradient norms.", "WandB Experiment Dashboard & Training Logs.", "Model loss decreases steadily without gradient explosion or NaN loss values."),
      ("Hyperparameter Tuning Sweep", "Baseline model, Optuna / WandB Sweep configuration file.", "Run hyperparameter optimization sweep across learning rates, batch sizes, and optimizer choices; select top checkpoint.", "Hyperparameter Search Matrix & Best Checkpoint.", "Best hyperparameter combination identified achieving optimal validation loss."),
      ("Model Checkpoint Export & Validation", "Best checkpoint weights, ONNX / TensorRT export scripts.", "Export model weights to ONNX/TensorRT format; verify inference latency on target GPU hardware.", "Exported Model Artifact (.onnx / .pt) & Benchmark Report.", "Inference latency on target hardware meets production SLA (< 50ms).")],
     ["Gate 1: Validation loss must show steady convergence over training epochs without NaN values.",
      "Gate 2: Exported ONNX model must pass precision parity test (difference < 1e-4) compared to raw PyTorch model."],
     ["Failure Mode 1: CUDA Out-Of-Memory (OOM) during training -> Action: Enable gradient accumulation, reduce per-GPU batch size, enable PyTorch AMP FP16/BF16.",
      "Failure Mode 2: Loss divergence / explosion -> Action: Implement gradient clipping (max norm 1.0), decrease learning rate by factor of 10."],
     "PyTorch Training Script repository, WandB Training Run Logs, Exported ONNX model file, and Inference Performance Benchmark Report.")
]

# Write batch 5
for item in wf_list:
    write_wf(*item)

print("Batch 5 (31-35) written successfully.")
