"""PFEM catalog.

The catalog is a read-only summary of the PFEM design pattern on disk.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pfem.adapter_runtime import load_adapter_registry
from pfem.capability_runtime import load_capability_manifest
from pfem.doctor import find_repo_root
from pfem.example_runtime import load_example_registry
from pfem.profile_runtime import load_profile_registry


def _capability_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    capabilities_dir = root / "capabilities"
    if not capabilities_dir.exists():
        return rows

    for path in sorted(capabilities_dir.rglob("*.capability.yaml")):
        manifest = load_capability_manifest(path)
        rows.append({
            "capability_id": manifest.capability_id,
            "display_name": manifest.display_name,
            "capability_kind": manifest.capability_kind,
            "requires": manifest.requires,
            "produces": manifest.produces,
            "path": str(path.relative_to(root)),
        })

    return rows


def _adapter_rows(root: Path) -> list[dict[str, Any]]:
    registry_path = root / "adapters" / "adapter-registry.json"
    if not registry_path.exists():
        return []

    registry = load_adapter_registry(registry_path)
    return [
        {
            "adapter_id": entry.adapter_id,
            "adapter_kind": entry.adapter_kind,
            "status": entry.status,
            "path": entry.path,
        }
        for entry in registry.adapters
    ]


def _profile_rows(root: Path) -> list[dict[str, Any]]:
    registry_path = root / "profiles" / "profile-registry.json"
    if not registry_path.exists():
        return []

    registry = load_profile_registry(registry_path)
    return [
        {
            "profile_id": entry.profile_id,
            "profile_kind": entry.profile_kind,
            "status": entry.status,
            "path": entry.path,
        }
        for entry in registry.profiles
    ]


def _example_rows(root: Path) -> list[dict[str, Any]]:
    registry_path = root / "examples" / "example-registry.json"
    if not registry_path.exists():
        return []

    registry = load_example_registry(registry_path)
    return [
        {
            "example_id": entry.example_id,
            "profile_id": entry.profile_id,
            "runnable": entry.runnable,
            "status": entry.status,
            "path": entry.path,
        }
        for entry in registry.examples
    ]


def build_catalog(start: str | Path | None = None) -> dict[str, Any]:
    """Build a read-only PFEM catalog."""
    root = find_repo_root(start)

    capabilities = _capability_rows(root)
    adapters = _adapter_rows(root)
    profiles = _profile_rows(root)
    examples = _example_rows(root)

    return {
        "root": str(root),
        "counts": {
            "capabilities": len(capabilities),
            "adapters": len(adapters),
            "profiles": len(profiles),
            "examples": len(examples),
        },
        "capabilities": capabilities,
        "adapters": adapters,
        "profiles": profiles,
        "examples": examples,
    }


def _format_table(title: str, rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines: list[str] = []
    lines.append("")
    lines.append(title)
    lines.append("-" * len(title))

    if not rows:
        lines.append("(none)")
        return lines

    widths = {
        column: max(len(column), *(len(str(row.get(column, ""))) for row in rows))
        for column in columns
    }

    header = "  ".join(column.ljust(widths[column]) for column in columns)
    lines.append(header)
    lines.append("  ".join("-" * widths[column] for column in columns))

    for row in rows:
        lines.append("  ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))

    return lines


def format_catalog(catalog: dict[str, Any]) -> str:
    """Format a PFEM catalog as readable text."""
    lines: list[str] = []
    counts = catalog["counts"]

    lines.append(f"PFEM catalog root: {catalog['root']}")
    lines.append(
        "Counts: "
        f"{counts['capabilities']} capabilities, "
        f"{counts['adapters']} adapters, "
        f"{counts['profiles']} profiles, "
        f"{counts['examples']} examples"
    )

    lines.extend(_format_table(
        "Capabilities",
        catalog["capabilities"],
        ["capability_id", "capability_kind", "path"],
    ))
    lines.extend(_format_table(
        "Adapters",
        catalog["adapters"],
        ["adapter_id", "adapter_kind", "status", "path"],
    ))
    lines.extend(_format_table(
        "Profiles",
        catalog["profiles"],
        ["profile_id", "profile_kind", "status", "path"],
    ))
    lines.extend(_format_table(
        "Examples",
        catalog["examples"],
        ["example_id", "profile_id", "runnable", "status", "path"],
    ))

    return "\n".join(lines)
