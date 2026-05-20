# PFEM workorders scoped guidance

This file is canonical for workorder-local workflow rules. Root `AGENTS.md` remains canonical for cross-cutting PFEM doctrine and routing.

## Core rule

A PFEM workorder is a committed, dated, pre-action contract for substantial work.

Workorders are for humans and AI executors. They are not vendor-specific prompts and they are not scratch notes.

## When to use a workorder

Use a workorder for substantial or process-sensitive work:

- PFEM boundary generation or boundary renaming;
- command protocol changes;
- AGENTS.md or `docs/AI_START_HERE.md` changes;
- check runner, check manifest, full-gate, or release process changes;
- architecture doctrine changes;
- broad documentation changes that affect future contributor behavior;
- tasks intended for Codex or another coding agent to execute later.

Do not require a workorder for tiny safe typo fixes or one-line direct edits unless the edit changes standing process.

## Filename rule

Use exactly one dated workorder file per substantial task:

```text
workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md
```

Do not create `current-task.md`, `latest.md`, `next.md`, or rotating pointer files.

## Launch rule

After a workorder exists, the executor launch instruction is:

```text
Read workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md and execute it.
```

Use the actual committed dated filename.

## Conflict rule

Before executing a workorder, inspect recent workorders for overlap with the same PFEM boundary, architecture doctrine, command protocol, adapter/subsystem rule, check runner, check manifest, full-gate, release path, or documentation convention.

If likely overlap exists, stop and report the conflict. Continue only with explicit override language:

```text
Force execute workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md despite the reported conflict.
```

## Direct-edit audit rule

If an AI directly changes tracked PFEM files for substantial or process-sensitive work, include a workorder or audit workorder in the same change set whenever practical.

Tiny safe direct edits do not require paperwork. Standing-process changes do.

## Boundary with other docs

- `AGENTS.md` and scoped AGENTS files are standing behavior/doctrine.
- `docs/` files are product and architecture documentation.
- `workorders/` files are task-specific execution contracts and decision records.
- `tools/pfem_check_manifest.json` is the executable check manifest.
