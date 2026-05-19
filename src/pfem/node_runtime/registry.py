"""Node registry helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from pfem.node_runtime.manifest import load_node_manifest
from pfem.profile_runtime import load_profile_registry


@dataclass(frozen=True)
class NodeRegistryEntry:
    node_id: str
    path: str
    profile_id: str
    status: str


@dataclass(frozen=True)
class NodeRegistry:
    registry_id: str
    version: str
    nodes: list[NodeRegistryEntry]


def load_node_registry(path: str | Path) -> NodeRegistry:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [
        NodeRegistryEntry(
            node_id=str(item.get("node_id", "")),
            path=str(item.get("path", "")),
            profile_id=str(item.get("profile_id", "")),
            status=str(item.get("status", "")),
        )
        for item in raw.get("nodes", [])
    ]
    return NodeRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        nodes=entries,
    )


def collect_node_ids(root: str | Path) -> set[str]:
    root_path = Path(root)
    registry_path = root_path / "nodes" / "node-registry.json"
    if not registry_path.exists():
        return set()
    registry = load_node_registry(registry_path)
    return {entry.node_id for entry in registry.nodes if entry.node_id}


def validate_node_registry(root: str | Path) -> list[str]:
    root_path = Path(root)
    registry_path = root_path / "nodes" / "node-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        failures.append("missing node registry: nodes/node-registry.json")
        return failures

    registry = load_node_registry(registry_path)
    seen: set[str] = set()

    profile_registry_path = root_path / "profiles" / "profile-registry.json"
    profile_ids: set[str] = set()
    if profile_registry_path.exists():
        profile_registry = load_profile_registry(profile_registry_path)
        profile_ids = {entry.profile_id for entry in profile_registry.profiles if entry.profile_id}

    if not registry.registry_id:
        failures.append("node registry missing registry_id")
    if not registry.version:
        failures.append("node registry missing version")

    for entry in registry.nodes:
        if not entry.node_id:
            failures.append("node registry entry missing node_id")
            continue
        if entry.node_id in seen:
            failures.append(f"duplicate node registry node_id: {entry.node_id}")
        seen.add(entry.node_id)

        if profile_ids and entry.profile_id not in profile_ids:
            failures.append(f"node registry references unknown profile_id {entry.profile_id!r}: {entry.node_id}")

        manifest_path = root_path / entry.path
        if not manifest_path.exists():
            failures.append(f"node registry path missing: {entry.path}")
            continue

        manifest = load_node_manifest(manifest_path)
        if manifest.node_id != entry.node_id:
            failures.append(
                f"node registry id mismatch for {entry.path}: "
                f"registry={entry.node_id!r} manifest={manifest.node_id!r}"
            )
        if manifest.profile_id != entry.profile_id:
            failures.append(
                f"node registry profile mismatch for {entry.path}: "
                f"registry={entry.profile_id!r} manifest={manifest.profile_id!r}"
            )

    return failures
