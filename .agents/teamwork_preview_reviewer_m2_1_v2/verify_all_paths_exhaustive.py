import os
import re

root_dir = r"c:\Users\PC\OneDrive\Documents\Master tool"
readme_path = os.path.join(root_dir, "README.md")

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

# Gather all backtick references and markdown links
paths_to_verify = []

for line_num, line in enumerate(lines, 1):
    # backticks
    backticks = re.findall(r"`([^`]+)`", line)
    for b in backticks:
        if any(b.startswith(prefix) for prefix in ["ai-os-v4/", "requirements", "pyproject", ".env", "vercel", ".gitignore", "api/", "README", "SKILL"]):
            paths_to_verify.append((line_num, b))

print(f"Total specific path references to verify: {len(paths_to_verify)}")

missing = []
for line_num, p in paths_to_verify:
    # exclude tutorial non-existing placeholders
    if p in ["ai-os-v4/ai-os-multi-agent-skill/agents/active/A14_new_agent.md", "ai-os-v4/ai-os-multi-agent-skill/workflows/custom_workflow.yaml"]:
        print(f"Line {line_num}: Tutorial placeholder `{p}` (OK)")
        continue
    # handle line with python command
    clean_p = p.replace("python ", "").replace("pip install -r ", "").strip()
    full_path = os.path.normpath(os.path.join(root_dir, clean_p))
    if not os.path.exists(full_path):
        missing.append((line_num, p, full_path))
    else:
        print(f"Line {line_num}: `{p}` -> EXISTS")

if missing:
    print(f"\nFAILED: {len(missing)} missing paths found:")
    for line_num, p, full_path in missing:
        print(f"  Line {line_num}: `{p}` -> {full_path}")
else:
    print(f"\nSUCCESS: All {len(paths_to_verify)} relative path references exist on disk!")
