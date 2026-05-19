"""Adapter manifest helpers.

This loader intentionally accepts a small YAML subset so the project does not
need runtime dependencies yet. It is enough for simple PFEM manifest smoke
checks, not a general YAML parser.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class AdapterManifest:
    adapter_id: str
    display_name: str
    capabilities: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)


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


def load_adapter_manifest(path: str | Path) -> AdapterManifest:
    raw = _parse_scalar_list_yaml(Path(path).read_text(encoding="utf-8"))

    return AdapterManifest(
        adapter_id=str(raw.get("adapter_id", "")),
        display_name=str(raw.get("display_name", "")),
        capabilities=list(raw.get("capabilities", [])),
        outputs=list(raw.get("outputs", [])),
    )
