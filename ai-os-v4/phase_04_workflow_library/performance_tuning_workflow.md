# Performance Tuning Workflow Specification

## 1. Purpose & Objective
Identify system bottlenecks, optimize database queries, adjust memory allocations, refine caching strategies, and verify latency improvements.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: APM monitoring data (Datadog/NewRelic), performance benchmark scripts (k6), system profile access.
- **Trigger Conditions**: SLA latency threshold breach alert or high resource utilization alert.

## 3. Participating Agent Roles & Responsibilities
- **Performance Engineer**: Conducts profiling analyses, identifies latency hotspots, and writes benchmark scripts.
- **DB Specialist**: Optimizes SQL queries, index structures, connection pooling, and cache invalidation.
- **System Architect**: Adjusts JVM/Node memory settings, thread pools, and distributed caching topology.

## 4. Step-by-Step Execution Sequence

### Step 1: Baseline Benchmarking & Bottleneck Profiling
- **Inputs**: APM telemetry, target endpoints, k6 load testing suite.
- **Actions**: Execute baseline load test, capture flame graphs (cpu/memory/io), identify top 3 latency bottleneck methods/queries.
- **Outputs**: Baseline Performance Report & Flame Graph Traces.
- **Verification**: Identified bottleneck contributing >= 40% to overall request latency.

### Step 2: Database & Query Optimization
- **Inputs**: Slow query log, EXPLAIN ANALYZE traces, DB schema.
- **Actions**: Optimize slow SQL queries, add composite database indices, adjust ORM eager/lazy loading strategy.
- **Outputs**: Optimized SQL Queries & Index Migration Scripts.
- **Verification**: EXPLAIN ANALYZE shows index scan replacing costly sequential table scan.

### Step 3: Caching Strategy Implementation
- **Inputs**: Frequent query patterns, Redis / Memcached cluster.
- **Actions**: Implement multi-level caching (in-memory + Redis), configure TTLs and cache invalidation hooks.
- **Outputs**: Caching Layer Integration Code.
- **Verification**: Cache hit ratio >= 85% verified under test load.

### Step 4: System & Memory Tuning
- **Inputs**: Runtime config (JVM flags / Node heap / Worker counts), load generator.
- **Actions**: Tune thread pool sizes, garbage collection parameters, keep-alive connections, and memory allocation caps.
- **Outputs**: Tuned System Configuration Files.
- **Verification**: Memory usage stabilized with zero full GC pause spikes under peak load.

### Step 5: Verification Load Test & SLA Audit
- **Inputs**: Tuned environment, k6 load test script.
- **Actions**: Re-run identical k6 load test benchmark, compare throughput (RPS), p95/p99 latency against baseline.
- **Outputs**: Final Performance Comparison Audit Report.
- **Verification**: p95 latency reduced by >= 40% and throughput increased by >= 50% vs baseline.

## 5. Decision Gates & Branching Rules
- Gate 1: Bottleneck root cause must be isolated via flame graph trace before code modification.
- Gate 2: Verification load test must prove >= 30% p95 latency reduction without introducing error rate spikes.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Cache stampede under high load -> Action: Implement probabilistic early expiration / mutex lock on cache refresh.
- Failure Mode 2: Database index addition causes write slowdown -> Action: Evaluate partial/sparse index alternative.

## 7. Artifact Delivery & Output Standard
Baseline vs Post-Tuning Performance Report, Flame Graph Profiling Artifacts, Index Migration Scripts, and k6 Execution Logs.
