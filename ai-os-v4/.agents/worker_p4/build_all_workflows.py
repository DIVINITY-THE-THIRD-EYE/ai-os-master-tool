import os
import sys

TARGET_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_04_workflow_library"
os.makedirs(TARGET_DIR, exist_ok=True)

workflows = [
    # 1. software_development_workflow.md
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
            ("Requirement Breakdown & Design Spec", "User story specification, existing codebase documentation, architectural guidelines.", "Analyze user story, map component touchpoints, outline class/interface structures, define unit test targets.", "Technical Design Specification (TDS) document and feature branch initialization.", "Lead Architect sign-off on design spec and branch naming compliance."),
            ("Test-Driven Implementation", "TDS document, unit testing framework, codebase mocks/fixtures.", "Write failing unit tests matching acceptance criteria; write feature code to pass unit tests; refactor.", "Implemented feature code and complete unit test suite.", "100% unit test pass rate with minimum 85% line coverage."),
            ("Integration & Static Code Analysis", "Feature code, integration test suite, linter/SAST configuration files.", "Execute static analysis tools (SonarQube/ESLint/PyLint); run integration test suite against local build.", "Static analysis report and integration test results.", "Zero critical linting/security findings and clean integration test run."),
            ("Peer Review & Refinement", "Pull Request diff, static analysis report, test execution logs.", "Peer reviewer inspects diff for code smells, security vulnerabilities, performance bottlenecks, and adherence to conventions.", "Pull Request comments, approval status, or change requests.", "Minimum 2 peer approvals and green CI status check."),
            ("Merge & Deployment Readiness", "Approved PR, target integration branch (main/develop).", "Perform squash-and-merge or rebase onto target branch; update issue tracker status.", "Merged commit in main branch and updated ticket state.", "Post-merge build pass notification on CI server.")
        ],
        "gates": [
            "Gate 1 (Design Gate): TDS must be approved by Lead Architect before any code is committed.",
            "Gate 2 (Quality Gate): CI pipeline must achieve >85% unit coverage and zero SAST critical warnings prior to PR review.",
            "Gate 3 (Merge Gate): Requires at least 2 explicit reviewer approvals and clean automated test suite."
        ],
        "failures": [
            "Failure Mode 1: Static analysis detects high-severity security flaw -> Action: PR automatically blocked; task returned to Engineer for immediate patching.",
            "Failure Mode 2: Integration test failure due to API schema mismatch -> Action: Revert feature branch to pre-integration state, re-verify API specs.",
            "Failure Mode 3: Merge conflict on main branch -> Action: Software Engineer performs local rebase and re-runs test suite before force-updating PR."
        ],
        "artifact_standard": "All feature branches must contain clean commit history, fully passing pytest/jest test suites, updated documentation in docs/ directory, and clear PR descriptions referencing ticket IDs."
    },
    # 2. website_creation_workflow.md
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
            ("Information Architecture & Wireframing", "Project brief, target audience personas, brand assets.", "Draft site map, user flows, and low-fidelity responsive wireframes for desktop and mobile viewports.", "Approved sitemap and Figma wireframes.", "Design review approval from UI/UX Specialist and Product Lead."),
            ("Component Development & Styling", "High-fidelity mockups, design tokens (colors, typography, spacing).", "Construct modular components, global layout grids, styling system, and interactive states.", "Component library codebase with Storybook/preview pages.", "Pixel-perfect visual audit against Figma specs across 3 breakpoint viewports."),
            ("Content Integration & SEO Optimization", "Final copy deck, imagery assets, target keywords.", "Inject content into templates, configure Open Graph tags, alt tags, canonical URLs, and JSON-LD structured data.", "Fully populated site pages with complete metadata.", "Zero missing alt attributes and validated JSON-LD schema via Google Structured Data Tool."),
            ("Performance & Accessibility Audit", "Staging URL, performance audit tools (Lighthouse, axe-core).", "Run Lighthouse performance benchmarks, optimize image sizes/formats (WebP/AVIF), audit WCAG 2.1 AA compliance.", "Audit report with Lighthouse score >= 90 across all categories.", "Lighthouse score >= 90 for Performance, Accessibility, Best Practices, and SEO."),
            ("Production Deployment & DNS Cutover", "Passed staging site, production domain settings, SSL certificate.", "Trigger production deployment on hosting platform (Vercel/Netlify/S3), update DNS records, verify SSL installation.", "Live website URL with HTTPS enabled.", "HTTP 200 responses across all key pages and valid SSL certificate check.")
        ],
        "gates": [
            "Gate 1: Wireframes and sitemap must be signed off before component development commences.",
            "Gate 2: Staging site must pass WCAG 2.1 AA and Lighthouse >= 90 benchmarks before DNS cutover is scheduled."
        ],
        "failures": [
            "Failure Mode 1: Lighthouse performance score below 90 due to unoptimized images -> Action: Compress assets, implement lazy loading, re-run audit.",
            "Failure Mode 2: DNS propagation failure or SSL provisioning error -> Action: Roll back DNS CNAME/A record to staging fallback, debug hosting SSL logs."
        ],
        "artifact_standard": "Production static assets hosted on CDN, clean Git repository with semantic commit messages, automated Lighthouse CI config, and complete SEO manifest."
    },
    # 3. flutter_app_development_workflow.md
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
            ("State Management & Architecture Setup", "Feature requirements, Flutter project scaffold, API documentation.", "Define state models, repositories, and state management providers (e.g. Riverpod / BLoC) for the feature module.", "Architecture scaffold with mock repositories and data models.", "Unit tests verifying state transitions and model serialization/deserialization."),
            ("Widget Implementation & Responsive Layout", "Figma design specs, state providers.", "Build custom Flutter widgets, implement adaptive layouts for screens/tablets, bind widgets to state streams.", "Functional Flutter screens with reactive UI updates.", "Flutter Golden tests passing for key screen states across light/dark themes."),
            ("Native Platform Channel Integration", "Native API requirements (camera, bluetooth, secure storage).", "Write Kotlin (Android) and Swift (iOS) platform channel implementations or configure pubspec plugins.", "Platform channel bridge and native permission configurations (AndroidManifest.xml, Info.plist).", "Device testing verifying native capability execution without crashes."),
            ("Integration & Performance Trace Run", "Complete feature codebase, integration test scripts (flutter_test / integration_test).", "Execute integration tests across simulated devices; profile memory consumption and frame rendering rates (60/120 fps).", "Integration test report and performance profiling trace.", "Zero jank (no dropped frames during scroll tests) and 100% integration test pass rate."),
            ("Build Generation & Artifact Signing", "Passed codebase, release keystore / iOS provisioning profiles.", "Build release APK/AAB for Android and IPA for iOS using Fastlane / Flutter build commands.", "Signed release binaries (.aab, .ipa) stored in build outputs.", "Binary signature verification and successful upload to TestFlight / Google Play Internal Track.")
        ],
        "gates": [
            "Gate 1: State management architecture must pass unit test coverage check (>80%) before UI integration.",
            "Gate 2: Release builds must be signed and verified on physical test devices prior to store submission."
        ],
        "failures": [
            "Failure Mode 1: iOS build failure due to provisioning profile expiration -> Action: Renew provisioning certificate in Apple Developer portal, re-run Fastlane sync.",
            "Failure Mode 2: Flutter widget layout overflow error -> Action: Refactor layout using Flexible/Expanded widgets, re-verify with golden tests."
        ],
        "artifact_standard": "Signed AAB and IPA release packages, flutter analyzer report with 0 warnings, and clean integration test logs."
    },
    # 4. react_app_development_workflow.md
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
            ("Component & Hook Architecture", "Feature specification, API contract, state management guidelines.", "Design component breakdown, custom hooks for data fetching (TanStack Query/SWR), and client-side state schema.", "TypeScript definitions and custom hook skeletons.", "TypeScript compiler verification (`tsc --noEmit`) passing with zero errors."),
            ("Interactive Component Construction", "TypeScript interfaces, Tailwind CSS / Styled Components design tokens.", "Implement JSX/TSX components, apply responsive styles, manage local component state, handle loading/error states.", "Functional React components co-located with tests and styles.", "Visual check and unit tests (React Testing Library) verifying state rendering."),
            ("API & Global State Binding", "REST/GraphQL endpoints, mock server handlers (MSW).", "Connect custom hooks to live API endpoints, handle authentication headers, implement optimistic updates.", "End-to-end data-bound React views.", "Integration tests passing with MSW mock server and live staging server."),
            ("Bundle Optimization & Code Splitting", "Built React application assets, bundler analyzer (rollup-plugin-visualizer / webpack-bundle-analyzer).", "Implement route-based dynamic imports (`React.lazy`), optimize tree-shaking, audit vendor bundle size.", "Optimized production bundle with chunk splitting.", "Initial JS bundle size below 150KB gzipped."),
            ("E2E Testing & Staging Deploy", "Staging environment configuration, Playwright / Cypress test suites.", "Run full E2E user flow tests on staging build; publish deployment preview.", "E2E test run video/trace artifacts and staging URL.", "100% E2E test pass rate across Chrome, Firefox, and Safari viewports.")
        ],
        "gates": [
            "Gate 1: Strict TypeScript compilation (`strict: true`) must pass before merging code into develop branch.",
            "Gate 2: Initial bundle size budget check must pass before production deployment approval."
        ],
        "failures": [
            "Failure Mode 1: React re-render loop causing performance degradation -> Action: Profile component via React DevTools, introduce `useMemo`/`useCallback` or state structure simplification.",
            "Failure Mode 2: Dynamic import chunk loading failure -> Action: Add Error Boundary wrapping lazy components, implement fallback retry logic."
        ],
        "artifact_standard": "Production build dist directory, clean TypeScript build output, zero ESLint/React Hooks warnings, and Playwright test execution reports."
    },
    # 5. node_backend_development_workflow.md
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
            ("Schema Design & Service Layer Setup", "Feature specification, database design rules.", "Define database migrations/models (Prisma/TypeORM/Mongoose), create DTOs, and outline service interface.", "Database migration scripts and TypeScript service interfaces.", "Database migration dry-run execution against local test database succeeds."),
            ("Controller & Business Logic Implementation", "Service interfaces, schema validation libraries (Zod/Joi).", "Write route handlers, express/fastify middleware, payload validation schemas, and business domain logic.", "Complete route module with controller, service, and validation logic.", "Unit tests for service functions and route handlers passing with high coverage."),
            ("Security & Middleware Hardening", "Route module, security baseline (Helmet, CORS, Rate-Limiter, JWT validator).", "Attach security middleware, sanitize parameters against SQLi/XSS, configure error handling middleware.", "Secured Node.js application module.", "Security audit script verifying header flags and unauthenticated route rejection."),
            ("Integration & Load Testing", "Running local/containerized Node service, Supertest / k6 load test scripts.", "Run HTTP integration tests with Supertest; perform stress testing with k6 to measure RPS and latency metrics.", "Integration test report and k6 performance report.", "p95 response latency < 200ms under target load, 0% unhandled promise rejections."),
            ("Containerization & Production Release", "Node codebase, multi-stage Dockerfile, production environment variables.", "Build lightweight Docker image (alpine/distroless), scan container vulnerability (Trivy), push image to registry.", "Verified Docker image artifact pushed to Container Registry.", "Trivy scan shows 0 HIGH/CRITICAL vulnerabilities.")
        ],
        "gates": [
            "Gate 1: DB migrations must be backward-compatible and tested on staging snapshot before deployment.",
            "Gate 2: Container image vulnerability scan must pass with 0 Critical/High issues prior to production release."
        ],
        "failures": [
            "Failure Mode 1: Node process memory leak under load -> Action: Profile process heap dump using clinic.js / Chrome DevTools, fix event listener / cache leaks.",
            "Failure Mode 2: Unhandled async promise rejection crashing process -> Action: Implement global exception / rejection handlers and audit async try/catch blocks."
        ],
        "artifact_standard": "Multi-stage Docker container, OpenAPI spec sync, clean TypeScript compilation, and 100% passing Supertest suite."
    }
]

print("Script template ready.")
