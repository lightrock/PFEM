"""Manual observer report decoder."""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = ["report_id", "reported_time", "observer_label", "description"]


def decode_raw(payload: dict[str, Any]) -> dict[str, Any]:
    """Decode a manual observer report into a raw evidence candidate."""
    missing = [field for field in REQUIRED_FIELDS if not payload.get(field)]
    if missing:
        raise ValueError(f"manual observer report missing required fields: {', '.join(missing)}")

    return {
        "evidence_id": f"manual-report-{payload['report_id']}",
        "evidence_kind": "manual_observer_report",
        "source_id": str(payload.get("source_channel") or "manual-entry"),
        "received_time": str(payload["reported_time"]),
        "observed_time": str(payload["reported_time"]),
        "payload": dict(payload),
        "provenance": {
            "adapter_id": "manual-observer-report",
            "observer_label": str(payload["observer_label"]),
        },
        "uncertainty_notes": payload.get("uncertainty_notes"),
    }
