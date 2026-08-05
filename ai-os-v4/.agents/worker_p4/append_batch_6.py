import os

TARGET_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_04_workflow_library"

def write_wf(filename, title, purpose, prereqs, trigger, roles, steps, gates, failures, artifact_standard):
    path = os.path.join(TARGET_DIR, filename)
    content = f"# {title} Specification\n\n"
    content += f"## 1. Purpose & Objective\n{purpose}\n\n"
    content += f"## 2. Prerequisites & Trigger Conditions\n"
    content += f"- **Prerequisites**: {prereqs}\n"
    content += f"- **Trigger Conditions**: {trigger}\n\n"
    content += f"## 3. Participating Agent Roles & Responsibilities\n"
    for rname, rdesc in roles:
        content += f"- **{rname}**: {rdesc}\n"
    content += f"\n## 4. Step-by-Step Execution Sequence\n\n"
    for i, (sname, sinp, sact, sout, sver) in enumerate(steps, 1):
        content += f"### Step {i}: {sname}\n"
        content += f"- **Inputs**: {sinp}\n"
        content += f"- **Actions**: {sact}\n"
        content += f"- **Outputs**: {sout}\n"
        content += f"- **Verification**: {sver}\n\n"
    content += f"## 5. Decision Gates & Branching Rules\n"
    for g in gates:
        content += f"- {g}\n"
    content += f"\n## 6. Failure Modes & Fallback/Recovery Procedures\n"
    for f in failures:
        content += f"- {f}\n"
    content += f"\n## 7. Artifact Delivery & Output Standard\n{artifact_standard}\n"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename}")

