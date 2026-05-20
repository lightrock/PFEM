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
- Treat each generated “doodad” as a full contract boundary: data, schema, validator, tool, catalog, audit, doctor wiring, docs, contract, tests, and check-manifest registration.
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
- Read `docs/developer/pfem-doodad-generation-standard.md`.
- Read `docs/developer/pfem-new-chat-handoff.md`.
- Read `docs/developer/pfem-terminal-tail-stabilization.md`.
- Inspect `tools/pfem_check_manifest.json`.
- `docs/developer/pfem-architecture-theory-notes.md` for the higher-level PFEM theory vocabulary.
- Inspect current `main` before assuming conversation memory is current.
