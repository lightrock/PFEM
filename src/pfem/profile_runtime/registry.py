"""Profile registry helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from pfem.profile_runtime.profile import load_node_profile


@dataclass(frozen=True)
class ProfileRegistryEntry:
    profile_id: str
    path: str
    profile_kind: str
    status: str


@dataclass(frozen=True)
class ProfileRegistry:
    registry_id: str
    version: str
    profiles: list[ProfileRegistryEntry]


def load_profile_registry(path: str | Path) -> ProfileRegistry:
    """Load the PFEM profile registry JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [
        ProfileRegistryEntry(
            profile_id=str(item.get("profile_id", "")),
            path=str(item.get("path", "")),
            profile_kind=str(item.get("profile_kind", "")),
            status=str(item.get("status", "")),
        )
        for item in raw.get("profiles", [])
    ]
    return ProfileRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        profiles=entries,
    )


def validate_profile_registry(root: str | Path) -> list[str]:
    """Validate profile registry entries against profile manifests."""
    root_path = Path(root)
    registry_path = root_path / "profiles" / "profile-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        failures.append("missing profile registry: profiles/profile-registry.json")
        return failures

    registry = load_profile_registry(registry_path)
    seen: set[str] = set()

    if not registry.registry_id:
        failures.append("profile registry missing registry_id")
    if not registry.version:
        failures.append("profile registry missing version")

    for entry in registry.profiles:
        if not entry.profile_id:
            failures.append("profile registry entry missing profile_id")
            continue
        if entry.profile_id in seen:
            failures.append(f"duplicate profile registry profile_id: {entry.profile_id}")
        seen.add(entry.profile_id)

        profile_path = root_path / entry.path
        if not profile_path.exists():
            failures.append(f"profile registry path missing: {entry.path}")
            continue

        profile = load_node_profile(profile_path)
        if profile.profile_id != entry.profile_id:
            failures.append(
                f"profile registry id mismatch for {entry.path}: "
                f"registry={entry.profile_id!r} profile={profile.profile_id!r}"
            )
        if profile.profile_kind != entry.profile_kind:
            failures.append(
                f"profile registry kind mismatch for {entry.path}: "
                f"registry={entry.profile_kind!r} profile={profile.profile_kind!r}"
            )

    return failures
