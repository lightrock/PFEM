"""Manual observer report adapter health."""

from __future__ import annotations


def check_health() -> dict[str, str]:
    """Return simple health for the manual adapter."""
    return {
        "status": "ok",
        "message": "Manual observer report adapter is file/function based.",
    }
