# PFEM Executor Modes

PFEM supports two executor modes for AI-assisted or human-assisted work.

The purpose is to reduce developer friction without losing reviewability, workorder traceability, or architecture discipline.

## Default: single-task mode

Single-task mode is the default.

Use one workorder, one executor task, one branch, and one PR.

Use single-task mode when:

```text
the task has a clear beginning and end
the work should be reviewed independently
a failure should not affect other work
the change needs easy rollback
the work touches schemas, contracts, checks, gates, or architecture-sensitive doctrine
the task is generated from one specific workorder
```

Good examples:

```text
clean up one failed documentation attempt
add one architecture doctrine document
fix one check-manifest issue
resolve one schema-contract failure
execute one generated-boundary workorder
```

Expected PR ledger:

```text
Execution mode: single-task
Workorder: workorders/YYYY-MM-DD-HHMM-by-githubusername-short-task-name.md
Checks run:
- <checks>
```

## Optional: campaign mode

Campaign mode is a lower-friction mode for a related sequence of small or medium changes that need the same context.

Use one campaign branch and one PR that is updated repeatedly.

Campaign mode is allowed only when the work is intentionally cumulative and tightly related.

Use campaign mode for:

```text
documentation alignment
README / AGENTS / AI_START_HERE cleanup
terminology and doctrine synchronization
minor repo-discipline cleanup
small follow-up fixes from the same review
```

Campaign mode must not be used to hide unrelated work in one branch.

Do not use campaign mode for:

```text
unrelated feature work
major schema or contract changes
generated-boundary batches
release or full-gate work
security, auth, infrastructure, database, queue, or service changes
anything where rollback should be simple
anything likely to conflict with active human edits
```

Expected PR ledger:

```text
Execution mode: campaign

Campaign workorder:
- workorders/YYYY-MM-DD-HHMM-by-githubusername-campaign-name.md

Executed subtasks:
- workorders/YYYY-MM-DD-HHMM-by-githubusername-first-task.md
- direct small fix: <short description>
- workorders/YYYY-MM-DD-HHMM-by-githubusername-second-task.md

Checks run:
- <checks>
```

## Campaign workorders

A campaign workorder should define the campaign boundary.

It should say:

```text
why campaign mode is appropriate
which files/areas are in scope
which files/areas are out of scope
how the PR ledger must be updated after each subtask
when to stop and split work into a separate branch
which checks must be run after each step or before final review
```

Campaign mode is not permission to improvise indefinitely.

If new work becomes unrelated, architecture-sensitive, difficult to review, or risky to roll back, stop and create a separate single-task workorder.

## Conflict behavior

Campaign branches are more likely to accumulate conflicts because they live longer.

When a campaign branch conflicts with another branch, use the campaign PR ledger and the cited workorders as intent evidence. Do not resolve conflicts by treating the branch as a random pile of edits.

If the campaign PR ledger is missing or stale, stop and repair the ledger before continuing.

## Human-facing rule

Use single-task mode when correctness and review isolation matter most.

Use campaign mode when continuity and lower user friction matter more than isolation.

When in doubt, use single-task mode.
