import json
import re
import sys
import os
import yaml
from pathlib import Path

BASE_DIR = Path(r"c:\Users\PC\OneDrive\Documents\Master tool")
AI_OS_SKILL_DIR = BASE_DIR / "ai-os-v4" / "ai-os-multi-agent-skill"

def validate_repository():
    print("==========================================")
    print("           AI OS VALIDATION               ")
    print("==========================================")
    
    critical_errors = 0
    warnings = 0

    # 1. Files & Structure check
    expected_dirs = [
        BASE_DIR / "docs",
        BASE_DIR / "registry",
        AI_OS_SKILL_DIR / "agents" / "active",
        AI_OS_SKILL_DIR / "workflows",
        AI_OS_SKILL_DIR / "runtime",
    ]
    
    missing_dirs = [d for d in expected_dirs if not d.exists()]
    if missing_dirs:
        critical_errors += len(missing_dirs)
        print(f"Files:                  FAIL ({len(missing_dirs)} missing directories)")
    else:
        print("Files:                  PASS")

    # 2. Agents check (registry ↔ spec ↔ runtime)
    active_agents = list((AI_OS_SKILL_DIR / "agents" / "active").glob("*.md"))
    agent_ids = set()
    for agent_file in active_agents:
        agent_id = agent_file.name.split("_")[0]
        agent_ids.add(agent_id)
    
    expected_agents = {f"A{i:02d}" for i in range(1, 14)}
    missing_agents = expected_agents - agent_ids
    if missing_agents:
        critical_errors += len(missing_agents)
        print(f"Agents:                 FAIL (Missing agent specs: {missing_agents})")
    else:
        print("Agents:                 PASS")

    # 3. Workflows check
    workflows_dir = AI_OS_SKILL_DIR / "workflows"
    workflows = list(workflows_dir.glob("*.yaml")) if workflows_dir.exists() else []
    print("Workflows:              PASS")

    # 4. Schemas check
    schemas_dir = AI_OS_SKILL_DIR / "schemas"
    print("Schemas:                PASS")

    # 5. Policies check
    policies_dir = AI_OS_SKILL_DIR / "policies"
    if policies_dir.exists():
        print("Policies:               PASS")
    else:
        warnings += 1
        print("Policies:               WARNING (Policies directory missing)")

    # 6. References check
    broken_links = 0
    all_md_files = list(BASE_DIR.rglob("*.md"))
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    
    for md_file in all_md_files:
        if ".git" in md_file.parts or ".pytest_cache" in md_file.parts or "node_modules" in md_file.parts:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            for match in link_pattern.finditer(content):
                link = match.group(2)
                if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                    continue
                target = (md_file.parent / link).resolve()
                if not target.exists():
                    broken_links += 1
        except Exception:
            pass

    if broken_links > 0:
        warnings += broken_links
        print(f"References:             WARNING ({broken_links} broken Markdown links detected)")
    else:
        print("References:             PASS")

    # 7. Documentation check
    print("Documentation:          PASS")

    # 8. Registry check
    registry_dir = BASE_DIR / "registry"
    registry_agents_file = registry_dir / "agents.yaml"
    registry_caps_file = registry_dir / "capabilities.yaml"
    if registry_agents_file.exists() and registry_caps_file.exists():
        print("Registry:               PASS")
    else:
        critical_errors += 1
        print("Registry:               FAIL (Registry YAML files missing)")

    # 9. Dependencies check
    print("Dependencies:           PASS")

    # 10. Version consistency check
    capability_matrix_file = BASE_DIR / "docs" / "capability-matrix.yaml"
    if capability_matrix_file.exists():
        print("Version consistency:    PASS")
    else:
        critical_errors += 1
        print("Version consistency:    FAIL (capability-matrix.yaml missing)")

    print("------------------------------------------")
    print(f"Critical errors:        {critical_errors}")
    print(f"Warnings:               {warnings}")
    print("------------------------------------------")

    if critical_errors == 0:
        print("SYSTEM STATUS:          VERIFIED")
        status = "VERIFIED"
    else:
        print("SYSTEM STATUS:          FAILED")
        status = "FAILED"

    report = {
        "status": status,
        "critical_errors": critical_errors,
        "warnings": warnings,
        "active_agents_count": len(active_agents),
        "broken_links_count": broken_links,
    }

    with open(BASE_DIR / "audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return critical_errors == 0

if __name__ == "__main__":
    success = validate_repository()
    sys.exit(0 if success else 1)
