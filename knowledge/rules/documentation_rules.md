# AI OS v4 Multi-Agent Documentation Rules (`documentation_rules.md`)

## 1. Overview & Quality Mandate

Documentation in AI OS v4 is treated as a first-class engineering artifact. Documentation Specialist (A09) and all contributing agents must ensure that every specification, prompt template, API reference, and architecture diagram is complete, accurate, self-contained, and free of placeholders or summaries.

---

## 2. Documentation Rule Specifications

### Rule DOC-001: Absolute Anti-Placeholder Mandate
- **Rule ID**: `DOC-001`
- **Severity**: `CRITICAL`
- **Scope**: All Markdown Files, Code Docstrings, YAML Configs
- **Description**: Documentation must contain complete, production-grade text. Tokens such as `TODO`, `FIXME`, `TBD`, `[Insert code here]`, `...`, or truncated summaries are strictly forbidden in committed documentation.

### Rule DOC-002: Standardized Markdown Header Hierarchy & Formatting
- **Rule ID**: `DOC-002`
- **Severity**: `HIGH`
- **Scope**: Repository Documentation
- **Description**: All Markdown files must begin with a single `# Heading 1` titling the document. Heading levels must strictly descend (`#`, `##`, `###`, `####`) without skipping levels (e.g., `#` directly to `###`).

### Rule DOC-003: Mandatory Code Docstring Conventions
- **Rule ID**: `DOC-003`
- **Severity**: `HIGH`
- **Scope**: Python (Google Style), TypeScript (TSDoc)
- **Description**: Every public class, interface, method, and function must have a complete docstring specifying summary, parameters, return types, and exceptions raised.
- **Python Google Style Example**:
  ```python
  def calculate_risk_score(impact: float, probability: float) -> float:
      """Calculates the composite risk score for a workflow execution step.

      Args:
          impact (float): Severity rating between 0.0 (negligible) and 1.0 (catastrophic).
          probability (float): Likelihood of occurrence between 0.0 and 1.0.

      Returns:
          float: Normalized composite risk rating bounded [0.0, 1.0].

      Raises:
          ValueError: If impact or probability are outside bounds [0.0, 1.0].
      """
      if not (0.0 <= impact <= 1.0 and 0.0 <= probability <= 1.0):
          raise ValueError("Impact and probability must be within [0.0, 1.0]")
      return impact * probability
  ```

### Rule DOC-004: Inline Architecture Diagrams (Mermaid Format)
- **Rule ID**: `DOC-004`
- **Severity**: `MEDIUM`
- **Scope**: System Architecture Documents
- **Description**: Structural diagrams must be rendered directly in Markdown using native Mermaid code blocks (` ```mermaid `). Static external image binaries (PNG, JPG) without underlying vector source code are prohibited.

### Rule DOC-005: OpenAPI 3.0 / JSON Schema API Documentation Standard
- **Rule ID**: `DOC-005`
- **Severity**: `HIGH`
- **Scope**: API Specifications & Tool Schemas
- **Description**: All API interfaces must provide complete OpenAPI 3.0 specs or JSON Schema descriptions including request/response body schemas, field descriptions, authentication headers, error codes, and concrete JSON request/response examples.

### Rule DOC-006: Self-Contained Handoff Reports (`handoff.md`)
- **Rule ID**: `DOC-006`
- **Severity**: `CRITICAL`
- **Scope**: All Agent-to-Agent Handoffs
- **Description**: Handoff reports MUST contain all five mandatory sections specified in the Handoff Protocol:
  1. `Observation`: Verbatim error outputs, exact file paths, line numbers.
  2. `Logic Chain`: Step-by-step reasoning linking observations to conclusions.
  3. `Caveats`: Uninvestigated areas, assumptions, alternative theories.
  4. `Conclusion`: Final actionable assessment.
  5. `Verification Method`: Concrete terminal commands and criteria to verify claims.

### Rule DOC-007: Standardized README Layout Structure
- **Rule ID**: `DOC-007`
- **Severity**: `MEDIUM`
- **Scope**: Package & Module Directories
- **Description**: Every package root directory must include a `README.md` adhering to the standard template structure: Title, Overview, Architecture Diagram, Prerequisites, Installation/Setup, Usage Examples, Configuration Parameters, Verification/Testing, and Maintenance Guide.

### Rule DOC-008: Automated Changelog Generation & Maintenance
- **Rule ID**: `DOC-008`
- **Severity**: `MEDIUM`
- **Scope**: Version Releases
- **Description**: Every release update must append a new entry to `CHANGELOG.md` following the Keep a Changelog standard, categorized into `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.

### Rule DOC-009: Code Snippet Executive Testability
- **Rule ID**: `DOC-009`
- **Severity**: `HIGH`
- **Scope**: Documentation Code Blocks
- **Description**: Code snippets featured in documentation must be syntactically valid and runnable without missing imports or non-existent helper variables.

### Rule DOC-010: Terminology & Glossary Alignment
- **Rule ID**: `DOC-010`
- **Severity**: `LOW`
- **Scope**: Repository Documentation
- **Description**: Documentation must strictly use terms defined in `knowledge/ontology/ontology_layers.md` (e.g., use `Agent`, `Artifact`, `TaskNode` rather than informal synonyms like `bot`, `output file`, `step`).
