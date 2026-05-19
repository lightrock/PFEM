"""Template PFEM adapter normalizer."""

from __future__ import annotations

from typing import Any


def normalize(decoded: dict[str, Any]) -> dict[str, Any]:
    """Normalize decoded source input into a PFEM observation candidate."""
    return {
        "observation_kind": "template_observation",
        "normalized_fields": {
            "source_summary": str(decoded.get("payload", ""))[:120],
        },
        "confidence": 0.0,
        "uncertainty_notes": "Template adapter output; replace with real normalization.",
    }
