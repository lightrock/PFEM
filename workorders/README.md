# PFEM Workorders

This folder stores substantial PFEM task instructions as committed repo files.

A PFEM workorder is a permanent pre-action decision record and executable contract. It is not a scratchpad, a chat transcript, a generic PR summary, or a replacement for standing doctrine.

## Why this exists

PFEM work crosses AI windows, human developers, local patch packages, GitHub commits, and future review. Workorders make substantial intent durable before execution.

Each workorder should help two audiences:

- the current executor, which needs exact scope and checks now;
- future humans/AIs, which need to know what was decided, by whom, when, and why.

The workorder file is the contract, not the AI vendor.

## Normal workflow

Workorders are meant to be generated for developers by a foreground assistant, not hand-written by developers in Notepad.

The normal flow is:

1. A developer discusses a substantial task with a foreground assistant.
2. The foreground assistant recognizes that the task is complex, broad, slow, environment-dependent, or better handled by an executor with the repository environment.
3. The foreground assistant creates a dated workorder file under `workorders/`.
4. The foreground assistant gives the developer one exact executor instruction to paste elsewhere.
5. The executor reads the committed workorder and performs only that named scope.

The developer decides and approves the work. The foreground assistant turns that decision into a durable task contract when the work needs one.

## When to create a workorder

Create a dated workorder for substantial or process-sensitive work, including:

- boundary-generation or boundary-renaming work;
- repo discipline, command protocol, or AGENTS/AI_START_HERE changes;
- check-runner, manifest, CI, or release-gate changes;
- architecture doctrine changes that future AI sessions will rely on;
- broad documentation changes that affect contributor behavior;
- tasks intended for Codex or another coding agent to execute later.

Also create a workorder when the foreground assistant cannot safely or efficiently do the work in its current UI because it lacks the executor environment. Examples:

- many coordinated file edits;
- long-running tests or full-gate runs;
- local repository commands that require the developer's checkout;
- branch, PR, or CI workflow tasks;
- changes that require Codex or another executor to inspect files, run checks, and report results from a real environment.

Do not create a workorder for every typo, one-line README fix, or tiny safe direct edit unless the change modifies standing process or future contributor behavior.

## Filename pattern

Use one permanent dated file per substantial task:

```text
workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md
```

Use the GitHub username of the human authorizing or creating the workorder after `by-` when known.

Examples:

```text
workorders/2026-05-20-0825-by-lightrock-adopt-pfem-workorders.md
workorders/2026-05-20-0910-by-lightrock-run-full-gate-release-cleanup.md
```

Do not use:

```text
workorders/current-task.md
workorders/latest.md
workorders/next.md
```

## Launch instruction

After a workorder exists, the foreground assistant should give the developer one exact line to paste into the executor:

```text
Read workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md and execute it.
```

Use the actual dated filename.

## Required workorder sections

A useful PFEM workorder should include:

```text
# <Task title>

## Purpose
## Scope
## Files/areas likely to change
## Out of scope
## Constraints
## Required checks
## Expected result
## Fallback behavior
```

Add more sections only when the task needs them.

## Conflict check

Before executing a workorder, inspect recent files in `workorders/` for overlap.

If a recent workorder appears to compete with, supersede, or modify the same PFEM boundary, docs, command protocol, check runner, release path, adapter/subsystem rule, or architecture doctrine, stop and report the possible conflict.

Do not proceed until the developer gives an explicit override, for example:

```text
Force execute workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md despite the reported conflict.
```

## Direct edits and audit workorders

If an AI directly changes tracked PFEM files for substantial or process-sensitive work, include a workorder or audit workorder in the same change set whenever practical.

Tiny safe direct edits do not require paperwork. Changes to repo discipline, command protocol, AGENTS.md, AI_START_HERE, check manifests, release gates, or boundary generation rules do.

## Relationship to other docs

- `AGENTS.md` and scoped AGENTS files are standing behavior/doctrine.
- `docs/` files are project and architecture documentation.
- `workorders/` files are task-specific execution contracts and decision records.
- `tools/pfem_check_manifest.json` is the executable check manifest.

Do not use workorders as a random scratchpad.
