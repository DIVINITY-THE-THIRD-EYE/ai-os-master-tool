import os
import json
import re

repo_root = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4"
agents_dir = os.path.join(repo_root, ".agents")

results = {}
failures = []

def log_result(check_name, status, details):
    results[check_name] = {"status": status, "details": details}
    if status == "FAIL":
        failures.append(f"[{check_name}] {details}")
    print(f"[{status}] {check_name}: {details}")

# 1. Total File Count Verification
all_files = []
for root, dirs, filenames in os.walk(repo_root):
    if ".git" in root or ".agents" in root:
        continue
    for f in filenames:
        all_files.append(os.path.join(root, f))

total_count = len(all_files)
if total_count >= 450:
    log_result("Total File Count", "PASS", f"Total files = {total_count} (>= 450 required)")
else:
    log_result("Total File Count", "FAIL", f"Total files = {total_count} (< 450 required)")

# Check Phase Folders
phase_folders = [f for f in os.listdir(repo_root) if f.startswith("phase_")]
phase_folders.sort()
print(f"Found {len(phase_folders)} phase folders: {phase_folders}")
if len(phase_folders) == 16:
    log_result("Phase Directory Count", "PASS", f"Found 16 phase directories")
else:
    log_result("Phase Directory Count", "FAIL", f"Found {len(phase_folders)} phase directories (expected 16)")

# Phase 00 Foundation
p0_dir = os.path.join(repo_root, "phase_00_foundation")
p0_files = [f for root, dirs, filenames in os.walk(p0_dir) for f in filenames]
p0_count = len(p0_files)
if p0_count >= 20:
    log_result("Phase 00 File Count", "PASS", f"Files = {p0_count} (>= 20)")
else:
    log_result("Phase 00 File Count", "FAIL", f"Files = {p0_count} (< 20)")

conventions_path = os.path.join(p0_dir, "CONVENTIONS.md")
if os.path.exists(conventions_path):
    with open(conventions_path, "r", encoding="utf-8") as f:
        conv_text = f.read()
    required_keywords = ["naming", "directory", "metadata", "file format"]
    missing_kw = []
    for kw in required_keywords:
        if kw.lower() not in conv_text.lower():
            missing_kw.append(kw)
    if not missing_kw:
        log_result("Phase 00 CONVENTIONS.md", "PASS", "Explicitly defines naming convention, directory convention, metadata standard, and file format standard")
    else:
        log_result("Phase 00 CONVENTIONS.md", "FAIL", f"Missing explicit standards for: {missing_kw}")
else:
    log_result("Phase 00 CONVENTIONS.md", "FAIL", "CONVENTIONS.md file not found in phase_00_foundation")

# Phase 01 Core Runtime
p1_dir = os.path.join(repo_root, "phase_01_core_runtime")
p1_files = [f for root, dirs, filenames in os.walk(p1_dir) for f in filenames]
p1_count = len(p1_files)
if p1_count >= 40:
    log_result("Phase 01 File Count", "PASS", f"Files = {p1_count} (>= 40)")
else:
    log_result("Phase 01 File Count", "FAIL", f"Files = {p1_count} (< 40)")

# Phase 02 Agent Framework
p2_dir = os.path.join(repo_root, "phase_02_agent_framework")
p2_spec_files = []
p2_prompt_files = []

for root, dirs, filenames in os.walk(p2_dir):
    for f in filenames:
        path = os.path.join(root, f)
        if "spec" in f.lower() or "agent" in f.lower():
            if "prompt" in f.lower() or "prompt" in root.lower():
                p2_prompt_files.append(path)
            else:
                p2_spec_files.append(path)
        elif "prompt" in f.lower() or "prompt" in root.lower():
            p2_prompt_files.append(path)

# Let's inspect phase_02 structure specifically
p2_all_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p2_dir) for f in filenames]
p2_specs = [f for f in p2_all_files if f.endswith(".md") and ("spec" in os.path.basename(f).lower() or "_agent.md" in os.path.basename(f).lower()) and "prompt" not in os.path.basename(f).lower()]
p2_prompts = [f for f in p2_all_files if f.endswith(".md") and "prompt" in os.path.basename(f).lower()]

