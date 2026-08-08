import os
import re

root_dir = r"c:\Users\PC\OneDrive\Documents\Master tool"
readme_path = os.path.join(root_dir, "README.md")

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

print("=== CHECKING ALL BACKTICK PATHS ACROSS ENTIRE README ===")

path_refs = []
for line_idx, line in enumerate(lines, 1):
    spans = re.findall(r"`([^`]+)`", line)
    for span in spans:
        # Check if span looks like a file/directory path
        if "/" in span or "\\" in span or span.endswith((".py", ".yaml", ".yml", ".json", ".md", ".txt", ".toml", ".db")):
            # Ignore command calls or URLs or APIs
            if any(span.startswith(x) for x in ["http", "POST", "GET", "v1/", "http:"]):
                continue
            if span.startswith(".venv") or span.startswith("backups/") or span.startswith("snapshots/") or span.startswith("feature/"):
                continue
            path_refs.append((line_idx, span))

print(f"Total path references found: {len(path_refs)}")

missing_count = 0
misaligned_count = 0

for line_idx, span in path_refs:
    clean = span.split("#")[0]
    full_root = os.path.normpath(os.path.join(root_dir, clean))
    exists_root = os.path.exists(full_root)
    
    full_skill = os.path.normpath(os.path.join(root_dir, "ai-os-v4", "ai-os-multi-agent-skill", clean))
    exists_skill = os.path.exists(full_skill)
    
    if exists_root:
        pass # print(f"LINE {line_idx:3d} [OK] `{span}`")
    elif exists_skill:
        misaligned_count += 1
        print(f"LINE {line_idx:3d} [MISALIGNED] `{span}` -> Not at repo root! Exists at `ai-os-v4/ai-os-multi-agent-skill/{clean}`")
    else:
        missing_count += 1
        print(f"LINE {line_idx:3d} [MISSING] `{span}` -> File/dir does not exist anywhere!")

print(f"\nSummary of Path Analysis:")
print(f"  Valid paths from root: {len(path_refs) - misaligned_count - missing_count}")
print(f"  Misaligned relative paths (missing `ai-os-v4/ai-os-multi-agent-skill/` prefix): {misaligned_count}")
print(f"  Completely missing paths: {missing_count}")
