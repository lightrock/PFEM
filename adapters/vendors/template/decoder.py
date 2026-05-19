"""Template PFEM adapter decoder."""

from __future__ import annotations

from typing import Any


def decode_raw(payload: Any) -> dict[str, Any]:
    """Decode source-specific payload into a raw evidence candidate.

    Real adapters should preserve enough source material for traceability.
    """
    return {
        "evidence_kind": "template_raw_input",
        "payload": payload,
    }