print(f"P2 Total Files: {len(p2_all_files)}")
print(f"P2 Specs: {len(p2_specs)}")
print(f"P2 Prompts: {len(p2_prompts)}")

required_11_sections = [
    "Role", "Mission", "Authority", "Responsibilities", "Inputs", "Outputs",
    "Decision Rules", "Escalation Rules", "Quality Metrics", "Prompt", "Examples"
]

missing_sections_by_spec = {}
for spec_path in p2_specs:
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = []
    for sec in required_11_sections:
        # Check for header like # Role, ## Role, ### Role, **Role**, or Role:
        pattern = r"(?i)(#+\s*|\*\*|^\s*)" + re.escape(sec) + r"(\*\*|:|\s*$|\n)"
        if not re.search(pattern, content, re.MULTILINE):
            missing.append(sec)
    if missing:
        missing_sections_by_spec[os.path.basename(spec_path)] = missing

if len(p2_all_files) == 70 and len(p2_specs) == 35 and len(p2_prompts) == 35:
    log_result("Phase 02 File Counts", "PASS", f"Exactly 35 spec files + 35 prompt files (70 total)")
else:
    log_result("Phase 02 File Counts", "FAIL", f"Total files = {len(p2_all_files)}, Specs = {len(p2_specs)}, Prompts = {len(p2_prompts)} (expected 35 specs + 35 prompts = 70 total)")

if not missing_sections_by_spec:
    log_result("Phase 02 Spec Sections", "PASS", f"ALL {len(p2_specs)} spec files contain all 11 required sections")
else:
    log_result("Phase 02 Spec Sections", "FAIL", f"Specs missing required sections: {missing_sections_by_spec}")

# Phase 03 Prompt Library
p3_dir = os.path.join(repo_root, "phase_03_prompt_library")
p3_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p3_dir) for f in filenames if f.endswith('.md') or f.endswith('.txt') or f.endswith('.prompt')]
p3_subdirs = [os.path.join(p3_dir, d) for d in os.listdir(p3_dir) if os.path.isdir(os.path.join(p3_dir, d))]

p3_short_prompts = []
for pf in p3_files:
    with open(pf, "r", encoding="utf-8") as f:
        text = f.read()
    word_count = len(text.split())
    if word_count < 200:
        p3_short_prompts.append((os.path.basename(pf), word_count))

if len(p3_files) >= 120 and len(p3_subdirs) >= 20:
    log_result("Phase 03 Count & Subdirs", "PASS", f"Prompts = {len(p3_files)} (>= 120), Subdirectories = {len(p3_subdirs)} (>= 20)")
else:
    log_result("Phase 03 Count & Subdirs", "FAIL", f"Prompts = {len(p3_files)} (expected >= 120), Subdirectories = {len(p3_subdirs)} (expected >= 20)")

if not p3_short_prompts:
    log_result("Phase 03 Word Count", "PASS", f"All {len(p3_files)} prompt files contain >= 200 words")
else:
    log_result("Phase 03 Word Count", "FAIL", f"{len(p3_short_prompts)} prompt files have < 200 words. Sample: {p3_short_prompts[:5]}")

# Phase 04 Workflow Library
p4_dir = os.path.join(repo_root, "phase_04_workflow_library")
p4_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p4_dir) for f in filenames]
if len(p4_files) >= 50:
    log_result("Phase 04 File Count", "PASS", f"Workflow files = {len(p4_files)} (>= 50)")
else:
    log_result("Phase 04 File Count", "FAIL", f"Workflow files = {len(p4_files)} (< 50)")

# Phase 05 Knowledge Platform
p5_dir = os.path.join(repo_root, "phase_05_knowledge_platform")
p5_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p5_dir) for f in filenames]
if len(p5_files) >= 12:
    log_result("Phase 05 File Count", "PASS", f"Files = {len(p5_files)} (>= 12)")
else:
    log_result("Phase 05 File Count", "FAIL", f"Files = {len(p5_files)} (< 12)")

