# AGENTS.md

This repository is PFEM: Polycentric Federated Evidence Mesh.

Before editing, read:

- `docs/AI_START_HERE.md`
- `docs/architecture/neutral-language.md`
- `docs/architecture/architecture-stack.md`
- `docs/architecture/evidence-lifecycle.md`
- `ai/architecture-rules.md`
- `ai/adapter-rules.md`
- `ai/evidence-rules.md`
- `ai/node-profile-rules.md`
- `ai/review-checklist.md`

Core rules:

- Use neutral deployment-shape language.
- Do not name specific customers, agencies, sponsors, programs, or private deployments in public repository files.
- Keep raw evidence, normalized observations, findings, alerts, evidence packages, rollups, and reports separate.
- Adapters translate source-specific inputs into PFEM contracts; adapters do not own policy.
- Profiles configure deployment shape; profiles do not fork the product.
- Schemas define contracts; code should follow schemas.
- Reports and dashboards are outputs, not source evidence.
- Do not add infrastructure, databases, queues, identity systems, or background services unless the architecture docs justify it.

When unsure, make the smallest doctrine-preserving change and explain the boundary affected.
