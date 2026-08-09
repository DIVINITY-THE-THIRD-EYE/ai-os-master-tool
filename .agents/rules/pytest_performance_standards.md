---
description: Mandatory performance flags and conventions for running pytest suites in this repository.
globs: ["tests/**/*", "validate_repository.py"]
alwaysApply: true
---

# Pytest Performance Standards & Execution Guidelines

When running tests in this repository, follow these standards to maximize speed and developer feedback loops:

1. **Parallel Execution (`pytest-xdist`)**:
   - Use `pytest -n auto` for running full or large test suites across available CPU cores.

2. **Targeted Subsets**:
   - During active development and incremental changes, execute targeted test subfolders (e.g. `python -m pytest tests/enforcement/`) rather than running the full test suite every time.

3. **In-Memory Persistence**:
   - Utilize SQLite `:memory:` mode for routine unit tests to eliminate disk I/O latency wherever physical persistence chaos testing is not explicitly required.

4. **Fail-Fast & Cache Flags**:
   - Use `-x` (exit on first failure) or `--lf` (run only last failed tests) during active debugging for rapid feedback loops.
