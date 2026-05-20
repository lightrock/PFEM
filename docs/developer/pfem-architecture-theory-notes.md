# PFEM Architecture Theory Notes

This file preserves the higher-level architecture vocabulary behind PFEM without turning the main README into consulting fog.

These notes are not a claim that PFEM implements a formal external standard. They are the conceptual lenses that shaped the design. The executable truth remains the repository: records, schemas, validators, tools, catalogs, audit records, doctor checks, and gates.

## Core phrase

PFEM means:

```text
Polycentric Federated Evidence Mesh
```

That phrase is allowed to sound fancy because each word carries a job.

## Polycentric

Polycentric means there can be many legitimate centers of observation, custody, authority, review, and reporting.

PFEM should not assume one master database, one master dashboard, one master AI, or one master institution owns the whole truth.

Practical PFEM meaning:

```text
local evidence nodes can operate locally
different authorities can receive different packages
rollups can exist at multiple levels
review can happen without erasing local provenance
no single center should flatten the evidence ecology
```

A polycentric PFEM architecture should support:

```text
site-level evidence
custody-level evidence
retention-level evidence
public-access evidence
authority-facing evidence
rollup evidence
terminal closeout evidence
```

Each center can have its own duties while still participating in a shared evidence mesh.

## Federated

Federated means PFEM nodes can share durable evidence products without pretending they are all one database.

Practical PFEM meaning:

```text
a node emits records
records carry stable identifiers
records cite prior records or artifacts
receipts verify specific claims
closeout records mark completed boundaries
rollups summarize without destroying underlying evidence
```

Federation is not just network connectivity. It is structured participation across boundaries.

## Evidence Mesh

Evidence mesh means records link to other records, artifacts, receipts, manifests, decisions, reports, and closeouts.

PFEM should not be a stack of isolated JSON files. It should be a web of accountable references.

Practical PFEM meaning:

```text
records identify what happened
verification receipts show what was checked
closeout records show what boundary was closed
catalogs make the mesh visible
audit records explain who/what recorded the event
integrity manifests make drift detectable
doctor checks make broken structure visible
```

The mesh is useful only if links are checkable.

## Miller / living systems lens

James Grier Miller's living-systems vocabulary is useful here as an architecture lens, not as biological cosplay.

PFEM can be read as a system of subsystems that must handle:

```text
inputs
channels
memory
deciders
boundary maintenance
processors
outputs
feedback
```

In PFEM terms:

```text
input = evidence received or recorded
channel = transport, routing, dispatch, inbox/outbox
memory = records, manifests, archives, retention stores
decider = validation, policy, audit, approval, release
boundary = custody, retention, access, publication, closeout
processor = validators, catalog builders, integrity checkers
output = reports, receipts, packages, rollups, public-access products
feedback = failures, audit findings, doctor checks, full-gate results
```

This lens helps prevent a blob architecture. If a concept has a different living-systems role, it probably deserves a separate record species or subsystem boundary.

## Process ecology

PFEM is not just object modeling. It is process ecology.

A record species is like a small ecological niche. It exists because a responsibility exists.

Healthy PFEM species have:

```text
a clear name
a clear predecessor or source
a clear downstream use
a schema
a validator
a catalog view
an audit event
a test
a closeout path when the responsibility is done
```

Unhealthy PFEM species are vague, orphaned, duplicate, or generated only because the generator could generate them.

The "semantic endcap" rule comes from process ecology: when a process chain has reached its real terminal niche, stop adding species and stabilize the ecosystem.

## Cybernetic control loop

PFEM has a cybernetic shape:

```text
observe
record
compare against policy/contract
verify
correct or escalate
close out
roll up
feed results back into the next check
```

This is why tests and doctor checks are part of the architecture, not afterthoughts.

PFEM should never be merely "data at rest." It should be a governed loop that can notice drift, missing references, broken schemas, stale assumptions, and fake closure.

## Provenance and chain-of-custody thinking

PFEM borrows heavily from provenance and chain-of-custody thinking.

A claim is stronger when PFEM can answer:

```text
what record made the claim
what evidence or prior record it cited
what receipt verified it
what closeout ended the boundary
what audit event recorded it
what integrity manifest covers it
what catalog exposes it
```

This is why "just add a JSON file" is not enough.

## Event-sourced flavor, without forcing the buzzword

PFEM has an event-sourced flavor because durable records matter more than mutable hidden state.

But PFEM should not use the phrase as decoration. The actual rule is simpler:

```text
if the state matters, record how it got that way
if a boundary closes, write the closeout
if a check passed, write the receipt
if a package moves, write the transport/custody evidence
```

## Neutral language and anti-hype rule

The fancy theory belongs in this file. The operator-facing docs should stay plain.

Use theory to guide structure. Do not use theory to obscure weak mechanics.

Bad:

```text
PFEM operationalizes a multidimensional hyper-governance substrate.
```

Good:

```text
PFEM keeps evidence, verification, closeout, catalog, audit, and rollup boundaries separate and testable.
```

## Design obligations implied by the theory

The theory implies practical obligations:

```text
do not collapse evidence into interpretation
do not collapse local nodes into one central truth
do not collapse receipt, report, and closeout into one blob
do not add species without a process role
do not add infrastructure without an earned need
do not let AI become the only place where doctrine lives
do not pass tests by inventing fake evidence
```

## Where this sits in the repo

Use these files together:

```text
README.md
AGENTS.md
docs/developer/pfem-boundary-language-generation-standard.md
docs/developer/pfem-new-chat-handoff.md
docs/developer/pfem-terminal-tail-stabilization.md
docs/developer/pfem-architecture-theory-notes.md
tools/pfem_check_manifest.json
```

The theory notes explain why PFEM feels like PFEM.

The standards and checks explain how to keep it from drifting.
