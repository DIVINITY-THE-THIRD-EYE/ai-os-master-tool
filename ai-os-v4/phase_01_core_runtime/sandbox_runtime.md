---
title: Sandbox Runtime Environment & Security Isolation Specification
document_id: SPEC-P01-KERN-010
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Security Sandbox Working Group
last_updated: 2026-08-05
---

# Sandbox Runtime Environment & Security Isolation Specification

## Executive Summary
This document specifies the Sandbox Runtime (`sandbox_runtime`), providing lightweight container isolation, seccomp system call filtering, ephemeral file system overlays, network egress proxying, and resource bounding for untrusted agent tool execution.

---

## 1. Sandbox Architecture & Isolation Layers

```text
[ UNTRUSTED AGENT TOOL EXECUTION ]
                 │
                 ▼
+-----------------------------------------------------------------+
| 1. SECCOMP SYSCALL FILTER (Blocks raw socket / ptrace calls)    |
+-----------------------------------------------------------------+
                 │
                 ▼
+-----------------------------------------------------------------+
| 2. GVISOR CONTAINER KERNEL / READ-ONLY OVERLAY FILESYSTEM       |
+-----------------------------------------------------------------+
                 │
                 ▼
+-----------------------------------------------------------------+
| 3. EGRESS PROXY (Whitelist HTTP/HTTPS filtering)                |
+-----------------------------------------------------------------+
```

---

## 2. Sandbox Runtime API Contract

```typescript
export interface SandboxExecutionOptions {
  readonly sandboxId: string;
  readonly command: string;
  readonly args: string[];
  readonly workingDir: string;
  readonly envVars: Record<string, string>;
  readonly timeoutMs: number;
  readonly allowedNetworkDomains: string[];
}

export interface SandboxExecutionResult {
  readonly exitCode: number;
  readonly stdout: string;
  readonly stderr: string;
  readonly durationMs: number;
  readonly networkRequestsMade: number;
  readonly isTimedOut: boolean;
}

export interface ISandboxRuntime {
  createSandbox(options: Partial<SandboxExecutionOptions>): Promise<string>;
  executeInSandbox(sandboxId: string, options: SandboxExecutionOptions): Promise<SandboxExecutionResult>;
  destroySandbox(sandboxId: string): Promise<void>;
}
```

---

## 3. Mandatory Security Boundaries

1. **Blocked System Calls**: System calls `ptrace`, `reboot`, `kexec_load`, `chroot`, `syslog` are explicitly blocked by seccomp profiles.
2. **Ephemeral Disk Scrubbing**: All temporary files created inside the sandbox workspace are wiped upon container destruction.

---

## 4. Verification Protocol

```bash
agy verify-sandbox --test-syscall-blocking
```
Attempts illegal system calls, verifies network domain whitelist enforcement, and tests memory cap breaches.
