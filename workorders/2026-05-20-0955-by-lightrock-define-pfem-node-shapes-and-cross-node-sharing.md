# Define PFEM Node Shapes and Cross-Node Sharing

## Purpose

Define PFEM's polymorphic node model and cross-node evidence-sharing doctrine so future humans, AI assistants, Codex sessions, and contributors understand the big architecture before they invent local-only assumptions.

PFEM is not just a drone-detection app, a vendor-adapter framework, or a central dashboard. PFEM is a polycentric evidence coordination pattern for many node shapes that may exchange bounded, lineage-preserving, confidence-aware summaries while preserving local sovereignty and source differences.

This workorder should produce front-door architecture documentation that explains how different PFEM node types can interoperate without collapsing into one central truth store.

## Scope

Create or update architecture documentation that defines at least these PFEM node shapes:

```text
critical-infrastructure / facility node
municipal / civic node
HAM/RACES / civic-observer node
sector / category rollup node
research / testbed node
disconnected / edge node
```

For each node shape, describe:

```text
what it may ingest
what it may retain locally
what it may emit/share
what it should not claim
what confidence/provenance/timing metadata it must preserve
how it relates to rollup/federation boundaries
```

Define the core cross-node rule:

```text
Local truth stays local.
Shared awareness moves through bounded, lineage-preserving summaries.
Rollup nodes may detect patterns, but they do not automatically own or replace local evidence.
```

Include a minimal illustrative message shape for cross-node sharing, clearly labeled as conceptual unless a real schema is being added.

The message example should include at least:

```text
message_type
source_node_id
source_node_shape
observation_window
observation_class
source_classes
confidence metadata
provenance_refs
sharing_boundary
raw_evidence_shared flag
recipient_scope
```

## Files/areas likely to change

Likely files:

```text
docs/architecture/pfem-node-shapes.md
docs/architecture/cross-node-sharing-model.md
README.md
AGENTS.md
docs/AI_START_HERE.md
docs/developer/pfem-new-tab-prompt.md
docs/developer/pfem-terminology-brake-rules.md
```

Optional follow-up files if the executor finds the repo already has the right place for them:

```text
contracts/*
ai/architecture-rules.md
ai/evidence-rules.md
```

Do not create schema files unless the work clearly earns them. A conceptual message example is enough for this pass unless a current contract folder already expects such a document.

## Out of scope

Do not implement runtime networking, peer discovery, databases, queues, identity, authorization, dashboards, drone-specific workflows, or real vendor integrations.

Do not generate more PFEM record species or retention/archive boundaries.

Do not make refinery, drone, HAM/RACES, APRS, ADS-B, or any specific operational sector the only public use case. Use neutral language such as facility node, civic observer node, volunteer radio node, municipal node, and sector rollup node. Specific examples may be used sparingly to explain why the architecture exists.

Do not collapse adapter, subsystem, evidence source, consumer, node, and PFEM core language.

## Constraints

Follow these repo rules first:

```text
AGENTS.md
docs/AI_START_HERE.md
docs/developer/pfem-adapters-and-subsystems.md
docs/developer/pfem-terminology-brake-rules.md
docs/developer/pfem-boundary-language-generation-standard.md
docs/developer/pfem-ai-patch-safety-rules.md
workorders/README.md
```

Use PFEM terminology carefully:

```text
external subsystem != PFEM adapter
confidence metadata != PFEM-certified truth
timing anomaly != known failure
rollup != central command
summary != raw evidence
profile != policy
```

Preserve the doctrine that PFEM observes contracts, provenance, timing, and confidence metadata; it does not automatically know real-world truth inside external subsystems.

If a term becomes ambiguous, use the brake-word protocol and clarify before continuing.

## Required checks

Run the lightest checks that prove the documentation and repo discipline are not broken.

At minimum, run any available quick/doc/repo-discipline checks. Prefer:

```text
pfem_check.bat --quick --timings
```

If `pfem_check.bat` is not available in the executor environment, run the relevant Python checks from `tools/` and report exactly what was run.

Do not run the expensive full gate unless the executor or maintainer intentionally promotes this task into release/stabilization work.

## Expected result

After execution, a new human or AI should be able to read the architecture docs and understand:

```text
PFEM has multiple node shapes.
Different node shapes can have different evidence classes, confidence, trust posture, and sharing rules.
A facility node is not a city node.
A civic/HAM/RACES observer node is not fake refinery instrumentation.
A sector rollup is not central command or master truth.
A PFEM adapter is not the whole subsystem.
Confidence metadata is not certified truth.
A rollup summary is not raw evidence.
```

The documentation should make the motivating idea obvious:

```text
PFEM supports many local truths, selectively shared upward or laterally as normalized, lineage-preserving, confidence-aware summaries.
```

## Fallback behavior

If the repo already has an equivalent node-shapes or cross-node-sharing document, update the existing document instead of duplicating it.

If a naming conflict appears in `workorders/`, stop and report it before proceeding unless explicitly overridden.

If the executor cannot run checks, it must say so plainly and explain what it inspected instead.

If the scope starts turning into implementation, stop and report that a follow-up workorder is needed.

## Executor launch instruction

After this workorder is committed, give the executor this exact instruction:

```text
Read workorders/2026-05-20-0955-by-lightrock-define-pfem-node-shapes-and-cross-node-sharing.md and execute it.
```
