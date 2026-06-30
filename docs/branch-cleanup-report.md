# PFEM Branch Cleanup Report

Date: 2026-06-30

## Summary

- Repository: `lightrock/PFEM`
- Canonical branch kept: `origin/main`
- Remote branches before cleanup: 83 real branches, excluding `origin/HEAD`
- Remote branches after cleanup: 1 real branch, excluding `origin/HEAD`
- Branches kept: 1
- Branches archived and deleted: 82
- Branches needing manual review: 0
- Archive tags before cleanup: 0
- Archive tags created: 82

## Inspection

The cleanup started from a fresh `git fetch --all --prune`.

Open PR inspection was available through GitHub CLI:

```text
gh pr list --repo lightrock/PFEM --state open --limit 100
```

The command returned no open PRs.

`git branch -r --no-merged origin/main` returned no branches, so every non-main remote branch selected for deletion was already merged to `origin/main`.

## Execution

The safe cleanup script created and pushed an `archive/<sanitized-branch-name>-2026-06-30` tag before each remote branch deletion.

The first execution timed out after partially completing the earliest branch deletions. The script was then patched to be restart-safe for already-deleted remote branches and resumed successfully. Final verification showed only `origin/main` remained.

## Classification

| Branch | Last commit date | Merged to main? | Open PR? | Classification | Reason |
|---|---:|---|---|---|---|
| `origin/main` | 2026-05-24 | Yes | No | `KEEP_CANONICAL` | Canonical default working branch. |
| `origin/ai-patch-safety-guardrails` | 2026-05-20 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/archive-checkpoint` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-15` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-16` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-17` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-20` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-21` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-22` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-23` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-24` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-25` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-26` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-27` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-28` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-29` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-30` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-31` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-32` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-33` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-34` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/checkpoint-98386ccf` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/codex/clarify-repo-access-in-environment` | 2026-05-20 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/codex/execute-codegraph-ai-executor-workflow` | 2026-05-20 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/codex/execute-codegraph-local-tooling` | 2026-05-20 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/cp12` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/cp13` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/lifecycle-checkpoint` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-apply-receipts` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-conflicts` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-delivery-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-delivery-jobs` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-dispatch-decisions` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-dispatch-policy` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-exchange-linkage` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-import-records` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-intake-decisions` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-merge-decisions` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-outbox-items` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-received-items` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-routing-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-rp` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-snapshots` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-state-transitions` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-transport-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore-transport-receipts-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/adapter-registry-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/audit-journal-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/before-codegraph` | 2026-05-20 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/capability-registry-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/catalog-cli-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/confidence-quality-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/doctor-cli-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/example-registry-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/examples-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/exchange-bundles-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/federation-topology-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/integrity-receipts-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/lineage-validation-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/manual-adapter-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/node-identity-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/playbooks-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/profile-registry-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/reconciliation-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/record-schema-contracts-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/retention-disposition-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/review-decisions-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/runtime-seed-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/sharing-policy-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/source-provenance-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/restore/workflow-fixed-2026-05-19` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare10` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare11` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare2` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare3` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare4` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare5` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare6` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare7` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare8` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |
| `origin/spare9` | 2026-05-19 | Yes | No | `ARCHIVE_AND_DELETE_MERGED` | Merged to main, no open PR, older than 7 days; archive tag created before deletion. |

## Files

- `docs/branch-cleanup-report.md`
- `docs/branch-policy.md`
- `tools/branch_cleanup_2026_06_30.sh`
