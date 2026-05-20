# PFEM CodeGraph Local Tooling

CodeGraph is optional local developer tooling for repository navigation by humans and AI executors working in PFEM.

CodeGraph is not PFEM runtime architecture and is not part of PFEM deployments, release gates, or evidence semantics.

## When to use CodeGraph

Use CodeGraph before broad edits that touch:

- check runners;
- generated validators;
- manifests;
- doctrine documents;
- adapter/subsystem documentation;
- workorders;
- related PFEM plumbing surfaces.

Lack of CodeGraph does not block PFEM work.

## Pre-edit discovery flow for AI executors

1. Start from repository root.
2. Initialize/index CodeGraph if needed.
3. Check status.
4. Run targeted PFEM queries to locate likely edit surfaces.
5. Open and inspect exact repository files before patching.

Use the normal local path:

```bash
npx -y @colbymchenry/codegraph init -i
npx -y @colbymchenry/codegraph status --json
npx -y @colbymchenry/codegraph sync
```

Manual sync is the default. Git hooks require explicit developer approval.

## Targeted PFEM query examples

Use queries like:

```bash
npx -y @colbymchenry/codegraph query "pfem_check"
npx -y @colbymchenry/codegraph query "pfem_check_manifest"
npx -y @colbymchenry/codegraph query "run_doctor"
npx -y @colbymchenry/codegraph query "workorders"
npx -y @colbymchenry/codegraph query "adapter subsystem doctrine"
npx -y @colbymchenry/codegraph query "retention_terminal_tail_audit"
```

CodeGraph discovery is advisory only. Executors must still inspect exact files before making changes.

## Fallback when CodeGraph is unavailable

If CodeGraph cannot run, say so in completion notes, then use ordinary repo inspection. Do not force the environment or pretend CodeGraph discovery passed.

## What CodeGraph does not replace

CodeGraph does not replace:

- direct inspection of exact files before patching;
- PFEM architecture doctrine and terminology discipline;
- PFEM runtime contracts;
- release-gate checks;
- evidence-semantics boundaries.

## Local-only artifacts

`.codegraph/` is local-only and must not be committed.
