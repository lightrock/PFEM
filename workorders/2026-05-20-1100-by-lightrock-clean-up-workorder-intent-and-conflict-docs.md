# Clean Up Workorder Intent and Conflict Documentation

## Purpose

Clean up the failed direct-edit attempt around PFEM workorder intent documentation and make the doctrine durable in the repository.

A previous foreground assistant attempted to update README/workorder guidance directly, but several GitHub write attempts were blocked. During that probe, a throwaway file was accidentally committed:

```text
docs/developer/test-small-delete-me.md
```

This workorder exists so an executor with a real repository environment can clean that up properly and land the intended documentation without relying on chat memory.

## Scope

Do all of the following:

1. Delete the accidental probe file:

```text
docs/developer/test-small-delete-me.md
```

2. Add a permanent developer doctrine file, likely:

```text
docs/developer/pfem-workorder-intent-and-merge-conflicts.md
```

3. Document that PFEM workorders are not only task prompts. They are intent evidence for future review, audit, and merge-conflict resolution.

4. Update workorder guidance so PRs and completion notes produced from a workorder cite the exact path:

```text
Workorder: workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md
```

5. Update README and/or workorders/README.md with human-facing language explaining that workorder references let future humans and connected AI tools recover original task intent when branches conflict.

6. Update AGENTS.md or the relevant scoped AGENTS file so AI assistants know this rule during future conflict resolution.

## Files/areas likely to change

Likely files:

```text
README.md
AGENTS.md
workorders/README.md
workorders/AGENTS.md
docs/developer/pfem-workorder-intent-and-merge-conflicts.md
```

Required deletion:

```text
docs/developer/test-small-delete-me.md
```

## Out of scope

Do not change PFEM architecture behavior, schemas, generated boundaries, validators, or runtime code.

Do not generate new PFEM record species.

Do not run full gate unless the executor intentionally promotes the task into release/stabilization work.

## Constraints

Follow the repository startup and contributor discipline:

```text
AGENTS.md
README.md
docs/AI_START_HERE.md
workorders/README.md
workorders/AGENTS.md
docs/developer/pfem-terminology-brake-rules.md
tools/pfem_check_manifest.json
```

Keep the language human-readable. The README should explain why developers benefit from the rule, not just command AI assistants.

Use the phrase "intent evidence" somewhere in the permanent docs, because that is the searchable concept future tools should find.

## Required checks

Run focused checks appropriate to a documentation/process change.

At minimum, run:

```text
pfem_check.bat --quick --timings
```

If the launcher is unavailable, run the relevant doc/repo-discipline Python checks under `tools/` and report exactly what was run.

Also verify that the accidental probe file no longer exists.

## Expected result

After execution:

- `docs/developer/test-small-delete-me.md` is gone.
- PFEM docs clearly state that workorder references are intent evidence.
- PR/completion-note guidance requires exact workorder path citation.
- Merge-conflict resolution guidance says to start from cited workorders before interpreting the final diff.
- Future humans and AI assistants understand that a conflict between workorder-backed branches should be resolved by comparing intent, scope, constraints, and checks, not by mechanically choosing one side of a text conflict.

## Fallback behavior

If an equivalent document already exists, update it instead of creating a duplicate.

If updating README.md or workorders/README.md causes tool or branch conflicts, make the smallest safe doc change and report what still needs manual review.

If two existing docs disagree semantically, stop and report the conflict instead of inventing a compromise.

## Executor launch instruction

After this workorder is committed, give the executor this exact instruction:

```text
Read workorders/2026-05-20-1100-by-lightrock-clean-up-workorder-intent-and-conflict-docs.md and execute it.
```
