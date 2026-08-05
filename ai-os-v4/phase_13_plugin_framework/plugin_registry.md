# AI OS v4 — Plugin Registry Specification

**Document Version:** 4.0.0  
**Phase:** Phase 13 — Plugin Framework  
**Classification:** Enterprise System Architecture Specification  
**Status:** Frozen / Production Standard  

---

## 1. Plugin System Architecture

The **Plugin Registry** serves as the enterprise package manager, distribution hub, and lifecycle governance repository for extensions to AI OS v4. Plugins bundle one or more tools, workflows, prompts, or agents into modular, versioned, and cryptographically verified packages (`.aiplugin` / OCI artifacts).

```
+-----------------------------------------------------------------------------------+
|                            PLUGIN REGISTRY CONTROL PLANE                          |
|  +---------------------+   +-----------------------+   +-----------------------+  |
|  |  Catalog & Indexing |   | Package Storage (OCI) |   | Cryptographic Verification|
|  |  Engine             |   | & Mirror Manager      |   | (Cosign / Notary v2)  |  |
|  +----------+----------+   +-----------+-----------+   +-----------+-----------+  |
+-------------|--------------------------|---------------------------|--------------+
              |                          |                           |
              +--------------------------+---------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         ENTERPRISE GOVERNANCE GATES                               |
|   [Certified Tier]              [Partner Tier]              [Untrusted Sandbox Tier] |
+----------------------------------------+------------------------------------------+
                                         | Distribute Artifact
                                         v
+-----------------------------------------------------------------------------------+
|                            RUNTIME INSTALLATION MANAGER                           |
|        [Dependency Solver] ──► [Sandbox Isolator] ──► [Hot Swapper]                |
+-----------------------------------------------------------------------------------+
```

---

## 2. Plugin Manifest Specification (`plugin.json`)

All plugins must contain a root manifest `plugin.json` at package root matching the canonical schema below.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AIOSPluginManifest",
  "type": "object",
  "required": [
    "plugin_id",
    "name",
    "version",
    "author",
    "license",
    "description",
    "min_kernel_version",
    "entry_point",
    "provided_tools",
    "capabilities_requested",
    "signature"
  ],
  "properties": {
    "plugin_id": {
      "type": "string",
      "pattern": "^[a-z0-9_\\-]+\\.[a-z0-9_\\-]+$"
    },
    "name": { "type": "string", "maxLength": 64 },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "author": {
      "type": "object",
      "required": ["name", "email"],
      "properties": {
        "name": { "type": "string" },
        "email": { "type": "string" }
      }
    },
    "license": { "type": "string" },
    "description": { "type": "string" },
    "min_kernel_version": { "type": "string" },
    "entry_point": { "type": "string" },
    "dependencies": {
      "type": "object",
      "additionalProperties": { "type": "string" }
    },
    "provided_tools": {
      "type": "array",
      "items": { "type": "string" }
    },
    "provided_workflows": {
      "type": "array",
      "items": { "type": "string" }
    },
    "capabilities_requested": {
      "type": "array",
      "items": { "type": "string" }
    },
    "signature": {
      "type": "object",
      "required": ["key_id", "sha256", "signature_bytes"],
      "properties": {
        "key_id": { "type": "string" },
        "sha256": { "type": "string" },
        "signature_bytes": { "type": "string" }
      }
    }
  }
}
```

---

## 3. Package Management & OCI Registry Storage

Plugins are packaged as OCI (Open Container Initiative) compliant artifacts and stored in enterprise registries (Harbor, AWS ECR, Azure ACR, or internal Artifactory).

### 3.1 Package Distribution Structure

```
plugin-package.tar.gz
├── plugin.json                 # Manifest
├── LICENSE                     # License terms
├── README.md                   # Plugin documentation
├── dist/                       # Compiled assets / binaries
│   ├── plugin_engine.wasm      # WASM binary module OR
│   └── main.py                 # Isolated script entry point
├── tools/                      # Tool schema definitions
│   └── custom_tool.json
└── metadata/                   # Cryptographic signatures & provenance
    ├── cosign.pub
    └── provenance.json
```

---

## 4. Dependency Resolution & Conflict Avoidance Matrix

The Plugin Registry includes a SAT-solver-based dependency resolution engine.

### 4.1 Dependency Resolution Algorithm

1. **Graph Construction:** Constructs a Directed Acyclic Graph (DAG) of plugin dependencies and SemVer version bounds.
2. **Conflict Detection:** Identifies duplicate tool registrations (`tool_id` collisions) or incompatible kernel version constraints.
3. **Resolution Strategy:**
   - If two plugins export identical tool names, namespacing is strictly applied: `plugin_a::tool_name` vs `plugin_b::tool_name`.
   - Incompatible dynamic shared libraries trigger separate WASM/MicroVM sandbox instantiation.

---

## 5. Software Supply Chain & Cryptographic Signing

No plugin is loaded without cryptographic verification against trusted public keys.

- **Signing Protocol:** Sigstore / Cosign keyless signing or standard PKI RSA-4096 / Ed25519 signatures.
- **SLSA Provenance:** All official plugins must be built in verified pipelines meeting SLSA Level 3 standards.
- **Vulnerability Scanning:** Automated Trivy/Grype vulnerability scanning executed during package ingestion. Packages with CRITICAL vulnerabilities are automatically blocked.

---

## 6. Certification Levels & Enterprise Governance

| Certification Tier | Verification Level | Sandbox Requirement | Execution Privilege |
| :--- | :--- | :--- | :--- |
| **Platform Certified** | Built by Core Team, 100% Code Audit | In-Process / WASM | High / Fast Path |
| **Enterprise Partner** | Verified Vendor, Signed SLSA Level 3 | WASM / Container | Medium |
| **Untrusted / Community** | Unaudited External Plugin | Strict MicroVM / gRPC RPC | Low / Isolated |

---

## 7. Plugin Registry API Specifications

```typescript
export interface PluginRegistryAPI {
  publishPlugin(packageStream: ReadableStream, manifest: PluginManifest): Promise<PublishResult>;
  inspectPlugin(pluginId: string, version: string): Promise<PluginMetadata>;
  searchCatalog(query: CatalogSearchFilter): Promise<PluginSearchResult>;
  installPlugin(pluginId: string, versionConstraint: string, tenantId: string): Promise<InstallationResult>;
  uninstallPlugin(pluginId: string, tenantId: string): Promise<boolean>;
  upgradePlugin(pluginId: string, targetVersion: string, tenantId: string): Promise<UpgradeResult>;
}
```

---

## 8. Summary Checklist for Plugin Registry Compliance

- [x] Canonical `plugin.json` schema and OCI artifact packaging defined.
- [x] SAT-solver dependency resolution and namespace collision avoidance specified.
- [x] Cosign/Sigstore cryptographic signing and SLSA Level 3 provenance required.
- [x] Three-tiered certification governance model established.
- [x] Full REST/gRPC management API contract published.
