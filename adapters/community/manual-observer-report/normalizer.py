"""Manual observer report normalizer."""

from __future__ import annotations

from typing import Any


def normalize(decoded: dict[str, Any]) -> dict[str, Any]:
    """Normalize decoded manual report evidence into an observation candidate."""
    payload = decoded.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("decoded manual report evidence is missing payload")

    normalized_fields: dict[str, Any] = {
        "description": payload.get("description", ""),
        "observer_label": payload.get("observer_label", ""),
        "location_text": payload.get("location_text"),
        "source_channel": payload.get("source_channel", "manual-entry"),
        "attachments": payload.get("attachments", []),
    }

    if "latitude" in payload:
        normalized_fields["latitude"] = payload["latitude"]
    if "longitude" in payload:
        normalized_fields["longitude"] = payload["longitude"]

    uncertainty_notes = payload.get("uncertainty_notes") or decoded.get("uncertainty_notes")
    confidence = 0.5 if uncertainty_notes else 0.7

    return {
        "observation_id": f"obs-{decoded['evidence_id']}",
        "observation_kind": "manual_observer_report",
        "source_evidence_ids": [decoded["evidence_id"]],
        "observed_time": decoded["observed_time"],
        "normalized_fields": normalized_fields,
        "confidence": confidence,
        "uncertainty_notes": uncertainty_notes,
    }
