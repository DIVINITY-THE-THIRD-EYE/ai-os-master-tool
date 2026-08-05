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
    # 25
    ("deployment_pipeline_workflow.md", "Deployment Pipeline Workflow",
     "Govern the automated deployment of verified application build artifacts into staging and production environments.",
     "Signed container image / build package, deployment manifests (Kubernetes/Terraform), environment secret key.",
     "Approved release trigger from Git release tag or manual approval button.",
     [("Release Engineer", "Oversees deployment pipelines, strategy selection (blue-green/canary), and rollout progress."),
      ("Cloud Specialist", "Monitors cluster resource allocation, load balancer state, and ingress routing."),
      ("QA Specialist", "Executes post-deployment smoke tests and automated health verification.")],
     [("Pre-Deployment Readiness Check", "Environment credentials, target cluster status, secrets store.", "Verify cluster capacity, validate secret store accessibility, confirm no lockouts on deployment targets.", "Pre-Flight Status Check Log.", "Cluster node capacity > 20% headroom and secret store online."),
      ("Artifact Retrieval & Manifest Rendering", "Signed release tag, Helm chart templates, environment variables.", "Pull signed container image, render Kubernetes manifests with production environment parameters.", "Rendered Kubernetes Manifests (YAML).", "Kubeval / datatree manifest schema validation passes with 0 errors."),
      ("Rolling Out / Blue-Green Switch", "Rendered manifests, Kubernetes API endpoint.", "Apply manifests to target namespace; execute rolling update or update blue/green ingress service selector.", "Kubernetes Rollout Status Output.", "Kubernetes deployment `kubectl rollout status` completes successfully."),
      ("Post-Deployment Synthetic Smoke Testing", "Live environment endpoints, synthetic test scripts.", "Run HTTP synthetic check suite targeting critical endpoints; verify database write capabilities.", "Post-Deployment Smoke Test Report.", "100% synthetic test pass rate and 0 HTTP 5xx responses."),
      ("Deployment Sign-Off & Notification", "Smoke test results, deployment metrics.", "Broadcast deployment completion message to Slack/Teams; update release tracker state to Released.", "Deployment Notification Record.", "Release Engineer formal sign-off.")],
     ["Gate 1: Pre-flight cluster resource headroom check must pass prior to deploying new pods.",
      "Gate 2: Smoke tests must pass 100% within 5 minutes of pod readiness, or rollback is triggered."],
     ["Failure Mode 1: Pod CrashLoopBackOff during rollout -> Action: Automated rollback triggered via `helm rollback` or `kubectl rollout undo`.",
      "Failure Mode 2: Ingress controller routing failure -> Action: Revert blue/green service selector to previous deployment revision."],
     "Rendered Deployment Manifests, Kubernetes Rollout Logs, Post-Deployment Smoke Test Summary, and Release Tracker Notification."),

    # 26
    ("release_pipeline_workflow.md", "Release Pipeline Workflow",
     "Coordinate release notes generation, semantic versioning, artifact signing, binary publishing, and public changelog distribution.",
     "Merged PRs in main branch, git commit history, issue tracker metadata.",
     "Scheduled release window or release candidate trigger.",
     [("Release Manager", "Defines version numbers (SemVer), authorizes release packages, and publishes release notes."),
      ("DevOps Specialist", "Automates release tag creation, artifact signing, and package repository publication."),
      ("Tech Writer", "Drafts release notes, customer-facing changelogs, and migration instructions.")],
     [("Release Scope & SemVer Calculation", "Git commit log since last tag, closed issue tickets.", "Analyze commits (Conventional Commits standard), calculate next Semantic Version (MAJOR.MINOR.PATCH).", "SemVer Version Target (e.g. v2.4.0) and Commit List.", "Release Manager confirmation of calculated SemVer bump."),
      ("Automated Changelog Generation", "Commit list, conventional commit parser (git-cliff / standard-version).", "Generate markdown changelog highlighting features, bug fixes, breaking changes, and contributor credits.", "Draft Release Notes (CHANGELOG.md).", "Tech Writer sign-off on changelog text readability."),
      ("Artifact Compilation & GPG Signing", "Source commit tag, GPG signing key, release build scripts.", "Compile binaries/packages, generate SHA-256 checksums, sign artifacts with corporate GPG key.", "Signed Release Packages (.tar.gz, .whl, .deb) and checksum files.", "GPG signature verification check passing."),
      ("Binary & Package Repository Publishing", "Signed artifacts, package registry credentials (npm, PyPI, Docker Hub, GitHub Releases).", "Publish signed packages to registry repositories; create GitHub Release with release notes.", "Published Package Metadata URLs.", "Registry download verification test passing."),
      ("Release Broadcast & Stakeholder Notification", "Published GitHub release URL, CHANGELOG text.", "Broadcast release announcement to customer newsletter, developer channels, and internal teams.", "Release Broadcast Record.", "Notification delivery verification to target channels.")],
     ["Gate 1: Breaking changes require MAJOR version bump and migration guide accompaniment.",
      "Gate 2: GPG signature verification must pass on all release binaries prior to registry publishing."],
     ["Failure Mode 1: Package publishing failure due to registry timeout -> Action: Retry upload with exponential backoff.",
      "Failure Mode 2: Incorrect version tag generated -> Action: Delete draft release, correct git tag, re-run release pipeline."],
     "Version-controlled CHANGELOG.md update, GPG-signed release binaries, checksum manifest, and published GitHub Release link."),

    # 27
    ("cicd_pipeline_workflow.md", "CI/CD Pipeline Workflow",
     "Integrate continuous code integration with automated continuous deployment into a unified end-to-end delivery framework.",
     "Git repository, CI/CD runner fleet, target deployment infrastructure, secret store configuration.",
     "Developer push to feature branch or PR pull request event.",
     [("CI/CD Specialist", "Maintains pipeline definitions (.github/workflows, .gitlab-ci.yml), runners, and cache strategies."),
      ("DevOps Lead", "Monitors pipeline performance, throughput metrics, and build security boundaries."),
      ("QA Auditor", "Configures test enforcement gates and code coverage requirements.")],
     [("Trigger Ingestion & Pipeline Initialization", "Git webhook event payload, workflow YAML config.", "Parse webhook, evaluate path filters, pull cached dependencies, allocate isolated pipeline runner.", "Pipeline Job Execution Environment.", "Successful runner initialization within 30 seconds."),
      ("Build & Unit Test Stage", "Source code, unit test runners, linter tools.", "Compile code, execute lint checks, run unit tests, publish code coverage report artifact.", "Build Artifacts & Test Coverage Output.", "100% unit test pass rate and clean build compilation."),
      ("Security & Static Analysis Stage", "Build artifacts, SAST scanner (SonarQube/Snyk), dependency checker.", "Run static analysis and dependency vulnerability scans; check against quality gate thresholds.", "Security Audit Log.", "Zero critical security vulnerabilities detected."),
      ("Staging Deploy & Integration Stage", "Passed security build, staging environment credentials.", "Deploy build artifact to staging environment; execute API integration test suite.", "Staging Deployment Report & Integration Test Summary.", "100% pass rate on integration test suite."),
      ("Production Promotion Stage", "Passed staging build, manual approval trigger (for prod).", "Promote staging build to production; execute zero-downtime deployment; verify APM metrics.", "Production Deployment Record.", "HTTP 200 health check responses on live production endpoints.")],
     ["Gate 1: SAST security scan must contain zero Critical/High vulnerabilities to proceed.",
      "Gate 2: Manual approval required for production promotion stage."],
     ["Failure Mode 1: CI runner out-of-memory error during build -> Action: Scale up runner memory allocation, optimize build cache.",
      "Failure Mode 2: Staging deployment timeout -> Action: Cancel pipeline run, re-trigger after staging environment status check."],
     "Pipeline Workflow Definition (.github/workflows), Unified Test & Security Report, Coverage Summary, and Production Deployment Log."),

    # 28
    ("customer_support_workflow.md", "Customer Support Workflow",
     "Triage incoming customer tickets, execute diagnostic resolution paths, escalate complex issues, and document knowledge base updates.",
     "Ticketing system (Zendesk/Jira Service Management), customer CRM account, knowledge base repository.",
     "Customer ticket submission via email, portal, or chat.",
     [("Support Lead", "Monitors ticket queues, SLA compliance, and escalation handling."),
      ("Knowledge Agent", "Queries knowledge base, drafts resolution articles, and maintains solution templates."),
      ("Technical Specialist", "Diagnoses complex bug reports, inspects system logs, and coordinates hotfixes with engineering.")],
     [("Ticket Ingestion & Classification", "Customer ticket payload (subject, body, tier, attachments).", "Parse ticket content, apply sentiment analysis, categorize topic, assign priority (P1-P4) based on impact.", "Categorized Ticket in Zendesk.", "Priority SLA assignment confirmation."),
      ("Diagnostic Lookup & First-Contact Resolution", "Categorized ticket, Knowledge Base search API.", "Query knowledge base for matching solution patterns; draft personalized resolution response if solution exists.", "First-Contact Resolution Response Draft.", "Verification that response addresses customer query accurately."),
      ("Technical Escalation & Diagnostics", "Unresolved ticket, system log viewer, APM dashboard.", "Replicate reported issue, collect diagnostic log traces, identify root cause component, assign to Tier 2/3 engineering.", "Technical Escalation Packet (Logs, Steps to Reproduce).", "Tier 2 Specialist acknowledgement of ticket assignment."),
      ("Resolution Execution & Customer Communication", "Engineered fix/workaround, customer ticket thread.", "Deploy hotfix or communicate workaround instructions to customer; request verification of issue resolution.", "Customer Resolution Message.", "Customer confirmation of issue resolution."),
      ("SLA Audit & Knowledge Article Creation", "Resolved ticket thread, root cause analysis.", "Verify SLA turnaround time compliance; create or update Knowledge Base article detailing solution pattern.", "New Knowledge Base Article draft.", "Support Lead approval of new KB article.")],
     ["Gate 1: P1 tickets must receive initial response within 15 minutes per SLA.",
      "Gate 2: Technical escalations require reproduction steps and log traces before assignment to engineering."],
     ["Failure Mode 1: Customer unsatisfied with resolution -> Action: Escalate ticket to Support Lead for direct outreach.",
      "Failure Mode 2: SLA breach imminent -> Action: Trigger automatic alert in team Slack channel to reassign idle tickets."],
     "Zendesk Ticket Resolution Log, Technical Escalation Packet, SLA Compliance Audit Report, and Published KB Article."),

    # 29
    ("security_audit_workflow.md", "Security Audit Workflow",
     "Perform dynamic/static vulnerability assessments, IAM privilege audits, compliance posture reviews, and penetration testing.",
     "Target application URLs, cloud infrastructure credentials, source code access, security scanning tools.",
     "Scheduled quarterly audit or major infrastructure architecture overhaul.",
     [("Security Auditor", "Leads security assessment, SAST/DAST scanner runs, and threat modeling."),
      ("Penetration Tester", "Executes manual penetration testing, exploit POCs, and privilege escalation tests."),
      ("DevOps Engineer", "Remediates infrastructure misconfigurations and updates security policy configurations.")],
     [("Scope Definition & Threat Modeling", "Architecture diagrams, API specs, IAM role lists.", "Identify attack surface, define audit boundaries, perform STRIDE threat modeling on system components.", "Security Audit Plan & Threat Model Matrix.", "Security Lead approval of audit scope."),
      ("Static & Dynamic Scanning (SAST/DAST)", "Source repository, staging environment URL, OWASP ZAP / Burp Suite.", "Execute automated SAST on codebase; run DAST crawler against staging endpoints; execute dependency vulnerability scan.", "Automated Security Scan Findings Log.", "Scan completion with 0 unhandled scanner exceptions."),
      ("Manual Penetration & Privilege Escalation Testing", "Staging environment access, security test accounts.", "Attempt manual SQLi, XSS, CSRF, broken access control (IDOR), and privilege escalation attacks.", "Penetration Testing Proof-of-Concept (PoC) Log.", "Documented PoC steps for all confirmed security flaws."),
      ("Infrastructure & IAM Posture Review", "Cloud infrastructure account, Prowler / AWS Security Hub.", "Audit IAM roles for over-privileged permissions, inspect S3 bucket policies, verify TLS cipher suite strength.", "Infrastructure Security Compliance Audit Report.", "Zero publicly exposed sensitive storage buckets or wildcard IAM admin policies."),
      ("Executive Findings Report & Remediation Roadmap", "All audit findings (SAST, DAST, Pen-Test, Infra).", "Risk-rank vulnerabilities using CVSS v3.1 scoring; draft executive summary and prioritized remediation tickets.", "Executive Security Audit Report & CVSS Remediation Roadmap.", "CISO sign-off on final audit report and remediation SLA targets.")],
     ["Gate 1: Critical CVSS score (>= 9.0) findings require immediate emergency patching within 24 hours.",
      "Gate 2: Executive Security Audit Report must be signed off by CISO before compliance filing."],
     ["Failure Mode 1: DAST scanner causing staging DB corruption -> Action: Pause DAST scan, restore staging database from snapshot, resume with read-only payload settings.",
      "Failure Mode 2: Over-privileged IAM role identified -> Action: Immediately apply least-privilege policy fix."],
     "Executive Security Audit Report PDF, CVSS-ranked Vulnerability Backlog, Penetration Testing PoC Artifacts, and Infrastructure Audit Log."),

    # 30
    ("vulnerability_remediation_workflow.md", "Vulnerability Remediation Workflow",
     "Triage security vulnerabilities, patch software dependencies, verify code fixes, and validate security patch deployment.",
     "Vulnerability report (CVSS scores, CVE IDs), source code repository, package manager manifests.",
     "Ingestion of security audit finding or automated CVE alert (Dependabot/Snyk).",
     [("Security Engineer", "Triages CVE severity, determines impact scope, and defines remediation strategy."),
      ("Patch Manager / Developer", "Applies library version bumps, refactors vulnerable code paths, and updates dependency locks."),
      ("QA Auditor", "Executes security regression test suite to ensure patch does not introduce functional regressions.")],
     [("Vulnerability Triage & CVSS Scoring", "CVE alert payload, dependency graph, application architecture.", "Validate vulnerability applicability, assess exploitability in current runtime context, set SLA deadline.", "Vulnerability Triage Record.", "Security Engineer validation of CVE applicability."),
      ("Dependency Patch & Code Fix Implementation", "Source code, package manifest (package.json/requirements.txt), fixed library release.", "Update vulnerable dependency version, refactor broken API signatures, write regression unit test.", "Patch Branch Pull Request.", "Build compilation and unit test execution passing locally."),
      ("Security Regression Testing", "Patch PR, SAST scanner, regression test suite.", "Re-run SAST scanner to confirm CVE resolution; execute functional regression tests to verify zero feature breakage.", "Security Patch Verification Log.", "Zero security findings for target CVE and 100% regression test pass rate."),
      ("Emergency PR Review & Approval", "Patch PR diff, security verification log.", "Expedite peer review for security patch, confirm clean vulnerability report.", "Approved Security Patch PR.", "Security Engineer sign-off on PR merge."),
      ("Production Deployment & CVE Closure", "Approved PR, production release pipeline.", "Deploy patch to production environment, verify runtime stability, close CVE ticket in security tracker.", "CVE Resolution & Closure Certificate.", "Security tracker ticket status updated to Closed.")],
     ["Gate 1: Critical CVEs (CVSS >= 9.0) must be patched and deployed within 24 hours of triage.",
      "Gate 2: Vulnerability fix must be verified by SAST/dependency scanner before merging PR."],
     ["Failure Mode 1: Dependency version bump introduces breaking code changes -> Action: Implement vendored security backport patch or wrap vulnerable call in protective input sanitizer.",
      "Failure Mode 2: Patch deployment causes production outage -> Action: Execute instant rollback, implement emergency hotfix."],
     "Patch Branch PR, Security Verification Log, SAST Re-scan Report, and CVE Closure Certificate.")
]

# Write batch 4
for item in wf_list:
    write_wf(*item)

print("Batch 4 (25-30) written successfully.")
