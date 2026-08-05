# Website Creation Workflow Specification

## 1. Purpose & Objective
Define the operational sequence for designing, developing, optimizing, and launching responsive, accessible, and SEO-optimized websites.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Brand guidelines, copy assets, wireframe approvals, domain name registration, hosting target configuration.
- **Trigger Conditions**: Kickoff of website project milestone by Product Lead.

## 3. Participating Agent Roles & Responsibilities
- **UI/UX Specialist**: Delivers wireframes, visual design specs, responsive layouts, and accessibility standards.
- **Frontend Developer**: Builds semantic HTML/CSS/JS or framework-based frontend (Next.js/Astro).
- **Content Specialist**: Integrates copy, media assets, metadata, and schema markup.
- **QA Engineer**: Performs cross-browser, cross-device, accessibility (WCAG), and performance (Lighthouse) audits.

## 4. Step-by-Step Execution Sequence

### Step 1: Information Architecture & Wireframing
- **Inputs**: Project brief, target audience personas, brand assets.
- **Actions**: Draft site map, user flows, and low-fidelity responsive wireframes for desktop and mobile viewports.
- **Outputs**: Approved sitemap and Figma wireframes.
- **Verification**: Design review approval from UI/UX Specialist and Product Lead.

### Step 2: Component Development & Styling
- **Inputs**: High-fidelity mockups, design tokens (colors, typography, spacing).
- **Actions**: Construct modular components, global layout grids, styling system, and interactive states.
- **Outputs**: Component library codebase with Storybook/preview pages.
- **Verification**: Pixel-perfect visual audit against Figma specs across 3 breakpoint viewports.

### Step 3: Content Integration & SEO Optimization
- **Inputs**: Final copy deck, imagery assets, target keywords.
- **Actions**: Inject content into templates, configure Open Graph tags, alt tags, canonical URLs, and JSON-LD structured data.
- **Outputs**: Fully populated site pages with complete metadata.
- **Verification**: Zero missing alt attributes and validated JSON-LD schema via Google Structured Data Tool.

### Step 4: Performance & Accessibility Audit
- **Inputs**: Staging URL, performance audit tools (Lighthouse, axe-core).
- **Actions**: Run Lighthouse performance benchmarks, optimize image sizes/formats (WebP/AVIF), audit WCAG 2.1 AA compliance.
- **Outputs**: Audit report with Lighthouse score >= 90 across all categories.
- **Verification**: Lighthouse score >= 90 for Performance, Accessibility, Best Practices, and SEO.

### Step 5: Production Deployment & DNS Cutover
- **Inputs**: Passed staging site, production domain settings, SSL certificate.
- **Actions**: Trigger production deployment on hosting platform (Vercel/Netlify/S3), update DNS records, verify SSL installation.
- **Outputs**: Live website URL with HTTPS enabled.
- **Verification**: HTTP 200 responses across all key pages and valid SSL certificate check.

## 5. Decision Gates & Branching Rules
- Gate 1: Wireframes and sitemap must be signed off before component development commences.
- Gate 2: Staging site must pass WCAG 2.1 AA and Lighthouse >= 90 benchmarks before DNS cutover is scheduled.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Lighthouse performance score below 90 due to unoptimized images -> Action: Compress assets, implement lazy loading, re-run audit.
- Failure Mode 2: DNS propagation failure or SSL provisioning error -> Action: Roll back DNS CNAME/A record to staging fallback, debug hosting SSL logs.

## 7. Artifact Delivery & Output Standard
Production static assets hosted on CDN, clean Git repository with semantic commit messages, automated Lighthouse CI config, and complete SEO manifest.
