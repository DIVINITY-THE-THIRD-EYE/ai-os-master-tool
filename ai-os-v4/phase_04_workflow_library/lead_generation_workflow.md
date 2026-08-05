# Lead Generation Workflow Specification

## 1. Purpose & Objective
Define Ideal Customer Profiles (ICP), execute web prospecting, score lead quality, enrich contact metadata, and trigger targeted outreach.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: ICP criteria spec, prospecting data tools (Apollo/ZoomInfo), lead scoring model, CRM system (HubSpot/Salesforce).
- **Trigger Conditions**: Marketing campaign kickoff or sales team pipeline growth goal.

## 3. Participating Agent Roles & Responsibilities
- **Growth Marketer**: Defines ICP criteria, designs outreach sequences, and tracks conversion metrics.
- **Data Prospector**: Executes web scraping, database queries, and contact email validation.
- **CRM Specialist**: Manages CRM data hygiene, lead assignment routing, and automation workflows.

## 4. Step-by-Step Execution Sequence

### Step 1: Ideal Customer Profile (ICP) & Target Spec
- **Inputs**: Market strategy, target industry verticals, company size limits, buyer personas.
- **Actions**: Define ICP filters (e.g. B2B SaaS, 50-200 employees, VP Engineering role), set target lead volume goals.
- **Outputs**: ICP Definition Specification.
- **Verification**: Growth Marketer approval of target criteria.

### Step 2: Prospect Data Mining & Extraction
- **Inputs**: ICP spec, prospecting tools (Apollo/LinkedIn Sales Navigator API).
- **Actions**: Query prospecting databases, extract targeted company records and prospect contact profiles.
- **Outputs**: Raw Lead Records List.
- **Verification**: Prospecting dataset meets volume targets with 0 empty records.

### Step 3: Contact Data Enrichment & Verification
- **Inputs**: Raw lead list, email verification API (ZeroBounce/NeverBounce).
- **Actions**: Verify email deliverability, enrich profile data (LinkedIn URL, technology stack, company revenue range).
- **Outputs**: Enriched & Verified Lead Dataset.
- **Verification**: Email bounce rate risk forecast < 3% based on verification status.

### Step 4: Lead Scoring & Segmentation
- **Inputs**: Enriched lead dataset, Lead Scoring rules matrix.
- **Actions**: Apply scoring algorithm based on company fit, title seniority, and tech stack match; segment into Tier 1/2/3.
- **Outputs**: Scored Lead Database Records.
- **Verification**: Proper distribution of leads across Tier 1, 2, and 3 segments.

### Step 5: CRM Ingestion & Outreach Automation Trigger
- **Inputs**: Scored lead records, CRM API, sales outreach platform (Outreach/Salesloft).
- **Actions**: Upsert leads into CRM, assign to appropriate SDR account owner, enroll Tier 1 leads into automated email sequence.
- **Outputs**: CRM Import Log & Active Campaign Status.
- **Verification**: 100% of verified leads successfully loaded into CRM with campaign tags.

## 5. Decision Gates & Branching Rules
- Gate 1: Email verification must confirm valid deliverability status before triggering automated outreach.
- Gate 2: Lead score must meet minimum threshold for automated sales rep assignment.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: High bounce rate alert (> 5%) during initial email blast -> Action: Immediately pause outreach sequence, re-verify email list via secondary verification tool.
- Failure Mode 2: CRM duplicate record creation -> Action: Trigger CRM deduplication workflow based on domain and email keys.

## 7. Artifact Delivery & Output Standard
ICP Specification Document, Enriched & Verified Lead CSV, Lead Scoring Matrix Report, and CRM Import Execution Logs.
