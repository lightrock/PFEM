# Operationalize CodeGraph for PFEM AI Executor Pre-Edit Discovery

## Purpose

Make CodeGraph actually useful for PFEM AI executor work, not just mentioned in documentation.

PFEM has a large architecture-first repository with check runners, generated validators, manifests, doctrine files, and workorders. AI executors should use a local semantic index when available so they can find the right PFEM surfaces before editing.

This workorder asks the executor to install or run CodeGraph locally in the PFEM checkout when the environment allows it, initialize the index, prove it can find PFEM-relevant surfaces, update the local-tooling guidance, run PFEM checks, and commit only safe repository changes.

CodeGraph remains optional local developer tooling. It is not PFEM runtime architecture, not a deployment dependency, not a release gate, not a PFEM evidence source, not an adapter, not a subsystem, and not a substitute for reading exact files before editing.

## Scope

1. Inspect current `main` before relying on this workorder or chat memory.
2. Read the required PFEM discipline files before editing:
   - `AGENTS.md`
   - `README.md`
   - `docs/AI_START_HERE.md`
   - `docs/developer/pfem-contributor-command-protocol.md`
   - `docs/developer/pfem-codegraph-local-tooling.md`
   - `docs/developer/pfem-new-tab-prompt.md`
   - `workorders/README.md`
   - `workorders/AGENTS.md`
   - `tools/pfem_check_manifest.json`
3. Inspect recent workorders for overlap or conflict before editing.
4. Confirm `.gitignore` protects local CodeGraph artifacts, especially `.codegraph/`.
5. Run CodeGraph in the PFEM repository root using the safest available local path.
6. Initialize CodeGraph and build the index if the environment allows it.
7. Run CodeGraph status/query commands to prove it can locate PFEM executor-relevant surfaces.
8. Update `docs/developer/pfem-codegraph-local-tooling.md` with a concrete pre-edit discovery workflow, targeted query examples, and fallback behavior.
9. Keep tracked repository edits small and reversible.
10. Run PFEM checks and commit the result back to the repository through a normal PR or branch workflow.

## Files/areas likely to change

Expected tracked changes should be minimal:

```text
docs/developer/pfem-codegraph-local-tooling.md
README.md                                             # optional, one-line pointer only if needed
.gitignore                                            # only if CodeGraph ignore coverage is missing
workorders/2026-05-20-1522-by-lightrock-operationalize-codegraph-ai-executor-workflow.md
```

Do not broaden this into unrelated cleanup.

## Out of scope

Do not:

- make CodeGraph a PFEM runtime dependency;
- add `@colbymchenry/codegraph` to PFEM package dependencies;
- create or commit a PFEM `package.json` just for CodeGraph;
- commit `.codegraph/`, `codegraph.db`, cache files, logs, or generated index artifacts;
- commit user-global config changes from Codex, Claude, Cursor, or opencode;
- commit `.cursor/rules/codegraph.mdc` unless the developer explicitly approves it in a later task;
- install git hooks unless the developer explicitly approves it;
- run the bare interactive installer as the default path;
- override CodeGraph, Node, npm, or environment warnings/errors;
- treat CodeGraph query output as PFEM truth or evidence;
- change PFEM schemas, generated boundary validators, records, evidence files, reports, rollups, adapters, subsystem doctrine, check-runner behavior, or release gates as part of this task.

## Constraints

- Current repo state beats this workorder if a filename has changed. Inspect the closest current equivalent.
- Use single-task mode: one workorder, one executor task, one branch, one PR.
- Keep the change small and reversible.
- CodeGraph may create local untracked files while running, but the final PR must not include those files.
- If CodeGraph prompts about keeping its index fresh, choose manual sync. Do not install git hooks.
- If CodeGraph writes project-local agent config, inspect it, remove it from the tracked change set, and report it. Do not commit it.
- If Node/npm is missing, Node is incompatible, network access is unavailable, npm policy blocks the package, or CodeGraph cannot run, do not fake success.

## Required CodeGraph commands

From the PFEM repository root, first record the environment:

```bash
git status --short
node --version
npm --version
```

Then try the safest non-persistent CodeGraph path:

```bash
npx -y @colbymchenry/codegraph --version
npx -y @colbymchenry/codegraph init -i
npx -y @colbymchenry/codegraph status --json
```

