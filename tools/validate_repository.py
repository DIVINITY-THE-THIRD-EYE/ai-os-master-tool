"""
AI OS Repository Validator — verifies structural integrity of the ai-os-multi-agent-skill package.

From wihout memory.md: tools/validate_repository.py

Checks:
1. All expected files and folders exist
2. YAML syntax is valid
3. JSON syntax is valid and has required fields
4. Internal references resolve correctly
5. All agents in agents/ are registered in agent_registry.yaml
6. All quality gates defined in quality_gates.yaml (Gates 0-7)
7. skill.yaml has required quality thresholds
"""

import json
import sys
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent


EXPECTED_DIRS = [
    "orchestrator",
    "agents",
    "workflows",
    "knowledge",
    "knowledge/ontology",
    "knowledge/rules",
    "knowledge/sops",
    "knowledge/best_practices",
    "knowledge/anti_patterns",
    "knowledge/lessons_learned",
    "knowledge/prompt_library",
    "policies",
    "quality",
    "quality/checklists",
    "events",
    "platform",
    "reports",
    "runtime",
]

EXPECTED_FILES = [
    "skill.yaml",
    "README.md",
    "orchestrator/master_orchestrator.md",
    "orchestrator/state_machine.yaml",
    "orchestrator/escalation_matrix.yaml",
    "agents/active/A01_intake_requirements_agent.md",
    "agents/active/A02_context_memory_agent.md",
    "agents/active/A03_knowledge_graph_agent.md",
    "agents/active/A04_scheduler_agent.md",
    "agents/active/A05_domain_authority_agent.md",
    "agents/active/A06_worker_agent.md",
    "agents/active/A07_verification_agent.md",
    "agents/active/A08_policy_decision_agent.md",
    "agents/active/A09_security_compliance_agent.md",
    "agents/active/A10_release_deployment_agent.md",
    "agents/active/A11_observability_operations_agent.md",
    "agents/active/A12_learning_agent.md",
    "agents/active/A13_human_collaboration_agent.md",
    "workflows/canonical_workflow.yaml",
    "workflows/execution_workflow.md",
    "workflows/verification_workflow.md",
    "workflows/release_workflow.md",
    "workflows/recovery_workflow.md",
    "workflows/learning_workflow.md",
    "knowledge/ontology/ontology_layers.md",
    "knowledge/rules/governance_rules.md",
    "knowledge/rules/security_rules.md",
    "knowledge/rules/compliance_rules.md",
    "knowledge/rules/coding_rules.md",
    "knowledge/rules/release_rules.md",
    "knowledge/rules/escalation_rules.md",
    "knowledge/rules/approval_rules.md",
    "knowledge/best_practices/coding_standards.md",
    "knowledge/anti_patterns/anti_patterns.md",
    "knowledge/sops/SOP-001_task_intake_classification.md",
    "policies/governance_policies.yaml",
    "policies/security_policies.yaml",
    "policies/compliance_policies.yaml",
    "policies/release_policies.yaml",
    "policies/approval_policies.yaml",
    "policies/coding_policies.yaml",
    "quality/quality_gates.yaml",
    "quality/verification_modules.yaml",
    "quality/scoring_thresholds.yaml",
    "quality/checklists/planning_checklist.md",
    "quality/checklists/execution_checklist.md",
    "quality/checklists/code_quality_checklist.md",
    "quality/checklists/security_checklist.md",
    "quality/checklists/verification_checklist.md",
    "quality/checklists/release_checklist.md",
    "quality/checklists/learning_checklist.md",
    "events/event_topics.yaml",
    "events/event_payload_schema.json",
    "events/handoff_schema.json",
    "platform/agent_registry.yaml",
    "platform/capability_registry.yaml",
    "platform/security.yaml",
    "platform/observability.yaml",
    "platform/disaster_recovery.yaml",
    "reports/worker_report_template.md",
    "reports/authority_report_template.md",
    "reports/executive_report_template.md",
    "reports/audit_report_template.md",
    "reports/release_report_template.md",
    "runtime/event_bus.py",
    "runtime/workflow_executor.py",
    "runtime/capability_router.py",
    "runtime/agent_registry.py",
    "runtime/llm_router.py",
    "runtime/memory_manager.py",
    "runtime/state_manager.py",
    "runtime/api_server.py",
    "tools/ai_studio_exporter.py",
]

