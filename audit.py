import json
import re
from pathlib import Path

BASE = Path(r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\ai-os-multi-agent-skill")
API_DIR = Path(r"c:\Users\PC\OneDrive\Documents\Master tool\api")

report = {
    "dead_python_code": [],
    "orphaned_docs": [],
    "unregistered_agents": [],
    "unreachable_workflows": [],
    "stale_config": [],
    "broken_links": [],
    "duplicate_schemas": [],
    "duplicate_prompts": [],
}

# 1. Gather all files
all_files = []
for p in Path(r"c:\Users\PC\OneDrive\Documents\Master tool").rglob("*"):
    if p.is_file() and ".git" not in p.parts and "node_modules" not in p.parts:
        all_files.append(p)

all_content = {}
for p in all_files:
    try:
        all_content[p] = p.read_text(encoding="utf-8")
    except Exception:
        pass


def is_referenced(filename):
    basename = filename.name
    for p, content in all_content.items():
        if p != filename and basename in content:
            return True
    return False


# Check orphaned docs
for p in all_files:
    if p.suffix == ".md" and "README" not in p.name:
        if not is_referenced(p):
            report["orphaned_docs"].append(str(p.relative_to(Path(r"c:\Users\PC\OneDrive\Documents\Master tool"))))

# Check unregistered agents
agents_dir = BASE / "agents"
agent_registry = BASE / "platform" / "agent_registry.yaml"
if agents_dir.exists():
    for p in agents_dir.rglob("*.md"):
        if "A" in p.name and not is_referenced(p):
            # check if agent id like A01 is referenced
            agent_id = p.name.split("_")[0]
            found = False
            for p2, content in all_content.items():
                if p2 != p and agent_id in content:
                    found = True
                    break
            if not found:
                report["unregistered_agents"].append(
                    str(p.relative_to(Path(r"c:\Users\PC\OneDrive\Documents\Master tool")))
                )

# Check unreachable workflows
workflows_dir = BASE / "workflows"
if workflows_dir.exists():
    for p in workflows_dir.rglob("*"):
        if p.is_file() and not is_referenced(p):
            report["unreachable_workflows"].append(
                str(p.relative_to(Path(r"c:\Users\PC\OneDrive\Documents\Master tool")))
            )

# Check stale config files
for p in all_files:
    if p.suffix in [".yaml", ".json"] and "package" not in p.name:
        if not is_referenced(p) and "agent_registry.yaml" not in p.name and "validate_repository" not in p.name:
            # Let's double check if it's referenced by base name
            if not is_referenced(p):
                report["stale_config"].append(str(p.relative_to(Path(r"c:\Users\PC\OneDrive\Documents\Master tool"))))

# Broken internal links
# Find all markdown links [text](path) or just paths
link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
for p, content in all_content.items():
    if p.suffix == ".md":
        for match in link_pattern.finditer(content):
            link = match.group(2)
            if link.startswith("http") or link.startswith("#"):
                continue
            # attempt to resolve
            target = (p.parent / link).resolve()
            if not target.exists():
                report["broken_links"].append(
                    {
                        "file": str(p.relative_to(Path(r"c:\Users\PC\OneDrive\Documents\Master tool"))),
                        "broken_link": link,
                    }
                )

# Duplicate schemas & prompts
schemas = {}
for p in all_files:
    if p.suffix == ".json":
        try:
            data = json.loads(all_content[p])
            if "$schema" in data or "type" in data:
                schema_str = json.dumps(data, sort_keys=True)
                if schema_str in schemas:
                    report["duplicate_schemas"].append([str(schemas[schema_str]), str(p)])
                else:
                    schemas[schema_str] = p
        except:
            pass

Path(r"c:\Users\PC\OneDrive\Documents\Master tool\audit_report.json").write_text(json.dumps(report, indent=2))
