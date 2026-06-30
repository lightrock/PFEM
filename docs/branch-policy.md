# PFEM Branch Policy

`main` is the canonical branch.

Remote branches are live operational objects. They should exist only for current work, open PRs, short-term restore, release/demo preparation, or explicit review.

Old work should be preserved with archive tags, not stale branches.

Default retention:

- Keep `main`.
- Keep branches with open PRs.
- Keep 3-5 active work branches.
- Keep 1-3 recent restore branches.
- Keep at most one release/demo/proposal branch unless there is a clear reason.
- Delete merged branches after 7 days.
- Archive and delete stale branches after 30-60 days.

Before deleting a branch, push an archive tag:

`archive/<branch-name>-YYYY-MM-DD`
