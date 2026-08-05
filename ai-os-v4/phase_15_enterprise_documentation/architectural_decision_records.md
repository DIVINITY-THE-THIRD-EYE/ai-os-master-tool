# AI OS v4 — Architectural Decision Records (ADR) Repository

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Enterprise Engineering Record Repository  
**Status:** Frozen / Production Standard  

---

## 1. Overview & ADR Governance

This document records the foundational architectural decisions made during the design and construction of AI OS v4. All ADRs follow Nygard format and represent binding platform choices.

---

## 2. Master ADR Index (ADR-001 through ADR-010)

```
+---------+-------------------------------------------------------------------------+----------+
| ADR ID  | Title                                                                   | Status   |
+---------+-------------------------------------------------------------------------+----------+
| ADR-001 | Two-Phase Commit (2PC) for Memory Mutation                              | ACCEPTED |
| ADR-002 | Decoupled Event-Driven Micro-Kernel over Monolithic RPC                 | ACCEPTED |
| ADR-003 | Multi-Tiered Sandbox Isolation (WASM, OCI, Firecracker)                 | ACCEPTED |
| ADR-004 | Declarative YAML/JSON Workflow DSL over Code-as-Workflow                | ACCEPTED |
| ADR-005 | Decentralized Verification Engine Quality Gates                         | ACCEPTED |
| ADR-006 | Cryptographic Merkle Hash-Chain Audit Logging                           | ACCEPTED |
| ADR-007 | Sliding Window Counter Rate Limiting with Redis Backing                 | ACCEPTED |
| ADR-008 | Mandatory SHA-256 Cryptographic Lineage Tracking                        | ACCEPTED |
| ADR-009 | Risk-Based Multi-Signature Approval Gates                               | ACCEPTED |
| ADR-010 | Candidate Memory Pipeline for Enterprise Knowledge Graph Commits        | ACCEPTED |
+---------+-------------------------------------------------------------------------+----------+
```

---

## 3. Concrete ADR Specifications

### ADR-001: Two-Phase Commit (2PC) for Memory Mutation
- **Status:** ACCEPTED  
- **Context:** Concurrent agents modifying working memory, vector stores, and the Enterprise Knowledge Graph (EKG) simultaneously risked data corruption during crashes or network partitions.
- **Decision:** Implement a lightweight 2PC transaction coordinator within the Memory Engine.
- **Alternatives Considered:** Sagas (rejected due to complex compensation logic), Eventual Consistency (rejected due to strict verification requirements).
- **Consequences:** Guarantees strict atomic consistency across memory stores; adds ~12ms latency to memory commits.

---

### ADR-002: Decoupled Event-Driven Micro-Kernel
- **Status:** ACCEPTED  
- **Context:** Direct inter-agent RPC created fragile, tight coupling and cascading timeouts.
- **Decision:** All cross-subsystem communication MUST occur via typed event contracts over NATS / Kafka Event Bus.
- **Alternatives Considered:** Direct gRPC (rejected due to coupling), Shared Memory Mutexes (rejected due to distributed scalability limits).
- **Consequences:** Maximizes asynchronous scaling and resilience; requires strict event schema registry maintenance.

---

### ADR-003: Multi-Tiered Sandbox Isolation
- **Status:** ACCEPTED  
- **Context:** Executing third-party tools and dynamic plugins presented extreme security risks (command injection, path traversal, host escape).
- **Decision:** Deploy a 4-tier isolation matrix (Tier 0: In-Process, Tier 1: WASM, Tier 2: OCI Container, Tier 3: AWS Firecracker MicroVM).
- **Alternatives Considered:** Docker-only (rejected due to slow boot times for simple tools), chroot (rejected due to weak isolation).
- **Consequences:** Delivers optimal performance-to-security tradeoff; requires managing WASM and KVM infrastructure.

---

