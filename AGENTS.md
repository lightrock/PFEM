# AGENTS.md

This repository is PFEM: Polycentric Federated Evidence Mesh.

Before editing, read:

- `docs/AI_START_HERE.md`
- `docs/architecture/neutral-language.md`
- `docs/architecture/architecture-stack.md`
- `docs/architecture/evidence-lifecycle.md`
- `ai/architecture-rules.md`
- `ai/adapter-rules.md`
- `ai/evidence-rules.md`
- `ai/node-profile-rules.md`
- `ai/review-checklist.md`

Core rules:

- Use neutral deployment-shape language.
- Do not name specific customers, agencies, sponsors, programs, or private deployments in public repository files.
- Keep raw evidence, normalized observations, findings, alerts, evidence packages, rollups, and reports separate.
- Adapters translate source-specific inputs into PFEM contracts; adapters do not own policy.
- Profiles configure deployment shape; profiles do not fork the product.
- Schemas define contracts; code should follow schemas.
- Reports and dashboards are outputs, not source evidence.
- Do not add infrastructure, databases, queues, identity systems, or background services unless the architecture docs justify it.

When unsure, make the smallest doctrine-preserving change and explain the boundary affected.

# PFEM Agent Instructions

Before making PFEM changes, read:

```text
docs/developer/pfem-boundary-language-generation-standard.md
docs/developer/pfem-new-chat-handoff.md
docs/developer/pfem-terminal-tail-stabilization.md
docs/developer/pfem-architecture-theory-notes.md
docs/developer/pfem-ai-patch-safety-rules.md
workorders/README.md
tools/pfem_check_manifest.json
```

Do not add more record species after the permanent-archive terminal final endcap unless a gate, document, or human request identifies a real missing boundary.

PFEM generated checks belong in Python tools under `tools/` and must be registered in `tools/pfem_check_manifest.json`. Do not add root-level `pfem_*.bat` wrappers other than `pfem_check.bat`.

For passed verification receipts, `missing_refs` is an optional diagnostic array. It may be present as `[]`, but it must not be required by the schema.

Patch scripts should write noisy `git status --short` output to `build/pfem-patch-status/` instead of dumping it into the terminal.

# PFEM Contributor Command Protocol

This protocol applies to any PFEM contributor, including human developers, AI assistants, Copilot sessions, Codex sessions, contractors, maintainers, and review tools.

When any developer says `start a new tab`, do not continue implementation work.

Instead, produce the canonical PFEM new-tab handoff prompt from:

```text
docs/developer/pfem-new-tab-prompt.md
```

The handoff prompt must point the next working context to the current repo discipline files and require inspection of current `main` before relying on memory.

Do not expose private chain-of-thought. Provide architecture rationale, operating discipline, concrete repo-reading instructions, and decision rules.

# PFEM Workorder Protocol

This protocol applies to complex, substantial, or process-sensitive tasks.

When any developer says `create a workorder`, `write a workorder`, or `make a workorder`, the foreground assistant should generate the dated workorder file for the developer. The developer should not be expected to hand-write the file in Notepad or manually reconstruct the task contract.

Use a workorder when the task is too large, slow, environment-dependent, or mechanically broad for a conversational foreground assistant to execute safely in the current UI. Typical examples include tasks that require Codex or another executor with the repository environment, local tests, branch/PR workflow, broad file edits, generated-boundary work, release-gate cleanup, or many coordinated updates.

The foreground assistant's job is to capture the human decision, write the workorder under `workorders/`, and give the developer the exact one-line executor instruction:

```text
Read workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md and execute it.
```

The executor's job is to read the committed workorder, inspect recent workorders for conflicts, perform only the named scope, run/report checks, and cite the exact workorder path in its PR or completion notes.

Tiny safe edits do not need workorders. Standing-process changes usually do.
