import os

TARGET_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_04_workflow_library"


def write_wf(filename, title, purpose, prereqs, trigger, roles, steps, gates, failures, artifact_standard):
    path = os.path.join(TARGET_DIR, filename)
    content = f"# {title} Specification\n\n"
    content += f"## 1. Purpose & Objective\n{purpose}\n\n"
    content += "## 2. Prerequisites & Trigger Conditions\n"
    content += f"- **Prerequisites**: {prereqs}\n"
    content += f"- **Trigger Conditions**: {trigger}\n\n"
    content += "## 3. Participating Agent Roles & Responsibilities\n"
    for rname, rdesc in roles:
        content += f"- **{rname}**: {rdesc}\n"
    content += "\n## 4. Step-by-Step Execution Sequence\n\n"
    for i, (sname, sinp, sact, sout, sver) in enumerate(steps, 1):
        content += f"### Step {i}: {sname}\n"
        content += f"- **Inputs**: {sinp}\n"
        content += f"- **Actions**: {sact}\n"
        content += f"- **Outputs**: {sout}\n"
        content += f"- **Verification**: {sver}\n\n"
    content += "## 5. Decision Gates & Branching Rules\n"
    for g in gates:
        content += f"- {g}\n"
    content += "\n## 6. Failure Modes & Fallback/Recovery Procedures\n"
    for f in failures:
        content += f"- {f}\n"
    content += f"\n## 7. Artifact Delivery & Output Standard\n{artifact_standard}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename}")


