import os

TARGET_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_04_workflow_library"
os.makedirs(TARGET_DIR, exist_ok=True)


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


# Complete list of 50 workflows
wf_list = [
    # 1
    (
        "software_development_workflow.md",
        "Software Development Workflow",
        "Provide a structured, end-to-end lifecycle for converting technical requirements into tested, verified, and deployable software components.",
        "Approved architecture spec, user stories with acceptance criteria, active git repository, baseline test suite.",
        "Creation or assignment of a feature branch / epic ticket in the project management system.",
        [
            (
                "Lead Architect",
                "Provides architectural guidance, validates component design, and reviews technical trade-offs.",
            ),
            ("Software Engineer", "Implements core feature code, writes unit tests, and creates pull requests."),
            (
                "QA Engineer",
                "Executes automated integration tests, validates edge cases, and verifies acceptance criteria.",
            ),
            ("Code Reviewer", "Conducts static code review, security analysis, and logic verification."),
        ],
        [
            (
                "Requirement Breakdown & Design Spec",
                "User story specification, existing codebase documentation, architectural guidelines.",
                "Analyze user story, map component touchpoints, outline class/interface structures, define unit test targets.",
                "Technical Design Specification (TDS) document and feature branch initialization.",
                "Lead Architect sign-off on design spec and branch naming compliance.",
            ),
            (
                "Test-Driven Implementation",
                "TDS document, unit testing framework, codebase mocks/fixtures.",
                "Write failing unit tests matching acceptance criteria; write feature code to pass unit tests; refactor.",
                "Implemented feature code and complete unit test suite.",
                "100% unit test pass rate with minimum 85% line coverage.",
            ),
            (
                "Integration & Static Code Analysis",
                "Feature code, integration test suite, linter/SAST configuration files.",
                "Execute static analysis tools (SonarQube/ESLint/PyLint); run integration test suite against local build.",
                "Static analysis report and integration test results.",
                "Zero critical linting/security findings and clean integration test run.",
            ),
            (
                "Peer Review & Refinement",
                "Pull Request diff, static analysis report, test execution logs.",
                "Peer reviewer inspects diff for code smells, security vulnerabilities, performance bottlenecks, and adherence to conventions.",
                "Pull Request comments, approval status, or change requests.",
                "Minimum 2 peer approvals and green CI status check.",
            ),
            (
                "Merge & Deployment Readiness",
                "Approved PR, target integration branch (main/develop).",
                "Perform squash-and-merge or rebase onto target branch; update issue tracker status.",
                "Merged commit in main branch and updated ticket state.",
                "Post-merge build pass notification on CI server.",
            ),
        ],
        [
            "Gate 1 (Design Gate): TDS must be approved by Lead Architect before any code is committed.",
            "Gate 2 (Quality Gate): CI pipeline must achieve >85% unit coverage and zero SAST critical warnings prior to PR review.",
            "Gate 3 (Merge Gate): Requires at least 2 explicit reviewer approvals and clean automated test suite.",
        ],
        [
            "Failure Mode 1: Static analysis detects high-severity security flaw -> Action: PR automatically blocked; task returned to Engineer for immediate patching.",
            "Failure Mode 2: Integration test failure due to API schema mismatch -> Action: Revert feature branch to pre-integration state, re-verify API specs.",
            "Failure Mode 3: Merge conflict on main branch -> Action: Software Engineer performs local rebase and re-runs test suite before force-updating PR.",
        ],
        "All feature branches must contain clean commit history, fully passing pytest/jest test suites, updated documentation in docs/ directory, and clear PR descriptions referencing ticket IDs.",
    ),
    # 2
    (
        "website_creation_workflow.md",
        "Website Creation Workflow",
        "Define the operational sequence for designing, developing, optimizing, and launching responsive, accessible, and SEO-optimized websites.",
        "Brand guidelines, copy assets, wireframe approvals, domain name registration, hosting target configuration.",
        "Kickoff of website project milestone by Product Lead.",
        [
            (
                "UI/UX Specialist",
                "Delivers wireframes, visual design specs, responsive layouts, and accessibility standards.",
            ),
            ("Frontend Developer", "Builds semantic HTML/CSS/JS or framework-based frontend (Next.js/Astro)."),
            ("Content Specialist", "Integrates copy, media assets, metadata, and schema markup."),
            (
                "QA Engineer",
                "Performs cross-browser, cross-device, accessibility (WCAG), and performance (Lighthouse) audits.",
            ),
        ],
        [
            (
                "Information Architecture & Wireframing",
                "Project brief, target audience personas, brand assets.",
                "Draft site map, user flows, and low-fidelity responsive wireframes for desktop and mobile viewports.",
                "Approved sitemap and Figma wireframes.",
                "Design review approval from UI/UX Specialist and Product Lead.",
            ),
            (
                "Component Development & Styling",
                "High-fidelity mockups, design tokens (colors, typography, spacing).",
                "Construct modular components, global layout grids, styling system, and interactive states.",
                "Component library codebase with Storybook/preview pages.",
                "Pixel-perfect visual audit against Figma specs across 3 breakpoint viewports.",
            ),
            (
                "Content Integration & SEO Optimization",
                "Final copy deck, imagery assets, target keywords.",
                "Inject content into templates, configure Open Graph tags, alt tags, canonical URLs, and JSON-LD structured data.",
                "Fully populated site pages with complete metadata.",
                "Zero missing alt attributes and validated JSON-LD schema via Google Structured Data Tool.",
            ),
            (
                "Performance & Accessibility Audit",
                "Staging URL, performance audit tools (Lighthouse, axe-core).",
                "Run Lighthouse performance benchmarks, optimize image sizes/formats (WebP/AVIF), audit WCAG 2.1 AA compliance.",
                "Audit report with Lighthouse score >= 90 across all categories.",
                "Lighthouse score >= 90 for Performance, Accessibility, Best Practices, and SEO.",
            ),
            (
                "Production Deployment & DNS Cutover",
                "Passed staging site, production domain settings, SSL certificate.",
                "Trigger production deployment on hosting platform (Vercel/Netlify/S3), update DNS records, verify SSL installation.",
                "Live website URL with HTTPS enabled.",
                "HTTP 200 responses across all key pages and valid SSL certificate check.",
            ),
        ],
        [
            "Gate 1: Wireframes and sitemap must be signed off before component development commences.",
            "Gate 2: Staging site must pass WCAG 2.1 AA and Lighthouse >= 90 benchmarks before DNS cutover is scheduled.",
        ],
        [
            "Failure Mode 1: Lighthouse performance score below 90 due to unoptimized images -> Action: Compress assets, implement lazy loading, re-run audit.",
            "Failure Mode 2: DNS propagation failure or SSL provisioning error -> Action: Roll back DNS CNAME/A record to staging fallback, debug hosting SSL logs.",
        ],
        "Production static assets hosted on CDN, clean Git repository with semantic commit messages, automated Lighthouse CI config, and complete SEO manifest.",
    ),
    # 3
    (
        "flutter_app_development_workflow.md",
        "Flutter App Development Workflow",
        "Standardize cross-platform mobile application development using Flutter, ensuring native performance, state management consistency, and automated app store artifact creation.",
        "Flutter SDK setup, Android SDK / Xcode toolchains, app design system, API specs.",
        "Mobile feature sprint initiation.",
        [
            (
                "Mobile Architect",
                "Defines Flutter architecture (Riverpod/BLoC), folder structure, and native platform integration standards.",
            ),
            ("Flutter Developer", "Implements Flutter UI widgets, state logic, and platform channels."),
            (
                "Mobile QA Specialist",
                "Executes integration testing on Android Emulators and iOS Simulators, checking device compatibility.",
            ),
        ],
        [
            (
                "State Management & Architecture Setup",
                "Feature requirements, Flutter project scaffold, API documentation.",
                "Define state models, repositories, and state management providers (e.g. Riverpod / BLoC) for the feature module.",
                "Architecture scaffold with mock repositories and data models.",
                "Unit tests verifying state transitions and model serialization/deserialization.",
            ),
            (
                "Widget Implementation & Responsive Layout",
                "Figma design specs, state providers.",
                "Build custom Flutter widgets, implement adaptive layouts for screens/tablets, bind widgets to state streams.",
                "Functional Flutter screens with reactive UI updates.",
                "Flutter Golden tests passing for key screen states across light/dark themes.",
            ),
            (
                "Native Platform Channel Integration",
                "Native API requirements (camera, bluetooth, secure storage).",
                "Write Kotlin (Android) and Swift (iOS) platform channel implementations or configure pubspec plugins.",
                "Platform channel bridge and native permission configurations (AndroidManifest.xml, Info.plist).",
                "Device testing verifying native capability execution without crashes.",
            ),
            (
                "Integration & Performance Trace Run",
                "Complete feature codebase, integration test scripts (flutter_test / integration_test).",
                "Execute integration tests across simulated devices; profile memory consumption and frame rendering rates (60/120 fps).",
                "Integration test report and performance profiling trace.",
                "Zero jank (no dropped frames during scroll tests) and 100% integration test pass rate.",
            ),
            (
                "Build Generation & Artifact Signing",
                "Passed codebase, release keystore / iOS provisioning profiles.",
                "Build release APK/AAB for Android and IPA for iOS using Fastlane / Flutter build commands.",
                "Signed release binaries (.aab, .ipa) stored in build outputs.",
                "Binary signature verification and successful upload to TestFlight / Google Play Internal Track.",
            ),
        ],
        [
            "Gate 1: State management architecture must pass unit test coverage check (>80%) before UI integration.",
            "Gate 2: Release builds must be signed and verified on physical test devices prior to store submission.",
        ],
        [
            "Failure Mode 1: iOS build failure due to provisioning profile expiration -> Action: Renew provisioning certificate in Apple Developer portal, re-run Fastlane sync.",
            "Failure Mode 2: Flutter widget layout overflow error -> Action: Refactor layout using Flexible/Expanded widgets, re-verify with golden tests.",
        ],
        "Signed AAB and IPA release packages, flutter analyzer report with 0 warnings, and clean integration test logs.",
    ),
    # 4
    (
        "react_app_development_workflow.md",
        "React App Development Workflow",
        "Govern the design, build, state management, testing, and bundling of modern React single-page or server-rendered web applications.",
        "Node.js environment, Vite/Next.js setup, component specs, backend API endpoints.",
        "Frontend feature sprint allocation.",
        [
            (
                "Frontend Lead",
                "Establishes React patterns, state management architecture (Zustand/Redux), and bundle optimization targets.",
            ),
            ("React Developer", "Builds React components, custom hooks, and route handlers."),
            ("UI Auditor", "Checks visual compliance, accessibility tree, and bundle size limits."),
        ],
        [
            (
                "Component & Hook Architecture",
                "Feature specification, API contract, state management guidelines.",
                "Design component breakdown, custom hooks for data fetching (TanStack Query/SWR), and client-side state schema.",
                "TypeScript definitions and custom hook skeletons.",
                "TypeScript compiler verification (`tsc --noEmit`) passing with zero errors.",
            ),
            (
                "Interactive Component Construction",
                "TypeScript interfaces, Tailwind CSS / Styled Components design tokens.",
                "Implement JSX/TSX components, apply responsive styles, manage local component state, handle loading/error states.",
                "Functional React components co-located with tests and styles.",
                "Visual check and unit tests (React Testing Library) verifying state rendering.",
            ),
            (
                "API & Global State Binding",
                "REST/GraphQL endpoints, mock server handlers (MSW).",
                "Connect custom hooks to live API endpoints, handle authentication headers, implement optimistic updates.",
                "End-to-end data-bound React views.",
                "Integration tests passing with MSW mock server and live staging server.",
            ),
            (
                "Bundle Optimization & Code Splitting",
                "Built React application assets, bundler analyzer (rollup-plugin-visualizer / webpack-bundle-analyzer).",
                "Implement route-based dynamic imports (`React.lazy`), optimize tree-shaking, audit vendor bundle size.",
                "Optimized production bundle with chunk splitting.",
                "Initial JS bundle size below 150KB gzipped.",
            ),
            (
                "E2E Testing & Staging Deploy",
                "Staging environment configuration, Playwright / Cypress test suites.",
                "Run full E2E user flow tests on staging build; publish deployment preview.",
                "E2E test run video/trace artifacts and staging URL.",
                "100% E2E test pass rate across Chrome, Firefox, and Safari viewports.",
            ),
        ],
        [
            "Gate 1: Strict TypeScript compilation (`strict: true`) must pass before merging code into develop branch.",
            "Gate 2: Initial bundle size budget check must pass before production deployment approval.",
        ],
        [
            "Failure Mode 1: React re-render loop causing performance degradation -> Action: Profile component via React DevTools, introduce `useMemo`/`useCallback` or state structure simplification.",
            "Failure Mode 2: Dynamic import chunk loading failure -> Action: Add Error Boundary wrapping lazy components, implement fallback retry logic.",
        ],
        "Production build dist directory, clean TypeScript build output, zero ESLint/React Hooks warnings, and Playwright test execution reports.",
    ),
    # 5
    (
        "node_backend_development_workflow.md",
        "Node Backend Development Workflow",
        "Provide a rigorous process for engineering scalable, secure, and asynchronous backend microservices and APIs using Node.js.",
        "Node.js runtime, database access (PostgreSQL/MongoDB), API design spec, environment configuration template.",
        "Backend service task assignment.",
        [
            (
                "Backend Architect",
                "Defines microservice architecture, DB schemas, auth standards, and middleware stack.",
            ),
            (
                "Node Specialist",
                "Implements route controllers, service layer logic, ORM models, and async event handlers.",
            ),
            ("Security Auditor", "Validates input sanitization, JWT/OAuth flow security, and rate limiting."),
        ],
        [
            (
                "Schema Design & Service Layer Setup",
                "Feature specification, database design rules.",
                "Define database migrations/models (Prisma/TypeORM/Mongoose), create DTOs, and outline service interface.",
                "Database migration scripts and TypeScript service interfaces.",
                "Database migration dry-run execution against local test database succeeds.",
            ),
            (
                "Controller & Business Logic Implementation",
                "Service interfaces, schema validation libraries (Zod/Joi).",
                "Write route handlers, express/fastify middleware, payload validation schemas, and business domain logic.",
                "Complete route module with controller, service, and validation logic.",
                "Unit tests for service functions and route handlers passing with high coverage.",
            ),
            (
                "Security & Middleware Hardening",
                "Route module, security baseline (Helmet, CORS, Rate-Limiter, JWT validator).",
                "Attach security middleware, sanitize parameters against SQLi/XSS, configure error handling middleware.",
                "Secured Node.js application module.",
                "Security audit script verifying header flags and unauthenticated route rejection.",
            ),
            (
                "Integration & Load Testing",
                "Running local/containerized Node service, Supertest / k6 load test scripts.",
                "Run HTTP integration tests with Supertest; perform stress testing with k6 to measure RPS and latency metrics.",
                "Integration test report and k6 performance report.",
                "p95 response latency < 200ms under target load, 0% unhandled promise rejections.",
            ),
            (
                "Containerization & Production Release",
                "Node codebase, multi-stage Dockerfile, production environment variables.",
                "Build lightweight Docker image (alpine/distroless), scan container vulnerability (Trivy), push image to registry.",
                "Verified Docker image artifact pushed to Container Registry.",
                "Trivy scan shows 0 HIGH/CRITICAL vulnerabilities.",
            ),
        ],
        [
            "Gate 1: DB migrations must be backward-compatible and tested on staging snapshot before deployment.",
            "Gate 2: Container image vulnerability scan must pass with 0 Critical/High issues prior to production release.",
        ],
        [
            "Failure Mode 1: Node process memory leak under load -> Action: Profile process heap dump using clinic.js / Chrome DevTools, fix event listener / cache leaks.",
            "Failure Mode 2: Unhandled async promise rejection crashing process -> Action: Implement global exception / rejection handlers and audit async try/catch blocks.",
        ],
        "Multi-stage Docker container, OpenAPI spec sync, clean TypeScript compilation, and 100% passing Supertest suite.",
    ),
    # 6
    (
        "api_development_workflow.md",
        "API Development Workflow",
        "Standardize RESTful and GraphQL API specification, implementation, contract testing, and lifecycle management.",
        "Business domain requirements, authentication provider specs, API gateway guidelines.",
        "New API endpoint or version release request.",
        [
            ("API Architect", "Designs OpenAPI / AsyncAPI specifications, payload contracts, and error structures."),
            ("Backend Developer", "Implements handlers, data mappers, and middleware logic."),
            ("Integration QA Lead", "Conducts contract testing (Pact), schema validation, and mock generation."),
        ],
        [
            (
                "API Specification & Contract Design",
                "Endpoint functional requirements.",
                "Draft OpenAPI 3.1 YAML spec including paths, query parameters, request bodies, response codes, and schemas.",
                "Validated OpenAPI YAML specification document.",
                "OpenAPI linter (Spectral) passes with zero errors.",
            ),
            (
                "Mock Server & SDK Generation",
                "OpenAPI spec file.",
                "Spin up Prism mock server for frontend parallel development and auto-generate client SDKs via OpenAPI Generator.",
                "Live mock server URL and generated SDK packages.",
                "Frontend developer contract confirmation on mock responses.",
            ),
            (
                "Endpoint Logic Implementation",
                "OpenAPI spec, database connections, service controllers.",
                "Develop controller handlers matching spec paths, bind DTO validations, implement business logic.",
                "Executable API route code co-located with unit tests.",
                "Unit tests covering 200 OK, 400 Bad Request, 401 Unauthorized, and 500 Internal Error codes.",
            ),
            (
                "Contract Testing & Security Validation",
                "Live service build, Prism / Pact test harness, OWASP ZAP scanner.",
                "Execute Pact contract tests verifying request/response payload adherence; run OWASP ZAP API scan.",
                "Contract verification report and security audit findings.",
                "100% Pact contract alignment and zero high-severity security findings.",
            ),
            (
                "API Gateway Routing & Versioning",
                "Verified service build, API Gateway configuration (Kong/Apigee/AWS API GW).",
                "Configure gateway route matching, CORS policy, rate limiting policies, and TLS termination.",
                "Deployed API gateway configuration.",
                "HTTP 200 response verification from external gateway endpoint URL.",
            ),
        ],
        [
            "Gate 1: Spectral linter approval of OpenAPI spec before implementation code is written.",
            "Gate 2: Pact contract test suite must pass before gateway deployment.",
        ],
        [
            "Failure Mode 1: Breaking API change detected in contract test -> Action: Increment major API version path (/v2/), retain legacy route support.",
            "Failure Mode 2: Rate limiter blocking legitimate test traffic -> Action: Adjust burst capacity and rate limit thresholds in Gateway config for test tenants.",
        ],
        "OpenAPI 3.1 specification, published SDK binaries, Pact contract verification logs, and active API gateway route configurations.",
    ),
    # 7
    (
        "ai_research_workflow.md",
        "AI Research Workflow",
        "Guide scientific exploration, literature synthesis, hypothesis formulation, model prototyping, and empirical evaluation.",
        "Research problem statement, compute resource allocation (GPU cluster), benchmark datasets.",
        "Initiation of AI research initiative or algorithm optimization grant.",
        [
            ("AI Research Lead", "Formulates hypotheses, defines metrics, and oversees experimental methodology."),
            ("Data Scientist", "Preprocesses datasets, runs statistical analyses, and engineers features."),
            (
                "ML Research Engineer",
                "Implements model architectures in PyTorch/JAX, trains baseline models, and logs experiments.",
            ),
        ],
        [
            (
                "Literature Review & State of the Art (SOTA) Analysis",
                "Research topic query, academic databases (ArXiv, PapersWithCode).",
                "Aggregate SOTA publications, compare architectural approaches, identify research gaps.",
                "Literature Review & Benchmark Survey synthesis document.",
                "AI Research Lead approval of research hypothesis.",
            ),
            (
                "Experimental Setup & Dataset Curation",
                "Raw datasets, compute environment (PyTorch, CUDA, WandB).",
                "Clean raw data, create reproducible train/val/test splits, verify label distribution, configure dataset loaders.",
                "Standardized dataset splits and data pipeline scripts.",
                "Dataset validation check confirming no data leakage across splits.",
            ),
            (
                "Model Architecture Prototyping",
                "Dataset loaders, model design hypotheses.",
                "Write modular PyTorch/JAX model components, construct loss functions, write training loops with mixed-precision support.",
                "Model codebase and modular component unit tests.",
                "Forward-pass sanity check with dummy input tensor passing without dimension mismatches.",
            ),
            (
                "Experimental Execution & Hyperparameter Tracking",
                "Model codebase, WandB / MLflow tracking, GPU cluster.",
                "Execute training sweeps across hyperparameter grids; track loss curves, accuracy, latency, and memory utilization.",
                "Experiment logs, checkpoint weights, and WandB runs dashboard.",
                "Validation metric convergence without gradient explosion or vanishing.",
            ),
            (
                "Results Synthesis & Paper Drafting",
                "WandB experiment runs, evaluation metrics, visual charts.",
                "Compile ablation study tables, draft methodology section, write comparative evaluation vs SOTA baselines.",
                "Comprehensive Research Paper draft (LaTeX format) and model weights repository.",
                "Internal peer review approval from AI Research Lead.",
            ),
        ],
        [
            "Gate 1: Dataset split verification must confirm zero data contamination before training run.",
            "Gate 2: Model ablation study must demonstrate statistically significant improvement over SOTA baseline (p < 0.05).",
        ],
        [
            "Failure Mode 1: Model gradient explosion during deep training -> Action: Implement gradient clipping, adjust learning rate scheduler, inspect norm distributions.",
            "Failure Mode 2: Overfitting on validation set -> Action: Add data augmentation, increase regularization (weight decay/dropout), re-run sweep.",
        ],
        "Compiled LaTeX research paper PDF, WandB experiment run logs, verified PyTorch model weights (.pt), and reproducible benchmark script.",
    ),
    # 8
    (
        "mechanical_design_workflow.md",
        "Mechanical Design Workflow",
        "Structure the physical engineering process from CAD drafting, GD&T tolerance modeling, finite element analysis (FEA), to prototype release.",
        "Mechanical requirements spec, material constraints, target assembly limits, CAD software suite (SolidWorks/CATIA).",
        "Engineering change request (ECR) or new hardware project kickoff.",
        [
            ("Mechanical Engineer", "Creates CAD models, assemblies, GD&T drawings, and material selection specs."),
            ("FEA Specialist", "Performs structural, thermal, and stress simulation analyses."),
            ("Drafting Lead", "Audits mechanical drawings against ISO/ASME Y14.5 standards."),
        ],
        [
            (
                "3D Solid Modeling & Parameterization",
                "Product requirements document, envelope dimensions, interference parameters.",
                "Create 3D parametric CAD parts, assemble component trees, define mate relationships, apply material properties.",
                "Parametric CAD model files (.SLDPRT, .SLDASM / STEP).",
                "Interference and clearance check passing with 0 overlapping volumes.",
            ),
            (
                "Structural & Stress Analysis (FEA)",
                "3D assembly model, load boundary conditions, yield strength constraints.",
                "Apply mesh constraints, define load cases (static force, dynamic vibration, thermal stress), run FEA solver.",
                "FEA simulation report detailing Von Mises stress distribution and Factor of Safety (FoS).",
                "Minimum FoS >= 2.0 across all critical load cases.",
            ),
            (
                "GD&T Drawing & Tolerance Stack-Up",
                "3D assembly model, FEA verification.",
                "Generate 2D drafting drawings, apply GD&T datums and tolerances (ISO 2768 / ASME Y14.5), perform tolerance stack-up analysis.",
                "Dimensioned 2D engineering drawings (PDF / DWG).",
                "Tolerance stack-up verification showing zero assembly binding at MMC (Maximum Material Condition).",
            ),
            (
                "Design for Manufacturability (DFM) Review",
                "CAD models, 2D drawings, vendor tooling limits.",
                "Review draft angles, wall thicknesses, bend radii, and machining access with manufacturing suppliers.",
                "DFM review report and updated CAD model.",
                "Supplier DFM sign-off with 0 unmanufacturable features.",
            ),
            (
                "BOM Generation & Prototype Release",
                "Final CAD package, verified drawing set.",
                "Generate Bill of Materials (BOM) with part numbers, quantities, material callouts, and vendor sources; release to ERP.",
                "Released Engineering BOM (eBOM) and prototype procurement package.",
                "Engineering Change Order (ECO) approval from Mechanical Engineer.",
            ),
        ],
        [
            "Gate 1: FEA simulation must confirm Factor of Safety >= 2.0 before drawing creation.",
            "Gate 2: Supplier DFM review approval required before releasing eBOM to procurement.",
        ],
        [
            "Failure Mode 1: High stress concentration in FEA simulation -> Action: Increase fillet radii, add reinforcing ribs, re-run FEA solver.",
            "Failure Mode 2: Interference detected during tolerance stack-up -> Action: Tighten feature tolerances or modify nominal dimensions.",
        ],
        "Approved 3D STEP models, ASME Y14.5 compliant 2D PDF drawings, FEA simulation report, and released eBOM package.",
    ),
    # 9
    (
        "manufacturing_process_workflow.md",
        "Manufacturing Process Workflow",
        "Govern production line setup, tool tooling validation, CNC path programming, quality control sampling, and assembly line balancing.",
        "Released eBOM, 2D drawings, raw material inventory, production machinery specifications.",
        "Production release order execution.",
        [
            ("Process Engineer", "Designs manufacturing operations, routing sheets, and assembly instructions."),
            (
                "Manufacturing Specialist",
                "Programs CNC/robotic equipment, setups tooling fixtures, and manages pilot runs.",
            ),
            (
                "Quality Control Auditor",
                "Conducts CMM inspection, Statistical Process Control (SPC) monitoring, and first-article inspection (FAI).",
            ),
        ],
        [
            (
                "Process Routing & Operation Sheet Definition",
                "Released eBOM, engineering drawings.",
                "Define step-by-step manufacturing routing, select machine centers (CNC, lathe, injection molding), calculate cycle times.",
                "Manufacturing Process Plan (MPP) and Operation Sheets.",
                "Process Engineer approval of operational routing sequence.",
            ),
            (
                "Tooling Design & CNC Programming",
                "CAD models, MPP operation specs, CAM software (Mastercam/Siemens NX).",
                "Design custom fixtures and jigs, generate CNC toolpaths, run CAM simulation to detect collisions.",
                "CAM files, G-code programs, and physical tooling fixtures.",
                "CAM simulation verification with 0 tool collision events.",
            ),
            (
                "Pilot Run & First Article Inspection (FAI)",
                "Tooling fixtures, CNC G-code, raw material stock.",
                "Execute pilot production run of 10 units, inspect dimensions using CMM (Coordinate Measuring Machine).",
                "First Article Inspection Report (FAIR) according to AS9102 standard.",
                "100% dimensional compliance on all critical-to-quality (CTQ) drawing features.",
            ),
            (
                "Statistical Process Control (SPC) Setup",
                "CMM measurement data, production line sensors.",
                "Establish control charts (X-bar, R-charts), define control limits, measure process capability index (Cpk).",
                "SPC dashboard and process capability report.",
                "Cpk index >= 1.33 across all CTQ parameters.",
            ),
            (
                "Mass Production Sign-Off",
                "Passed FAIR, SPC capability report, standard work instructions.",
                "Publish standard operating procedures (SOPs) on shop floor terminals; authorize full-scale production run.",
                "Production Authorization Certificate and live MES routing.",
                "Quality Control Auditor formal sign-off.",
            ),
        ],
        [
            "Gate 1: CAM simulation must confirm zero collision prior to loading G-code onto CNC machines.",
            "Gate 2: First Article Inspection Report (FAIR) must achieve 100% CTQ feature pass rate.",
        ],
        [
            "Failure Mode 1: Tool wear causing dimensional drift in pilot run -> Action: Adjust CNC tool offset, update tool replacement cycle in MPP.",
            "Failure Mode 2: Process capability Cpk < 1.33 -> Action: Perform gage R&R study, recalibrate machine center tolerances.",
        ],
        "AS9102 FAIR documentation, verified CNC G-code programs, SPC process capability reports, and released shop floor SOPs.",
    ),
    # 10
    (
        "construction_project_workflow.md",
        "Construction Project Workflow",
        "Orchestrate architectural blueprint verification, site preparation, structural execution, safety compliance, and commissioning.",
        "Architectural drawings, civil engineering specs, environmental permits, structural calculations.",
        "Issuance of municipal building permit and site handover.",
        [
            (
                "Construction Manager",
                "Oversees site logistics, contractor scheduling, budget tracking, and subcontractor coordination.",
            ),
            ("Civil Engineer", "Verifies structural integrity, foundation soil tests, and concrete pour specs."),
            ("Safety Auditor", "Conducts OSHA safety compliance inspections and risk hazard assessments."),
        ],
        [
            (
                "Blueprint Audit & BIM Coordination",
                "Architectural/structural CAD/BIM models (Revit), municipal permits.",
                "Run Building Information Modeling (BIM) clash detection between structural, MEP (mechanical, electrical, plumbing) systems.",
                "Clash Detection Report and coordinated BIM master model.",
                "BIM Coordinator sign-off with 0 hard structural clashes.",
            ),
            (
                "Site Preparation & Excavation",
                "Site survey drawings, geotechnical soil report, heavy equipment schedule.",
                "Execute site grading, soil compaction testing, utility line layout, and foundation excavation.",
                "Soil compaction test results and survey verification log.",
                "Geotechnical engineer validation of soil bearing capacity >= target kPa.",
            ),
            (
                "Structural Framing & Concrete Pour",
                "Structural drawings, rebar schedules, concrete batch mix specs.",
                "Form foundation footings, place rebar cages, conduct slump test, perform concrete pour, monitor curing strength.",
                "Concrete cylinder break test reports (7-day and 28-day).",
                "28-day break test confirming compressive strength meets specified PSI/MPa.",
            ),
            (
                "MEP Installation & Enclosure",
                "MEP drawings, framing inspection sign-off.",
                "Install framing studs, exterior cladding, roofing, electrical wiring, plumbing runs, and HVAC ductwork.",
                "Rough-in inspection report from municipal inspector.",
                "Passed municipal rough-in inspections for electrical, plumbing, and framing.",
            ),
            (
                "Commissioning & Handover",
                "As-built drawings, punch list, HVAC balancing reports.",
                "Perform HVAC balancing, fire alarm system testing, resolve punch list items, conduct final walkthrough.",
                "Certificate of Occupancy (CO) and final handover binder.",
                "Issuance of official Certificate of Occupancy by municipal authority.",
            ),
        ],
        [
            "Gate 1: BIM clash detection must resolve all MEP vs structural interferences before site excavation.",
            "Gate 2: Concrete pour requires passed rebar inspection and batch slump test prior to delivery.",
        ],
        [
            "Failure Mode 1: Soil bearing capacity below spec during excavation -> Action: Perform soil stabilization (grouting/deep piers), re-test bearing capacity.",
            "Failure Mode 2: Structural framing inspection failure -> Action: Issue Subcontractor Corrective Action Notice, re-inspect framing within 48 hours.",
        ],
        "Coordinated BIM model, municipal inspection sign-offs, 28-day concrete strength certificates, and final Certificate of Occupancy.",
    ),
]

# Write initial batch 1-10
for item in wf_list:
    write_wf(*item)

print("Batch 1 (1-10) created successfully.")
