"""Node profile helpers.

Uses the same tiny YAML subset approach as adapter manifests. This keeps the
architecture seed dependency-free while still giving tests something real to
exercise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class NodeProfile:
    profile_id: str
    profile_kind: str
    enabled_capabilities: list[str] = field(default_factory=list)
    disabled_capabilities: list[str] = field(default_factory=list)
    default_adapters: list[str] = field(default_factory=list)
    dashboard_mode: str | None = None
    review_gates: list[str] = field(default_factory=list)
    offline_behavior: str | None = None


def _parse_scalar_list_yaml(text: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- ") and current_key:
            value = stripped[2:].strip()
            data.setdefault(current_key, [])
            target = data[current_key]
            if isinstance(target, list):
                target.append(value)
            continue

        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "[]":
                data[key] = []
            elif value:
                data[key] = value
            else:
                data[key] = []

    return data


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_node_profile(path: str | Path) -> NodeProfile:
    raw = _parse_scalar_list_yaml(Path(path).read_text(encoding="utf-8"))

    return NodeProfile(
        profile_id=str(raw.get("profile_id", "")),
        profile_kind=str(raw.get("profile_kind", "")),
        enabled_capabilities=_as_list(raw.get("enabled_capabilities", [])),
        disabled_capabilities=_as_list(raw.get("disabled_capabilities", [])),
        default_adapters=_as_list(raw.get("default_adapters", [])),
        dashboard_mode=str(raw["dashboard_mode"]) if "dashboard_mode" in raw else None,
        review_gates=_as_list(raw.get("review_gates", [])),
        offline_behavior=str(raw["offline_behavior"]) if "offline_behavior" in raw else None,
    )
