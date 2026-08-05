# Node Backend Development Workflow Specification

## 1. Purpose & Objective
Provide a rigorous process for engineering scalable, secure, and asynchronous backend microservices and APIs using Node.js.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Node.js runtime, database access (PostgreSQL/MongoDB), API design spec, environment configuration template.
- **Trigger Conditions**: Backend service task assignment.

## 3. Participating Agent Roles & Responsibilities
- **Backend Architect**: Defines microservice architecture, DB schemas, auth standards, and middleware stack.
- **Node Specialist**: Implements route controllers, service layer logic, ORM models, and async event handlers.
- **Security Auditor**: Validates input sanitization, JWT/OAuth flow security, and rate limiting.

## 4. Step-by-Step Execution Sequence

### Step 1: Schema Design & Service Layer Setup
- **Inputs**: Feature specification, database design rules.
- **Actions**: Define database migrations/models (Prisma/TypeORM/Mongoose), create DTOs, and outline service interface.
- **Outputs**: Database migration scripts and TypeScript service interfaces.
- **Verification**: Database migration dry-run execution against local test database succeeds.

### Step 2: Controller & Business Logic Implementation
- **Inputs**: Service interfaces, schema validation libraries (Zod/Joi).
- **Actions**: Write route handlers, express/fastify middleware, payload validation schemas, and business domain logic.
- **Outputs**: Complete route module with controller, service, and validation logic.
- **Verification**: Unit tests for service functions and route handlers passing with high coverage.

### Step 3: Security & Middleware Hardening
- **Inputs**: Route module, security baseline (Helmet, CORS, Rate-Limiter, JWT validator).
- **Actions**: Attach security middleware, sanitize parameters against SQLi/XSS, configure error handling middleware.
- **Outputs**: Secured Node.js application module.
- **Verification**: Security audit script verifying header flags and unauthenticated route rejection.

### Step 4: Integration & Load Testing
- **Inputs**: Running local/containerized Node service, Supertest / k6 load test scripts.
- **Actions**: Run HTTP integration tests with Supertest; perform stress testing with k6 to measure RPS and latency metrics.
- **Outputs**: Integration test report and k6 performance report.
- **Verification**: p95 response latency < 200ms under target load, 0% unhandled promise rejections.

### Step 5: Containerization & Production Release
- **Inputs**: Node codebase, multi-stage Dockerfile, production environment variables.
- **Actions**: Build lightweight Docker image (alpine/distroless), scan container vulnerability (Trivy), push image to registry.
- **Outputs**: Verified Docker image artifact pushed to Container Registry.
- **Verification**: Trivy scan shows 0 HIGH/CRITICAL vulnerabilities.

## 5. Decision Gates & Branching Rules
- Gate 1: DB migrations must be backward-compatible and tested on staging snapshot before deployment.
- Gate 2: Container image vulnerability scan must pass with 0 Critical/High issues prior to production release.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Node process memory leak under load -> Action: Profile process heap dump using clinic.js / Chrome DevTools, fix event listener / cache leaks.
- Failure Mode 2: Unhandled async promise rejection crashing process -> Action: Implement global exception / rejection handlers and audit async try/catch blocks.

## 7. Artifact Delivery & Output Standard
Multi-stage Docker container, OpenAPI spec sync, clean TypeScript compilation, and 100% passing Supertest suite.
