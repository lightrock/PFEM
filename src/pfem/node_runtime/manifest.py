"""Node manifest helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class NodeManifest:
    node_id: str
    display_name: str
    profile_id: str
    node_kind: str
    status: str
    default_sharing_scope: str | None = None
    configured_adapters: list[str] = field(default_factory=list)


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


def load_node_manifest(path: str | Path) -> NodeManifest:
    raw = _parse_scalar_list_yaml(Path(path).read_text(encoding="utf-8"))

    return NodeManifest(
        node_id=str(raw.get("node_id", "")),
        display_name=str(raw.get("display_name", "")),
        profile_id=str(raw.get("profile_id", "")),
        node_kind=str(raw.get("node_kind", "")),
        status=str(raw.get("status", "")),
        default_sharing_scope=str(raw["default_sharing_scope"]) if "default_sharing_scope" in raw else None,
        configured_adapters=_as_list(raw.get("configured_adapters", [])),
    )