wf_list = [
    # 16
    (
        "financial_modeling_workflow.md",
        "Financial Modeling Workflow",
        "Construct 3-statement financial models, discounted cash flow (DCF) valuations, sensitivity analyses, and budget variance forecasts.",
        "Historical financial statements (Income Statement, Balance Sheet, Cash Flow), chart of accounts, growth assumptions.",
        "Quarterly financial planning or investment valuation trigger.",
        [
            (
                "Financial Analyst",
                "Builds financial model tabs, formula links, DCF calculations, and sensitivity tables.",
            ),
            (
                "Chief Financial Officer Agent",
                "Validates capital structure, discount rate assumptions, and strategic growth drivers.",
            ),
            (
                "Risk Auditor",
                "Audits formula integrity, scenario edge cases, and compliance with GAAP/IFRS principles.",
            ),
        ],
        [
            (
                "Historical Financial Ingestion & Cleanup",
                "3-year historical financial statements, trial balance data.",
                "Normalize account groupings, verify historical Balance Sheet balancing (Assets = Liabilities + Equity).",
                "Historical Financial Baseline Matrix.",
                "Balance Sheet equation holds 100% across all historical periods.",
            ),
            (
                "Revenue & Operational Expense Modeling",
                "Sales pipeline forecasts, headcount growth plans, OPEX assumptions.",
                "Build driver-based revenue projections (volume x price) and OPEX formulas linked to headcount assumptions.",
                "Revenue & OPEX Projection Module.",
                "Financial Analyst verification of driver logic.",
            ),
            (
                "3-Statement Integration & Cash Flow Modeling",
                "Revenue/OPEX modules, working capital assumptions, CAPEX schedules.",
                "Integrate Income Statement, Balance Sheet, and Statement of Cash Flows with dynamic debt/cash sweeps.",
                "Integrated 3-Statement Financial Model.",
                "Balance sheet balances dynamically across all 5 forecast years.",
            ),
            (
                "Valuation & Sensitivity Scenario Analysis",
                "3-statement model, Weighted Average Cost of Capital (WACC), terminal growth rates.",
                "Perform Discounted Cash Flow (DCF) valuation, build sensitivity matrices across WACC vs growth rates.",
                "DCF Valuation & Sensitivity Matrix Report.",
                "Risk Auditor verification of cell formula integrity.",
            ),
            (
                "Executive Summary & Board Reporting",
                "Completed model, valuation summary, sensitivity tables.",
                "Draft executive summary dashboard, visualize revenue bridges, compile board presentation pack.",
                "Executive Financial Model Binder & Deck.",
                "CFO Agent sign-off on valuation targets.",
            ),
        ],
        [
            "Gate 1: Balance Sheet must balance perfectly across all 5 forecast years before valuation calculation.",
            "Gate 2: WACC calculation requires formal CFO sign-off.",
        ],
        [
            "Failure Mode 1: Circular reference in debt interest calculation -> Action: Implement iterative calculation flag or lag interest expense by 1 period.",
            "Failure Mode 2: Unrealistic terminal growth rate assumption -> Action: Cap terminal growth at long-term GDP growth rate (2-3%).",
        ],
        "Integrated 3-Statement Model Spreadsheet, DCF Valuation Report, Sensitivity Matrix, and Executive Board Deck.",
    ),
    # 17
    (
        "marketing_campaign_workflow.md",
        "Marketing Campaign Workflow",
        "Structure multi-channel marketing campaigns from target audience profiling, content calendar design, ad channel setup, to ROI optimization.",
        "Product messaging framework, brand assets, ad budget allocation, campaign target KPIs.",
        "Quarterly marketing strategy launch or new product release campaign.",
        [
            ("Marketing Director", "Defines campaign goals, budget distribution, channel strategy, and ROI targets."),
            (
                "Campaign Specialist",
                "Designs ad creatives, copy decks, landing page funnels, and email nurture sequences.",
            ),
            (
                "Analytics Specialist",
                "Configures UTM tracking, conversion pixels, attribution models, and performance dashboards.",
            ),
        ],
        [
            (
                "Campaign Strategy & Channel Allocation",
                "Product value proposition, target buyer personas, budget envelope.",
                "Define campaign theme, select channel mix (Paid Search, Social, Content, Email), establish conversion benchmarks.",
                "Campaign Strategy Brief.",
                "Marketing Director approval of channel budget allocation.",
            ),
            (
                "Creative Asset & Copy Development",
                "Campaign brief, brand visual guidelines.",
                "Draft ad copy variations, design banner creatives, build landing page templates, write email sequence copy.",
                "Marketing Creative Package & Copy Deck.",
                "Pixel-perfect visual check and copy proofreading approval.",
            ),
            (
                "Tracking & Attribution Setup",
                "Landing page URLs, Google Analytics / HubSpot / Meta Pixel.",
                "Generate standardized UTM parameter tracking links, place conversion tracking pixels, configure attribution goals.",
                "UTM Tracking Matrix & Conversion Setup Log.",
                "Analytics Specialist verification of test pixel triggers.",
            ),
            (
                "Multi-Channel Campaign Launch",
                "Creative package, verified tracking, ad platform accounts.",
                "Upload ad campaigns to Google Ads, Meta Ads, LinkedIn Campaign Manager; launch email nurture workflow.",
                "Live Campaign Activation Record.",
                "Confirmation of live ad approvals across all platforms.",
            ),
            (
                "Performance Monitoring & ROI Optimization",
                "Live campaign analytics, conversion data, ad spending logs.",
                "Track Customer Acquisition Cost (CAC), Return on Ad Spend (ROAS), reallocate budget from low to high-performing ads.",
                "Campaign Performance & ROAS Optimization Report.",
                "ROAS target >= 3.0x achieved.",
            ),
        ],
        [
            "Gate 1: Tracking pixels must be verified via test conversion prior to ad budget release.",
            "Gate 2: Ad campaigns with ROAS < 1.0x after 72 hours automatically trigger budget pause.",
        ],
        [
            "Failure Mode 1: High ad click-through rate but low landing page conversion -> Action: Audit landing page load speed, optimize CTA visibility.",
            "Failure Mode 2: Disapproved ad creative on ad network -> Action: Revise copy to comply with platform policy guidelines, re-submit.",
        ],
        "Campaign Strategy Brief, Creative Asset Library, UTM Tracking Matrix, Live Campaign Report, and ROAS Optimization Audit.",
    ),
    # 18
    (
        "hiring_process_workflow.md",
        "Hiring Process Workflow",
        "Orchestrate job specification creation, candidate sourcing, initial screening, technical evaluation, interview coordination, and offer drafting.",
        "Approved headcount budget, role competency matrix, compensation band guidelines.",
        "Department headcount requisition approval.",
        [
            (
                "HR Specialist",
                "Manages ATS job postings, candidate screening calls, interview scheduling, and offer letters.",
            ),
            (
                "Technical Interviewer",
                "Conducts technical coding/architecture interviews and scores candidate competency.",
            ),
            (
                "Hiring Manager",
                "Defines role requirements, conducts culture fit interviews, and makes final hiring decisions.",
            ),
        ],
        [
            (
                "Role Specification & Job Posting",
                "Headcount requisition, department competency matrix, compensation band.",
                "Draft job description (JD), define mandatory vs preferred qualifications, post to ATS (Greenhouse/Lever) and job boards.",
                "Published Job Description & ATS Requisition.",
                "Hiring Manager sign-off on JD requirements.",
            ),
            (
                "Candidate Sourcing & Resume Screening",
                "ATS applicant pool, LinkedIn Recruiter database.",
                "Screen inbound applications against mandatory criteria, execute outbound sourcing, select candidate pool for phone screen.",
                "Screened Candidate Shortlist.",
                "HR Specialist confirmation of candidate qualifications.",
            ),
            (
                "Recruiter Phone Screen & Intake",
                "Candidate shortlist, screening question rubric.",
                "Conduct 30-minute phone screen evaluating candidate background, salary expectations, remote status, and availability.",
                "Candidate Intake Assessment Notes.",
                "Candidate alignment on compensation range and start date.",
            ),
            (
                "Technical Evaluation & Panel Interview",
                "Qualified candidate pool, technical interview scoring rubric.",
                "Conduct 60-minute technical assessment / architecture interview; score candidate across technical criteria.",
                "Technical Evaluation Scorecard.",
                "Technical Interviewer formal recommendation (Hire / No Hire).",
            ),
            (
                "Final Interview & Offer Execution",
                "Top candidate technical scorecard, executive approval.",
                "Conduct final Hiring Manager interview, run reference checks, draft formal offer letter, secure candidate signature.",
                "Executed Offer Letter & Onboarding Handoff Packet.",
                "Signed candidate offer letter.",
            ),
        ],
        [
            "Gate 1: Recruiter screen must verify salary expectation alignment before scheduling technical panel.",
            "Gate 2: Minimum 2 positive interview scorecards required prior to extending job offer.",
        ],
        [
            "Failure Mode 1: High candidate drop-out rate during interview process -> Action: Shorten interview stage turnaround times to < 48 hours.",
            "Failure Mode 2: Candidate rejects offer -> Action: Conduct exit feedback, re-engage runner-up candidate.",
        ],
        "Published Job Description, ATS Candidate Scorecards, Reference Check Notes, and Signed Offer Letter.",
    ),
    # 19
    (
        "incident_response_workflow.md",
        "Incident Response Workflow",
        "Triage PagerDuty alerts, classify severity (SEV1-SEV4), execute containment strategies, identify root cause, remediate, and author post-mortems.",
        "Monitoring alert system (PagerDuty/Datadog), incident management channel, runbook documentation.",
        "Automated P1 alert trigger or user-reported system outage.",
        [
            (
                "Incident Commander",
                "Coordinates incident triage, assigns task leads, manages communications, and enforces SEV protocol.",
            ),
            (
                "SRE Specialist",
                "Executes system diagnostics, traffic redirection, service isolation, and hotfix application.",
            ),
            (
                "Communications Lead",
                "Updates public status page, notifies executive stakeholders, and drafts incident updates.",
            ),
        ],
        [
            (
                "Alert Triage & SEV Classification",
                "PagerDuty alert payload, APM metrics, incident intake report.",
                "Acknowledge alert within SLA (5 min), assess customer impact, declare Severity Level (SEV1: Critical, SEV2: Major).",
                "Declared Incident Record & War Room Initialization.",
                "Incident Commander confirmation of SEV classification.",
            ),
            (
                "Containment & Traffic Redirection",
                "Incident War Room, system runbooks, load balancer controls.",
                "Execute immediate containment (e.g. isolate failing node pool, enable static fallback, block DDoS IPs).",
                "System Containment Log.",
                "Impact mitigation verified (error rates dropping).",
            ),
            (
                "Root Cause Analysis & Remediation",
                "System logs, metric graphs, git commit history.",
                "Analyze log traces, identify faulty commit or infrastructure failure, deploy emergency hotfix or revert commit.",
                "Hotfix Deployment & Resolution Log.",
                "100% resolution of error condition and system telemetry return to normal baseline.",
            ),
            (
                "Stakeholder & Status Page Communication",
                "Incident resolution status, Statuspage API.",
                "Publish regular incident updates to Statuspage every 15 mins during SEV1; publish resolution post once stable.",
                "Published Statuspage Resolution Notice.",
                "Statuspage updated to All Systems Operational.",
            ),
            (
                "Blameless Post-Mortem & Action Items",
                "Incident timeline, log traces, chat logs.",
                "Convene blameless post-mortem meeting within 48 hours, document root cause timeline, assign preventive action items.",
                "Blameless Post-Mortem Document.",
                "Incident Commander sign-off on post-mortem action items.",
            ),
        ],
        [
            "Gate 1: SEV1 incidents require war room assembly within 10 minutes of alert trigger.",
            "Gate 2: Blameless post-mortem document mandatory for all SEV1/SEV2 incidents within 48 hours.",
        ],
        [
            "Failure Mode 1: Hotfix fails to resolve containment -> Action: Immediately revert system to last known stable release version.",
            "Failure Mode 2: Secondary outage triggered during containment -> Action: Spin up isolated disaster recovery environment.",
        ],
        "Declared Incident Record, War Room Logs, Statuspage Update History, and Blameless Post-Mortem Document.",
    ),
    # 20
    (
        "disaster_recovery_workflow.md",
        "Disaster Recovery Workflow",
        "Evaluate Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO), execute backup failover, restore secondary regions, and audit data integrity.",
        "Primary environment status, secondary region infrastructure (AWS us-west-2), secondary database snapshots, DNS routing control.",
        "Primary region catastrophic failure notification or annual DR exercise initiation.",
        [
            (
                "DR Manager",
                "Declares disaster recovery event, directs failover sequence, and oversees RTO/RPO targets.",
            ),
            (
                "Infrastructure Specialist",
                "Spins up secondary region compute resources, updates DNS failover routing, and verifies network stability.",
            ),
            (
                "Database Specialist",
                "Executes database failover promotion, verifies data replication state, and runs data integrity checks.",
            ),
        ],
        [
            (
                "Disaster Declaration & Severity Assessment",
                "Primary region outage report, infrastructure health metrics.",
                "Confirm primary region total outage (e.g. cloud region blackout), declare DR event, notify DR execution team.",
                "DR Event Declaration Record.",
                "DR Manager sign-off on failover activation.",
            ),
            (
                "Secondary Region Compute Provisioning",
                "Terraform DR modules, secondary region API endpoints.",
                "Trigger automated Terraform deployment to spin up compute clusters, container instances, and microservices in secondary region.",
                "Secondary Region Provisioning Log.",
                "Terraform apply completes with 0 infrastructure errors.",
            ),
            (
                "Database Promotion & Data Replication Audit",
                "Secondary DB read replica, latest cross-region snapshot.",
                "Promote secondary DB read-replica to primary master status, verify transaction log sequence numbers.",
                "Database Promotion Execution Log.",
                "Database Specialist validation of zero data corruption and RPO within target limit.",
            ),
            (
                "DNS Cutover & Traffic Failover Routing",
                "Secondary cluster ingress URL, Cloudflare / Route53 DNS settings.",
                "Update global DNS routing to direct 100% user traffic to secondary cloud region.",
                "DNS Cutover Verification Report.",
                "HTTP 200 health check responses from secondary region endpoints.",
            ),
            (
                "Post-Failover Audit & Primary Region Restoration Plan",
                "Secondary region operational metrics, primary region recovery status.",
                "Monitor secondary region stability, calculate achieved RTO/RPO metrics, draft failback plan once primary region recovers.",
                "DR Execution Audit Report & Failback Strategy.",
                "Executive sign-off on DR exercise completion.",
            ),
        ],
        [
            "Gate 1: Failover promotion required within 15 minutes of primary region outage declaration.",
            "Gate 2: Database promotion verification must confirm zero data loss (RPO < 15 mins).",
        ],
        [
            "Failure Mode 1: Secondary DB replica out of sync -> Action: Restore database from latest verified cross-region snapshot.",
            "Failure Mode 2: DNS cache delay preventing traffic cutover -> Action: Lower DNS TTL settings, issue flush cache commands to major resolvers.",
        ],
        "DR Event Declaration Record, Terraform Secondary Deployment Logs, Database Promotion Verification, and DR Audit Report.",
    ),
]

# Write missing 5 items
for item in wf_list:
    write_wf(*item)

print("Missing 5 workflows (16-20) written successfully.")
