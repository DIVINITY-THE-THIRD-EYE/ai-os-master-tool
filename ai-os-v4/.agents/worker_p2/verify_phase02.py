import glob
import os

SPECS_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_02_agent_framework\specs"
PROMPTS_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_02_agent_framework\prompts"

REQUIRED_SECTIONS = [
    "## 1. Role",
    "## 2. Mission",
    "## 3. Authority",
    "## 4. Responsibilities",
    "## 5. Inputs",
    "## 6. Outputs",
    "## 7. Decision Rules",
    "## 8. Escalation Rules",
    "## 9. Quality Metrics",
    "## 10. Prompt",
    "## 11. Examples",
]

spec_files = glob.glob(os.path.join(SPECS_DIR, "*.md"))
prompt_files = glob.glob(os.path.join(PROMPTS_DIR, "*.md"))

print(f"Spec files found: {len(spec_files)}")
print(f"Prompt files found: {len(prompt_files)}")
print(f"Total files: {len(spec_files) + len(prompt_files)}")

assert len(spec_files) == 35, f"Expected 35 spec files, found {len(spec_files)}"
assert len(prompt_files) == 35, f"Expected 35 prompt files, found {len(prompt_files)}"

# Check spec file sections
spec_errors = 0
for spec in sorted(spec_files):
    filename = os.path.basename(spec)
    with open(spec, "r", encoding="utf-8") as f:
        content = f.read()

    missing = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing.append(section)

    if missing:
        print(f"FAIL: {filename} missing sections: {missing}")
        spec_errors += 1

# Check prompt word counts
prompt_errors = 0
for prompt in sorted(prompt_files):
    filename = os.path.basename(prompt)
    with open(prompt, "r", encoding="utf-8") as f:
        content = f.read()

    words = len(content.split())
    if words < 200:
        print(f"FAIL: {filename} word count is {words} (< 200 words)")
        prompt_errors += 1

print(f"Spec errors: {spec_errors}")
print(f"Prompt errors: {prompt_errors}")

if spec_errors == 0 and prompt_errors == 0:
    print("SUCCESS: ALL 70 PHASE 02 FILES VERIFIED PERFECTLY!")
else:
    print("VERIFICATION FAILED! Please fix issues above.")
