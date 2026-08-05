# Data Pipeline Workflow Specification

## 1. Purpose & Objective
Construct scalable Extract, Transform, Load (ETL/ELT) data pipelines, ensuring schema validation, data quality checks, and data warehouse ingestion.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Raw data sources (Kafka/S3/SQL), target data warehouse (Snowflake/BigQuery), Airflow/dbt environment.
- **Trigger Conditions**: New data source integration request or scheduled ETL pipeline trigger.

## 3. Participating Agent Roles & Responsibilities
- **Data Engineer**: Author Airflow DAGs, Spark jobs, dbt transformation models, and pipeline code.
- **Analytics Specialist**: Defines data warehouse schemas, business metrics, and dimensional models (Kimball).
- **Data Quality Auditor**: Configures Great Expectations data quality tests, anomaly detection, and schema drift checks.

## 4. Step-by-Step Execution Sequence

### Step 1: Data Source Discovery & Schema Mapping
- **Inputs**: Raw data sample (JSON/CSV/Parquet), source API/DB specs.
- **Actions**: Analyze source data schema, define target staging/marts tables in data warehouse, outline ETL transformation steps.
- **Outputs**: Data Architecture & Schema Mapping Spec.
- **Verification**: Analytics Specialist approval of dimensional model layout.

### Step 2: Pipeline & DAG Implementation
- **Inputs**: Schema mapping, Apache Airflow / Prefect framework, PySpark / SQL scripts.
- **Actions**: Develop pipeline extraction scripts, transformation logic, and load handlers; construct Airflow DAG dependencies.
- **Outputs**: Airflow DAG python code co-located with unit tests.
- **Verification**: Airflow DAG syntax check (`airflow dags test`) passing with zero errors.

### Step 3: Data Quality Check Configuration
- **Inputs**: Transformed data models, Great Expectations framework.
- **Actions**: Define validation rules (non-null constraints, unique keys, range checks, foreign key integrity).
- **Outputs**: Great Expectations Suite JSON config.
- **Verification**: Data Quality test suite passes against sample staging dataset.

### Step 4: Pipeline Integration & Staging Run
- **Inputs**: Airflow environment, staging data warehouse dataset.
- **Actions**: Trigger DAG run on staging cluster, monitor task execution duration, inspect data loading efficiency.
- **Outputs**: Staging Pipeline Execution Log & Audit Dashboard.
- **Verification**: 100% task success rate in Airflow DAG execution.

### Step 5: Production Deployment & Telemetry Alerting
- **Inputs**: Passed Airflow DAG, production Snowflake/BigQuery credentials.
- **Actions**: Deploy DAG to production Airflow scheduler; configure PagerDuty / Slack alerts for pipeline failures or SLA breaches.
- **Outputs**: Production Pipeline Deployment Log.
- **Verification**: Successful initial production DAG run with verified table counts.

## 5. Decision Gates & Branching Rules
- Gate 1: Great Expectations data quality suite must pass 100% prior to pushing data to production marts.
- Gate 2: Pipeline execution time must meet target SLA window (e.g. completed before 06:00 AM UTC).

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Source schema drift breaks ETL parser -> Action: Quarantine bad batch into dead-letter queue, notify Data Engineer, auto-adjust schema mapping.
- Failure Mode 2: Data warehouse loading out-of-memory -> Action: Optimize Spark partition sizing, adjust chunk load limits.

## 7. Artifact Delivery & Output Standard
Airflow DAG Python code, dbt transformation models, Great Expectations validation report, and Production Pipeline Run Logs.
