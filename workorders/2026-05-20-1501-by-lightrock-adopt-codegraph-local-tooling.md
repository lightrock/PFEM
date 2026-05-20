# Adopt CodeGraph as optional local AI navigation tooling

## Purpose

PFEM has grown into a large architecture-first repository with generated validators, check-runner routing, doctor modes, workorders, and doctrine files. AI executors can waste time or make bad edits when they rediscover the repository structure through repeated grep/read cycles.

This workorder asks the executor to safely install and run CodeGraph as developer-local code-intelligence tooling for PFEM, then record the right repo changes so future AI/Codex sessions can use it without turning CodeGraph into PFEM runtime architecture.

CodeGraph must be treated as optional local developer tooling. It is not a PFEM evidence contract, runtime dependency, model host, subsystem, adapter, queue, database, service, or release requirement.

## Scope

1. Inspect current `main` before relying on this workorder or any chat memory.
2. Read the required PFEM discipline files before editing:
   - `AGENTS.md`
   - `README.md`
   - `docs/AI_START_HERE.md`
   - `docs/developer/pfem-contributor-command-protocol.md`
   - `docs/developer/pfem-new-tab-prompt.md`
   - `workorders/README.md`
   - `workorders/AGENTS.md`
   - `tools/pfem_check_manifest.json`
3. Inspect recent workorders for overlap or conflict before editing.
4. Add or confirm ignore coverage so local CodeGraph indexes are not committed:
   - `.codegraph/`
   - any generated CodeGraph database/cache/log files if they appear outside `.codegraph/`
5. Run CodeGraph from the PFEM repository root using the safest available local path.
6. Capture CodeGraph status and at least a few targeted CodeGraph queries that prove it can find PFEM runner/validator/doctrine surfaces.
7. Add a concise developer note explaining how PFEM contributors and AI executors should use CodeGraph locally.
8. Report exactly what CodeGraph commands were run and what checks passed.

## Files/areas likely to change

Expected tracked changes should be small:

```text
.gitignore
docs/developer/pfem-codegraph-local-tooling.md
README.md                 # optional, only if adding one short pointer to the new developer note
AGENTS.md                 # optional, only if adding one short optional-tooling pointer is clearly justified
```

Prefer adding a developer note under `docs/developer/` plus a short README pointer. Avoid broad doctrine rewrites.

## Out of scope

Do not:

- add CodeGraph to PFEM runtime architecture;
- add `@colbymchenry/codegraph` to PFEM package dependencies;
- create a PFEM `package.json` just for CodeGraph;
- commit `.codegraph/`, `codegraph.db`, cache files, local logs, or generated index artifacts;
- commit user-global config changes from `~/.codex`, `~/.claude`, `~/.cursor`, or opencode;
- commit `.cursor/rules/codegraph.mdc` unless the developer explicitly approves it in a later task;
- install git hooks unless the developer explicitly approves it;
- run the bare interactive installer as the default path;
- treat CodeGraph query output as PFEM truth or evidence;
- change PFEM schemas, generated boundary validators, evidence records, reports, rollups, adapters, or subsystem doctrine as part of this task.

## Constraints

- Current repo state beats this workorder if a filename has changed. Inspect the closest current equivalent.
- Use single-task mode. This is one workorder, one branch, one PR.
- Keep the change small and reversible.
- CodeGraph is allowed to create local untracked files during execution, but the PR must not include those files.
- If CodeGraph prompts about keeping its index fresh, choose the manual-sync option. Do not install git hooks during this task.
- If CodeGraph writes project-local agent config such as `.cursor/rules/codegraph.mdc`, inspect it, remove it from the tracked change set, and report it. Do not commit it without later explicit approval.
- If Node/npm is missing, Node is incompatible, network access is unavailable, or CodeGraph cannot run in the executor environment, do not fake success. Add the ignore/doc changes that are still valid, then report the exact blocker.
- If the executor environment runs Node 25 and CodeGraph refuses to run, do not bypass the safety check with `CODEGRAPH_ALLOW_UNSAFE_NODE` unless the developer explicitly approves that later.

## Suggested safe command sequence

From the PFEM repository root:

```bash
git status --short
node --version
npm --version
```

If Node is available and compatible with CodeGraph, prefer this non-persistent path first:

```bash
npx -y @colbymchenry/codegraph --version
npx -y @colbymchenry/codegraph init -i
npx -y @colbymchenry/codegraph status --json
```

If the executor already has `codegraph` installed globally, this is also acceptable:

```bash
codegraph --version
codegraph init -i
codegraph status --json
```

If CodeGraph prompts about index freshness, choose manual sync. Do not install git hooks in this workorder.

After indexing, run a few targeted checks such as:

```bash
npx -y @colbymchenry/codegraph query "pfem_check"
npx -y @colbymchenry/codegraph query "run_doctor"
npx -y @colbymchenry/codegraph query "retention_terminal_tail_audit"
npx -y @colbymchenry/codegraph query "pfem_check_manifest"
```

Use the global `codegraph` command instead of `npx -y ...` if that is what succeeded earlier.

Then verify local artifacts are ignored:

```bash
git status --short
git check-ignore -v .codegraph/codegraph.db || true
```

## Developer note requirements

Create `docs/developer/pfem-codegraph-local-tooling.md` unless a clearly better current location already exists.

The note should say:

- CodeGraph is optional local developer tooling for codebase navigation by humans and AI executors.
- CodeGraph is recommended for broad PFEM edits involving check runners, generated validators, manifests, adapters, subsystem docs, workorders, or doctrine files.
- CodeGraph is not part of PFEM runtime architecture and is not required for deployments or releases.
- `.codegraph/` is local-only and must not be committed.
- Safe commands for contributors:

```bash
npx -y @colbymchenry/codegraph init -i
npx -y @colbymchenry/codegraph status --json
npx -y @colbymchenry/codegraph sync
```

- Use manual sync unless a developer deliberately approves git-hook installation.
- AI executors should use CodeGraph to find relevant files before broad edits, but still inspect exact files before patching.

Optionally add one short pointer to this developer note from `README.md` contributor handoff. Keep it brief.

## Required checks

Run the closest available checks for a doc/tooling-only change:

```bash
python tools/pfem_doctor.py
python tools/pfem_check.py --quick --list
```

If the repository uses `.bat`/`.sh` launchers in the current environment, also run the appropriate launcher self-check when practical:

```bash
python tools/pfem_check.py --check-launchers
```

If any command is unavailable in the executor environment, report the command and exact reason. Do not invent a passing result.

## Expected result

A PR or completion change set should include:

- `.gitignore` updated, if needed, so `.codegraph/` is ignored;
- a concise `docs/developer/pfem-codegraph-local-tooling.md` developer note;
- optionally a one-line README pointer to the new note;
- no committed CodeGraph database/index/cache/log files;
- no committed global or project-local agent config files unless later explicitly approved;
- completion notes with:
  - CodeGraph version command result;
  - initialization/index status summary;
  - CodeGraph `status --json` summary;
  - targeted query results summary;
  - required PFEM checks run.

## Fallback behavior

If CodeGraph cannot be installed or run:

1. Do not install unrelated tools to force it.
2. Do not bypass CodeGraph's Node safety guard.
3. Preserve the safe `.gitignore` and developer-note work if applicable.
4. Record the exact blocker in the PR/completion notes.
5. Mark CodeGraph runtime verification as not completed, not as passed.

## PR body requirement

The PR body must include:

```text
## Workorder
Executed: workorders/2026-05-20-1501-by-lightrock-adopt-codegraph-local-tooling.md
```
