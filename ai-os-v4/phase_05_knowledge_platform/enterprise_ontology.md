# Enterprise Ontology Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-EO-003  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. Domain Modeling Philosophy & Standards

The Enterprise Ontology defines the formal taxonomy, concepts, relationships, and semantic constraints governing all entities in AI OS v4. It is specified using standard Web Ontology Language (OWL 2) concepts mapped into JSON Schema and RDF/Turtle formats.

### Core Architectural Objectives
- Provide unambiguous semantic definitions across all 18 enterprise domain skill packs.
- Enable automated SHACL reasoning, validation, and consistency checks on candidate knowledge graph updates.
- Ensure backwards-compatible schema evolutions through semantic versioning.

---

## 2. Root Class Hierarchy & Taxonomy

```text
aios:Entity (Root)
 ├── aios:SystemDomain
 ├── aios:TechnicalConcept
 ├── aios:Artifact
 │     ├── aios:CodeArtifact
 │     ├── aios:SpecificationDocument
 │     └── aios:ConfigArtifact
 ├── aios:Process
 │     ├── aios:Workflow
 │     └── aios:TaskExecution
 ├── aios:Policy
 │     ├── aios:SecurityPolicy
 │     └── aios:QualityGatePolicy
 ├── aios:AgentRole
 └── aios:Metric
```

---

## 3. Class Definitions & JSON Schema Declarations

### Class: `aios:CodeArtifact`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://aios.enterprise/schemas/ontology/CodeArtifact.json",
  "title": "CodeArtifactOntologyClass",
  "type": "object",
  "properties": {
    "uri": { "type": "string", "format": "uri" },
    "label": { "type": "string" },
    "language": { "type": "string", "enum": ["TypeScript", "Go", "Python", "Rust", "Java", "SQL"] },
    "file_path": { "type": "string" },
    "module_name": { "type": "string" },
    "exported_symbols": {
      "type": "array",
      "items": { "type": "string" }
    },
    "has_dependency": {
      "type": "array",
      "items": { "type": "string", "format": "uri" }
    },
    "implements_specification": {
      "type": "string",
      "format": "uri"
    }
  },
  "required": ["uri", "label", "language", "file_path"]
}
```

---

## 4. Relationship Axioms & Cardinality Rules

| Property URI | Domain Class | Range Class | Characteristics | Cardinality |
| :--- | :--- | :--- | :--- | :--- |
| `aios:dependsOn` | `aios:Artifact` | `aios:Artifact` | Transitive, Asymmetric | `0..*` |
| `aios:implements` | `aios:CodeArtifact` | `aios:SpecificationDocument` | Functional | `1..*` |
| `aios:governedBy` | `aios:Process` | `aios:Policy` | Non-transitive | `1..*` |
| `aios:executedBy` | `aios:TaskExecution` | `aios:AgentRole` | Functional | `1..1` |
| `aios:supercedes` | `aios:Artifact` | `aios:Artifact` | Transitive, Asymmetric | `0..*` |

---

## 5. Formal SHACL Validation Shapes

SHACL shapes enforce data shape constraints prior to committing to the Enterprise Knowledge Graph.

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix aios: <https://aios.enterprise/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

aios:CodeArtifactShape
    a sh:NodeShape ;
    sh:targetClass aios:CodeArtifact ;
    sh:property [
        sh:path aios:file_path ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:message "CodeArtifact must have exactly one file_path string." ;
    ] ;
    sh:property [
        sh:path aios:implements ;
        sh:nodeKind sh:IRI ;
        sh:minCount 1 ;
        sh:message "CodeArtifact must implement at least one specification IRI." ;
    ] .
```

---

## 6. Migration & Schema Evolution Protocol

1. **Version Identifier Format:** `vMAJOR.MINOR.PATCH` (e.g. `v1.2.0`).
2. **Backward Compatibility Guarantee:** Adding new optional properties or classes is MINOR version bump; removing properties or narrowing ranges requires MAJOR version bump and migration transform script.
3. **Deprecation Window:** Deprecated terms remain in active ontology for a minimum of 2 release cycles with explicit `owl:deprecated true` annotations.
