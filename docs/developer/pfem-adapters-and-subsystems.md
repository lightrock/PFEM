# PFEM Adapters, External Subsystems, Timing, and Confidence

This note exists because AI assistants, Copilot sessions, Codex sessions, and human contributors can easily flatten several different PFEM concepts into one overloaded word: adapter.

Do not do that.

PFEM needs clear language for these different things:

```text
external subsystem = real-world or separately deployed capability
PFEM adapter = software boundary glue that translates to or from PFEM contracts
evidence source = the thing that produces or supplies evidence/confidence messages
PFEM core = the repository/runtime contracts, checks, catalogs, receipts, and relay logic
consumer = the downstream human, system, policy layer, node, or review process that decides what evidence means operationally
```

## External subsystem

An external subsystem is a real operational capability outside the PFEM core.

Examples:

```text
field sensor subsystem
radio subsystem
file-drop subsystem
archive subsystem
public-access subsystem
authority reporting subsystem
PFEM peer-discovery subsystem
another PFEM node
```

A subsystem may include people, devices, services, databases, files, policies, organizations, or other PFEM deployments.

A subsystem is not automatically a Python module and is not automatically part of this repository.

## PFEM adapter

A PFEM adapter is software boundary glue.

A PFEM adapter may translate messages, files, payloads, or service calls between PFEM contracts and an external subsystem. It may live inside this repository for core-supported integrations, or it may live outside this repository as part of a separately deployed subsystem.

A PFEM adapter should usually:

```text
isolate source-specific weirdness
preserve provenance
preserve confidence metadata
translate into PFEM contracts
avoid owning policy
avoid deciding findings by itself
avoid pretending to be the whole subsystem
```

## Contract, not ownership

External subsystems may be autonomous.

PFEM core should not assume it owns an external subsystem just because there is an adapter-shaped integration point.

For external subsystems, PFEM primarily sees:

```text
messages that arrive
messages that do not arrive
message shape
provenance metadata
confidence metadata
timing, recency, and heartbeat behavior
references to evidence products or prior records
```

PFEM may not know why an external subsystem is silent, late, malformed, noisy, or wrong.

PFEM should not pretend to have ground truth about the inside of another subsystem.

## Timing anomaly is not known failure

If PFEM has not heard from a source in a while, PFEM can record or surface a timing anomaly.

That is not the same as PFEM knowing the external subsystem failed.

Good language:

```text
PFEM has not received an expected message from source X within the expected window.
PFEM observed an abnormal timing pattern for source X.
PFEM received malformed or contract-invalid input from source X.
```

Bad language:

```text
PFEM knows the adapter failed.
PFEM repaired the adapter.
PFEM certified that the source is wrong.
```

## Confidence metadata is not PFEM-certified truth

PFEM may carry confidence metadata on evidence and messages.

That confidence metadata may be source-declared, computed elsewhere, inherited from another node, or produced by a downstream consumer. The exact semantics must be documented by the boundary that produces it.

PFEM core should preserve the metadata and make it visible. PFEM core should not silently convert confidence metadata into certified truth.

Good language:

```text
the source declared 82% confidence
the record carries confidence metadata
the consumer may weigh this evidence with timing, provenance, and other sources
```

Bad language:

```text
PFEM proved this is 82% true.
PFEM certified the source as correct.
```

## Validation boundaries

PFEM validates its own contracts and internal consistency.

PFEM can validate:

```text
schema shape
required fields
record references
verification receipt structure
catalog/audit/integrity wiring
timing and heartbeat expectations
provenance and confidence fields being present and well-formed
```

PFEM does not automatically validate:

```text
real-world truth inside an external subsystem
why an external subsystem went silent
whether an external subsystem's self-reported confidence is honest
whether a sensor was physically correct
whether a human source was mistaken
```

That judgment belongs to consumers, review processes, policy layers, cross-source comparison, or other PFEM nodes.

## Mesh behavior

PFEM is not a central puppeteer.

The mesh should support evidence movement, provenance, timing awareness, confidence metadata, and bounded sharing across nodes and subsystems.

The mesh should not imply that PFEM core centrally controls or fully understands every subsystem.

## AI instruction

When working on PFEM, do not collapse these terms:

```text
external subsystem
PFEM adapter
evidence source
message producer
consumer
PFEM core
```

If a task uses the word adapter, inspect the surrounding docs and ask which meaning is intended before changing architecture.

Prefer precise phrasing over familiar software assumptions.
