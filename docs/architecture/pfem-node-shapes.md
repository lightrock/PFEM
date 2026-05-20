# PFEM Node Shapes

PFEM supports many node shapes that share architecture contracts while retaining local sovereignty.

Core cross-node rule:

- Local truth stays local.
- Shared awareness moves through bounded, lineage-preserving summaries.
- Rollup nodes may detect patterns, but they do not automatically own or replace local evidence.

All node shapes should preserve provenance, timing, and confidence metadata when producing PFEM objects or federation messages.

## Critical-infrastructure / facility node

A facility node is a local operational node for a bounded site or installation.

- May ingest:
  - facility instrumentation outputs
  - local observer reports
  - external subsystem messages through PFEM adapters
- May retain locally:
  - raw evidence and source metadata
  - normalized observations and local findings/alerts
  - local review records and evidence packages
- May emit/share:
  - bounded summaries
  - attributable alert/finding summaries
  - evidence-package references when sharing policy allows
- Should not claim:
  - sector-wide global truth
  - that source-declared confidence is PFEM-certified truth
- Must preserve metadata:
  - source identity/class, timing windows, declared confidence, provenance refs
- Rollup/federation boundary relation:
  - local records remain authoritative for local events
  - outbound sharing uses explicit recipient scope and boundary rules

## Municipal / civic node

A municipal node coordinates civic situational awareness from multiple local contributors.

- May ingest:
  - summaries from facility nodes
  - public-safety observations
  - civic observer submissions through adapters
- May retain locally:
  - received federation messages
  - local correlation context and municipal findings
  - local review and policy decision records
- May emit/share:
  - municipality-level summaries and requests
  - bounded packages for regional coordination
- Should not claim:
  - ownership of all local raw evidence from contributing nodes
  - that missing messages prove external subsystem failure
- Must preserve metadata:
  - source-node identity, freshness windows, confidence semantics, provenance lineage
- Rollup/federation boundary relation:
  - municipal rollups summarize cross-source context without replacing site-level records

## HAM/RACES / civic-observer node

A civic-observer node contributes observer and open-source telemetry with explicit uncertainty handling.

- May ingest:
  - volunteer radio reports
  - open telemetry feeds and public observation channels
  - locally collected observer notes
- May retain locally:
  - raw observer evidence
  - normalization output with confidence and uncertainty markers
- May emit/share:
  - observation summaries and attributable references
  - requests for corroboration
- Should not claim:
  - equivalent certainty to calibrated site instrumentation by default
  - command authority over facility or municipal policy
- Must preserve metadata:
  - observer/source class, capture method, timing, uncertainty flags, provenance refs
- Rollup/federation boundary relation:
  - provides complementary evidence into shared awareness layers with explicit confidence posture

## Sector / category rollup node

A sector rollup node aggregates attributable summaries from many participant nodes.

- May ingest:
  - rollup/federation summaries from facility, civic, and observer nodes
  - evidence-package references within allowed sharing scope
- May retain locally:
  - aggregated summaries
  - pattern/campaign hypotheses and trend views
  - lineage references back to contributing messages
- May emit/share:
  - sector-level pattern summaries
  - requests for additional corroboration
- Should not claim:
  - master truth for all participating local nodes
  - possession of all underlying raw records
- Must preserve metadata:
  - source-node lineage, observation windows, confidence composition notes, completeness bounds
- Rollup/federation boundary relation:
  - rollup outputs remain derived summaries and must reference contributing boundaries

## Research / testbed node

A research node evaluates methods, replay, and comparison experiments under controlled boundaries.

- May ingest:
  - replay datasets
  - synthetic or historical PFEM-compatible records
  - bounded exports from operational nodes where policy permits
- May retain locally:
  - experiment datasets and outcomes
  - method-comparison findings
- May emit/share:
  - reproducible summaries, test artifacts, and method notes
- Should not claim:
  - direct operational authority over production decisions
  - that a testbed confidence model automatically transfers to all deployments
- Must preserve metadata:
  - dataset provenance, replay windows, model/version context, uncertainty and limits
- Rollup/federation boundary relation:
  - can share bounded findings into rollups as research-context outputs, not operational truth replacement

## Disconnected / edge node

A disconnected edge node operates with intermittent links and delayed federation.

- May ingest:
  - local sensors and manual reports
  - delayed bundle imports when links are available
- May retain locally:
  - raw and derived evidence for offline operation
  - sync queue state and replay references
- May emit/share:
  - deferred summaries and packages during synchronization windows
  - explicit freshness and completeness notes
- Should not claim:
  - complete global context during disconnection windows
  - that delayed federation implies remote failure causality
- Must preserve metadata:
  - capture times, enqueue/dequeue times, confidence semantics, provenance chain continuity
- Rollup/federation boundary relation:
  - synchronizes through explicit bounded sharing once channels resume

## Cross-shape doctrine

Across all node shapes:

- A PFEM adapter is boundary translation glue, not the external subsystem itself.
- PFEM can validate contract shape and lineage wiring, but does not automatically certify real-world truth inside external subsystems.
- Confidence metadata must remain visible as metadata and should not be upgraded into certainty claims.
