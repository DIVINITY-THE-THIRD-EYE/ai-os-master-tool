# AI OS v4 — Platform Developer Guide

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Core Platform Engineering Guide  
**Status:** Frozen / Production Standard  

---

## 1. Developer Onboarding & Prerequisites

This guide provides step-by-step instructions for engineers contributing to or extending the AI OS v4 platform core runtime.

### 1.1 Workstation Requirements

- **Operating System:** Linux (Ubuntu 22.04 LTS recommended), macOS (Apple Silicon / Intel), or Windows 11 with WSL2.
- **Go Compiler:** v1.22+
- **Node.js / TypeScript:** v20.x LTS+ / TS v5.4+
- **Python Runtime:** v3.11+
- **Container Engine:** Docker Engine v25+ or Podman v4.8+
- **KVM Virtualization:** Required for Firecracker MicroVM local testing (`/dev/kvm` access).

---

## 2. Local Environment Setup & Compilation

### 2.1 Repository Cloning & Dependency Bootstrap

```bash
# Clone the repository
git clone https://github.com/enterprise/ai-os-v4.git
cd ai-os-v4

# Verify system prerequisites
./scripts/check_prereqs.sh

# Install Go & Node dependencies
go mod download
npm install --prefix sdk/typescript
pip install -r requirements-dev.txt
```

### 2.2 Local Core Platform Build

```bash
# Compile Kernel, Event Bus Router, and PDP Engine
make build-all

# Execute Unit & Integration Test Suites
make test-unit
make test-integration
```

---

## 3. Emulated Local Infrastructure Stack

AI OS v4 provides a one-command local emulation stack using Docker Compose:

```yaml
version: '3.8'
services:
  nats-server:
    image: nats:2.10-alpine
    ports: ["4222:4222", "8222:8222"]
    command: ["-m", "8222", "-js"]

  redis-cluster:
    image: redis:7.2-alpine
    ports: ["6379:6379"]

  postgres-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: aios_db
      POSTGRES_PASSWORD: secret_password
    ports: ["5432:5432"]

  qdrant-vector:
    image: qdrant/qdrant:v1.8.0
    ports: ["6333:6333"]
```

Launch local infrastructure:

```bash
make local-env-up
```

---

## 4. Coding Standards & Linter Enforcements

1. **Go:** Standard `gofmt`, `golangci-lint` with strict errcheck enabled.
2. **TypeScript:** Strict type checking (`noImplicitAny: true`, `strictNullChecks: true`), ESLint with Prettier formatting.
3. **Python:** `ruff` linter + `mypy --strict` static type checking.
4. **Documentation:** All public interfaces must contain JSDoc / GoDoc comments explaining input/output bounds and exception cases.

---

## 5. Summary Checklist for Developer Guide Compliance

- [x] Workstation hardware and software prerequisites listed.
- [x] Build and test commands for local development documented.
- [x] Complete Docker Compose emulation stack provided.
- [x] Multi-language linting and formatting standards defined.
