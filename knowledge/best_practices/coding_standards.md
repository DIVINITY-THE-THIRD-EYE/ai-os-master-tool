# Coding Standards

## 16.1 General Standards
1. Functions must have a single responsibility
2. Functions must be documented with purpose, parameters, and return values
3. No hardcoded values: secrets, URLs, or environment-specific config
4. Dependencies declared and version-pinned
5. No commented-out code without explanation
6. All variables named clearly (no single-letter variables outside loop indices)
7. Maximum function length: 50 lines; decompose if longer
8. Cyclomatic complexity max: 10 per function
9. No global mutable state without explicit justification
10. Side effects must be minimized and documented
11. Pure functions preferred over stateful functions where practical
12. All file handles, connections, and resources must be properly closed

## 16.2 Error Handling
1. All external calls must have explicit error handling
2. Errors must propagate with context, not silently swallowed
3. Custom error types must include: error code, message, severity, and context
4. Retry logic must use exponential backoff with jitter
5. Timeout must be set on all external calls
6. Circuit breaker pattern required for high-frequency external calls
7. All uncaught exceptions must be logged before re-raising
8. User-facing error messages must not expose internal implementation details

## 16.3 Testing
1. Unit tests required for all business logic functions
2. Test coverage >= 80%
3. Tests must be deterministic — no random failures
4. Edge cases and negative cases must be covered
5. No external dependencies in unit tests (use mocks/stubs)
6. Integration tests required for all API and service boundaries
7. Test names must clearly describe the scenario being tested
8. Performance tests required for critical path operations
9. Security tests required for authentication and authorization logic

## 16.4 Logging
1. All external calls must log: request, response, duration, status
2. Log levels: DEBUG (dev only), INFO (production flow), WARNING (recoverable issue), ERROR (failure), CRITICAL (system failure)
3. Logs must be structured (JSON)
4. Logs must not contain secrets or PII
5. Trace ID must be included in all log entries for correlation
6. Log retention configured per data classification policy

## 16.5 API Standards
1. RESTful conventions followed (or GraphQL conventions where applicable)
2. All endpoints documented with request/response schemas
3. Errors return structured error objects: {code, message, detail, trace_id}
4. Authentication applied to all endpoints
5. Rate limiting defined and enforced
6. API versioning required (URL or header-based)
7. Input validation applied on all request fields
8. Output sanitized before returning to client

## 16.6 Backend Standards
1. Database queries parameterized (no string concatenation)
2. Transactions used for multi-step operations
3. Database connection pooling configured
4. Indexes defined for all frequently queried fields
5. Schema migrations versioned and reversible
6. No direct production database access from agent code
7. Repository pattern used for all data access
8. Data access layer separated from business logic

## 16.7 Frontend Standards
1. Components have single responsibility
2. State management follows approved pattern (Redux, Zustand, etc.)
3. No business logic in UI components
4. Accessibility: WCAG 2.1 AA minimum
5. Performance budget enforced: LCP < 2.5s, FID < 100ms, CLS < 0.1
6. Responsive design required for all user-facing surfaces
7. Error boundaries implemented
8. Loading and empty states handled explicitly

## 16.8 AI-Specific Standards
1. Prompts versioned and stored in prompt library
2. Prompts evaluated before production use
3. Model selection documented with rationale
4. Output validation required before consuming model output
5. Hallucination risk documented for each prompt
6. Safety guardrails enforced for all user-facing AI outputs
7. Token budgets enforced per call
8. Fallback behavior defined when model is unavailable

## 16.9 Documentation Standards
1. README present with: purpose, setup, usage, examples
2. All public interfaces documented with input/output/limitations
3. Architecture decisions documented as ADRs
4. API documentation complete and current
5. Runbooks present for all operational procedures
6. Changelog maintained with semantic versioning
7. Diagrams use standard notation (C4, sequence, etc.)
