import os

root_dir = r"c:\Users\PC\OneDrive\Documents\Master tool"

test_files = [
    "runtime/api_server.py",
    "knowledge/",
    "runtime/memory_manager.py",
    "runtime/managers/health_monitor.py",
    "observability.yaml",
    "agents/active/A05_domain_authority_agent.md",
    "platform/security.yaml",
    "policies/security_policies.yaml",
    "configuration.yaml",
    "canonical_workflow.yaml",
    "execution_workflow.md",
    "verification_workflow.md",
    "release_workflow.md",
    "recovery_workflow.md",
    "learning_workflow.md",
    "phase_12_domain_skill_packs/"
]

print("=== CHECKING SPECIFIC FILE LOCATIONS ===")
for ref in test_files:
    root_p = os.path.normpath(os.path.join(root_dir, ref))
    skill_p = os.path.normpath(os.path.join(root_dir, "ai-os-v4", "ai-os-multi-agent-skill", ref))
    v4_p = os.path.normpath(os.path.join(root_dir, "ai-os-v4", ref))
    
    if os.path.exists(root_p):
        print(f"[OK ROOT] '{ref}' exists at root: {root_p}")
    elif os.path.exists(skill_p):
        print(f"[MISALIGNED] '{ref}' -> missing 'ai-os-v4/ai-os-multi-agent-skill/' prefix! Exists at: {skill_p}")
    elif os.path.exists(v4_p):
        print(f"[MISALIGNED] '{ref}' -> missing 'ai-os-v4/' prefix! Exists at: {v4_p}")
    else:
        print(f"[NOT FOUND ANYWHERE] '{ref}'")
