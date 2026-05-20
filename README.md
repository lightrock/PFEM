# PFEM

**PFEM** means **Polycentric Federated Evidence Mesh**.

PFEM is an architecture-first project for configurable evidence, sensor-input, human-report, dashboard, and rollup nodes.

The goal is one core architecture that can support many deployment shapes by configuration rather than product forks:

- field-radio nodes
- community mesh nodes
- infrastructure site nodes
- civil dashboard nodes
- research testbed nodes
- formal authority rollup nodes
- disconnected edge nodes

## Core rule

PFEM keeps these separate:

- raw evidence
- normalized observations
- correlated entities or tracks
- findings
- alerts
- evidence packages
- dashboard actions
- federation messages
- rollup summaries
- reports

Adapters bring source-specific inputs into PFEM contracts.

Profiles decide what kind of node is being deployed.

Dashboard/action flows help humans decide what to do next.

Federation and rollup move attributable summaries, requests, and evidence packages across explicit sharing boundaries.

Start here:

- `docs/AI_START_HERE.md`
- `docs/architecture/neutral-language.md`
- `ai/architecture-rules.md`
- `contracts/adapter-contract.md`

## Architecture and testing principles observed

PFEM is being built as an evidence-governance architecture, not as a pile of scripts. The project should keep proving its shape through small, named, auditable boundaries.

Architecture principles:

- Keep evidence, interpretation, action, package, report, and rollup concepts separate.
- Prefer explicit record species over ambiguous blobs when a boundary matters.
- Treat each generated PFEM boundary as a full contract boundary: data, schema, validator, tool, catalog, audit, doctor wiring, docs, contract, tests, and check-manifest registration.
- Use real domain nouns for generated boundaries. Names should describe the PFEM responsibility, not the implementation trick.
- Stop generating new species when a chain reaches a real semantic endcap. After an endcap, stabilize and run gates.
- Do not preserve project knowledge only in chat. Put doctrine, handoff, standards, and gotchas in the repo.
- Do not add infrastructure, queues, databases, services, or auth just because they are familiar. Add them only when the architecture earns them.

Testing principles:

- Make the normal path boring: one launcher, one manifest, predictable focused checks.
- New PFEM checks belong under `tools/` and should be registered in `tools/pfem_check_manifest.json`.
- Avoid root-level `.bat` wrapper churn. Keep `pfem_check.bat` and `pfem_check.sh` as the launcher pair.
- During large generation work, run focused validators and quick gates. Save the full gate for stabilization, release, and broad plumbing changes.
- Let gates reveal real missing boundaries. Do not invent fake references or fake species just to quiet a failing check.
- Write noisy patch status output to `build/pfem-patch-status/` so operators can see actual failures without scrolling through hundreds of status lines.
- Treat schema-contract failures as design feedback. Example: `missing_refs` is an optional diagnostic array for passed verification receipts, not a required non-empty field.

Contributor handoff:

- Start with `AGENTS.md`.
- Read `docs/developer/pfem-boundary-language-generation-standard.md`.
- Read `docs/developer/pfem-new-chat-handoff.md`.
- Read `docs/developer/pfem-terminal-tail-stabilization.md`.
- Inspect `tools/pfem_check_manifest.json`.
- Read `workorders/README.md` before creating or executing substantial task instructions.
- `docs/developer/pfem-architecture-theory-notes.md` for the higher-level PFEM theory vocabulary.
- Inspect current `main` before assuming conversation memory is current.

## Your first new session instruction to an AI

Before asking a new AI/chat/development session to work on PFEM, paste this first:

```text
We are working in the PFEM repository: lightrock/PFEM.
Inspect current main before relying on chat memory.
Read AGENTS.md, README.md, docs/AI_START_HERE.md, docs/developer/pfem-contributor-command-protocol.md, docs/developer/pfem-new-tab-prompt.md, workorders/README.md, and tools/pfem_check_manifest.json before making changes.
Follow PFEM boundary language, workorder discipline, and patch safety rules.
If any filename has changed, inspect the closest current equivalent in the repository before proceeding.
```

PFEM has a project-level command protocol for humans and AI assistants.

When any developer says `start a new tab`, the worker should produce the canonical PFEM new-tab handoff prompt instead of continuing implementation work.

When any developer says `create a workorder`, `write a workorder`, or `make a workorder`, create a dated PFEM workorder file under `workorders/` instead of treating the task as throwaway chat text.

See:

```text
docs/developer/pfem-contributor-command-protocol.md
docs/developer/pfem-new-tab-prompt.md
workorders/README.md
workorders/AGENTS.md
```

## Workorders

PFEM has the ability to differente your AI interactions with an extra audit trail.  If you are in GPT for example, and you tell it to do something substantial, it may decide it should hand this process off to Codex (or another AI).  If so, it will generate a Work Order and stick that into the repository and tell you to "copy this line and paste it to Codex (or another AI). This line will tell Codex (or another AI) to go read and execute that file. A github PR alone does not carry the trail of what GPT said to Codex. Codex should respond when making a PR what GPT workorder filename that it used. There is an audit trail that is AI vendor agnostic here between foreground AI and automated AI. This is worth it because PFEM is AI-assisted, repo-disciplined, and likely to cross chat windows, coding agents, manual edits, and future release gates.

Now, if Codex encounters a hard problem it also automatically carries instructions to generate a "lessons learned" in the Work Order History in case this action should be replayed in the future and if so it will be more efficient the next time.

A workorder is a committed pre-action decision record and executable task contract. It is useful when the work affects boundaries, command protocol, AGENTS/AI_START_HERE, check runners, release gates, architecture doctrine, or broad contributor behavior.

The standard filename shape is:

```text
workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md
```

After a workorder is created, the executor instruction is:

```text
Read workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md and execute it.
```

Tiny safe edits do not need workorders. Standing-process changes usually do.