If `codegraph` is already installed globally and `npx` is blocked, this path is acceptable:

```bash
codegraph --version
codegraph init -i
codegraph status --json
```

If CodeGraph is already initialized, do not delete the index. Run sync and status instead.

## Required CodeGraph discovery examples

Run at least these targeted discovery commands, adapting only if the installed CodeGraph CLI exposes equivalent names/options:

```bash
npx -y @colbymchenry/codegraph query "pfem_check"
npx -y @colbymchenry/codegraph query "pfem_check_manifest"
npx -y @colbymchenry/codegraph query "run_doctor"
npx -y @colbymchenry/codegraph query "workorders"
npx -y @colbymchenry/codegraph query "adapter subsystem doctrine"
npx -y @colbymchenry/codegraph query "retention_terminal_tail_audit"
```

Use global `codegraph` instead of `npx -y @colbymchenry/codegraph` if that is what succeeded.

Summarize the results in completion notes. Do not paste huge output into the PR body.

## Required documentation update

Update `docs/developer/pfem-codegraph-local-tooling.md` so it contains these sections or clear equivalents:

```text
## When to use CodeGraph
## Pre-edit discovery flow for AI executors
## Targeted PFEM query examples
## Fallback when CodeGraph is unavailable
## What CodeGraph does not replace
```

The doctrine must say:

- Use CodeGraph before broad edits that touch check runners, generated validators, manifests, doctrine, adapter/subsystem docs, workorders, or related PFEM plumbing.
- CodeGraph discovery is advisory. The executor must still inspect exact files before patching.
- If CodeGraph is unavailable, fall back to normal repository inspection/search and report that fallback.
- Lack of CodeGraph does not block PFEM work.
- CodeGraph is not PFEM runtime architecture and is not part of deployments, release gates, or evidence semantics.
- `.codegraph/` is local-only and must not be committed.
- Manual sync is the default; git hooks require explicit developer approval.

Add a short command block showing the normal path:

```bash
npx -y @colbymchenry/codegraph init -i
npx -y @colbymchenry/codegraph status --json
npx -y @colbymchenry/codegraph sync
```

Add a short fallback block:

```text
If CodeGraph cannot run, say so in completion notes, then use ordinary repo inspection. Do not force the environment or pretend CodeGraph discovery passed.
```

## Verify local artifacts stay out of Git

After running CodeGraph, verify local artifacts are ignored:

```bash
git status --short
git check-ignore -v .codegraph/codegraph.db || true
```

If `.codegraph/` appears as an untracked add candidate, fix `.gitignore` before continuing.

## Required PFEM checks

Run these checks after documentation changes:

```bash
python tools/pfem_doctor.py
python tools/pfem_check.py --quick --list
python tools/pfem_check.py --check-launchers
```

If the current platform requires a launcher instead, use the closest available `.bat` or `.sh` path and report exactly what ran.

If any command is unavailable, report the command and exact reason. Do not invent a passing result.

## Expected result

The final PR/commit should show:

- CodeGraph was installed/initialized/synced if the environment allowed it;
- CodeGraph status and targeted discovery commands were attempted and summarized;
- local `.codegraph/` artifacts were not committed;
- `docs/developer/pfem-codegraph-local-tooling.md` now gives AI executors a repeatable pre-edit discovery workflow;
- PFEM checks were run and reported;
- no unrelated PFEM architecture/runtime changes were made.

## Fallback behavior

If CodeGraph cannot be installed or run:

1. Do not install unrelated tools to force it.
2. Do not commit generated local artifacts.
3. Still update the developer note with deterministic fallback behavior if that can be done safely.
4. Record the exact blocker in the PR/completion notes.
5. Mark CodeGraph runtime verification as blocked, not passed.

## Commit and PR requirements

Commit the safe tracked changes back to the repository on a branch and open a PR unless the current executor environment uses a different approved PFEM branch workflow.

The PR body must include:

```text
## Workorder
Executed: workorders/2026-05-20-1522-by-lightrock-operationalize-codegraph-ai-executor-workflow.md
```

The PR body or completion notes must also include:

```text
CodeGraph commands attempted:
- <commands and concise results>

PFEM checks run:
- <commands and results>

Local artifact check:
- <git status / git check-ignore summary>
```
