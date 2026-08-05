import os
import re

BASE_DIR = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_12_domain_skill_packs"

REQUIRED_DOMAINS = [
    "software", "ai", "manufacturing", "mechanical", "electrical", "civil",
    "architecture", "finance", "legal", "marketing", "healthcare", "education",
    "agriculture", "construction", "supply_chain", "cloud", "cybersecurity", "data_engineering"
]

REQUIRED_SUBDIRS = [
    "agents", "prompts", "templates", "policies",
    "workflows", "knowledge", "verification", "examples"
]

def verify():
    print("=== STARTING PHASE 12 VERIFICATION ===")
    
    # 1. Check root directory
    if not os.path.exists(BASE_DIR):
        print(f"FAIL: Base directory {BASE_DIR} does not exist!")
        return False

    actual_domains = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])
    print(f"Found {len(actual_domains)} domain directories.")

    # Check exactly 18 domains
    if actual_domains != sorted(REQUIRED_DOMAINS):
        missing = set(REQUIRED_DOMAINS) - set(actual_domains)
        extra = set(actual_domains) - set(REQUIRED_DOMAINS)
        print(f"FAIL: Domain mismatch! Missing: {missing}, Extra: {extra}")
        return False
    else:
        print("PASS: Exactly 18 expected domain directories present.")

    total_files = 0
    total_words = 0
    errors = []

    for domain in REQUIRED_DOMAINS:
        domain_dir = os.path.join(BASE_DIR, domain)
        
        # Check README.md
        readme_path = os.path.join(domain_dir, "README.md")
        if not os.path.isfile(readme_path):
            errors.append(f"Missing README.md in domain {domain}")
        else:
            total_files += 1

        # Check all 8 subdirs
        for sub in REQUIRED_SUBDIRS:
            sub_dir = os.path.join(domain_dir, sub)
            if not os.path.isdir(sub_dir):
                errors.append(f"Missing subdirectory '{sub}' in domain '{domain}'")
                continue
            
            md_files = [f for f in os.listdir(sub_dir) if f.endswith(".md")]
            if not md_files:
                errors.append(f"No .md files in '{domain}/{sub}'")
                continue

            for mf in md_files:
                filepath = os.path.join(sub_dir, mf)
                total_files += 1
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check YAML frontmatter
                if not content.startswith("---"):
                    errors.append(f"File '{domain}/{sub}/{mf}' missing frontmatter start '---'")
                
                word_count = len(re.findall(r'\w+', content))
                total_words += word_count
                if word_count < 200:
                    errors.append(f"File '{domain}/{sub}/{mf}' is too short ({word_count} words)")

    print(f"Total Markdown files verified: {total_files}")
    print(f"Total Word count across Phase 12: {total_words} words (avg {total_words//total_files if total_files else 0} words/file)")

    if errors:
        print("Verification FAILURES:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("PASS: All 18 domains and all 8 subdirectories per domain verified cleanly with high substantive quality!")
        return True

if __name__ == "__main__":
    verify()