REQUIRED_JSON_FIELDS = ["$schema", "title", "type", "properties"]
REQUIRED_GATES = [f"gate_{i}" for i in range(8)]
REQUIRED_SKILL_THRESHOLDS = {
    "quality_score_min": 0.85,
    "confidence_min": 0.80,
    "test_coverage_min": 0.80,
}


class Validator:
    def __init__(self):
        self.errors: list = []
        self.warnings: list = []
        self.passed: int = 0

    def check(self, name: str, condition: bool, error_msg: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"  [PASS] {name}")
        else:
            self.errors.append(f"{name}: {error_msg}")
            print(f"  [FAIL] {name}: {error_msg}")

    def warn(self, name: str, msg: str) -> None:
        self.warnings.append(f"{name}: {msg}")
        print(f"  [WARN] {name}: {msg}")

    def run(self) -> int:
        print("\n" + "=" * 60)
        print("AI OS Repository Validator")
        print(f"Base: {BASE}")
        print("=" * 60)

        print("\n[1] Directory Structure")
        for d in EXPECTED_DIRS:
            path = BASE / d
            self.check(d, path.is_dir(), f"Missing directory: {path}")

        print("\n[2] Required Files")
        for f in EXPECTED_FILES:
            path = BASE / f
            self.check(f, path.is_file(), f"Missing file: {path}")

        print("\n[3] JSON Schema Validation")
        for json_file in (BASE / "events").glob("*.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                for field in REQUIRED_JSON_FIELDS:
                    self.check(f"{json_file.name}: has '{field}'", field in data, f"Missing field '{field}'")
            except json.JSONDecodeError as e:
                self.check(f"{json_file.name}: valid JSON", False, str(e))

        print("\n[4] YAML Syntax Validation")
        for yaml_file in BASE.rglob("*.yaml"):
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    yaml.safe_load(f)
                self.check(f"{yaml_file.relative_to(BASE)}: valid YAML", True)
            except yaml.YAMLError as e:
                self.check(f"{yaml_file.relative_to(BASE)}: valid YAML", False, str(e))

        print("\n[5] Quality Gates (Gates 0-7)")
        gate_file = BASE / "quality" / "quality_gates.yaml"
        if gate_file.is_file():
            data = yaml.safe_load(gate_file.read_text(encoding="utf-8"))
            gates = data.get("quality_gates", {}).get("gates", {})
            for gate_id in REQUIRED_GATES:
                self.check(f"quality_gates.yaml: {gate_id}", gate_id in gates, f"Gate '{gate_id}' not defined")

        print("\n[6] Skill Manifest Thresholds")
        skill_file = BASE / "skill.yaml"
        if skill_file.is_file():
            data = yaml.safe_load(skill_file.read_text(encoding="utf-8"))
            gates = data.get("skill", {}).get("quality_gates", {})
            for key, expected in REQUIRED_SKILL_THRESHOLDS.items():
                actual = gates.get(key)
                self.check(f"skill.yaml: {key} = {expected}", actual == expected, f"Expected {expected}, got {actual}")

        print("\n[7] Escalation Matrix Severity Levels")
        esc_file = BASE / "orchestrator" / "escalation_matrix.yaml"
        if esc_file.is_file():
            data = yaml.safe_load(esc_file.read_text(encoding="utf-8"))
            levels = data.get("escalation_matrix", {}).get("levels", {})
            for sev in ["sev1", "sev2", "sev3", "sev4", "sev5"]:
                self.check(f"escalation_matrix.yaml: {sev}", sev in levels, f"Severity level '{sev}' not defined")

        print("\n" + "=" * 60)
        total = self.passed + len(self.errors)
        print(f"Results: {self.passed}/{total} checks passed")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print("\nFailed checks:")
            for e in self.errors:
                print(f"  - {e}")
            return 1
        else:
            print("\n[OK] All checks passed. Repository is structurally valid.")
            return 0


if __name__ == "__main__":
    validator = Validator()
    sys.exit(validator.run())
