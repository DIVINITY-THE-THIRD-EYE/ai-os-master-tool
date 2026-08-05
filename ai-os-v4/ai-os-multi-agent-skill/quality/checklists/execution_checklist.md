# Execution Checklist (Gate 3)

**Responsible Agent:** A06 (Worker Agent)
**Gate:** Gate 3 (Worker Self-Validation Gate)

## Before Starting Work
- [ ] Task assignment received and parsed — **Blocking**
- [ ] Worker context loaded from A02 — **Blocking**
- [ ] All dependencies available in Artifact Store — **Blocking**
- [ ] Tool permissions verified — **Blocking**
- [ ] Acceptance criteria reviewed — **Blocking**

## During Execution
- [ ] Work is following coding standards from knowledge/best_practices/coding_standards.md — **Blocking**
- [ ] Progress events published to Event Bus at each milestone — **Advisory**
- [ ] No hardcoded secrets, credentials, or API keys — **Blocking**
- [ ] Dependencies are declared and version-pinned — **Blocking**

## Artifact Production
- [ ] All required artifacts produced — **Blocking**
- [ ] Each artifact has complete metadata: id, version, type, trace_id, task_id — **Blocking**
- [ ] Each artifact stored in Artifact Store immediately upon creation — **Blocking**
- [ ] artifact.generated event published for each artifact — **Blocking**

## Self-Validation
- [ ] Output satisfies all acceptance criteria — **Blocking**
- [ ] Linting passes with zero errors — **Blocking**
- [ ] Unit tests pass where applicable — **Blocking**
- [ ] Documentation present and complete — **Blocking**
- [ ] No secrets present in any output file — **Blocking**
- [ ] Self-validation report produced — **Blocking**
- [ ] self_validation.completed event published — **Blocking**
