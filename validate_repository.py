import json
import re
import sys
import os
import yaml
from pathlib import Path
import importlib.util

BASE_DIR = Path(r"c:\Users\PC\OneDrive\Documents\Master tool")

def _check_path(path_str):
    if not path_str:
        return False
    
    # Handle pytest module paths like 'tools/test_runtime.py::TestAgentRegistry'
    if "::" in path_str:
        path_str = path_str.split("::")[0]
        
    p = BASE_DIR / path_str
    
    if p.exists():
        return True
    
    # Check if it's a python module string like 'runtime.workflow_executor.WorkflowExecutor'
    if "." in path_str and not "/" in path_str and not "\\" in path_str and not path_str.endswith(".py"):
        module_path = path_str.split(".")[0] + "/" + path_str.split(".")[1] + ".py"
        if (BASE_DIR / module_path).exists():
            return True
            
    return False

def validate_repository():
    print("==========================================")
    print("           AI OS VALIDATOR 2.0            ")
    print("==========================================")
    
    critical_errors = 0
    warnings = 0

    # 1. Structure
    expected_dirs = ["docs", "registry", "agents", "workflows", "runtime"]
    missing_dirs = [d for d in expected_dirs if not (BASE_DIR / d).exists()]
    if missing_dirs:
        critical_errors += len(missing_dirs)
        print(f"Files:                  FAIL ({len(missing_dirs)} missing directories)")
    else:
        print("Files:                  PASS")

    # 2. Registry authoritative check
    agents_yaml = BASE_DIR / "registry" / "agents.yaml"
    if agents_yaml.exists():
        with open(agents_yaml, 'r', encoding='utf-8') as f:
            registry_data = yaml.safe_load(f)
            agents = registry_data.get('agents', [])
            missing_specs = 0
            for agent in agents:
                if not _check_path(agent.get('spec', '')):
                    missing_specs += 1
                    print(f"Agent {agent['id']} spec missing: {agent.get('spec')}")
                if not _check_path(agent.get('runtime_impl', '')):
                    missing_specs += 1
                    print(f"Agent {agent['id']} impl missing: {agent.get('runtime_impl')}")
            
            if missing_specs > 0:
                critical_errors += missing_specs
                print(f"Agents (Registry):      FAIL ({missing_specs} broken references)")
            else:
                print("Agents (Registry):      PASS")
    else:
        critical_errors += 1
        print("Agents (Registry):      FAIL (agents.yaml not found)")

    # 3. Capability Matrix authoritative check
    cap_yaml = BASE_DIR / "docs" / "capability-matrix.yaml"
    if cap_yaml.exists():
        with open(cap_yaml, 'r', encoding='utf-8') as f:
            cap_data = yaml.safe_load(f)
            caps = cap_data.get('capabilities', [])
            broken_evidence = 0
            for cap in caps:
                ev = cap.get('evidence', {})
                for k, v in ev.items():
                    if not _check_path(v):
                        broken_evidence += 1
                        print(f"Capability {cap['id']} {k} missing: {v}")
            if broken_evidence > 0:
                critical_errors += broken_evidence
                print(f"Capabilities:           FAIL ({broken_evidence} broken evidence paths)")
            else:
                print("Capabilities:           PASS (All evidence PROVEN)")
    else:
        critical_errors += 1
        print("Capabilities:           FAIL (capability-matrix.yaml not found)")

    # 4. References check
    broken_links = 0
    all_md_files = list(BASE_DIR.rglob("*.md"))
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    
    for md_file in all_md_files:
        if any(skip in md_file.parts for skip in [".git", ".pytest_cache", "node_modules"]):
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

    print("------------------------------------------")
    print(f"Critical errors:        {critical_errors}")
    print(f"Warnings:               {warnings}")
    print("------------------------------------------")

    if critical_errors == 0:
        print("SYSTEM STATUS:          VERIFIED")
    else:
        print("SYSTEM STATUS:          FAILED")

    return critical_errors == 0

if __name__ == "__main__":
    success = validate_repository()
    sys.exit(0 if success else 1)
