# PFEM CodeGraph Local Tooling

CodeGraph is optional local developer tooling for repository navigation by humans and AI executors working in PFEM.

Use it when preparing broad PFEM edits that touch check runners, generated validators, check manifests, adapter/subsystem docs, workorders, or doctrine files.

CodeGraph is not part of PFEM runtime architecture and is not required for PFEM deployments, validation gates, or releases.

## Local-only artifacts

CodeGraph index data under `.codegraph/` is local-only and must not be committed.

## Safe local commands

Run from repository root:

```bash
npx -y @colbymchenry/codegraph init -i
npx -y @colbymchenry/codegraph status --json
npx -y @colbymchenry/codegraph sync
```

Use manual sync unless a developer deliberately approves git-hook installation.

## AI executor usage

AI executors should use CodeGraph to locate likely PFEM surfaces before broad edits, then still inspect exact files before patching.
