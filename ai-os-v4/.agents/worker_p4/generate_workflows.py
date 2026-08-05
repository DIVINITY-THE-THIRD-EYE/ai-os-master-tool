import os
import sys

TARGET_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_04_workflow_library"
os.makedirs(TARGET_DIR, exist_ok=True)

workflows_data = [
    {
        "filename": "software_development_workflow.md",
        "title": "Software Development Workflow",
        "purpose": "Provide a structured, end-to-end lifecycle for converting technical requirements into tested, verified, and deployable software components.",
        "prereqs": "Approved architecture spec, user stories with acceptance criteria, active git repository, baseline test suite.",
        "trigger": "Creation or assignment of a feature branch / epic ticket in the project management system.",
        "roles": [
            ("Lead Architect", "Provides architectural guidance, validates component design, and reviews technical trade-offs."),
            ("Software Engineer", "Implements core feature code, writes unit tests, and creates pull requests."),
            ("QA Engineer", "Executes automated integration tests, validates edge cases, and verifies acceptance criteria."),
            ("Code Reviewer", "Conducts static code review, security analysis, and logic verification.")
        ],
        "steps": [
            {
                "num": 1,
                "name": "Requirement Breakdown & Design Spec",
                "inputs": "User story specification, existing codebase documentation, architectural guidelines.",
                "actions": "Analyze user story, map component touchpoints, outline class/interface structures, define unit test targets.",
                "outputs": "Technical Design Specification (TDS) document and feature branch initialization.",
                "verification": "Lead Architect sign-off on design spec and branch naming compliance."
            },
            {
                "num": 2,
                "name": "Test-Driven Implementation",
                "inputs": "TDS document, unit testing framework, codebase mocks/fixtures.",
                "actions": "Write failing unit tests matching acceptance criteria; write feature code to pass unit tests; refactor.",
                "outputs": "Implemented feature code and complete unit test suite.",
                "verification": "100% unit test pass rate with minimum 85% line coverage."
            },
            {
                "num": 3,
                "name": "Integration & Static Code Analysis",
                "inputs": "Feature code, integration test suite, linter/SAST configuration files.",
                "actions": "Execute static analysis tools (SonarQube/ESLint/PyLint); run integration test suite against local build.",
                "outputs": "Static analysis report and integration test results.",
                "verification": "Zero critical linting/security findings and clean integration test run."
            },
            {
                "num": 4,
                "name": "Peer Review & Refinement",
                "inputs": "Pull Request diff, static analysis report, test execution logs.",
                "actions": "Peer reviewer inspects diff for code smells, security vulnerabilities, performance bottlenecks, and adherence to conventions.",
                "outputs": "Pull Request comments, approval status, or change requests.",
                "verification": "Minimum 2 peer approvals and green CI status check."
            },
            {
                "num": 5,
                "name": "Merge & Deployment Readiness",
                "inputs": "Approved PR, target integration branch (main/develop).",
                "actions": "Perform squash-and-merge or rebase onto target branch; update issue tracker status.",
                "outputs": "Merged commit in main branch and updated ticket state.",
                "verification": "Post-merge build pass notification on CI server."
            }
        ],
        "decision_gates": [
            "Gate 1 (Design Gate): TDS must be approved by Lead Architect before any code is committed.",
            "Gate 2 (Quality Gate): CI pipeline must achieve >85% unit coverage and zero SAST critical warnings prior to PR review.",
            "Gate 3 (Merge Gate): Requires at least 2 explicit reviewer approvals and clean automated test suite."
        ],
        "failure_modes": [
            "Failure Mode 1: Static analysis detects high-severity security flaw -> Action: PR automatically blocked; task returned to Engineer for immediate patching.",
            "Failure Mode 2: Integration test failure due to API schema mismatch -> Action: Revert feature branch to pre-integration state, re-verify API specs.",
            "Failure Mode 3: Merge conflict on main branch -> Action: Software Engineer performs local rebase and re-runs test suite before force-updating PR."
        ],
        "artifact_standard": "All feature branches must contain clean commit history, fully passing pytest/jest test suites, updated documentation in docs/ directory, and clear PR descriptions referencing ticket IDs."
    },
    {
        "filename": "website_creation_workflow.md",
        "title": "Website Creation Workflow",
        "purpose": "Define the operational sequence for designing, developing, optimizing, and launching responsive, accessible, and SEO-optimized websites.",
        "prereqs": "Brand guidelines, copy assets, wireframe approvals, domain name registration, hosting target configuration.",
        "trigger": "Kickoff of website project milestone by Product Lead.",
        "roles": [
            ("UI/UX Specialist", "Delivers wireframes, visual design specs, responsive layouts, and accessibility standards."),
            ("Frontend Developer", "Builds semantic HTML/CSS/JS or framework-based frontend (Next.js/Astro)."),
            ("Content Specialist", "Integrates copy, media assets, metadata, and schema markup."),
            ("QA Engineer", "Performs cross-browser, cross-device, accessibility (WCAG), and performance (Lighthouse) audits.")
        ],
        "steps": [
            {
                "num": 1,
                "name": "Information Architecture & Wireframing",
                "inputs": "Project brief, target audience personas, brand assets.",
                "actions": "Draft site map, user flows, and low-fidelity responsive wireframes for desktop and mobile viewports.",
                "outputs": "Approved sitemap and Figma wireframes.",
                "verification": "Design review approval from UI/UX Specialist and Product Lead."
            },
            {
                "num": 2,
                "name": "Component Development & Styling",
                "inputs": "High-fidelity mockups, design tokens (colors, typography, spacing).",
                "actions": "Construct modular components, global layout grids, styling system, and interactive states.",
                "outputs": "Component library codebase with Storybook/preview pages.",
                "verification": "Pixel-perfect visual audit against Figma specs across 3 breakpoint viewports."
            },
            {
                "num": 3,
                "name": "Content Integration & SEO Optimization",
                "inputs": "Final copy deck, imagery assets, target keywords.",
                "actions": "Inject content into templates, configure Open Graph tags, alt tags, canonical URLs, and JSON-LD structured data.",
                "outputs": "Fully populated site pages with complete metadata.",
                "verification": "Zero missing alt attributes and validated JSON-LD schema via Google Structured Data Tool."
            },
            {
                "num": 4,
                "name": "Performance & Accessibility Audit",
                "inputs": "Staging URL, performance audit tools (Lighthouse, axe-core).",
                "actions": "Run Lighthouse performance benchmarks, optimize image sizes/formats (WebP/AVIF), audit WCAG 2.1 AA compliance.",
                "outputs": "Audit report with Lighthouse score >= 90 across all categories.",
                "verification": "Lighthouse score >= 90 for Performance, Accessibility, Best Practices, and SEO."
            },
            {
                "num": 5,
                "name": "Production Deployment & DNS Cutover",
                "inputs": "Passed staging site, production domain settings, SSL certificate.",
                "actions": "Trigger production deployment on hosting platform (Vercel/Netlify/S3), update DNS records, verify SSL installation.",
                "outputs": "Live website URL with HTTPS enabled.",
                "verification": "HTTP 200 responses across all key pages and valid SSL certificate check."
            }
        ],
        "decision_gates": [
            "Gate 1: Wireframes and sitemap must be signed off before component development commences.",
            "Gate 2: Staging site must pass WCAG 2.1 AA and Lighthouse >= 90 benchmarks before DNS cutover is scheduled."
        ],
        "failure_modes": [
            "Failure Mode 1: Lighthouse performance score below 90 due to unoptimized images -> Action: Compress assets, implement lazy loading, re-run audit.",
            "Failure Mode 2: DNS propagation failure or SSL provisioning error -> Action: Roll back DNS CNAME/A record to staging fallback, debug hosting SSL logs."
        ],
        "artifact_standard": "Production static assets hosted on CDN, clean Git repository with semantic commit messages, automated Lighthouse CI config, and complete SEO manifest."
    },
    {
        "filename": "flutter_app_development_workflow.md",
        "title": "Flutter App Development Workflow",
        "purpose": "Standardize cross-platform mobile application development using Flutter, ensuring native performance, state management consistency, and automated app store artifact creation.",
        "prereqs": "Flutter SDK setup, Android SDK / Xcode toolchains, app design system, API specs.",
        "trigger": "Mobile feature sprint initiation.",
        "roles": [
            ("Mobile Architect", "Defines Flutter architecture (Riverpod/BLoC), folder structure, and native platform integration standards."),
            ("Flutter Developer", "Implements Flutter UI widgets, state logic, and platform channels."),
            ("Mobile QA Specialist", "Executes integration testing on Android Emulators and iOS Simulators, checking device compatibility.")
        ],
        "steps": [
            {
                "num": 1,
                "name": "State Management & Architecture Setup",
                "inputs": "Feature requirements, Flutter project scaffold, API documentation.",
                "actions": "Define state models, repositories, and state management providers (e.g. Riverpod / BLoC) for the feature module.",
                "outputs": "Architecture scaffold with mock repositories and data models.",
                "verification": "Unit tests verifying state transitions and model serialization/deserialization."
            },
            {
                "num": 2,
                "name": "Widget Implementation & Responsive Layout",
                "inputs": "Figma design specs, state providers.",
                "actions": "Build custom Flutter widgets, implement adaptive layouts for screens/tablets, bind widgets to state streams.",
                "outputs": "Functional Flutter screens with reactive UI updates.",
                "verification": "Flutter Golden tests passing for key screen states across light/dark themes."
            },
            {
                "num": 3,
                "name": "Native Platform Channel Integration",
                "inputs": "Native API requirements (camera, bluetooth, secure storage).",
                "actions": "Write Kotlin (Android) and Swift (iOS) platform channel implementations or configure pubspec plugins.",
                "outputs": "Platform channel bridge and native permission configurations (AndroidManifest.xml, Info.plist).",
                "verification": "Device testing verifying native capability execution without crashes."
            },
            {
                "num": 4,
                "name": "Integration & Integration Test Run",
                "inputs": "Complete feature codebase, integration test scripts (flutter_test / integration_test).",
                "actions": "Execute integration tests across simulated devices; profile memory consumption and frame rendering rates (60/120 fps).",
                "outputs": "Integration test report and performance profiling trace.",
                "verification": "Zero jank (no dropped frames during scroll tests) and 100% integration test pass rate."
            },
            {
                "num": 5,
                "name": "Build Generation & Artifact Signing",
                "inputs": "Passed codebase, release keystore / iOS provisioning profiles.",
                "actions": "Build release APK/AAB for Android and IPA for iOS using Fastlane / Flutter build commands.",
                "outputs": "Signed release binaries (.aab, .ipa) stored in build outputs.",
                "verification": "Binary signature verification and successful upload to TestFlight / Google Play Internal Track."
            }
        ],
        "decision_gates": [
            "Gate 1: State management architecture must pass unit test coverage check (>80%) before UI integration.",
            "Gate 2: Release builds must be signed and verified on physical test devices prior to store submission."
        ],
        "failure_modes": [
            "Failure Mode 1: iOS build failure due to provisioning profile expiration -> Action: Renew provisioning certificate in Apple Developer portal, re-run Fastlane sync.",
            "Failure Mode 2: Flutter widget layout overflow error -> Action: Refactor layout using Flexible/Expanded widgets, re-verify with golden tests."
        ],
        "artifact_standard": "Signed AAB and IPA release packages, flutter analyzer report with 0 warnings, and clean integration test logs."
    },
    {
        "filename": "react_app_development_workflow.md",
        "title": "React App Development Workflow",
        "purpose": "Govern the design, build, state management, testing, and bundling of modern React single-page or server-rendered web applications.",
        "prereqs": "Node.js environment, Vite/Next.js setup, component specs, backend API endpoints.",
        "trigger": "Frontend feature sprint allocation.",
        "roles": [
            ("Frontend Lead", "Establishes React patterns, state management architecture (Zustand/Redux), and bundle optimization targets."),
            ("React Developer", "Builds React components, custom hooks, and route handlers."),
            ("UI Auditor", "Checks visual compliance, accessibility tree, and bundle size limits.")
        ],
        "steps": [
            {
                "num": 1,
                "name": "Component & Hook Architecture",
                "inputs": "Feature specification, API contract, state management guidelines.",
                "actions": "Design component breakdown, custom hooks for data fetching (TanStack Query/SWR), and client-side state schema.",
                "outputs": "Component interfaces (TypeScript definitions) and custom hook skeletons.",
                "verification": "TypeScript compiler verification (`tsc --noEmit`) passing with zero errors."
            },
            {
                "num": 2,
                "name": "Interactive Component Construction",
                "inputs": "TypeScript interfaces, Tailwind CSS / Styled Components design tokens.",
                "actions": "Implement JSX/TSX components, apply responsive styles, manage local component state, handle loading/error states.",
                "outputs": "Functional React components co-located with tests and styles.",
                "verification": "Visual check and unit tests (React Testing Library) verifying state rendering."
            },
            {
                "num": 3,
                "name": "API & Global State Binding",
                "inputs": "REST/GraphQL endpoints, mock server handlers (MSW).",
                "actions": "Connect custom hooks to live API endpoints, handle authentication headers, implement optimistic updates.",
                "outputs": "End-to-end data-bound React views.",
                "verification": "Integration tests passing with MSW mock server and live staging server."
            },
            {
                "num": 4,
                "name": "Bundle Optimization & Code Splitting",
                "inputs": "Built React application assets, bundler analyzer (rollup-plugin-visualizer / webpack-bundle-analyzer).",
                "actions": "Implement route-based dynamic imports (`React.lazy`), optimize tree-shaking, audit vendor bundle size.",
                "outputs": "Optimized production bundle with chunk splitting.",
                "verification": "Initial JS bundle size below 150KB gzipped."
            },
            {
                "num": 5,
                "name": "E2E Testing & Staging Deploy",
                "inputs": "Staging environment configuration, Playwright / Cypress test suites.",
                "actions": "Run full E2E user flow tests on staging build; publish deployment preview.",
                "outputs": "E2E test run video/trace artifacts and staging URL.",
                "verification": "100% E2E test pass rate across Chrome, Firefox, and Safari viewports."
            }
        ],
        "decision_gates": [
            "Gate 1: Strict TypeScript compilation (`strict: true`) must pass before merging code into develop branch.",
            "Gate 2: Initial bundle size budget check must pass before production deployment approval."
        ],
        "failure_modes": [
            "Failure Mode 1: React re-render loop causing performance degradation -> Action: Profile component via React DevTools, introduce `useMemo`/`useCallback` or state structure simplification.",
            "Failure Mode 2: Dynamic import chunk loading failure -> Action: Add Error Boundary wrapping lazy components, implement fallback retry logic."
        ],
        "artifact_standard": "Production build dist directory, clean TypeScript build output, zero ESLint/React Hooks warnings, and Playwright test execution reports."
    },
    {
        "filename": "node_backend_development_workflow.md",
        "title": "Node Backend Development Workflow",
        "purpose": "Provide a rigorous process for engineering scalable, secure, and asynchronous backend microservices and APIs using Node.js.",
        "prereqs": "Node.js runtime, database access (PostgreSQL/MongoDB), API design spec, environment configuration template.",
        "trigger": "Backend service task assignment.",
        "roles": [
            ("Backend Architect", "Defines microservice architecture, DB schemas, auth standards, and middleware stack."),
            ("Node Specialist", "Implements route controllers, service layer logic, ORM models, and async event handlers."),
            ("Security Auditor", "Validates input sanitization, JWT/OAuth flow security, and rate limiting.")
        ],
        "steps": [
            {
                "num": 1,
                "name": "Schema Design & Service Layer Setup",
                "inputs": "Feature specification, database design rules.",
                "actions": "Define database migrations/models (Prisma/TypeORM/Mongoose), create DTOs (Data Transfer Objects), and outline service interface.",
                "outputs": "Database migration scripts and TypeScript service interfaces.",
                "verification": "Database migration dry-run execution against local test database succeeds."
            },
            {
                "num": 2,
                "name": "Controller & Business Logic Implementation",
                "inputs": "Service interfaces, schema validation libraries (Zod/Joi).",
                "actions": "Write route handlers, express/fastify middleware, payload validation schemas, and business domain logic.",
                "outputs": "Complete route module with controller, service, and validation logic.",
                "verification": "Unit tests for service functions and route handlers passing with high coverage."
            },
            {
                "num": 3,
                "name": "Security & Middleware Hardening",
                "inputs": "Route module, security baseline (Helmet, CORS, Rate-Limiter, JWT validator).",
                "actions": "Attach security middleware, sanitize parameters against SQLi/XSS, configure error handling middleware.",
                "outputs": "Secured Node.js application module.",
                "verification": "Security audit script verifying header flags and unauthenticated route rejection."
            },
            {
                "num": 4,
                "name": "Integration & Load Testing",
                "inputs": "Running local/containerized Node service, Supertest / k6 load test scripts.",
                "actions": "Run HTTP integration tests with Supertest; perform stress testing with k6 to measure RPS and latency metrics.",
                "outputs": "Integration test report and k6 performance report.",
                "verification": "p95 response latency < 200ms under target load, 0% unhandled promise rejections."
            },
            {
                "num": 5,
                "name": "Containerization & Production Release",
                "inputs": "Node codebase, multi-stage Dockerfile, production environment variables.",
                "actions": "Build lightweight Docker image (alpine/distroless), scan container vulnerability (Trivy), push image to registry.",
                "outputs": "Verified Docker image artifact pushed to Container Registry.",
                "verification": "Trivy scan shows 0 HIGH/CRITICAL vulnerabilities."
            }
        ],
        "decision_gates": [
            "Gate 1: DB migrations must be backward-compatible and tested on staging snapshot before deployment.",
            "Gate 2: Container image vulnerability scan must pass with 0 Critical/High issues prior to production release."
        ],
        "failure_modes": [
            "Failure Mode 1: Node process memory leak under load -> Action: Profile process heap dump using clinic.js / Chrome DevTools, fix event listener / cache leaks.",
            "Failure Mode 2: Unhandled async promise rejection crashing process -> Action: Implement global exception / rejection handlers and audit async try/catch blocks."
        ],
        "artifact_standard": "Multi-stage Docker container, OpenAPI spec sync, clean TypeScript compilation, and 100% passing Supertest suite."
    }
]

# We will generate all 50 items programmatically using structured templates tailored to each domain.
print(f"Base data has {len(workflows_data)} pre-defined templates.")