### ADR-004: Declarative Workflow DSL
- **Status:** ACCEPTED  
- **Context:** Imperative Python workflow scripts were hard to validate, visualize, and dynamically modify at runtime.
- **Decision:** Formulate a declarative JSON/YAML Workflow Definition Language (DSL) parsed into AST state graphs by the DAG Scheduler.
- **Alternatives Considered:** Python-based Workflows (Temporal/Airflow) (rejected due to lack of safe dynamic inspectability).
- **Consequences:** Workflows can be fully validated before execution; eliminates dynamic code execution risks.

---

### ADR-005: Decentralized Verification Engine Quality Gates
- **Status:** ACCEPTED  
- **Context:** Unverified agent outputs frequently introduced subtle bugs, security vulnerabilities, or incomplete documentation into production repositories.
- **Decision:** Mandate automated 9-dimension quality gate verification before any task transitions to `COMPLETED`.
- **Alternatives Considered:** Post-deployment testing (rejected due to high cost of failure).
- **Consequences:** Prevents low-quality artifacts from entering production; increases average task processing duration by ~5%.

---

### ADR-006: Cryptographic Merkle Hash-Chain Audit Logging
- **Status:** ACCEPTED  
- **Context:** Compliance frameworks (SOC2, EU AI Act) require tamper-evident records of agent decisions and tool calls.
- **Decision:** Chain all audit log entries using SHA-256 Merkle trees stored in WORM storage.
- **Alternatives Considered:** Standard database logging (rejected due to vulnerability to insider tampering).
- **Consequences:** Audit logs are legally binding and cryptographically tamper-evident.

---

### ADR-007: Sliding Window Counter Rate Limiting with Redis Backing
- **Status:** ACCEPTED  
- **Context:** Burst traffic and upstream LLM API throttling caused service outages.
- **Decision:** Implement multi-tier sliding window rate limiters executed via atomic Lua scripts in Redis Cluster.
- **Alternatives Considered:** Fixed window counters (rejected due to boundary traffic spikes).
- **Consequences:** Smooths traffic bursts cleanly; requires high-availability Redis infrastructure.

---

### ADR-008: Mandatory Cryptographic Lineage Tracking
- **Status:** ACCEPTED  
- **Context:** Enterprise teams need complete traceability to know which LLM, prompt, and agent created a specific line of code.
- **Decision:** Every generated artifact MUST embed a signed provenance block with input SHA-256 hashes and prompt template IDs.
- **Alternatives Considered:** External database mapping (rejected due to loss of lineage during file copies).
- **Consequences:** Lineage survives file movement; increases artifact header size slightly.

---

### ADR-009: Risk-Based Multi-Signature Approval Gates
- **Status:** ACCEPTED  
- **Context:** High-risk actions (production database drops, financial transactions) require human oversight.
- **Decision:** Integrate a 4-tier risk matrix requiring $M$-of-$N$ human cryptographic sign-offs for CRITICAL actions.
- **Alternatives Considered:** Single admin approval (rejected due to single point of failure/compromise).
- **Consequences:** Protects production environments from rogue agent executions; adds approval delay for high-risk operations.

---

### ADR-010: Candidate Memory Pipeline for EKG Commits
- **Status:** ACCEPTED  
- **Context:** Direct agent writes to the Enterprise Knowledge Graph degraded graph accuracy with unverified hallucinated facts.
- **Decision:** Invariant Rule #1: All knowledge mutations MUST go through Candidate Memory $\rightarrow$ Verification $\rightarrow$ HITL Gate $\rightarrow$ Commit.
- **Alternatives Considered:** Direct write with background cleanup (rejected due to dirty read propagation).
- **Consequences:** Ensures 100% verified accuracy of knowledge graph; requires candidate memory buffer maintenance.

---

## 4. Summary Checklist for ADR Compliance

- [x] Full master index of ADRs (001 through 010) created.
- [x] Standard Nygard ADR format (Status, Context, Decision, Alternatives, Consequences) followed.
- [x] All 5 core architectural invariants formally backed by accepted ADRs.
