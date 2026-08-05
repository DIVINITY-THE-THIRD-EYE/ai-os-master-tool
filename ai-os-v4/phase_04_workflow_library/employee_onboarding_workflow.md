# Employee Onboarding Workflow Specification

## 1. Purpose & Objective
Provision IT access credentials, coordinate hardware delivery, assign orientation documentation, schedule training, and verify 30-day check-ins.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Signed employment offer letter, IT asset inventory, identity provider (Okta/Google Workspace), HRIS system (BambooHR/Workday).
- **Trigger Conditions**: HR notification of new hire start date.

## 3. Participating Agent Roles & Responsibilities
- **HR Operations**: Oversees onboarding checklist, orientation scheduling, and HRIS profile creation.
- **IT Admin**: Provisions email accounts, IAM group access, hardware configuration, and MDM enrollment.
- **People Manager**: Assigns 30-day goals, schedules introductory team meetings, and pairs candidate with onboarding buddy.

## 4. Step-by-Step Execution Sequence

### Step 1: HRIS Profile Creation & Trigger Dispatch
- **Inputs**: Signed offer letter, candidate personal details.
- **Actions**: Create employee profile in HRIS, generate employee ID, trigger automated onboarding task checklist.
- **Outputs**: Created HRIS Employee Profile & Task Checklist.
- **Verification**: HR Operations confirmation of profile completeness.

### Step 2: IT Identity & Access Provisioning
- **Inputs**: HRIS profile notification, role-based access matrix.
- **Actions**: Create corporate email account, provision Okta single-sign-on (SSO), assign role-based Slack channels and GitHub access.
- **Outputs**: Provisioned IT Credentials & Okta Profile.
- **Verification**: Okta group assignment check matching job role requirements.

### Step 3: Hardware Provisioning & Shipping
- **Inputs**: Employee location, hardware specification request, MDM enrollment system (Jamf/Intune).
- **Actions**: Configure laptop with standard security software/MDM, pack peripheral kit, ship via trackable carrier.
- **Outputs**: Hardware Shipment Tracking Number & MDM Profile.
- **Verification**: Delivery tracking confirmation showing hardware arrival before Day 1.

### Step 4: Day 1 Orientation & Buddy Pair Setup
- **Inputs**: New hire, onboarding guide materials, assigned onboarding buddy.
- **Actions**: Conduct Day 1 welcome call, verify system login success, guide through compliance training modules.
- **Outputs**: Day 1 Orientation Checklist Log.
- **Verification**: New hire successful login to company email and Slack.

### Step 5: 30-Day Check-in & Feedback Survey
- **Inputs**: 30-day performance goals, onboarding survey form.
- **Actions**: Conduct 30-day review meeting between manager and new hire, collect onboarding feedback survey score.
- **Outputs**: 30-Day Onboarding Review & Survey Report.
- **Verification**: Completion of 30-day check-in and signed goal roadmap.

## 5. Decision Gates & Branching Rules
- Gate 1: IT credentials and hardware must be delivered at least 24 hours prior to employee start date.
- Gate 2: Mandatory compliance training modules must be completed within first 7 days.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Laptop delivery delayed by carrier -> Action: Issue temporary virtual desktop (VDI) login credentials for Day 1 orientation.
- Failure Mode 2: Incomplete access permissions on Day 1 -> Action: Route urgent ticket to IT Admin on-call queue.

## 7. Artifact Delivery & Output Standard
HRIS Employee Record, Okta Provisioning Log, Hardware Delivery Receipts, and 30-Day Onboarding Evaluation Report.
