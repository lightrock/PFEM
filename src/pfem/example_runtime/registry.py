"""Example registry helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class ExampleRegistryEntry:
    example_id: str
    path: str
    profile_id: str
    runnable: bool
    status: str


@dataclass(frozen=True)
class ExampleRegistry:
    registry_id: str
    version: str
    examples: list[ExampleRegistryEntry]


def load_example_registry(path: str | Path) -> ExampleRegistry:
    """Load the PFEM example registry JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [
        ExampleRegistryEntry(
            example_id=str(item.get("example_id", "")),
            path=str(item.get("path", "")),
            profile_id=str(item.get("profile_id", "")),
            runnable=bool(item.get("runnable", False)),
            status=str(item.get("status", "")),
        )
        for item in raw.get("examples", [])
    ]
    return ExampleRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        examples=entries,
    )


def validate_example_registry(root: str | Path) -> list[str]:
    """Validate example registry entries against example manifests."""
    root_path = Path(root)
    registry_path = root_path / "examples" / "example-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        failures.append("missing example registry: examples/example-registry.json")
        return failures

    registry = load_example_registry(registry_path)
    seen: set[str] = set()

    if not registry.registry_id:
        failures.append("example registry missing registry_id")
    if not registry.version:
        failures.append("example registry missing version")

    for entry in registry.examples:
        if not entry.example_id:
            failures.append("example registry entry missing example_id")
            continue
        if entry.example_id in seen:
            failures.append(f"duplicate example registry example_id: {entry.example_id}")
        seen.add(entry.example_id)

        manifest_path = root_path / entry.path
        if not manifest_path.exists():
            failures.append(f"example registry path missing: {entry.path}")
            continue

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("example_id") != entry.example_id:
            failures.append(
                f"example registry id mismatch for {entry.path}: "
                f"registry={entry.example_id!r} manifest={manifest.get('example_id')!r}"
            )
        if manifest.get("profile_id") != entry.profile_id:
            failures.append(
                f"example registry profile mismatch for {entry.path}: "
                f"registry={entry.profile_id!r} manifest={manifest.get('profile_id')!r}"
            )

        if entry.runnable:
            for key in ["adapter_path", "input_path", "expected_observation_path"]:
                if key not in manifest:
                    failures.append(f"runnable example missing {key}: {entry.path}")

    return failures