# Phase 06 Memory System
p6_dir = os.path.join(repo_root, "phase_06_memory_system")
p6_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p6_dir) for f in filenames]
if len(p6_files) >= 10:
    log_result("Phase 06 File Count", "PASS", f"Files = {len(p6_files)} (>= 10)")
else:
    log_result("Phase 06 File Count", "FAIL", f"Files = {len(p6_files)} (< 10)")

# Phase 07 Decision Engine
p7_dir = os.path.join(repo_root, "phase_07_decision_engine")
p7_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p7_dir) for f in filenames]
if len(p7_files) >= 10:
    log_result("Phase 07 File Count", "PASS", f"Files = {len(p7_files)} (>= 10)")
else:
    log_result("Phase 07 File Count", "FAIL", f"Files = {len(p7_files)} (< 10)")

# Phase 08 Reflection & Learning
p8_dir = os.path.join(repo_root, "phase_08_reflection_learning") if os.path.exists(os.path.join(repo_root, "phase_08_reflection_learning")) else os.path.join(repo_root, "phase_08_reflection_and_learning")
p8_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p8_dir) for f in filenames] if os.path.exists(p8_dir) else []
if len(p8_files) >= 10:
    log_result("Phase 08 File Count", "PASS", f"Files = {len(p8_files)} (>= 10)")
else:
    log_result("Phase 08 File Count", "FAIL", f"Files = {len(p8_files)} (< 10)")

# Phase 09 Verification Platform
p9_dir = os.path.join(repo_root, "phase_09_verification_platform")
p9_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p9_dir) for f in filenames]
if len(p9_files) >= 12:
    log_result("Phase 09 File Count", "PASS", f"Files = {len(p9_files)} (>= 12)")
else:
    log_result("Phase 09 File Count", "FAIL", f"Files = {len(p9_files)} (< 12)")

# Phase 10 Template Library
p10_dir = os.path.join(repo_root, "phase_10_template_library")
p10_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p10_dir) for f in filenames]
if len(p10_files) >= 60:
    log_result("Phase 10 File Count", "PASS", f"Files = {len(p10_files)} (>= 60)")
else:
    log_result("Phase 10 File Count", "FAIL", f"Files = {len(p10_files)} (< 60)")

# Phase 11 Schemas
p11_dir = os.path.join(repo_root, "phase_11_schemas")
p11_schema_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p11_dir) for f in filenames if f.endswith(".json")]

invalid_json = []
missing_schema_keys = []

for sf in p11_schema_files:
    try:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
        required_keys = ["$schema", "title", "type", "properties"]
        missing_k = [k for k in required_keys if k not in data]
        if missing_k:
            missing_schema_keys.append((os.path.basename(sf), missing_k))
    except Exception as e:
        invalid_json.append((os.path.basename(sf), str(e)))

if len(p11_schema_files) >= 40:
    log_result("Phase 11 Schema Count", "PASS", f"JSON Schema files = {len(p11_schema_files)} (>= 40)")
else:
    log_result("Phase 11 Schema Count", "FAIL", f"JSON Schema files = {len(p11_schema_files)} (< 40)")

if not invalid_json:
    log_result("Phase 11 Valid JSON", "PASS", f"All {len(p11_schema_files)} JSON schema files are valid JSON")
else:
    log_result("Phase 11 Valid JSON", "FAIL", f"Invalid JSON files: {invalid_json}")

if not missing_schema_keys:
    log_result("Phase 11 Required Fields", "PASS", "ALL schema files contain $schema, title, type, and properties")
else:
    log_result("Phase 11 Required Fields", "FAIL", f"Schema files missing required keys: {missing_schema_keys}")

# Phase 12 Domain Skill Packs
p12_dir = os.path.join(repo_root, "phase_12_domain_skill_packs")
p12_domain_dirs = [os.path.join(p12_dir, d) for d in os.listdir(p12_dir) if os.path.isdir(os.path.join(p12_dir, d))]

required_subdirs = ["agents", "prompts", "templates", "policies", "workflows", "knowledge", "verification", "examples"]
domains_with_insufficient_subdirs = {}

