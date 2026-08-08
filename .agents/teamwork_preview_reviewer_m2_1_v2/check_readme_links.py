import os
import re

root_dir = r"c:\Users\PC\OneDrive\Documents\Master tool"
readme_path = os.path.join(root_dir, "README.md")

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

print("==================================================")
print("1. VERIFYING TOC ANCHOR LINKS")
print("==================================================")

# Extract HTML anchors <a id="..."></a>
html_anchors = set(re.findall(r'<a\s+id="([^"]+)"></a>', text))
print(f"Found {len(html_anchors)} HTML anchors in README.md.")

# Extract all section headers
headers = []
for line in lines:
    if line.startswith("#"):
        # standard header anchor generation slug: lowercase, replace spaces with hyphens, remove special chars
        clean_header = line.lstrip("#").strip()
        headers.append(clean_header)

# Extract markdown links of form [Text](#anchor)
toc_links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', text)
print(f"Found {len(toc_links)} TOC anchor links in README.md.")

broken_toc = []
for text_label, anchor in toc_links:
    if anchor in html_anchors:
        continue
    # check if anchor matches header slug
    slug = re.sub(r'[^\w\- ]', '', text_label.lower()).replace(' ', '-')
    if anchor == slug:
        continue
    broken_toc.append((text_label, anchor))

if broken_toc:
    print(f"FAILED: Found {len(broken_toc)} broken TOC links:")
    for label, anchor in broken_toc:
        print(f"  - [{label}](#{anchor})")
else:
    print("SUCCESS: All TOC anchor links resolve cleanly to HTML anchors or headers!")

print("\n==================================================")
print("2. VERIFYING RELATIVE FILE/DIRECTORY PATHS")
print("==================================================")

# Extract markdown links [text](path) where path does not start with http or #
markdown_path_links = []
for line_idx, line in enumerate(lines, 1):
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
    for text_label, target in links:
        if not target.startswith("http") and not target.startswith("#"):
            markdown_path_links.append((line_idx, text_label, target))

print(f"Found {len(markdown_path_links)} Markdown relative path links.")

missing_markdown_paths = []
for line_idx, label, target in markdown_path_links:
    clean_target = target.split("#")[0]
    if not clean_target:
        continue
    abs_path = os.path.normpath(os.path.join(root_dir, clean_target))
    if not os.path.exists(abs_path):
        missing_markdown_paths.append((line_idx, label, target, abs_path))

if missing_markdown_paths:
    print(f"FAILED: Found {len(missing_markdown_paths)} broken Markdown path links:")
    for line_idx, label, target, abs_path in missing_markdown_paths:
        print(f"  Line {line_idx}: [{label}]({target}) -> {abs_path} does not exist!")
else:
    print("SUCCESS: All Markdown relative path links resolve to existing files/dirs on disk!")

print("\n==================================================")
print("3. VERIFYING ALL FILE PATH BACKTICK REFERENCES")
print("==================================================")

backtick_file_paths = []
for line_idx, line in enumerate(lines, 1):
    spans = re.findall(r"`([^`]+)`", line)
    for span in spans:
        # Check if span looks like a file/directory path within the project repo
        # Exclude commands, http, route patterns, tutorial placeholders, python code snippets
        if ("/" in span or "\\" in span or span.endswith((".py", ".yaml", ".yml", ".json", ".md", ".txt", ".toml", ".db"))):
            # filter out non-paths
            if any(span.startswith(x) for x in ["http", "POST", "GET", "v1/", "http:", "pip ", "python ", "git ", "npm ", "pytest", "curl"]):
                continue
            if span in ["/v1/health", "/v1/tasks", "/v1/tasks/{task_id}", "/v1/agents", "/v1/events", "/v1/usage", "/v1/(.*)", "/api/index.py", "/api/(.*)", "/index.html", "/tmp/local_os_state.db", "@vercel/python", "@vercel/static", "/(.*)"]:
                continue
            if span.startswith("feature/") or span.startswith(".venv") or span.startswith("backups/") or span.startswith("snapshots/"):
                continue
            # Tutorial placeholders explicitly noted in README
            if span in ["ai-os-v4/ai-os-multi-agent-skill/agents/active/A14_new_agent.md", "ai-os-v4/ai-os-multi-agent-skill/workflows/custom_workflow.yaml"]:
                print(f"Line {line_idx}: Instructional tutorial path `{span}` (Expected non-file placeholder)")
                continue

            backtick_file_paths.append((line_idx, span))

missing_backticks = []
for line_idx, span in backtick_file_paths:
    clean_span = span.split("#")[0]
    abs_path = os.path.normpath(os.path.join(root_dir, clean_span))
    if not os.path.exists(abs_path):
        missing_backticks.append((line_idx, span, abs_path))

if missing_backticks:
    print(f"FAILED: Found {len(missing_backticks)} missing file paths in backtick references:")
    for line_idx, span, abs_path in missing_backticks:
        print(f"  Line {line_idx}: `{span}` -> {abs_path} does not exist!")
else:
    print("SUCCESS: All project file paths in backtick references exist on disk!")
