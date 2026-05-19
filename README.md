# PFEM

**PFEM** means **Polycentric Federated Evidence Mesh**.

PFEM is an architecture-first project for configurable evidence, sensor-input, human-report, dashboard, and rollup nodes.

The goal is one core architecture that can support many deployment shapes by configuration rather than product forks:

- field-radio nodes
- community mesh nodes
- infrastructure site nodes
- civil dashboard nodes
- research testbed nodes
- formal authority rollup nodes
- disconnected edge nodes

## Core rule

PFEM keeps these separate:

- raw evidence
- normalized observations
- correlated entities or tracks
- findings
- alerts
- evidence packages
- dashboard actions
- federation messages
- rollup summaries
- reports

Adapters bring source-specific inputs into PFEM contracts.

Profiles decide what kind of node is being deployed.

Dashboard/action flows help humans decide what to do next.

Federation and rollup move attributable summaries, requests, and evidence packages across explicit sharing boundaries.

Start here:

- `docs/AI_START_HERE.md`
- `docs/architecture/neutral-language.md`
- `ai/architecture-rules.md`
- `contracts/adapter-contract.md`
