# Database Migration Workflow Specification

## 1. Purpose & Objective
Execute zero-downtime database schema updates, column migrations, and data transformations across production environments.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Database migration scripts (up/down SQL), staging database snapshot, schema migration tool (Flyway/Prisma/Liquibase).
- **Trigger Conditions**: Feature release requiring DB schema changes or table restructuring.

## 3. Participating Agent Roles & Responsibilities
- **Database Administrator**: Reviews SQL migration scripts, locks table indices, and oversees execution safety.
- **Backend Engineer**: Writes ORM model migrations, backward-compatible data access code, and rollback scripts.
- **SRE Specialist**: Monitors DB connection pool, query execution latency, and replication lag during migration.

## 4. Step-by-Step Execution Sequence

### Step 1: Migration Script Authoring & Dry-Run Test
- **Inputs**: Schema diff, ORM migration generator, local database instance.
- **Actions**: Write backward-compatible migration script (expand-contract pattern), draft rollback down-script.
- **Outputs**: Validated SQL Migration Scripts (UP/DOWN).
- **Verification**: Dry-run execution against local test database succeeds.

### Step 2: Staging Environment Validation
- **Inputs**: SQL migration scripts, staging database clone.
- **Actions**: Apply migration script to staging database; verify ORM queries against modified schema.
- **Outputs**: Staging Migration Execution Log.
- **Verification**: Migration completes on staging with 0 query syntax errors and clean rollback test.

### Step 3: Pre-Migration Backup & Locking Audit
- **Inputs**: Production DB instance, snapshot tool (AWS RDS Snapshots).
- **Actions**: Trigger manual DB snapshot, inspect active long-running queries, verify replication lag is zero.
- **Outputs**: Pre-Migration Snapshot ID & Health Check Log.
- **Verification**: Snapshot completed and verified restored on sandbox instance.

### Step 4: Production Migration Execution
- **Inputs**: Production DB credentials, migration runner, SRE monitoring.
- **Actions**: Apply migration script to production DB using expand-contract strategy; monitor locks and CPU utilization.
- **Outputs**: Production Migration Execution Log.
- **Verification**: Migration runner exits with code 0 and table locks released.

### Step 5: Data Validation & Application Sync
- **Inputs**: Production database, application servers, verification queries.
- **Actions**: Run data validation queries to check row counts and column constraints; deploy application code update.
- **Outputs**: Post-Migration Data Verification Report.
- **Verification**: 100% row count checksum match and 0 database query errors in application logs.

## 5. Decision Gates & Branching Rules
- Gate 1: Migration scripts must follow expand-contract pattern (no destructive drops in initial migration).
- Gate 2: Pre-migration snapshot verification must pass before executing scripts on production.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Table lock timeout during schema migration -> Action: Abort migration, kill blocking query, re-run with explicit lock timeout parameters.
- Failure Mode 2: Data corruption during column transform -> Action: Execute down-script rollback or restore DB state from pre-migration snapshot.

## 7. Artifact Delivery & Output Standard
Tested SQL Migration Scripts, Pre-Migration Snapshot Verification, Production Execution Log, and Post-Migration Data Report.
