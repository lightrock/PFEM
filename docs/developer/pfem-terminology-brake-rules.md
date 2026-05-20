# PFEM Terminology Brake Rules

This file captures terms that should make humans and AI assistants slow down before designing, coding, or generating files.

A brake word does not mean the project is blocked. It means the term is overloaded enough that a wrong assumption can damage the architecture.

When a brake word is ambiguous, stop implementation work, explain the PFEM meanings, identify which meaning is intended in the current task, and continue only after the intended meaning is clear.

## Brake-word protocol

Use this protocol when a developer asks what a term means, uses a term in a way that could collapse PFEM boundaries, or asks for work that depends on an ambiguous PFEM term.

```text
1. Stop implementation work.
2. Name the ambiguity.
3. Explain the PFEM distinction in plain language.
4. Ask or infer which meaning is intended only if the repo/task context makes it safe.
5. Continue with the smallest doctrine-preserving change.
```

Do not use this protocol to stall obvious small edits. Use it when continuing under the wrong meaning could create wrong architecture, wrong records, wrong checks, or misleading documentation.

## Adapter / subsystem / source / consumer

Brake words:

```text
adapter
subsystem
source
consumer
connector
integration
```

PFEM distinction:

```text
external subsystem = real-world or separately deployed capability
PFEM adapter = software boundary glue that translates to/from PFEM contracts
evidence source = producer of evidence/confidence messages
consumer = downstream human/system/policy layer deciding what evidence means
PFEM core = contracts, checks, catalogs, receipts, relay logic, timing/provenance/confidence handling
```

Do not treat a vendor API, field system, sensor system, archive, or another PFEM node as automatically being a PFEM adapter.

## Validate / verify / prove / certify / truth

Brake words:

```text
validate
verify
prove
certify
truth
correct
accurate
```

PFEM can validate contract shape, schema fields, references, receipts, catalog/audit/integrity wiring, timing expectations, and provenance/confidence metadata shape.

PFEM does not automatically validate real-world truth inside an external subsystem.

Good language:

```text
PFEM validated the message shape.
PFEM verified required references are present.
PFEM recorded a timing anomaly.
The consumer judged the evidence sufficient for its purpose.
```

Bad language:

```text
PFEM proved the source was correct.
PFEM certified the vendor system's real-world truth.
PFEM knows the adapter failed.
```

## Confidence

Brake words:

```text
confidence
confidence percent
score
trust
reliability
```

Confidence metadata is not PFEM-certified truth.

Confidence may be source-declared, computed elsewhere, inherited from another node, or produced by a downstream consumer. The boundary producing the value must document its semantics.

PFEM should preserve confidence metadata and make it visible. PFEM should not silently convert it into a truth claim.

## Mesh

Brake words:

```text
mesh
federation
peer discovery
node discovery
availability
```

PFEM uses mesh in two related but different senses:

```text
internal evidence-reference mesh = records, receipts, closeouts, catalogs, audits, references
operational PFEM discovery mesh = later PFEM-to-PFEM discovery / ad hoc availability / capability exchange
```

Do not collapse those layers.

## Boundary / record species / generated boundary

Brake words:

```text
boundary
record species
generated boundary
add another boundary
next boundary
```

PFEM boundary generation is not casual.

Do not generate more PFEM boundaries unless:

```text
a gate exposes a real missing boundary
a documented workflow is incomplete
a record / verification receipt / closeout record triple was left half-finished
a developer deliberately opens a new chain
```

After a semantic endcap, stabilize and run gates instead of inventing more species.

## Profile / policy

Brake words:

```text
profile
policy
configuration
rule
```

PFEM distinction:

```text
profile = deployment shape/configuration
policy = decision logic, authorization rule, scoring rule, or interpretation rule
```

Do not silently put policy into a profile just because it is convenient.

## Evidence / observation / finding / report

Brake words:

```text
evidence
observation
finding
alert
report
package
rollup
```

PFEM keeps these separate.

Good language:

```text
raw evidence was recorded
an observation was normalized from evidence
a finding was derived by a policy/review layer
a report summarized findings and packages
```

Bad language:

```text
the report is the evidence
the alert proves the finding
the normalized observation replaces the raw source
```

## Rollup / federation / central control

Brake words:

```text
rollup
federation
central dashboard
master truth
single source of truth
```

Rollup moves attributable summaries, requests, and evidence packages across explicit sharing boundaries.

Rollup does not automatically mean central control, one master database, or one master truth system.

## Workorder

Brake words:

```text
workorder
handoff
executor
Codex task
agent task
```

Official PFEM workorders happen through the GitHub repository process.

A workorder must be a committed file under `workorders/`, launched by exact path, and referenced in PR or completion notes. Local-only files, Notepad drafts, downloadable prompts, and chat-only text are not official PFEM workorders.

## Full gate / release

Brake words:

```text
full gate
release
tag
ship
stabilize
```

Full gate is expensive and release/stabilization-oriented. Do not invoke it as filler.

Use focused checks for small changes. Use full gate for semantic closure, release/tag preparation, broad plumbing changes, or stabilization.

## AI instruction

When any of these terms becomes ambiguous, stop and clarify before implementing.

Do not pretend familiar software meanings are automatically PFEM meanings.
