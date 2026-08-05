# AI OS v4 — Sandbox Isolation Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** Runtime Security & Infrastructure Architecture  
**Status:** Frozen / Production Standard  

---

## 1. Multi-Tier Sandbox Isolation Architecture

The **Sandbox Isolation Framework** guarantees strict multi-tenant isolation, resource containment, and security boundaries for executable tools, plugins, and third-party code. AI OS v4 employs a 4-tier isolation hierarchy tailored to tool trust levels and performance requirements.

```
+-----------------------------------------------------------------------------------+
|                              SANDBOX ROUTING LAYER                                |
|  +-----------------------------------------------------------------------------+  |
|  | Determines Trust Tier, Resource Budget, and Security Profile                |  |
|  +-------------------------------------+---------------------------------------+  |
+----------------------------------------|------------------------------------------+
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
         v                               v                               v
+------------------+           +-------------------+           +-------------------+
|  TIER 0 / TIER 1 |           |      TIER 2       |           |      TIER 3       |
| In-Process / WASM|           | OCI Container /   |           | MicroVM           |
| High Latency-SLA |           | gRPC Worker       |           | (Firecracker)     |
| Sub-millisecond  |           | Isolated Network  |           | Hardware Isolation|
+------------------+           +-------------------+           +-------------------+
```

---

## 2. Sandbox Tier Taxonomy & Characteristics

| Tier | Technology | Boot Time | Memory Overhead | Network Isolation | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 0 (In-Process)** | Native Go/Rust DLL / V8 | <1 ms | Low (<5 MB) | Filtered Host | Built-in system primitives |
| **Tier 1 (WASM/WASI)** | WebAssembly (wasmtime) | <5 ms | Minimal (<10 MB) | Virtual Socket | Safe algorithmic plugins |
| **Tier 2 (Container)** | OCI Docker / Podman | 500-1500 ms | Medium (~50 MB) | eBPF Isolated Net | Data science, Python tools |
| **Tier 3 (MicroVM)** | AWS Firecracker / KVM | 5-15 ms | High (~128 MB+) | Tap Device / Vsock | Untrusted 3rd party code |

---

## 3. Resource Boundary Constraints & Enforcement

Every sandbox execution is bound by strict cgroups v2 resource hard-limits:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SandboxResourceLimits",
  "type": "object",
  "required": [
    "max_memory_mb",
    "cpu_shares",
    "max_processes",
    "max_open_files",
    "max_execution_time_ms",
    "read_only_root_fs"
  ],
  "properties": {
    "max_memory_mb": { "type": "integer", "default": 512, "maximum": 4096 },
    "cpu_shares": { "type": "integer", "default": 1024 },
    "max_processes": { "type": "integer", "default": 32, "maximum": 128 },
    "max_open_files": { "type": "integer", "default": 256 },
    "max_execution_time_ms": { "type": "integer", "default": 30000 },
    "read_only_root_fs": { "type": "boolean", "default": true },
    "tmpfs_mount_mb": { "type": "integer", "default": 64 }
  }
}
```

---

## 4. Network Isolation & eBPF Egress Filtering

1. **Default State:** Sandboxes operate with zero network interfaces (`net=none`) unless explicitly granted outbound HTTP capabilities.
2. **eBPF Packet Filtering:** Outbound network traffic is intercepted at the kernel veth interface using eBPF programs. Traffic to non-whitelisted IP addresses or domain names is dropped at the socket layer.
3. **No Inbound Bindings:** Sandboxes are prohibited from opening listening ports on host interfaces.

---

## 5. File System Containment & OverlayFS

```
+-------------------------------------------------------------------+
|                        SANDBOX FILESYSTEM MOUNT                   |
|  +-------------------------------------------------------------+  |
|  | Upper (Writable Ephemeral tmpfs - Discarded on Exit)        |  |
|  +-------------------------------------------------------------+  |
|  | Lower (Read-Only Base Image / Tool Runtime Dependencies)     |  |
|  +-------------------------------------------------------------+  |
|  | Workspace Binding (Read/Write /workspace/project/ - Isolated)|  |
+-------------------------------------------------------------------+
```

- **Ephemeral Storage:** All temporary writes (`/tmp`, `/var/tmp`) use memory-backed tmpfs mounted with `noexec, nosuid, nodev` flags.
- **Immediate Cleanup:** Ephemeral filesystems are securely zeroized and unmounted immediately upon sandbox termination.

---

## 6. IPC & gRPC Protocol over Unix Domain Sockets

Communication between the AI OS Kernel and Tier 2/Tier 3 Sandboxes occurs exclusively over **gRPC over Unix Domain Sockets (UDS)** mounted in private socket directories.

```protobuf
syntax = "proto3";

package aios.sandbox.v4;

service SandboxExecutionService {
  rpc ExecuteTool (ExecutionRequest) returns (ExecutionResponse);
  rpc StreamExecutionLogs (LogStreamRequest) returns (stream LogChunk);
  rpc TerminateSandbox (TerminationRequest) returns (TerminationResponse);
}

message ExecutionRequest {
  string execution_id = 1;
  string tool_id = 2;
  bytes input_json = 3;
  int64 timeout_ms = 4;
}

message ExecutionResponse {
  string execution_id = 1;
  int32 exit_code = 2;
  bytes output_json = 3;
  string error_message = 4;
  int64 execution_time_ms = 5;
  int64 peak_memory_bytes = 6;
}
```

---

## 7. Escape Prevention & Defense-in-Depth

1. **Seccomp Filters:** System calls restricted to a strict whitelist (~40 syscalls allowed; `ptrace`, `kexec`, `sys_module` strictly blocked).
2. **Linux Capabilities:** Stripped of all root capabilities (`CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, `CAP_DAC_OVERRIDE` removed).
3. **User Namespaces:** Processes inside containers run as unprivileged UID 65534 (`nobody`).
4. **Hardware Virtualization (Tier 3):** MicroVMs utilize Intel VT-x / AMD-V virtualization, providing hardware-enforced memory isolation.

---

## 8. Summary Checklist for Sandbox Isolation Compliance

- [x] 4-tier isolation matrix established (In-Process, WASM, Container, MicroVM).
- [x] cgroups v2 memory, CPU, process count, and execution time bounds specified.
- [x] eBPF egress filtering and default zero-network configuration detailed.
- [x] Read-only OverlayFS and ephemeral memory-backed storage mounts defined.
- [x] gRPC over Unix Domain Socket IPC protocol specification locked.
