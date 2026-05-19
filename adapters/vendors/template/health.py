"""Template PFEM adapter health check."""

from __future__ import annotations


def check_health() -> dict[str, str]:
    """Return basic adapter health."""
    return {
        "status": "template",
        "message": "Template adapter health check is not connected to a real source.",
    }
