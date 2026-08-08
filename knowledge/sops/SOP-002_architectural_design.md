# Standard Operating Procedure: SOP-002

## 1. Title & SOP Identification Number
- **SOP ID**: SOP-002
- **Title**: Architectural Design, Component Decomposition, and Interface Specification
- **Version**: 1.0.0
- **Status**: Production-Active
- **Domain**: Multi-Agent System Architecture & Engineering

---

## 2. Purpose & Objectives
The purpose of SOP-002 is to establish a rigorous, standardized methodology for transforming verified requirement specifications into scalable, modular, secure, and maintainable software architectures.

### Key Objectives:
1. **System Topology Definition**: Establish robust component boundaries, interface contracts, and data-flow topologies.
2. **Trade-Off Rationalization**: Evaluate architectural decisions against latency, complexity, security, and cost trade-offs using formal Architectural Decision Records (ADRs).
3. **Interface Standardization**: Define explicit, version-controlled REST/gRPC/JSON-Schema interface specifications prior to code generation.
4. **Structural Compliance**: Guarantee zero Single Points of Failure (SPOFs) for critical paths and enforce strict coupling/cohesion targets.

---

## 3. Scope & Applicability
This procedure applies to:
- Systems engineering, architectural blueprint modeling, API contract creation, and database schema design.
- The **Solution Architect (A03)**, supported by the **Lead Developer (A05)**, **Security Auditor (A07)**, and **QA Verification Agent (A06)**.

This procedure does **not** cover granular code syntax implementation (SOP-004) or deployment pipeline setup (SOP-007).

---

## 4. Trigger Conditions & Frequency
- **Trigger Condition 1**: Successful validation and signature of `requirements_spec.json` from SOP-001.
- **Trigger Condition 2**: Identification of architectural debt or structural redesign mandate during SOP-009 (Learning & Reflection).
- **Frequency**: Milestone-driven per discrete project phase or major feature addition.

---

## 5. Prerequisites & Required Inputs
### Prerequisites
- Formally signed `requirements_spec.json` (from SOP-001).
- Operational state machine transition to state `STATE_ARCHITECTURE`.
- Available technology stack guidelines (`policies/tech_stack_policy.yaml`).

### Required Inputs
1. `requirements_spec.json` (JSON object, required): Immutable intake spec.
2. `existing_architecture_manifest` (JSON object, optional): Baseline architecture spec for incremental designs.
3. `compliance_policies` (JSON array, required): Security, privacy (GDPR/HIPAA), and regulatory rule sets.

---

## 6. Roles & Responsibilities Matrix (RACI)

| Role | Agent / Identifier | RACI Responsibility | Key Duties |
| :--- | :--- | :--- | :--- |
| **Solution Architect** | A03_Architect | **Accountable (A) / Responsible (R)** | Leads design, defines topologies, authors ADRs, validates models. |
| **Lead Developer** | A05_LeadDev | **Consulted (C)** | Evaluates implementability, component feasibility, and library choices. |
| **Security Auditor** | A07_SecurityAuditor | **Consulted (C)** | Audits attack surfaces, auth models, and data encryption specs. |
| **QA Verification Agent** | A06_QAVerifier | **Consulted (C)** | Verifies testability and observable telemetry hook placements. |
| **Master Orchestrator** | A01_Orchestrator | **Informed (I)** | Tracks progress, enforces phase SLAs, receives architecture signoff. |

---

## 7. Step-by-Step Execution Procedure

```
 [requirements_spec.json] ---> (Step 1: Structural Analysis)
                                     |
                                     v
                              (Step 2: Component Topology)
                                     |
                                     v
                              (Step 3: Interface & Schema Spec)
                                     |
                                     v
                              (Step 4: Data & Persistence Modeling)
                                     |
                                     v
                              (Step 5: NFR & ADR Authoring)
                                     |
                                     v
                              (Step 6: Architecture Verification)
                                     |
                                     v
                         [architecture_spec.json]
```

### Step 1: Structural Analysis & Requirement Mapping
- **1.1 Requirement Matrix Mapping**: Map each Functional Requirement (FR) and Non-Functional Requirement (NFR) from SOP-001 into candidate architectural subsystems.
- **1.2 Constraint Audit**: Identify hard technical constraints (e.g., latency $< 50\text{ms}$, target runtime OS, memory caps).

### Step 2: Component Topology Definition
- **2.1 Subsystem Decomposition**: Partition system into decoupled modules using domain-driven design (DDD) principles.
- **2.2 Module Boundary Enforcement**: Define high cohesion within components and loose coupling across components. Coupling Index target: $C_{index} < 0.20$.
- **2.3 Data-Flow Diagramming**: Generate ASCII and Mermaid data-flow diagrams depicting component relationships, protocols, and message directions.

