# API Development Workflow Specification

## 1. Purpose & Objective
Standardize RESTful and GraphQL API specification, implementation, contract testing, and lifecycle management.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Business domain requirements, authentication provider specs, API gateway guidelines.
- **Trigger Conditions**: New API endpoint or version release request.

## 3. Participating Agent Roles & Responsibilities
- **API Architect**: Designs OpenAPI / AsyncAPI specifications, payload contracts, and error structures.
- **Backend Developer**: Implements handlers, data mappers, and middleware logic.
- **Integration QA Lead**: Conducts contract testing (Pact), schema validation, and mock generation.

## 4. Step-by-Step Execution Sequence

### Step 1: API Specification & Contract Design
- **Inputs**: Endpoint functional requirements.
- **Actions**: Draft OpenAPI 3.1 YAML spec including paths, query parameters, request bodies, response codes, and schemas.
- **Outputs**: Validated OpenAPI YAML specification document.
- **Verification**: OpenAPI linter (Spectral) passes with zero errors.

### Step 2: Mock Server & SDK Generation
- **Inputs**: OpenAPI spec file.
- **Actions**: Spin up Prism mock server for frontend parallel development and auto-generate client SDKs via OpenAPI Generator.
- **Outputs**: Live mock server URL and generated SDK packages.
- **Verification**: Frontend developer contract confirmation on mock responses.

### Step 3: Endpoint Logic Implementation
- **Inputs**: OpenAPI spec, database connections, service controllers.
- **Actions**: Develop controller handlers matching spec paths, bind DTO validations, implement business logic.
- **Outputs**: Executable API route code co-located with unit tests.
- **Verification**: Unit tests covering 200 OK, 400 Bad Request, 401 Unauthorized, and 500 Internal Error codes.

### Step 4: Contract Testing & Security Validation
- **Inputs**: Live service build, Prism / Pact test harness, OWASP ZAP scanner.
- **Actions**: Execute Pact contract tests verifying request/response payload adherence; run OWASP ZAP API scan.
- **Outputs**: Contract verification report and security audit findings.
- **Verification**: 100% Pact contract alignment and zero high-severity security findings.

### Step 5: API Gateway Routing & Versioning
- **Inputs**: Verified service build, API Gateway configuration (Kong/Apigee/AWS API GW).
- **Actions**: Configure gateway route matching, CORS policy, rate limiting policies, and TLS termination.
- **Outputs**: Deployed API gateway configuration.
- **Verification**: HTTP 200 response verification from external gateway endpoint URL.

## 5. Decision Gates & Branching Rules
- Gate 1: Spectral linter approval of OpenAPI spec before implementation code is written.
- Gate 2: Pact contract test suite must pass before gateway deployment.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Breaking API change detected in contract test -> Action: Increment major API version path (/v2/), retain legacy route support.
- Failure Mode 2: Rate limiter blocking legitimate test traffic -> Action: Adjust burst capacity and rate limit thresholds in Gateway config for test tenants.

## 7. Artifact Delivery & Output Standard
OpenAPI 3.1 specification, published SDK binaries, Pact contract verification logs, and active API gateway route configurations.
