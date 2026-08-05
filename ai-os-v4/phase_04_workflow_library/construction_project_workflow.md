# Construction Project Workflow Specification

## 1. Purpose & Objective
Orchestrate architectural blueprint verification, site preparation, structural execution, safety compliance, and commissioning.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Architectural drawings, civil engineering specs, environmental permits, structural calculations.
- **Trigger Conditions**: Issuance of municipal building permit and site handover.

## 3. Participating Agent Roles & Responsibilities
- **Construction Manager**: Oversees site logistics, contractor scheduling, budget tracking, and subcontractor coordination.
- **Civil Engineer**: Verifies structural integrity, foundation soil tests, and concrete pour specs.
- **Safety Auditor**: Conducts OSHA safety compliance inspections and risk hazard assessments.

## 4. Step-by-Step Execution Sequence

### Step 1: Blueprint Audit & BIM Coordination
- **Inputs**: Architectural/structural CAD/BIM models (Revit), municipal permits.
- **Actions**: Run Building Information Modeling (BIM) clash detection between structural, MEP (mechanical, electrical, plumbing) systems.
- **Outputs**: Clash Detection Report and coordinated BIM master model.
- **Verification**: BIM Coordinator sign-off with 0 hard structural clashes.

### Step 2: Site Preparation & Excavation
- **Inputs**: Site survey drawings, geotechnical soil report, heavy equipment schedule.
- **Actions**: Execute site grading, soil compaction testing, utility line layout, and foundation excavation.
- **Outputs**: Soil compaction test results and survey verification log.
- **Verification**: Geotechnical engineer validation of soil bearing capacity >= target kPa.

### Step 3: Structural Framing & Concrete Pour
- **Inputs**: Structural drawings, rebar schedules, concrete batch mix specs.
- **Actions**: Form foundation footings, place rebar cages, conduct slump test, perform concrete pour, monitor curing strength.
- **Outputs**: Concrete cylinder break test reports (7-day and 28-day).
- **Verification**: 28-day break test confirming compressive strength meets specified PSI/MPa.

### Step 4: MEP Installation & Enclosure
- **Inputs**: MEP drawings, framing inspection sign-off.
- **Actions**: Install framing studs, exterior cladding, roofing, electrical wiring, plumbing runs, and HVAC ductwork.
- **Outputs**: Rough-in inspection report from municipal inspector.
- **Verification**: Passed municipal rough-in inspections for electrical, plumbing, and framing.

### Step 5: Commissioning & Handover
- **Inputs**: As-built drawings, punch list, HVAC balancing reports.
- **Actions**: Perform HVAC balancing, fire alarm system testing, resolve punch list items, conduct final walkthrough.
- **Outputs**: Certificate of Occupancy (CO) and final handover binder.
- **Verification**: Issuance of official Certificate of Occupancy by municipal authority.

## 5. Decision Gates & Branching Rules
- Gate 1: BIM clash detection must resolve all MEP vs structural interferences before site excavation.
- Gate 2: Concrete pour requires passed rebar inspection and batch slump test prior to delivery.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Soil bearing capacity below spec during excavation -> Action: Perform soil stabilization (grouting/deep piers), re-test bearing capacity.
- Failure Mode 2: Structural framing inspection failure -> Action: Issue Subcontractor Corrective Action Notice, re-inspect framing within 48 hours.

## 7. Artifact Delivery & Output Standard
Coordinated BIM model, municipal inspection sign-offs, 28-day concrete strength certificates, and final Certificate of Occupancy.