### Step 3: Interface & Schema Specification
- **3.1 API Contract Generation**: Define explicit REST (OpenAPI 3.0), gRPC (Protobuf), or Event (AsyncAPI) contracts for all inter-module communications.
- **3.2 Type Safety Enforcement**: Mandate strong typing and strict schema definitions for request/response payloads. Zero `any` or untyped dictionary primitives allowed.
- **3.3 Error Code Registry**: Standardize HTTP/RPC status code mappings and custom error payloads.

### Step 4: Data Modeling & Persistence Architecture
- **4.1 Entity-Relationship Modeling**: Define logical data models, tables, indexes, and relationship constraints.
- **4.2 Persistence Engine Selection**: Select target database (Relational, Document, Key-Value, Graph) based on workload profiles.
- **4.3 Migration Strategy**: Define schema versioning and zero-downtime migration scripts structure.

### Step 5: NFR & ADR Authoring
- **5.1 Resilience Modeling**: Define retry policies, circuit breakers, fallback handlers, and rate limiters for every external interaction point.
- **5.2 ADR Generation**: Document every key design decision using the standardized ADR template:
  - Context & Problem Statement
  - Decision Drivers
  - Considered Options
  - Decision Outcome & Rationale
  - Pros & Cons / Consequences

### Step 6: Architecture Verification & Sign-off
- **5.3 Static Verification**: Pass architectural model through static verification tool (`verification_engine.py`) to confirm zero circular dependencies.
- **5.4 Security Alignment**: Verify alignment with OWASP Top 10 prevention strategies and zero-trust data access models.

---

## 8. Decision Points & Verification Checks

```
Decision Matrix 2: Architecture Integrity Gate
----------------------------------------------------------------------------------
Metric / Check                       | Threshold Target | Result = PASS | Result = FAIL
----------------------------------------------------------------------------------
Circular Dependencies Count          | Exactly 0        | Advance       | Reject Topology
Coupling Index C_index               | < 0.20           | Advance       | Re-partition Subsystems
Requirement Coverage Ratio          | Exactly 1.0 (100%)| Advance       | Unmapped FRs Detected
ADR Completeness                     | All decisions doc| Final Signoff | Require ADR Drafts
----------------------------------------------------------------------------------
```

---

## 9. Exit Criteria & Deliverables
### Exit Criteria
- 100% requirement mapping coverage ($Coverage = 1.0$).
- Static verification passes with zero dependency violations.
- Formal sign-off by Solution Architect (A03) and Security Auditor (A07).

### Deliverables
1. `knowledge/artifacts/architecture/architecture_spec.json` — Structural blueprint and component registry.
2. `knowledge/artifacts/architecture/architecture_model.md` — Complete system specification with Mermaid flowcharts.
3. `knowledge/artifacts/architecture/adrs/ADR-001_*.md` — Suite of Architectural Decision Records.
4. `knowledge/artifacts/architecture/schemas/` — OpenAPI/JSON schema definitions for all interfaces.

---

## 10. Failure Handling & Escalation Path
- **Failure Scenario A: Unresolvable Architectural Trade-off**
  - *Action*: Halt architecture pipeline. Summarize trade-off matrix (Cost vs Latency vs Complexity).
  - *Escalation*: Trigger SOP-010 (Human Escalation) for executive decision.
- **Failure Scenario B: Security Policy Invalidation**
  - *Action*: Mark architecture draft as `SECURITY_REJECTED`. Refer back to Step 5.
  - *Escalation*: Trigger SOP-006 (Security Audit) for specialized review.

---

## 11. Audit Logging & Compliance Recordkeeping
Audit log generated upon completion of SOP-002, stored at `logs/audit/sops/sop_002_audit.json`:

```json
{
  "sop_id": "SOP-002",
  "execution_id": "exec_20260805_002931",
  "timestamp_utc": "2026-08-05T23:05:26Z",
  "initiator_agent": "A01_Orchestrator",
  "executing_agent": "A03_Architect",
  "input_requirements_hash": "a1b2c3d4e5f6...",
  "architecture_metrics": {
    "component_count": 6,
    "interface_contract_count": 12,
    "adr_count": 4,
    "coupling_index": 0.14,
    "requirement_coverage": 1.0
  },
  "deliverable_path": "knowledge/artifacts/architecture/architecture_spec.json",
  "verification_status": "PASSED",
  "signature": "8f7e6d5c4b3a..."
}
```
