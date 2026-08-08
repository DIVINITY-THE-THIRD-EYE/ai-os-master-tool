# Code Quality Checklist (Gate 3 & Gate 4)

**Responsible Agent:** A06 (Worker Agent), A07 (Verification Agent)
**Gate:** Gate 3 (Self-Validation), Gate 4 (Verification Gate)

## General Code Standards
- [ ] Functions have single responsibility — **Blocking**
- [ ] Functions documented with purpose, parameters, and return value — **Blocking**
- [ ] No hardcoded values (secrets, URLs, config) — **Blocking**
- [ ] Error handling present on all external calls — **Blocking**
- [ ] Input validation implemented on all public interfaces — **Blocking**
- [ ] Linting passes with zero errors — **Blocking**
- [ ] No commented-out code without explanation — **Advisory**

## Testing
- [ ] Unit tests present for all business logic — **Blocking**
- [ ] Test coverage >= 80% — **Blocking**
- [ ] Tests are deterministic (no random failures) — **Blocking**
- [ ] Edge cases and negative cases covered — **Blocking**
- [ ] No external dependencies in unit tests (mocked) — **Blocking**
- [ ] Integration tests present for API and service boundaries — **Blocking**

## API Standards
- [ ] API follows RESTful or GraphQL conventions — **Blocking**
- [ ] All endpoints have documented request/response schemas — **Blocking**
- [ ] Errors return structured error objects with code, message, detail — **Blocking**
- [ ] Authentication and authorization applied to all endpoints — **Blocking**
- [ ] Rate limiting documented — **Blocking**

## Documentation
- [ ] README present with purpose, setup, and usage — **Blocking**
- [ ] All public functions have docstrings — **Blocking**
- [ ] Architecture decisions documented as ADRs where applicable — **Advisory**
- [ ] API documentation auto-generated or manually complete — **Blocking**
