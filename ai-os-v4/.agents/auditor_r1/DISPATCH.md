## 2026-08-05T15:46:54Z
Perform a comprehensive Forensic Integrity & Quality Audit of the entire AI OS v4 repository (`c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\`).

Verify all acceptance criteria from `ORIGINAL_REQUEST.md`:

1. **Total File Count Verification**:
   - Verify overall repository file count (must be ≥ 450 files).
   - Check every phase folder (`phase_00_foundation` through `phase_15_enterprise_documentation`).

2. **Phase Specific Audits**:
   - **Phase 00 Foundation**: Check for ≥ 20 files and verify `CONVENTIONS.md` explicitly defines naming convention, directory convention, metadata standard, and file format standard.
   - **Phase 01 Core Runtime**: Check for ≥ 40 files across kernel, messaging, scheduler, safety/health subsystems.
   - **Phase 02 Agent Framework**: Check for EXACTLY 35 spec files + 35 corresponding prompt files (70 files total). Verify EVERY spec file contains ALL 11 required sections (Role, Mission, Authority, Responsibilities, Inputs, Outputs, Decision Rules, Escalation Rules, Quality Metrics, Prompt, Examples).
   - **Phase 03 Prompt Library**: Check for ≥ 120 prompt files across 20 domain subdirectories. Verify prompt files contain substantive prompt content (≥ 200 words each).
   - **Phase 04 Workflow Library**: Check for ≥ 50 workflow files with complete step-by-step processes.
   - **Phase 05 Knowledge Platform**: Check for ≥ 12 files.
   - **Phase 06 Memory System**: Check for ≥ 10 files.
   - **Phase 07 Decision Engine**: Check for ≥ 10 files.
   - **Phase 08 Reflection & Learning**: Check for ≥ 10 files.
   - **Phase 09 Verification Platform**: Check for ≥ 12 files.
   - **Phase 10 Template Library**: Check for ≥ 60 document templates.
   - **Phase 11 Schemas**: Check for ≥ 40 JSON schema files (`.json`), verify valid JSON, and verify `$schema`, `title`, `type`, and `properties` fields are present in every file.
   - **Phase 12 Domain Skill Packs**: Check for EXACTLY 18 domain subdirectories. Verify EVERY domain subdirectory contains at minimum 7 of the 8 required subdirectories (`agents/`, `prompts/`, `templates/`, `policies/`, `workflows/`, `knowledge/`, `verification/`, `examples/`).
   - **Phase 13 Plugin Framework**: Check for ≥ 10 files.
   - **Phase 14 Runtime Policies**: Check for ≥ 10 files.
   - **Phase 15 Enterprise Documentation**: Check for ≥ 12 files.

3. **Content Quality & Integrity Verification**:
   - Confirm there are zero placeholder files, zero empty files, and zero fake implementations.

Write your findings, exact counts, sample checks, and final verdict (`CLEAN` or `INTEGRITY VIOLATION`) to `c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\.agents\auditor_r1\handoff.md`.
Then send a completion message to the parent orchestrator.
