# Engineering Onboarding Guide: {{TEAM_NAME}}

> **Document Type**: Team Onboarding & Setup Guide  
> **Target Role**: {{TARGET_ROLE}} (e.g., Software Engineer / DevOps Engineer)  
> **Team**: {{TEAM_NAME}}  
> **Onboarding Buddy**: {{BUDDY_NAME}}  
> **Engineering Lead**: {{LEAD_NAME}}  
> **Last Updated**: {{LAST_UPDATED}}  

---

## 1. Welcome & Team Overview

### 1.1 Team Mission
*Instruction: Introduce {{TEAM_NAME}}, core responsibilities, key projects, and team culture.*

- **Slack Channels**: `#{{TEAM_SLACK_CHANNEL}}`, `#{{DEV_SLACK_CHANNEL}}`
- **Weekly Team Ceremony Schedule**:
  - Daily Standup: 09:45 AM EST (Mon-Fri)
  - Sprint Grooming: Tuesday 14:00 EST
  - Retrospective: Alternate Fridays 15:00 EST

---

## 2. Day 1: Access & Accounts Checklist

- [ ] Corporate Email & SSO Account Activated.
- [ ] Hardware / Laptop encryption verified.
- [ ] GitHub Organization invitation accepted (`https://github.com/{{ORG_NAME}}`).
- [ ] Password Manager & MFA authenticator setup.
- [ ] 1Password / Vault credentials access granted.
- [ ] Join team Slack channels and introduce yourself!

---

## 3. Week 1: Development Environment Setup

### 3.1 Prerequisite Tooling
Install local development tools:
- Docker Desktop / Rancher Desktop
- Node.js LTS / Python 3.11 / Go 1.22
- Git & GitHub CLI (`gh`)
- IDE (VS Code / JetBrains IntelliJ)

### 3.2 Repository Setup & Local Run
```bash
# 1. Clone primary repository
git clone git@github.com:{{ORG_NAME}}/{{PRIMARY_REPO}}.git
cd {{PRIMARY_REPO}}

# 2. Install dependencies & initialize environment
cp .env.example .env.local
npm install

# 3. Start local development environment
npm run dev
```

Verify service is running locally at `http://localhost:3000/health`.

---

## 4. Month 1: First Milestone & Deliverable

- **First Ticket Goal**: Complete starter bug fix or small documentation update within 5 business days.
- **First Production Release**: Pair with {{BUDDY_NAME}} to execute your first production release by Week 3.

---

## 5. Helpful Links & Knowledge Base
- Architectural Specs: `docs/architecture.md`
- Deployment Runbooks: `docs/runbooks/`
- Team Wiki & API Specs: `https://wiki.{{DOMAIN}}/display/{{TEAM_KEY}}`
