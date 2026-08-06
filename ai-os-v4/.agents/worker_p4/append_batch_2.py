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


# Batch 2: Workflows 11 to 20
wf_list = [
    # 11
    (
        "cloud_migration_workflow.md",
        "Cloud Migration Workflow",
        "Structure legacy application and infrastructure migration to cloud environments (AWS/GCP/Azure) with minimal downtime and data integrity assurance.",
        "Inventory of legacy workloads, target cloud architecture diagram, IAM policies, connectivity (VPN/DirectConnect).",
        "Initiation of cloud transformation project charter.",
        [
            ("Cloud Architect", "Designs target cloud architecture, landing zone, and migration strategy (6 Rs)."),
            (
                "Migration Engineer",
                "Executes data synchronization, server rehosting/replatforming, and containerization.",
            ),
            ("DevOps Specialist", "Configures IaC (Terraform), CI/CD pipelines, and cloud monitoring tools."),
        ],
        [
            (
                "Workload Assessment & Strategy Mapping",
                "Application inventory, dependency matrix, performance baselines.",
                "Categorize workloads into 6 Rs (Rehost, Replatform, Rearchitect, Retain, Retire, Repurchase), estimate cloud cost.",
                "Migration Assessment & Strategy Report.",
                "Cloud Architect sign-off on target landing zone design.",
            ),
            (
                "Target Environment Provisioning",
                "Terraform modules, cloud provider credentials, security compliance benchmarks.",
                "Provision VPCs, subnets, IAM roles, security groups, KMS keys, and Kubernetes clusters using Terraform.",
                "Provisioned Cloud Landing Zone infrastructure.",
                "Terraform plan/apply verification with 0 security compliance violations.",
            ),
            (
                "Data Migration & Synchronization",
                "Legacy databases, object storage, AWS DMS / GCP Database Migration Service.",
                "Configure continuous data replication streams, perform initial snapshot transfer, verify delta sync speeds.",
                "Data Migration Sync Status Log.",
                "Data integrity checksum validation comparing source DB and target cloud DB.",
            ),
            (
                "Application Cutover & Traffic Routing",
                "Replatformed application containers, Route53 / Cloudflare DNS settings.",
                "Drain legacy traffic, execute final DB delta sync, update DNS CNAME/A records to cloud load balancer.",
                "DNS Cutover Verification Report.",
                "HTTP 200 health check responses on new cloud endpoints.",
            ),
            (
                "Post-Migration Optimization & Decommissioning",
                "Live cloud application metrics, legacy server pool.",
                "Monitor CloudWatch/Datadog metrics, scale autoscaling groups, decommission legacy physical/virtual servers.",
                "Post-Migration Performance Audit & Legacy Decommission Sign-off.",
                "Cost and performance metrics meeting target SLAs.",
            ),
        ],
        [
            "Gate 1: Data checksum validation must achieve 100% parity before DNS cutover.",
            "Gate 2: Rollback plan must be documented and tested prior to cutover execution.",
        ],
        [
            "Failure Mode 1: High latency during database delta sync -> Action: Increase DirectConnect bandwidth allocation, re-run sync.",
            "Failure Mode 2: DNS cutover fails health check -> Action: Roll back DNS records immediately to legacy IP addresses.",
        ],
        "Terraform IaC codebase, Data Checksum Validation Log, DNS Cutover Report, and CloudWatch Performance Dashboard.",
    ),
    # 12
    (
        "devops_pipeline_workflow.md",
        "DevOps Pipeline Workflow",
        "Automate software delivery, infrastructure management, automated testing, continuous integration, and continuous deployment.",
        "Git repository, Kubernetes cluster access, CI system (GitHub Actions/GitLab CI), container registry.",
        "Code commit to main branch or git tag creation.",
        [
            ("DevOps Lead", "Establishes CI/CD architecture, deployment strategies, and telemetry standards."),
            ("Infrastructure Engineer", "Maintains Kubernetes manifests, Helm charts, and Terraform modules."),
            ("Security Analyst", "Integrates SAST, DAST, container scanning, and secrets detection into pipeline."),
        ],
        [
            (
                "Source Code Analysis & Linting",
                "Git commit payload, repository code.",
                "Trigger pipeline run, execute language linters, check commit signature validity, run secret scanners (TruffleHog).",
                "Lint report and secrets audit log.",
                "Zero hardcoded secrets detected and clean linter exit status.",
            ),
            (
                "Build & Container Image Compilation",
                "Dockerfile, dependency locks, build scripts.",
                "Build application binary, construct multi-stage OCI container image, tag with git commit SHA.",
                "Container Image in local docker cache.",
                "Successful Docker build without cached security layer warnings.",
            ),
            (
                "Security Scanning (SAST & Container)",
                "Container image artifact, source codebase, Trivy / SonarQube tools.",
                "Scan source code via SAST; scan container image layers for CVE vulnerabilities using Trivy.",
                "Trivy Vulnerability Scan & SAST Analysis Report.",
                "Zero CRITICAL or HIGH severity CVEs in scan output.",
            ),
            (
                "Staging Deployment & Automated Testing",
                "Container image SHA, staging Kubernetes cluster, Helm values.",
                "Deploy container to staging namespace via Helm/ArgoCD; trigger automated integration and regression tests.",
                "Staging Deployment Status & Test Execution Logs.",
                "100% pass rate on staging E2E integration test suite.",
            ),
            (
                "Production Deployment (Canary / Blue-Green)",
                "Approved staging release, Argo Rollouts / Flagger config.",
                "Initiate canary deployment (10% traffic increment every 5 minutes); monitor error rate and latency metrics.",
                "Argo Rollouts Promotion Log.",
                "Canary promotion success with 0 metric threshold breaches.",
            ),
        ],
        [
            "Gate 1: Vulnerability scan must yield zero Critical/High CVEs to proceed to staging.",
            "Gate 2: Canary automated rollback triggers if HTTP 5xx error rate exceeds 0.5% during rollout.",
        ],
        [
            "Failure Mode 1: Secret detected in source commit -> Action: Immediately fail pipeline, notify author, revoke leaked credential.",
            "Failure Mode 2: Canary deployment error rate spike -> Action: Argo Rollouts automatically aborts deployment and reverts 100% traffic to previous stable version.",
        ],
        "Helm chart package, signed container image in ECR/GCR, Trivy security report, and Argo Rollouts deployment log.",
    ),
    # 13
    (
        "product_launch_workflow.md",
        "Product Launch Workflow",
        "Align engineering, marketing, sales, customer support, and legal teams for external product feature releases.",
        "Feature completeness sign-off, marketing collateral, support documentation, press release draft.",
        "Target Go-Live date arrival or Executive launch authorization.",
        [
            (
                "Product Manager",
                "Coordinates launch timeline, feature scope confirmation, and launch readiness sign-offs.",
            ),
            (
                "Marketing Lead",
                "Manages campaign execution, press releases, landing page updates, and promotional emails.",
            ),
            (
                "Release Manager",
                "Executes feature flag toggles, release notes publication, and operational monitoring.",
            ),
        ],
        [
            (
                "Launch Readiness Audit",
                "Feature verification sign-off, load test report, support training status.",
                "Audit engineering stability, verify customer support team training, check legal/compliance approvals.",
                "Product Launch Readiness Matrix.",
                "Unanimous sign-off from PM, Engineering, Support, and Legal leads.",
            ),
            (
                "Marketing Asset & Communication Prep",
                "Product messaging framework, demo videos, press kit.",
                "Publish blog posts, configure email marketing campaigns, schedule social media announcements, update homepage.",
                "Staged Marketing Campaigns & Published Blog Drafts.",
                "Marketing Lead sign-off on campaign timing alignment.",
            ),
            (
                "Feature Flag Toggle & Production Enablement",
                "Production Launch Checklist, LaunchDarkly / Unleash feature flag system.",
                "Toggle feature flag to 100% user rollout; verify backend service telemetry.",
                "Feature Flag Activation Log.",
                "Production monitoring showing stable request traffic and normal error rates.",
            ),
            (
                "Press & Public Announcement Execution",
                "Press release deck, social media channels.",
                "Distribute press release, publish social media threads, send product update email blast to existing users.",
                "Public Announcement Tracking Dashboard.",
                "Successful distribution across wire services and social channels.",
            ),
            (
                "Post-Launch Triage & Feedback Synthesis",
                "Support ticket queue, social media feedback, user analytics.",
                "Monitor support escalation tickets, track user adoption metrics, conduct daily post-launch triage standups.",
                "Post-Launch Report (30-day summary).",
                "Support ticket escalation rate remaining within baseline limits.",
            ),
        ],
        [
            "Gate 1: Launch Readiness Matrix requires 100% sign-off before feature flag toggle.",
            "Gate 2: Post-launch triage standup triggers hotfix rollback if critical support bugs exceed 5 tickets in 1 hour.",
        ],
        [
            "Failure Mode 1: High system load upon feature toggle -> Action: Throttle feature flag percentage (e.g. down to 25%), scale backend pods.",
            "Failure Mode 2: Marketing link broken in email blast -> Action: Update redirect link on web server within 5 minutes.",
        ],
        "Product Launch Readiness Matrix, Feature Flag Activation Logs, Press Distribution Reports, and 30-day Post-Launch Summary.",
    ),
    # 14
    (
        "business_planning_workflow.md",
        "Business Planning Workflow",
        "Synthesize strategic market analysis, financial projections, operational resource requirements, and risk matrices into actionable business plans.",
        "Executive charter, market research reports, historical financial statements, strategic objectives.",
        "Annual strategy cycle or new business unit proposal.",
        [
            ("Strategy Consultant", "Conducts TAM/SAM/SOM analysis, competitive benchmarking, and strategic framing."),
            (
                "Business Analyst",
                "Maps operational capabilities, resource allocation requirements, and organizational structure.",
            ),
            (
                "Financial Analyst",
                "Builds 5-year financial projections, P&L models, cash flow forecasts, and sensitivity analyses.",
            ),
        ],
        [
            (
                "Market & Competitive Analysis",
                "Industry research reports, competitor filings, customer survey data.",
                "Analyze Total Addressable Market (TAM), Serviceable Addressable Market (SAM), build Porter's Five Forces matrix.",
                "Market Analysis & Competitive Positioning Document.",
                "Strategy Consultant validation of market sizing methodology.",
            ),
            (
                "Operational Strategy & Resource Mapping",
                "Business goals, department headcount estimates, tech stack needs.",
                "Define organizational hiring plan, operational workflows, milestone roadmaps, and key performance indicators (KPIs).",
                "Operational Plan & Organizational Roadmap.",
                "Business Analyst confirmation of resource feasibility.",
            ),
            (
                "Financial Modeling & Revenue Forecasting",
                "Pricing strategy, CAC/LTV estimates, operational cost projections.",
                "Build 5-year financial model including Income Statement, Balance Sheet, Cash Flow, and sensitivity scenario analysis.",
                "5-Year Financial Model (Excel / Financial System).",
                "Financial Analyst sign-off on unit economics and cash runway.",
            ),
            (
                "Risk Assessment & Mitigation Matrix",
                "Market analysis, financial model, operational dependencies.",
                "Identify regulatory, financial, operational, and competitive risks; define mitigation strategies and trigger conditions.",
                "Risk Register & Response Plan.",
                "Executive Sponsor sign-off on risk mitigation framework.",
            ),
            (
                "Executive Business Plan Compilation",
                "All section deliverables (Market, Operations, Financials, Risks).",
                "Synthesize findings into an Executive Business Plan document and Board Presentation deck.",
                "Master Business Plan Document & Pitch Deck.",
                "Formal Board / Executive Committee approval.",
            ),
        ],
        [
            "Gate 1: Financial model unit economics (LTV/CAC >= 3.0) must be validated prior to plan compilation.",
            "Gate 2: Executive Board approval required for resource allocation and budget release.",
        ],
        [
            "Failure Mode 1: Financial projections show cash negative within 12 months -> Action: Revise pricing structure, reduce OPEX headcount growth.",
            "Failure Mode 2: Competitive threat invalidates core differentiator -> Action: Pivot value proposition, update TAM analysis.",
        ],
        "Master Business Plan PDF, 5-Year Financial Model spreadsheet, Risk Register, and Board Presentation Deck.",
    ),
    # 15
    (
        "legal_review_workflow.md",
        "Legal Review Workflow",
        "Ensure regulatory compliance, liability mitigation, intellectual property protection, and contractual integrity across corporate operations.",
        "Draft legal document (contract, terms of service, IP agreement), regulatory baseline guidelines.",
        "Submission of contract or compliance policy for legal review.",
        [
            (
                "Legal Counsel",
                "Audits contract language, drafts indemnity clauses, negotiates terms, and assesses legal exposure.",
            ),
            ("Compliance Analyst", "Verifies compliance with statutory frameworks (GDPR, CCPA, HIPAA, SOC2)."),
            ("Risk Officer", "Evaluates liability caps, insurance coverage mandates, and operational risk exposure."),
        ],
        [
            (
                "Document Ingestion & Clause Analysis",
                "Submitted draft agreement/contract, organizational legal playbook.",
                "Extract standard clauses (indemnity, liability, IP rights, governing law), compare against corporate legal playbook.",
                "Redlined Contract Draft & Clause Comparison Matrix.",
                "Legal Counsel confirmation of redline accuracy.",
            ),
            (
                "Regulatory & Compliance Verification",
                "Contract payload, applicable regulatory frameworks.",
                "Check data privacy provisions (DPA), cross-border data transfer rules, data retention clauses.",
                "Compliance Assessment Report.",
                "Compliance Analyst approval of data privacy annexes.",
            ),
            (
                "Risk Evaluation & Exposure Modeling",
                "Redlined contract, risk appetite threshold policy.",
                "Evaluate financial liability caps, consequential damage waivers, indemnification scope, insurance obligations.",
                "Risk Exposure Memorandum.",
                "Risk Officer approval of liability parameters.",
            ),
            (
                "Contract Negotiation & Revision",
                "Redlined document, counterparty comments.",
                "Negotiate contested terms with counterparty legal counsel, revise redline text, finalize agreement terms.",
                "Final Negotiated Agreement Draft.",
                "Mutual agreement on all contractual terms.",
            ),
            (
                "Execution & Document Archival",
                "Final approved agreement, authorized signatory list.",
                "Route document for executive electronic signature (DocuSign), index contract in Contract Lifecycle Management (CLM).",
                "Executed Contract PDF & CLM Metadata Record.",
                "DocuSign signature audit trail completion.",
            ),
        ],
        [
            "Gate 1: Liability cap must not exceed 2x annual contract value without CFO written approval.",
            "Gate 2: Data Processing Addendum (DPA) required for any vendor processing PII.",
        ],
        [
            "Failure Mode 1: Counterparty rejects standard indemnity clause -> Action: Escalate to General Counsel for custom fallback clause authorization.",
            "Failure Mode 2: Unacceptable governing law jurisdiction requested -> Action: Require arbitration clause under neutral jurisdiction.",
        ],
        "Redlined and Final Negotiated Contract PDF, Compliance Assessment Report, Risk Memorandum, and CLM Repository Record.",
    ),
]

# Write batch 2
for item in wf_list:
    write_wf(*item)

print("Batch 2 (11-20) written successfully.")
