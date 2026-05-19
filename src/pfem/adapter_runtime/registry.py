"""Adapter registry helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from pfem.adapter_runtime.manifest import load_adapter_manifest


@dataclass(frozen=True)
class AdapterRegistryEntry:
    adapter_id: str
    path: str
    adapter_kind: str
    status: str


@dataclass(frozen=True)
class AdapterRegistry:
    registry_id: str
    version: str
    adapters: list[AdapterRegistryEntry]


def load_adapter_registry(path: str | Path) -> AdapterRegistry:
    """Load the PFEM adapter registry JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [
        AdapterRegistryEntry(
            adapter_id=str(item.get("adapter_id", "")),
            path=str(item.get("path", "")),
            adapter_kind=str(item.get("adapter_kind", "")),
            status=str(item.get("status", "")),
        )
        for item in raw.get("adapters", [])
    ]
    return AdapterRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        adapters=entries,
    )


def validate_adapter_registry(root: str | Path) -> list[str]:
    """Validate adapter registry entries against their manifests."""
    root_path = Path(root)
    registry_path = root_path / "adapters" / "adapter-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        failures.append("missing adapter registry: adapters/adapter-registry.json")
        return failures

    registry = load_adapter_registry(registry_path)
    seen: set[str] = set()

    if not registry.registry_id:
        failures.append("adapter registry missing registry_id")
    if not registry.version:
        failures.append("adapter registry missing version")

    for entry in registry.adapters:
        if not entry.adapter_id:
            failures.append("adapter registry entry missing adapter_id")
            continue
        if entry.adapter_id in seen:
            failures.append(f"duplicate adapter registry adapter_id: {entry.adapter_id}")
        seen.add(entry.adapter_id)

        manifest_path = root_path / entry.path
        if not manifest_path.exists():
            failures.append(f"adapter registry path missing: {entry.path}")
            continue

        manifest = load_adapter_manifest(manifest_path)
        if manifest.adapter_id != entry.adapter_id:
            failures.append(
                f"adapter registry id mismatch for {entry.path}: "
                f"registry={entry.adapter_id!r} manifest={manifest.adapter_id!r}"
            )

    return failures
