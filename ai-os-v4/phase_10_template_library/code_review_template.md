# Code Review Checklist & Assessment: PR #{{PR_NUMBER}}

> **Document Type**: Code Review Checklist  
> **Pull Request**: `#{{PR_NUMBER}} - {{PR_TITLE}}`  
> **Author**: {{PR_AUTHOR}}  
> **Reviewer(s)**: {{PR_REVIEWERS}}  
> **Target Branch**: `{{TARGET_BRANCH}}`  
> **Date**: {{REVIEW_DATE}}  

---

## 1. Automated Checks Status

- [ ] CI Pipeline Passed: {{CI_STATUS}}
- [ ] Linter & Formatter Clean: {{LINTER_STATUS}}
- [ ] Unit Test Coverage Threshold Met (>= 80%): {{TEST_COVERAGE}}%
- [ ] SAST Code Security Scan Passed (Zero Critical/High): {{SECURITY_SCAN_STATUS}}

---

## 2. Review Quality Checklist

### 2.1 Functional Correctness & Logic
- [ ] Code accurately satisfies the requirements defined in task ticket `#{{TICKET_ID}}`.
- [ ] Edge cases handled gracefully (e.g., null pointers, empty arrays, timeout errors).
- [ ] No unhandled exceptions or potential thread race conditions.

### 2.2 Security & Data Validation
- [ ] Input data sanitized and validated before processing (SQL injection, XSS prevention).
- [ ] No sensitive credentials, API keys, or personal tokens committed in code.
- [ ] Authentication and authorization checks properly applied on new endpoints.

### 2.3 Maintainability & Code Quality
- [ ] Variable and function names are clean, intuitive, and self-documenting.
- [ ] No duplicate code blocks or unnecessary complexity (DRY principle).
- [ ] Complex algorithms accompanied by concise internal inline comments.

---

## 3. Detailed Review Feedback & File Comments

| File Path | Line Number(s) | Comment / Required Modification | Severity | Status |
| :--- | :--- | :--- | :--- | :--- |
| `src/{{FILE_PATH_1}}` | L42-L48 | Move SQL query into repository layer to adhere to separation of concerns | Blocking | Open |
| `src/{{FILE_PATH_2}}` | L105 | Add explicit timeout to external HTTP client request | Non-Blocking | Addressed |

---

## 4. Final Review Decision

- [ ] **Approve**: Code is clean, tested, and ready for merge.
- [ ] **Request Changes**: Blocking issues identified above must be addressed.
- [ ] **Comment**: Feedback provided without blocking merge.
