import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

readme_path = r"c:\Users\PC\OneDrive\Documents\Master tool\README.md"
root_dir = r"c:\Users\PC\OneDrive\Documents\Master tool"

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== 1. MARKDOWN HYPERLINKS [text](link) ===")
markdown_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
broken_markdown_links = []
valid_markdown_links = []

for text, link in markdown_links:
    if link.startswith("http://") or link.startswith("https://"):
        valid_markdown_links.append((text, link, "URL"))
    elif link.startswith("#"):
        valid_markdown_links.append((text, link, "ANCHOR"))
    else:
        full_path = os.path.normpath(os.path.join(root_dir, link))
        exists = os.path.exists(full_path)
        if exists:
            valid_markdown_links.append((text, link, f"EXISTS"))
        else:
            broken_markdown_links.append((text, link, full_path))

print(f"Total markdown links: {len(markdown_links)}")
print(f"Valid markdown links: {len(valid_markdown_links)}")
print(f"Broken markdown links: {len(broken_markdown_links)}")
for text, link, err in broken_markdown_links:
    print(f"  BROKEN MARKDOWN LINK: [{text}]({link}) -> {err}")

print("\n=== 2. CAPABILITY MATRIX TABLE PATH AUDIT ===")
section_5_start = content.find("## 5. Capability / Implementation Matrix")
section_6_start = content.find("## 6. Architecture")
matrix_text = content[section_5_start:section_6_start]

matrix_lines = matrix_text.splitlines()
matrix_path_issues = []

for line in matrix_lines:
    if line.startswith("|") and not line.startswith("| Subsystem") and not line.startswith("|---"):
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 4:
            subsystem = parts[0]
            status = parts[2]
            source = parts[3]
            code_spans = re.findall(r"`([^`]+)`", source)
            for cs in code_spans:
                raw_paths = re.split(r"\s+&\s+|\s+", cs)
                for rp in raw_paths:
                    rp = rp.strip()
                    if not rp or rp in ("&", "and", "static", "markdown"):
                        continue
                    if rp.endswith("/") or rp.endswith(".py") or rp.endswith(".yaml") or rp.endswith(".json") or rp.endswith(".toml") or rp.endswith(".md"):
                        full_path = os.path.normpath(os.path.join(root_dir, rp))
                        if not os.path.exists(full_path):
                            matrix_path_issues.append({
                                "subsystem": subsystem,
                                "status": status,
                                "referenced_path": rp,
                                "full_path": full_path
                            })

print(f"Total Section 5 path references checked: {len(matrix_path_issues)} issues found.")
for issue in matrix_path_issues:
    print(f"  [Matrix Path Issue] Subsystem: '{issue['subsystem']}' | Status: '{issue['status']}' | Referenced: '{issue['referenced_path']}' -> NOT FOUND AT '{issue['full_path']}'")

print("\n=== 3. ALL SINGLE-LINE BACKTICK PATHS ACROSS ENTIRE README ===")
backtick_spans = re.findall(r"`([^`\n]+)`", content)
all_path_issues = []

for cs in set(backtick_spans):
    cs = cs.strip()
    if ("/" in cs or "\\" in cs) and not cs.startswith("http") and not cs.startswith("pip ") and not cs.startswith("python ") and not cs.startswith("git ") and not cs.startswith("pre-commit") and not cs.startswith("POST") and not cs.startswith("GET"):
        if "<" in cs or "YYYY" in cs or cs.startswith("http://") or cs.startswith("https://"):
            continue
        tokens = [t.strip() for t in re.split(r"\s+&\s+|\s+", cs) if t.strip()]
        for tok in tokens:
            if (tok.endswith("/") or tok.endswith(".py") or tok.endswith(".yaml") or tok.endswith(".json") or tok.endswith(".toml") or tok.endswith(".txt") or tok.endswith(".md") or tok.endswith(".db")) and not tok.startswith("http"):
                full_path = os.path.normpath(os.path.join(root_dir, tok))
                if not os.path.exists(full_path):
                    all_path_issues.append((cs, tok, full_path))

print(f"Total backtick path issues found across whole README: {len(all_path_issues)}")
for original_cs, tok, full_p in sorted(set(all_path_issues)):
    print(f"  [Unresolved Path] Text: `{original_cs}` | Token: `{tok}` | Target: {full_p}")
