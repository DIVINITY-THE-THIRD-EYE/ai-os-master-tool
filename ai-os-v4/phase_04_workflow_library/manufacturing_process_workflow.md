# Manufacturing Process Workflow Specification

## 1. Purpose & Objective
Govern production line setup, tool tooling validation, CNC path programming, quality control sampling, and assembly line balancing.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Released eBOM, 2D drawings, raw material inventory, production machinery specifications.
- **Trigger Conditions**: Production release order execution.

## 3. Participating Agent Roles & Responsibilities
- **Process Engineer**: Designs manufacturing operations, routing sheets, and assembly instructions.
- **Manufacturing Specialist**: Programs CNC/robotic equipment, setups tooling fixtures, and manages pilot runs.
- **Quality Control Auditor**: Conducts CMM inspection, Statistical Process Control (SPC) monitoring, and first-article inspection (FAI).

## 4. Step-by-Step Execution Sequence

### Step 1: Process Routing & Operation Sheet Definition
- **Inputs**: Released eBOM, engineering drawings.
- **Actions**: Define step-by-step manufacturing routing, select machine centers (CNC, lathe, injection molding), calculate cycle times.
- **Outputs**: Manufacturing Process Plan (MPP) and Operation Sheets.
- **Verification**: Process Engineer approval of operational routing sequence.

### Step 2: Tooling Design & CNC Programming
- **Inputs**: CAD models, MPP operation specs, CAM software (Mastercam/Siemens NX).
- **Actions**: Design custom fixtures and jigs, generate CNC toolpaths, run CAM simulation to detect collisions.
- **Outputs**: CAM files, G-code programs, and physical tooling fixtures.
- **Verification**: CAM simulation verification with 0 tool collision events.

### Step 3: Pilot Run & First Article Inspection (FAI)
- **Inputs**: Tooling fixtures, CNC G-code, raw material stock.
- **Actions**: Execute pilot production run of 10 units, inspect dimensions using CMM (Coordinate Measuring Machine).
- **Outputs**: First Article Inspection Report (FAIR) according to AS9102 standard.
- **Verification**: 100% dimensional compliance on all critical-to-quality (CTQ) drawing features.

### Step 4: Statistical Process Control (SPC) Setup
- **Inputs**: CMM measurement data, production line sensors.
- **Actions**: Establish control charts (X-bar, R-charts), define control limits, measure process capability index (Cpk).
- **Outputs**: SPC dashboard and process capability report.
- **Verification**: Cpk index >= 1.33 across all CTQ parameters.

### Step 5: Mass Production Sign-Off
- **Inputs**: Passed FAIR, SPC capability report, standard work instructions.
- **Actions**: Publish standard operating procedures (SOPs) on shop floor terminals; authorize full-scale production run.
- **Outputs**: Production Authorization Certificate and live MES routing.
- **Verification**: Quality Control Auditor formal sign-off.

## 5. Decision Gates & Branching Rules
- Gate 1: CAM simulation must confirm zero collision prior to loading G-code onto CNC machines.
- Gate 2: First Article Inspection Report (FAIR) must achieve 100% CTQ feature pass rate.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Tool wear causing dimensional drift in pilot run -> Action: Adjust CNC tool offset, update tool replacement cycle in MPP.
- Failure Mode 2: Process capability Cpk < 1.33 -> Action: Perform gage R&R study, recalibrate machine center tolerances.

## 7. Artifact Delivery & Output Standard
AS9102 FAIR documentation, verified CNC G-code programs, SPC process capability reports, and released shop floor SOPs.
