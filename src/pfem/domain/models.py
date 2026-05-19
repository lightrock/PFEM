"""Core PFEM domain models.

These are intentionally small dataclasses. They are not a database model, API
model, or UI model. They exist to keep the domain nouns explicit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class RawEvidence:
    evidence_id: str
    evidence_kind: str
    source_id: str
    received_time: str
    observed_time: str | None = None
    payload_ref: str | None = None
    payload: Any | None = None
    integrity: JsonObject = field(default_factory=dict)
    provenance: JsonObject = field(default_factory=dict)
    uncertainty_notes: str | None = None


@dataclass(frozen=True)
class NormalizedObservation:
    observation_id: str
    observation_kind: str
    source_evidence_ids: list[str]
    observed_time: str
    normalized_fields: JsonObject = field(default_factory=dict)
    confidence: float | None = None
    uncertainty_notes: str | None = None


@dataclass(frozen=True)
class Finding:
    finding_id: str
    finding_kind: str
    created_time: str
    source_observation_ids: list[str]
    subject_refs: list[str] = field(default_factory=list)
    reasoning_ref: str | None = None
    confidence: float | None = None
    uncertainty_notes: str | None = None


@dataclass(frozen=True)
class Alert:
    alert_id: str
    alert_kind: str
    finding_id: str
    created_time: str
    status: str
    severity: str | None = None
    policy_basis: str | None = None
    recommended_review_path: str | None = None


@dataclass(frozen=True)
class EvidencePackage:
    package_id: str
    created_time: str
    included_refs: list[str]
    scope: str | None = None
    summary: str | None = None
    lineage_notes: str | None = None


@dataclass(frozen=True)
class FederationMessage:
    message_id: str
    message_kind: str
    sender_node_id: str
    created_time: str
    subject_refs: list[str] = field(default_factory=list)
    payload_summary: str | None = None
    lineage_refs: list[str] = field(default_factory=list)
    sharing_scope: str | None = None
    attribution: JsonObject = field(default_factory=dict)


@dataclass(frozen=True)
class RollupSummary:
    rollup_id: str
    producer_node_id: str
    created_time: str
    summary_kind: str
    scope: str | None = None
    included_subject_refs: list[str] = field(default_factory=list)
    source_lineage_refs: list[str] = field(default_factory=list)
    confidence_notes: str | None = None
    completeness_notes: str | None = None
    sharing_scope: str | None = None