wf_list = [
    # 36
    ("model_evaluation_workflow.md", "Model Evaluation Workflow",
     "Assess AI model performance across metrics (Precision, Recall, F1, Latency), perform bias/fairness audits, evaluate out-of-distribution robustness, and create Model Cards.",
     "Trained model artifact, held-out test dataset, evaluation metric definitions, model evaluation framework.",
     "Completion of model training workflow or pre-deployment validation request.",
     [("Model Evaluator", "Executes evaluation test suites, computes statistical metrics, and benchmarks latency."),
      ("Data Ethics Auditor", "Evaluates fairness, demographic parity, and bias metrics across protected sub-groups."),
      ("ML Engineer", "Verifies runtime inference latency, memory footprint, and deployment readiness.")],
     [("Evaluation Dataset Preparation", "Held-out test set, out-of-distribution (OOD) test set, demographic metadata.", "Verify test set integrity, split test cases by domain slice and demographic attributes, format inputs.", "Curated Test Evaluation Dataset.", "Verification that evaluation set has zero overlap with training dataset."),
      ("Metric Calculation & Performance Profiling", "Trained model, test dataset, scikit-learn / Fairlearn evaluation scripts.", "Compute Accuracy, Precision, Recall, F1-score, ROC-AUC, Confusion Matrix, and latency percentiles.", "Model Performance Metrics Matrix.", "Precision and Recall metrics meeting minimum domain target thresholds."),
      ("Demographic Fairness & Bias Audit", "Model predictions, demographic attributes, Fairlearn framework.", "Calculate Demographic Parity Difference and Equalized Odds Ratio across protected demographic groups.", "Bias & Fairness Audit Report.", "Demographic parity difference <= 0.05 across evaluated sub-groups."),
      ("Robustness & Adversarial Testing", "Trained model, perturbed / noisy test inputs, adversarial attack payloads.", "Apply Gaussian noise, text typos, and adversarial perturbations to test inputs; measure performance drop.", "Model Robustness Benchmark Report.", "Accuracy drop under standard noise perturbation < 5%."),
      ("Model Card Generation & Sign-Off", "All evaluation metrics, bias audit, model architecture metadata.", "Draft comprehensive Model Card detailing model details, intended use, limitations, metrics, and ethical considerations.", "Published Model Card Specification (Markdown/PDF).", "Model Evaluator and Data Ethics Auditor formal sign-off.")],
     ["Gate 1: Model Card requires formal sign-off from Data Ethics Auditor prior to model deployment.",
      "Gate 2: Out-of-distribution performance drop must remain below 10% target limit."],
     ["Failure Mode 1: Demographic bias detected in sub-group evaluation -> Action: Reject model deployment, route back to ML team for re-balancing / re-weighting.",
      "Failure Mode 2: Inference latency exceeds deployment SLA -> Action: Apply quantization / pruning to model weights, re-evaluate."],
     "Published Model Card Document, Performance Metrics Matrix, Bias Audit Report, and Adversarial Benchmark Logs."),

    # 37
    ("compliance_audit_workflow.md", "Compliance Audit Workflow",
     "Conduct enterprise compliance assessments against SOC2, ISO 27001, GDPR, and HIPAA frameworks, collecting evidence and gap analysis reports.",
     "Regulatory framework baselines, policy documentation, system audit logs, IAM configurations.",
     "Annual compliance cycle or external audit request.",
     [("Compliance Officer", "Oversees compliance framework mapping, policy enforcement, and auditor liaison."),
      ("Security Auditor", "Collects technical evidence, reviews security configurations, and audits access controls."),
      ("Systems Specialist", "Provides system configurations, log exports, and infrastructure evidence artifacts.")],
     [("Framework Scope Definition & Policy Audit", "Target regulatory framework (SOC2 Type II / ISO 27001), corporate policies.", "Map framework control criteria to internal operational policies; verify annual policy review status.", "Compliance Control Matrix & Scope Document.", "Compliance Officer approval of control matrix."),
      ("Automated Evidence Collection", "Cloud infrastructure account, Vanta / Drata compliance automation tool.", "Collect automated evidence (IAM policies, MFA enforcement, disk encryption, backup logs, access reviews).", "Compliance Evidence Repository & Automated Log Collection.", "100% automated evidence check execution across cloud accounts."),
      ("Manual Sampling & Access Review Audit", "User access lists, ticket logs, HR termination records.", "Sample employee onboarding/offboarding tickets, verify timely access revocation, review privileged access logs.", "Access Control & Sampling Audit Log.", "Zero unrevoked terminated employee accounts found in active directory."),
      ("Gap Analysis & Remediation Plan", "Evidence repository, control matrix.", "Identify non-compliant controls, score risk levels, draft corrective action requests (CARs) for control owners.", "Compliance Gap Analysis Report & Remediation Roadmap.", "Control owner sign-off on remediation timelines."),
      ("Audit Package Compilation & Filing", "All evidence artifacts, gap analysis report, policy documents.", "Compile master compliance binder; submit package to external AICPA / ISO auditor for formal audit examination.", "Final Audit Package & Compliance Certificate Request.", "External auditor formal receipt and acceptance of audit binder.")],
     ["Gate 1: Zero unrevoked access instances for terminated employees allowed in audit sampling.",
      "Gate 2: Remediation of high-risk compliance gaps required before final external audit submission."],
     ["Failure Mode 1: Missing backup restoration evidence -> Action: Execute manual backup restoration test immediately, log evidence artifact.",
      "Failure Mode 2: Unencrypted database volume detected -> Action: Issue emergency ticket to encrypt volume, update infrastructure Terraform policy."],
     "Compliance Control Matrix, Automated Evidence Archives, Gap Analysis Report, and Final External Audit Package."),

    # 38
    ("contract_review_workflow.md", "Contract Review Workflow",
     "Automate clause extraction, risk flag identification, standard term comparison, redline generation, and executive summary drafting.",
     "Draft vendor or customer contract, corporate legal playbook, clause risk rules.",
     "Ingestion of new third-party contract for legal evaluation.",
     [("Legal Counsel", "Reviews flagged clauses, negotiates fallback terms, and approves final contract wording."),
      ("Risk Analyst", "Scores financial, operational, and indemnification risks against corporate risk matrix."),
      ("Procurement Lead", "Ensures commercial terms, SLAs, and pricing structures align with business requirements.")],
     [("Contract Text Ingestion & Parsing", "Raw contract file (PDF/Word), OCR / document parser.", "Convert contract into machine-readable text, extract structured sections, identify party names and key dates.", "Parsed Contract JSON Structure.", "Verification that 100% of contract text was extracted without truncation."),
      ("Clause Extraction & Playbook Alignment", "Parsed contract text, Legal Playbook rules.", "Identify standard clauses (Term, Termination, Indemnity, Liability Cap, IP, Governing Law), compare against baseline.", "Clause Extraction & Comparison Table.", "Zero missing critical legal clauses."),
      ("Risk Flagging & Deviation Scoring", "Clause comparison table, risk scoring rules.", "Flag non-standard terms (e.g. unlimited liability, unfavorable jurisdiction), assign risk rating (Low/Medium/High).", "Contract Risk Analysis Report & Flagged Deviations.", "Risk Analyst validation of flagged risk items."),
      ("Automated Redline & Fallback Generation", "Flagged deviations, Legal Playbook fallback clause library.", "Generate proposed redline text using pre-approved playbook fallback clauses for high-risk sections.", "Redlined Contract Document (.docx).", "Legal Counsel sign-off on proposed redline changes."),
      ("Executive Summary & Procurement Routing", "Redlined contract, risk analysis report.", "Draft 1-page Contract Executive Summary detailing key commercial terms, remaining risks, and recommendation.", "Contract Executive Summary & Approval Routing Ticket.", "Approval sign-off from Legal Counsel and Procurement Lead.")],
     ["Gate 1: Contracts with unlimited liability clauses automatically blocked until CFO approval is granted.",
      "Gate 2: Redline must utilize pre-approved Legal Playbook fallback clauses for indemnity terms."],
     ["Failure Mode 1: Contract contains non-standard jurisdiction clause -> Action: Insert standard arbitration fallback clause, flag for Legal Counsel manual review.",
      "Failure Mode 2: Unclear payment terms -> Action: Route back to Procurement Lead for commercial clarification."],
     "Redlined Contract Word Document, Contract Risk Analysis Report, Executive Summary PDF, and Approval Routing Log."),

    # 39
    ("lead_generation_workflow.md", "Lead Generation Workflow",
     "Define Ideal Customer Profiles (ICP), execute web prospecting, score lead quality, enrich contact metadata, and trigger targeted outreach.",
     "ICP criteria spec, prospecting data tools (Apollo/ZoomInfo), lead scoring model, CRM system (HubSpot/Salesforce).",
     "Marketing campaign kickoff or sales team pipeline growth goal.",
     [("Growth Marketer", "Defines ICP criteria, designs outreach sequences, and tracks conversion metrics."),
      ("Data Prospector", "Executes web scraping, database queries, and contact email validation."),
      ("CRM Specialist", "Manages CRM data hygiene, lead assignment routing, and automation workflows.")],
     [("Ideal Customer Profile (ICP) & Target Spec", "Market strategy, target industry verticals, company size limits, buyer personas.", "Define ICP filters (e.g. B2B SaaS, 50-200 employees, VP Engineering role), set target lead volume goals.", "ICP Definition Specification.", "Growth Marketer approval of target criteria."),
      ("Prospect Data Mining & Extraction", "ICP spec, prospecting tools (Apollo/LinkedIn Sales Navigator API).", "Query prospecting databases, extract targeted company records and prospect contact profiles.", "Raw Lead Records List.", "Prospecting dataset meets volume targets with 0 empty records."),
      ("Contact Data Enrichment & Verification", "Raw lead list, email verification API (ZeroBounce/NeverBounce).", "Verify email deliverability, enrich profile data (LinkedIn URL, technology stack, company revenue range).", "Enriched & Verified Lead Dataset.", "Email bounce rate risk forecast < 3% based on verification status."),
      ("Lead Scoring & Segmentation", "Enriched lead dataset, Lead Scoring rules matrix.", "Apply scoring algorithm based on company fit, title seniority, and tech stack match; segment into Tier 1/2/3.", "Scored Lead Database Records.", "Proper distribution of leads across Tier 1, 2, and 3 segments."),
      ("CRM Ingestion & Outreach Automation Trigger", "Scored lead records, CRM API, sales outreach platform (Outreach/Salesloft).", "Upsert leads into CRM, assign to appropriate SDR account owner, enroll Tier 1 leads into automated email sequence.", "CRM Import Log & Active Campaign Status.", "100% of verified leads successfully loaded into CRM with campaign tags.")],
     ["Gate 1: Email verification must confirm valid deliverability status before triggering automated outreach.",
      "Gate 2: Lead score must meet minimum threshold for automated sales rep assignment."],
     ["Failure Mode 1: High bounce rate alert (> 5%) during initial email blast -> Action: Immediately pause outreach sequence, re-verify email list via secondary verification tool.",
      "Failure Mode 2: CRM duplicate record creation -> Action: Trigger CRM deduplication workflow based on domain and email keys."],
     "ICP Specification Document, Enriched & Verified Lead CSV, Lead Scoring Matrix Report, and CRM Import Execution Logs."),

    # 40
    ("employee_onboarding_workflow.md", "Employee Onboarding Workflow",
     "Provision IT access credentials, coordinate hardware delivery, assign orientation documentation, schedule training, and verify 30-day check-ins.",
     "Signed employment offer letter, IT asset inventory, identity provider (Okta/Google Workspace), HRIS system (BambooHR/Workday).",
     "HR notification of new hire start date.",
     [("HR Operations", "Oversees onboarding checklist, orientation scheduling, and HRIS profile creation."),
      ("IT Admin", "Provisions email accounts, IAM group access, hardware configuration, and MDM enrollment."),
      ("People Manager", "Assigns 30-day goals, schedules introductory team meetings, and pairs candidate with onboarding buddy.")],
     [("HRIS Profile Creation & Trigger Dispatch", "Signed offer letter, candidate personal details.", "Create employee profile in HRIS, generate employee ID, trigger automated onboarding task checklist.", "Created HRIS Employee Profile & Task Checklist.", "HR Operations confirmation of profile completeness."),
      ("IT Identity & Access Provisioning", "HRIS profile notification, role-based access matrix.", "Create corporate email account, provision Okta single-sign-on (SSO), assign role-based Slack channels and GitHub access.", "Provisioned IT Credentials & Okta Profile.", "Okta group assignment check matching job role requirements."),
      ("Hardware Provisioning & Shipping", "Employee location, hardware specification request, MDM enrollment system (Jamf/Intune).", "Configure laptop with standard security software/MDM, pack peripheral kit, ship via trackable carrier.", "Hardware Shipment Tracking Number & MDM Profile.", "Delivery tracking confirmation showing hardware arrival before Day 1."),
      ("Day 1 Orientation & Buddy Pair Setup", "New hire, onboarding guide materials, assigned onboarding buddy.", "Conduct Day 1 welcome call, verify system login success, guide through compliance training modules.", "Day 1 Orientation Checklist Log.", "New hire successful login to company email and Slack."),
      ("30-Day Check-in & Feedback Survey", "30-day performance goals, onboarding survey form.", "Conduct 30-day review meeting between manager and new hire, collect onboarding feedback survey score.", "30-Day Onboarding Review & Survey Report.", "Completion of 30-day check-in and signed goal roadmap.")],
     ["Gate 1: IT credentials and hardware must be delivered at least 24 hours prior to employee start date.",
      "Gate 2: Mandatory compliance training modules must be completed within first 7 days."],
     ["Failure Mode 1: Laptop delivery delayed by carrier -> Action: Issue temporary virtual desktop (VDI) login credentials for Day 1 orientation.",
      "Failure Mode 2: Incomplete access permissions on Day 1 -> Action: Route urgent ticket to IT Admin on-call queue."],
     "HRIS Employee Record, Okta Provisioning Log, Hardware Delivery Receipts, and 30-Day Onboarding Evaluation Report.")
]

# Write batch 6
for item in wf_list:
    write_wf(*item)

print("Batch 6 (36-40) written successfully.")