for domain_path in p12_domain_dirs:
    domain_name = os.path.basename(domain_path)
    subdirs = [d for d in os.listdir(domain_path) if os.path.isdir(os.path.join(domain_path, d))]
    matching_subdirs = [req for req in required_subdirs if req in subdirs]
    if len(matching_subdirs) < 7:
        domains_with_insufficient_subdirs[domain_name] = f"Found {len(matching_subdirs)} of 8: {matching_subdirs}"

if len(p12_domain_dirs) == 18:
    log_result("Phase 12 Domain Directory Count", "PASS", f"EXACTLY 18 domain subdirectories found")
else:
    log_result("Phase 12 Domain Directory Count", "FAIL", f"Found {len(p12_domain_dirs)} domain subdirectories (expected EXACTLY 18)")

if not domains_with_insufficient_subdirs:
    log_result("Phase 12 Subdirectory Compliance", "PASS", f"EVERY domain subdirectory contains at minimum 7 of the 8 required subdirectories")
else:
    log_result("Phase 12 Subdirectory Compliance", "FAIL", f"Domains with < 7 required subdirectories: {domains_with_insufficient_subdirs}")

# Phase 13 Plugin Framework
p13_dir = os.path.join(repo_root, "phase_13_plugin_framework")
p13_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p13_dir) for f in filenames]
if len(p13_files) >= 10:
    log_result("Phase 13 File Count", "PASS", f"Files = {len(p13_files)} (>= 10)")
else:
    log_result("Phase 13 File Count", "FAIL", f"Files = {len(p13_files)} (< 10)")

# Phase 14 Runtime Policies
p14_dir = os.path.join(repo_root, "phase_14_runtime_policies")
p14_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p14_dir) for f in filenames]
if len(p14_files) >= 10:
    log_result("Phase 14 File Count", "PASS", f"Files = {len(p14_files)} (>= 10)")
else:
    log_result("Phase 14 File Count", "FAIL", f"Files = {len(p14_files)} (< 10)")

# Phase 15 Enterprise Documentation
p15_dir = os.path.join(repo_root, "phase_15_enterprise_documentation")
p15_files = [os.path.join(root, f) for root, dirs, filenames in os.walk(p15_dir) for f in filenames]
if len(p15_files) >= 12:
    log_result("Phase 15 File Count", "PASS", f"Files = {len(p15_files)} (>= 12)")
else:
    log_result("Phase 15 File Count", "FAIL", f"Files = {len(p15_files)} (< 12)")

# Content Quality & Integrity Check (Empty, Placeholders, Fake Implementation)
empty_files = []
placeholder_files = []

placeholder_patterns = [
    r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"\bLOREM IPSUM\b", r"\[INSERT HERE\]", r"\[STUB\]", r"\bPLACEHOLDER\b"
]

for file_path in all_files:
    rel_path = os.path.relpath(file_path, repo_root)
    # Check 0-byte empty files
    size = os.path.getsize(file_path)
    if size == 0:
        empty_files.append(rel_path)
        continue
    
    # Read text content to scan for suspicious placeholder strings
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        # If file is very small (< 50 bytes), check if it's substantive
        if len(text.strip()) == 0:
            empty_files.append(rel_path)
            continue
            
        # Scan for explicit placeholder markers
        for pat in placeholder_patterns:
            if re.search(pat, text, re.IGNORECASE):
                # Allow if it's documented in a convention or schema explanation, but flag suspicious usages
                placeholder_files.append((rel_path, pat))
                break
    except Exception as e:
        pass

if not empty_files:
    log_result("Zero Empty Files Check", "PASS", "No empty (0-byte) files found")
else:
    log_result("Zero Empty Files Check", "FAIL", f"Found {len(empty_files)} empty files: {empty_files}")

if not placeholder_files:
    log_result("Zero Placeholder Files Check", "PASS", "No explicit placeholder markers (TODO, TBD, FIXME, etc.) found")
else:
    log_result("Zero Placeholder Files Check", "FAIL", f"Found {len(placeholder_files)} files with placeholder patterns. Sample: {placeholder_files[:10]}")

print("========================================")
if failures:
    print(f"VERDICT: INTEGRITY VIOLATION ({len(failures)} failures)")
    for f in failures:
        print(f"  - {f}")
else:
    print("VERDICT: CLEAN")
