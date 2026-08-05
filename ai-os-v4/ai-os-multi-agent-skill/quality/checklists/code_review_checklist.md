# Code Review Checklist
**Document ID:** CHK-QUAL-001  
**Version:** 4.0.0  
**Package:** `ai-os-multi-agent-skill`  
**Target Role:** A04 Lead Engineer / Peer Reviewer  
**Scope:** All pull requests, code modifications, and subagent outputs prior to merge  

---

## 1. Metadata & Control Header

| Attribute | Value |
|---|---|
| **Checklist ID** | CHK-QUAL-001 |
| **Enforcement Gate** | GATE-02 (Static Analysis & Lint Gate) |
| **Required Sign-Off** | Peer Reviewer (A04) / Quality Authority (A05) |
| **Target Repository** | `ai-os-v4` |
| **Review Standard** | PEP 8, Clean Code Principles, AI OS v4 Coding Standards |

---

## 2. Pre-Review Prerequisites

Before beginning code review, ensure the following prerequisite automated checks have passed:

- [ ] **Automated Syntax Check**: Target file parses cleanly with zero AST or syntax errors.
- [ ] **Automated Linter Run**: Automated linter (`MOD-LINT-02`) reports zero critical or major style violations.
- [ ] **Unit Test Execution**: All existing unit tests pass without failure or skipped tests.
- [ ] **Diff Scope Verification**: The PR/commit contains only changes relevant to the single task/issue (no unrelated refactoring or "while-I'm-here" edits).

---

## 3. Detailed Review Categories & Verification Criteria

### 3.1 Functional Correctness & Requirement Alignment
- [ ] **Requirement Traceability**: Code directly fulfills the acceptance criteria specified in the issue/task definition.
- [ ] **Edge Case Handling**: Boundary conditions (empty input, null values, maximum numbers, zero lengths, concurrent calls) are handled gracefully.
- [ ] **State Machine Invariants**: Component state transitions maintain defined invariants and cannot enter invalid or unreachable states.
- [ ] **Data Type Safety**: Inputs and outputs conform to expected types; type annotations are complete and valid.

### 3.2 Code Quality, Maintainability & Clean Code
- [ ] **Naming Conventions**: Variables, functions, classes, and constants follow clear, descriptive, standard naming patterns.
- [ ] **Single Responsibility Principle (SRP)**: Modules, classes, and functions have a single, well-defined responsibility.
- [ ] **Complexity Capping**: Function cyclomatic complexity does not exceed 10. Complex functions are decomposed into focused helpers.
- [ ] **No Dead Code / Commented-Out Code**: No unused variables, uncalled functions, or commented-out legacy code blocks exist.
- [ ] **DRY (Don't Repeat Yourself)**: Code avoids duplication; common logic is extracted into shared utilities or modules.

### 3.3 Error Handling, Logging & Diagnostics
- [ ] **Explicit Exception Handling**: Exceptions are caught specifically; naked `except:` or `catch (Exception e)` blocks are avoided unless re-raising.
- [ ] **Structured Logging**: Log entries include context (timestamp, component, request/task ID, severity level).
- [ ] **No Sensitive Data Logging**: Passwords, API tokens, JWTs, and PII are strictly excluded from log outputs.
- [ ] **Error Propagation**: Failures return informative, actionable error responses up the call stack without crashing background runners.

### 3.4 Security & Input Sanitization
- [ ] **Input Validation**: All incoming external inputs (API payloads, query params, file paths) are sanitized and validated against schemas.
- [ ] **Resource Leak Protection**: File handlers, network sockets, and database connections are wrapped in context managers (`with` statements) or explicit try-finally blocks.
- [ ] **SQL / Command Injection Prevention**: Parameterized queries or ORM calls are used exclusively; raw string concatenations for SQL/shell execution are strictly prohibited.

### 3.5 Performance & Resource Optimization
- [ ] **Algorithmic Efficiency**: Time and space complexity are optimal for expected input scales (no $O(N^2)$ loops over large datasets where $O(N)$ or $O(N \log N)$ is possible).
- [ ] **Lazy Loading & Caching**: Expensive evaluations or repetitive disk/network I/O operations utilize appropriate caching or lazy evaluation strategies.
- [ ] **Memory Management**: Collections and buffers do not grow unbounded; stream processing is used for large payloads.

### 3.6 Test Quality & Coverage
- [ ] **Comprehensive Test Coverage**: New logic is covered by unit tests matching or exceeding the project line coverage threshold (min 85%).
- [ ] **Meaningful Assertions**: Tests check behavior and state outcomes rather than mock implementation details.
- [ ] **Deterministic Execution**: Tests execute reliably without depending on system time, external network availability, or order of execution.

---

## 4. Response Guidance & Escalation Matrix

| Observation | Impact Level | Action Required | Escalation Target |
|---|---|---|---|
| Critical security bug / secret leak | **SEV-1 (Blocker)** | Reject PR immediately; revoke credentials if secret leaked | Security Authority (A06) |
| Functional flaw / broken test | **SEV-2 (High)** | Request changes; block merge until resolved | Peer Author / Worker |
| Architectural layer violation | **SEV-2 (High)** | Request redesign to adhere to layer boundaries | Architect Authority (A03) |
| Minor style / naming suggestion | **SEV-3 (Low)** | Note in review comment; optional for immediate fix | Peer Author |

---

## 5. Verification Sign-Off Protocol

Reviewers must record sign-off in the PR/task metadata before merging:

```markdown
### Code Review Sign-off
- **Reviewer**: [Name / Agent ID]
- **Date**: YYYY-MM-DD
- **Status**: APPROVED / CHANGES_REQUESTED
- **Checklist Version**: CHK-QUAL-001
- **Comments/Notes**: All verification criteria satisfied without exception.
```
