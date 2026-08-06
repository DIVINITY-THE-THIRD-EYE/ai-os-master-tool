import ast
import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\PC\OneDrive\Documents\Master tool")

report = {
    "dead_python_code": [],
    "unused_python_modules": [],
    "orphaned_docs": [],
    "unused_prompts": [],
    "unregistered_agents": [],
    "unreachable_workflows": [],
    "stale_config_files": [],
    "broken_internal_links": [],
    "duplicate_schemas": [],
    "duplicate_prompt_ids": [],
    "unused_feature_flags": [],
    "obsolete_migrations": [],
    "unreferenced_runtime_components": [],
}

all_files = [
    p
    for p in REPO_ROOT.rglob("*")
    if p.is_file()
    and ".git" not in p.parts
    and "node_modules" not in p.parts
    and "__pycache__" not in p.parts
    and ".pytest_cache" not in p.parts
]

all_content = {}
for p in all_files:
    try:
        all_content[p] = p.read_text(encoding="utf-8")
    except Exception:
        pass


def is_referenced_by_basename(filename, exclude_self=True):
    basename = filename.name
    # remove extension for some checks
    stem = filename.stem
    for p, content in all_content.items():
        if exclude_self and p == filename:
            continue
        if basename in content or stem in content:
            return True
    return False


# 1. Unused Python Modules & Dead Code
python_files = [
    p for p in all_files if p.suffix == ".py" and p.name != "audit.py" and p.name != "comprehensive_audit.py"
]
for p in python_files:
    if p.name == "validate_repository.py" or p.name == "index.py":
        continue
    # check if module is imported
    if not is_referenced_by_basename(p):
        report["unused_python_modules"].append(str(p.relative_to(REPO_ROOT)))

    # naive dead code: look for function/class definitions
    try:
        tree = ast.parse(all_content[p])
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = node.name
                if name.startswith("__"):
                    continue
                # check if this name is used anywhere else
                used = False
                for p2, content in all_content.items():
                    if p2 != p and name in content:
                        used = True
                        break
                if not used:
                    report["dead_python_code"].append({"file": str(p.relative_to(REPO_ROOT)), "name": name})
    except Exception:
        pass

# 2. Orphaned Documentation
for p in all_files:
    if p.suffix == ".md" and p.name.lower() != "readme.md":
        if not is_referenced_by_basename(p):
            report["orphaned_docs"].append(str(p.relative_to(REPO_ROOT)))

# 3. Unused Prompts
# Assuming prompts are in directories named "prompts" or "prompt_library" or end with prompt.yaml/md
for p in all_files:
    if "prompt" in p.name.lower() or "prompts" in p.parts:
        if not is_referenced_by_basename(p):
            report["unused_prompts"].append(str(p.relative_to(REPO_ROOT)))

# 4. Unregistered Agents
agent_registry_content = ""
for p in all_files:
    if p.name == "agent_registry.yaml":
        agent_registry_content += all_content[p]

for p in all_files:
    if "agents" in p.parts and p.suffix in [".md", ".yaml"]:
        if p.stem not in agent_registry_content and not is_referenced_by_basename(p):
            report["unregistered_agents"].append(str(p.relative_to(REPO_ROOT)))

# 5. Unreachable workflows
for p in all_files:
    if "workflows" in p.parts and p.suffix in [".yaml", ".md"]:
        if not is_referenced_by_basename(p):
            report["unreachable_workflows"].append(str(p.relative_to(REPO_ROOT)))

# 6. Stale config files
for p in all_files:
    if p.suffix in [".yaml", ".json"] and "package" not in p.name.lower():
        if not is_referenced_by_basename(p):
            report["stale_config_files"].append(str(p.relative_to(REPO_ROOT)))

# 7. Broken internal links
link_pattern = re.compile(r"\[.*?\]\(([^)]+)\)")
for p, content in all_content.items():
    if p.suffix == ".md":
        for match in link_pattern.finditer(content):
            link = match.group(1)
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                continue
            # remove anchor
            link_path = link.split("#")[0]
            if not link_path:
                continue

            target = (p.parent / link_path).resolve()
            if not target.exists():
                # fallback: try relative to repo root
                if not (REPO_ROOT / link_path).exists():
                    report["broken_internal_links"].append({"file": str(p.relative_to(REPO_ROOT)), "link": link})

# 8. Duplicate schemas
schemas_hashes = {}
for p in all_files:
    if p.suffix == ".json" and "schema" in p.name.lower():
        try:
            data = json.loads(all_content[p])
            hash_val = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
            if hash_val in schemas_hashes:
                report["duplicate_schemas"].append(
                    [str(schemas_hashes[hash_val].relative_to(REPO_ROOT)), str(p.relative_to(REPO_ROOT))]
                )
            else:
                schemas_hashes[hash_val] = p
        except Exception:
            pass

# 9. Duplicate prompt IDs
prompt_ids = {}
for p, content in all_content.items():
    if "prompt" in p.name.lower() or "prompts" in p.parts:
        if p.suffix in [".yaml", ".json"]:
            try:
                data = json.loads(content) if p.suffix == ".json" else __import__("yaml").safe_load(content)
                if isinstance(data, dict) and "prompt_id" in data:
                    pid = data["prompt_id"]
                    if pid in prompt_ids:
                        report["duplicate_prompt_ids"].append(
                            {
                                "id": pid,
                                "files": [str(prompt_ids[pid].relative_to(REPO_ROOT)), str(p.relative_to(REPO_ROOT))],
                            }
                        )
                    else:
                        prompt_ids[pid] = p
            except:
                pass
        # search for ID in md files
        import re

        m = re.search(r"Prompt\s*ID:\s*([A-Za-z0-9_-]+)", content, re.IGNORECASE)
        if m:
            pid = m.group(1)
            if pid in prompt_ids:
                report["duplicate_prompt_ids"].append(
                    {"id": pid, "files": [str(prompt_ids[pid].relative_to(REPO_ROOT)), str(p.relative_to(REPO_ROOT))]}
                )
            else:
                prompt_ids[pid] = p

# 10. Unused feature flags
# Assuming feature flags are defined in something like "features.yaml" or environment
# Let's search for FLAG_ or FEATURE_ in python
for p, content in all_content.items():
    if p.suffix == ".py":
        for m in re.finditer(r"(FEATURE_[A-Z0-9_]+|FLAG_[A-Z0-9_]+)", content):
            flag = m.group(1)
            # check if used anywhere else
            used = False
            for p2, content2 in all_content.items():
                if p2 != p and flag in content2:
                    used = True
                    break
            if not used:
                report["unused_feature_flags"].append({"flag": flag, "file": str(p.relative_to(REPO_ROOT))})

Path(REPO_ROOT / "comprehensive_audit_report.json").write_text(json.dumps(report, indent=2))
