# Dependency Graph Engine Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-DG-005  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. Subsystem Purpose & Dependency Taxonomy

The Dependency Graph Engine tracks, validates, resolves, and manages multi-tier dependencies across microservices, code modules, software libraries, agent task DAGs, and runtime infrastructure components.

### Dependency Classification Types
1. **Compile-Time Dependencies (Hard):** Direct language imports, static links, module compile dependencies.
2. **Runtime Service Dependencies (Soft):** REST/gRPC API calls, database connections, message queue topics.
3. **Temporal Task Dependencies:** Directed Acyclic Graph (DAG) task execution ordering.
4. **Resource Lock Dependencies:** Shared state locks, hardware budget allocations, rate-limit reservations.

---

## 2. Directed Acyclic Graph (DAG) Data Structure

```text
[Module: Core Kernel] ◄── HARD ── [Module: Task Scheduler] ◄── HARD ── [Module: Worker Agent]
        │                                                                     │
        └── SOFT ─────────────────► [Service: Audit Logger] ◄──────────── SOFT ┘
```

### Dependency Node Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DependencyNode",
  "type": "object",
  "properties": {
    "node_id": { "type": "string" },
    "name": { "type": "string" },
    "version": { "type": "string" },
    "type": { "type": "string", "enum": ["MODULE", "SERVICE", "PACKAGE", "TASK", "RESOURCE"] },
    "outbound_edges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "target_id": { "type": "string" },
          "dependency_type": { "type": "string", "enum": ["HARD", "SOFT", "TEMPORAL", "LOCK"] },
          "version_constraint": { "type": "string" }
        },
        "required": ["target_id", "dependency_type"]
      }
    }
  },
  "required": ["node_id", "name", "version", "type"]
}
```

---

## 3. Resolution & Cycle Detection Algorithms

### Tarjan's Strongly Connected Components Algorithm
To ensure task DAGs and module dependencies remain acyclic, Tarjan's algorithm runs automatically on every candidate edge insertion.

```python
# Pseudocode implementation of cycle detection
def detect_cycle_tarjan(graph_nodes):
    index = 0
    stack = []
    indices = {}
    lowlink = {}
    on_stack = set()
    sccs = []

    def strongconnect(node):
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for edge in node.outbound_edges:
            target = edge.target_id
            if target not in indices:
                strongconnect(target)
                lowlink[node] = min(lowlink[node], lowlink[target])
            elif target in on_stack:
                lowlink[node] = min(lowlink[node], indices[target])

        if lowlink[node] == indices[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            if len(scc) > 1 or graph_has_self_loop(node):
                sccs.append(scc)

    for node in graph_nodes:
        if node not in indices:
            strongconnect(node)

    return sccs # Returns non-empty list if cycles exist
```

---

## 4. Upstream & Downstream Blast Radius Impact Analysis

When a component version update or breaking change is proposed, the Blast Radius Engine calculates total impact across all dependents:

$$\text{Impact Score} = \sum_{d \in \text{Dependents}} \text{DepthWeight}(d) \times \text{CriticalityScore}(d)$$

Where Depth Weight decays exponentially ($0.5^{\text{depth}}$) and Criticality Score ranges from 1 (Non-critical) to 10 (Kernel Core).

---

## 5. API Contracts & Serialization Formats

### REST API: Query Blast Radius Endpoint

```http
POST /api/v4/dependency/impact-analysis HTTP/1.1
Content-Type: application/json

{
  "target_node_id": "mod_kernel_v3",
  "proposed_version": "v4.0.0",
  "include_soft_dependencies": true
}
```

### Response Payload

```json
{
  "target_node_id": "mod_kernel_v3",
  "total_affected_dependents": 18,
  "has_breaking_changes": true,
  "high_risk_dependents": [
    { "node_id": "mod_scheduler_v1", "depth": 1, "criticality": 10 },
    { "node_id": "mod_agent_executor_v2", "depth": 2, "criticality": 9 }
  ],
  "recommendation": "REQUIRES_MAJOR_VERSION_BUMP_AND_APPROVAL_GATE"
}
```

---

## 6. Performance Benchmarks

- **Cycle Detection:** < 15 ms for 50,000 nodes and 200,000 edges.
- **Topological Sorting:** < 8 ms for execution DAG ordering.
- **In-Memory Cache:** Graph topological state cached in Redis with instant invalidated updates via Kafka events.
