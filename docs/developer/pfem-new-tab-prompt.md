# PFEM New-Tab Handoff Prompt

Use this when any PFEM developer says:

```text
start a new tab
```

Copy/paste the prompt below into the new AI/chat/development context.

---

We are working in the PFEM repository: `lightrock/PFEM`.

Before answering or making changes, inspect current `main` and read the repo discipline files that exist:

- `AGENTS.md`
- `README.md`
- `docs/AI_START_HERE.md`
- `docs/architecture/README.md`
- `docs/developer/pfem-new-chat-handoff.md`
- `docs/developer/pfem-contributor-command-protocol.md`
- `docs/developer/pfem-new-tab-prompt.md`
- `docs/developer/pfem-ai-patch-safety-rules.md`
- `docs/developer/pfem-boundary-language-generation-standard.md`
- `docs/developer/pfem-boundary-generation-standard.md`
- `docs/developer/pfem-architecture-theory-notes.md`
- `docs/developer/pfem-adapters-and-subsystems.md`
- `docs/developer/pfem-terminal-tail-stabilization.md`
- `tools/pfem_check_manifest.json`

Current repo state beats chat memory. If any listed filename has changed, inspect the closest current equivalent in the repository before proceeding.

PFEM means Polycentric Federated Evidence Mesh.

Keep these conceptually separate: raw evidence, normalized observations, findings, alerts, records, verification receipts, closeout records, catalog rows, audit events, evidence packages, reports, rollups, adapters, and subsystems.

Formal language:

- Use "PFEM boundary" for the generated record / verification receipt / closeout contract unit.
- "Adapter" means software integration layer.
- "Subsystem" means real-world or architectural capability.
- "Mesh" has two meanings: internal evidence-reference mesh and later PFEM-to-PFEM discovery / ad hoc availability mesh.

Current likely state, to verify against the repo:

The permanent-archive terminal chain reached its semantic endcap:

```text
retention permanent archive terminal closure final endcap closeout records
```

Do not generate more PFEM boundaries unless:

- a gate exposes a real missing boundary,
- a documented workflow is incomplete,
- a previous record / verification receipt / closeout record triple was left half-finished,
- or a developer deliberately opens a new chain.

Next normal work is likely:

```text
stabilization
speed cleanup
catalog readability
documentation cleanup
full gate
release/tag
```

Patch discipline:

When giving code changes, prefer a runnable patch package with a top-level wrapper script. For Windows patch packages, a top-level `.bat` is acceptable. The wrapper must preserve the caller's repository root, pass that root explicitly to Python, validate the PFEM root, run focused checks, and write noisy git status output to `build/pfem-patch-status`.

Do not change into the patch folder and accidentally treat that as the repository root. Do not run optional tests unless their files exist. Do not dump giant `git status --short` output into the terminal.

Decision rule:

If unsure, inspect the repo and make the smallest doctrine-preserving change. Do not invent fake refs, fake evidence, fake boundaries, or broad rewrites just to make a check pass.

When a developer says "start a new tab," do not continue implementation work. Output this handoff prompt for the next working context.
