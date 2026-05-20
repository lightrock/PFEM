# Cross-Node Sharing Model

PFEM cross-node sharing is bounded federation of attributable summaries, requests, and package references.

## Core rule

- Local truth stays local.
- Shared awareness moves through bounded, lineage-preserving summaries.
- Rollup nodes may detect patterns, but they do not automatically own or replace local evidence.

## Sharing boundary principles

- Share by explicit recipient scope rather than implicit global broadcast.
- Preserve provenance references to contributing evidence or summaries.
- Preserve timing windows and freshness metadata.
- Preserve confidence and uncertainty metadata without converting it into certainty claims.
- Mark completeness limits when summaries omit local detail.
- Keep rollups as derived products, not source-evidence replacement.

## Conceptual cross-node message shape

The following shape is conceptual architecture guidance, not a committed schema contract.

```yaml
message_type: observation_summary
source_node_id: node-123
source_node_shape: facility-node
observation_window:
  start_time: 2026-05-20T09:00:00Z
  end_time: 2026-05-20T09:15:00Z
observation_class: airspace_activity
source_classes:
  - facility_instrumentation
  - civic_observer
confidence_metadata:
  declared_confidence: 0.72
  confidence_semantics: source_declared_probability
  uncertainty_notes:
    - intermittent line-of-sight
provenance_refs:
  - evidence:raw:site-a:evt-00917
  - observation:norm:site-a:obs-553
sharing_boundary: municipal-coordination
raw_evidence_shared: false
recipient_scope:
  - municipal-node-west
  - sector-rollup-regional
```

## Field intent summary

- `message_type`: declares the PFEM message intent/category.
- `source_node_id`: identifies sender for attribution and follow-up.
- `source_node_shape`: indicates deployment-shape context.
- `observation_window`: bounds timing for recency and sequencing.
- `observation_class`: high-level normalized class for downstream handling.
- `source_classes`: indicates contributing source categories without collapsing distinctions.
- `confidence_metadata`: preserves confidence and uncertainty semantics as metadata.
- `provenance_refs`: points to upstream records/summaries for lineage.
- `sharing_boundary`: identifies policy boundary used for transmission.
- `raw_evidence_shared`: explicit flag preventing ambiguity about payload sensitivity.
- `recipient_scope`: explicit destination scope for bounded dissemination.

## Non-claims to preserve

A cross-node message should not imply:

- the sender has global truth;
- the receiver now owns all source raw evidence;
- confidence metadata is certified truth;
- timing anomalies are proof of subsystem failure.

## Relationship to existing PFEM models

- Use this model with the federation model for attributable exchange behavior.
- Use this model with the rollup model for derived-summary expectations.
- Use this model with evidence lifecycle rules to preserve object separation and lineage.
