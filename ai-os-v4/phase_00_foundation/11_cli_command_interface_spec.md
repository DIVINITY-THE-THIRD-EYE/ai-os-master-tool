---
title: CLI Command Interface & Tooling Specification (`agy`)
document_id: SPEC-P00-CLI-011
phase: phase_00_foundation
version: 1.0.0
status: APPROVED
owner: Developer Tooling Working Group
last_updated: 2026-08-05
---

# CLI Command Interface & Tooling Specification (`agy`)

## Executive Summary
This document specifies the interface contracts, command taxonomy, argument parsing rules, exit codes, and output formatting modes for the primary AI OS v4 Command-Line Interface (`agy`).

---

## 1. Command Syntax & Standard Flags

```bash
agy <subsystem> <command> [arguments] [flags]
```

### Global Standard Flags Matrix
- `--config, -c <path>`: Override runtime configuration file path.
- `--output, -o <format>`: Format mode: `text` (default), `json`, `yaml`, `table`.
- `--verbose, -v`: Enable detailed debug output.
- `--quiet, -q`: Suppress non-error console output.
- `--help, -h`: Display context-sensitive help page.

---

## 2. Command Subsystem Hierarchy

```text
agy
├── kernel        --> Manage runtime node startup, status, shutdown
│   ├── start     --config=<path> [--daemon]
│   ├── stop      [--force]
│   └── status    [--json]
├── agent         --> Deploy, list, inspect, and invoke agents
│   ├── run       --agent=<name> --input=<string|file>
│   ├── list      [--status=active]
│   └── inspect   <agent_id>
├── workflow      --> Execute and monitor workflow DAGs
│   ├── run       --file=<workflow.json> [--var key=value]
│   ├── status    <workflow_execution_id>
│   └── validate  <workflow.json>
├── verify        --> Run quality gates and compliance verification
│   ├── all       [--phase=<phase_dir>]
│   └── spec      <spec_file.md>
└── dev           --> Developer scaffolding and linting commands
    ├── lint      [--fix]
    └── new-skill --name=<skill_name> --domain=<domain>
```

---

## 3. Exit Code Taxonomy

| Exit Code | Symbol / Meaning | Description |
| :---: | :--- | :--- |
| `0` | `EXIT_SUCCESS` | Command completed successfully |
| `1` | `EXIT_GENERAL_ERROR` | Unhandled error or runtime failure |
| `2` | `EXIT_INVALID_ARGS` | Flag parsing error or missing required arguments |
| `10` | `EXIT_CONFIG_ERROR` | Invalid runtime configuration schema |
| `20` | `EXIT_VERIFICATION_FAILED` | Verification checker or quality gate failure |
| `30` | `EXIT_SECURITY_VIOLATION` | Security sandbox violation or unauthorized operation |
| `130` | `EXIT_SIGINT` | Terminated by User Interrupt (Ctrl+C) |

---

## 4. Verification Protocol

Test CLI command binary and help system:
```bash
agy --help && agy verify --version
```
Validates CLI argument parser, exit code mapping, and JSON output formatting.
