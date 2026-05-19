"""PFEM sharing policy validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.profile_runtime import load_node_profile


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class SharingScope:
    scope_id: str
    display_name: str
    description: str


@dataclass(frozen=True)
class ReviewGate:
    gate_id: str
    display_name: str
    description: str


@dataclass(frozen=True)
class SharingPolicy:
    policy_id: str
    version: str
    sharing_scopes: list[SharingScope]
    review_gates: list[ReviewGate]


@dataclass(frozen=True)
class PolicyReport:
    source: str
    checked_profiles: int = 0
    checked_sharing_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def load_sharing_policy(path: str | Path) -> SharingPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))

    scopes = [
        SharingScope(
            scope_id=str(item.get("scope_id", "")),
            display_name=str(item.get("display_name", "")),
            description=str(item.get("description", "")),
        )
        for item in raw.get("sharing_scopes", [])
    ]

    gates = [
        ReviewGate(
            gate_id=str(item.get("gate_id", "")),
            display_name=str(item.get("display_name", "")),
            description=str(item.get("description", "")),
        )
        for item in raw.get("review_gates", [])
    ]

    return SharingPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        sharing_scopes=scopes,
        review_gates=gates,
    )


def known_scope_ids(policy: SharingPolicy) -> set[str]:
    return {scope.scope_id for scope in policy.sharing_scopes if scope.scope_id}


def known_review_gate_ids(policy: SharingPolicy) -> set[str]:
    return {gate.gate_id for gate in policy.review_gates if gate.gate_id}


def validate_policy_manifest(policy: SharingPolicy) -> list[str]:
    failures: list[str] = []
    scope_ids: set[str] = set()
    gate_ids: set[str] = set()

    if not policy.policy_id:
        failures.append("sharing policy missing policy_id")
    if not policy.version:
        failures.append("sharing policy missing version")

    for scope in policy.sharing_scopes:
        if not scope.scope_id:
            failures.append("sharing scope missing scope_id")
            continue
        if scope.scope_id in scope_ids:
            failures.append(f"duplicate sharing scope {scope.scope_id!r}")
        scope_ids.add(scope.scope_id)

    for gate in policy.review_gates:
        if not gate.gate_id:
            failures.append("review gate missing gate_id")
            continue
        if gate.gate_id in gate_ids:
            failures.append(f"duplicate review gate {gate.gate_id!r}")
        gate_ids.add(gate.gate_id)

    return failures


def validate_profile_review_gates(root: Path, policy: SharingPolicy) -> tuple[int, list[str]]:
    failures: list[str] = []
    known_gates = known_review_gate_ids(policy)
    checked = 0

    profiles_dir = root / "profiles"
    if not profiles_dir.exists():
        return checked, failures

    for path in sorted(profiles_dir.rglob("*.profile.yaml")):
        checked += 1
        profile = load_node_profile(path)
        for gate in profile.review_gates:
            if gate not in known_gates:
                failures.append(
                    f"profile {profile.profile_id!r} references unknown review gate {gate!r}: {path.relative_to(root)}"
                )

    return checked, failures


def _load_records_if_exists(path: Path) -> list[JsonObject]:
    if not path.exists():
        return []

    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        records: list[JsonObject] = []
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError(f"expected JSON object records in {path}")
            records.append(item)
        return records

    raise ValueError(f"expected JSON object or array in {path}")


def _sharing_search_roots(root: Path) -> list[Path]:
    """Return places that may contain sharing records.

    Accept either the repository root or a direct fixture/example root. This keeps
    unit tests and future targeted validators from depending on one caller shape.
    """
    roots: list[Path] = []

    fixtures_root = root / "tests" / "fixtures"
    examples_root = root / "examples"

    if fixtures_root.exists():
        roots.append(fixtures_root)
    if examples_root.exists():
        roots.append(examples_root)

    if not roots:
        roots.append(root)

    return roots


def _iter_sharing_records(root: Path) -> list[tuple[Path, JsonObject]]:
    candidates: list[Path] = []

    for search_root in _sharing_search_roots(root):
        candidates.extend(search_root.glob("**/rollup_summary.json"))
        candidates.extend(search_root.glob("**/federation_message.json"))

    records: list[tuple[Path, JsonObject]] = []
    for path in sorted(set(candidates)):
        for record in _load_records_if_exists(path):
            records.append((path, record))
    return records


def validate_record_sharing_scopes(root: Path, policy: SharingPolicy) -> tuple[int, list[str]]:
    failures: list[str] = []
    known_scopes = known_scope_ids(policy)
    records = _iter_sharing_records(root)

    for path, record in records:
        record_id = (
            record.get("rollup_id")
            or record.get("message_id")
            or record.get("id")
            or "<missing id>"
        )
        scope = record.get("sharing_scope")
        if scope and scope not in known_scopes:
            try:
                display_path = path.relative_to(root)
            except ValueError:
                display_path = path
            failures.append(
                f"record {record_id!r} uses unknown sharing_scope {scope!r}: {display_path}"
            )

    return len(records), failures


def validate_policy_repository(root: str | Path) -> PolicyReport:
    root_path = Path(root)
    policy_path = root_path / "policy" / "sharing-policy.json"
    failures: list[str] = []

    if not policy_path.exists():
        return PolicyReport(
            source=str(policy_path),
            failures=["missing sharing policy: policy/sharing-policy.json"],
        )

    policy = load_sharing_policy(policy_path)
    failures.extend(validate_policy_manifest(policy))

    checked_profiles, profile_failures = validate_profile_review_gates(root_path, policy)
    failures.extend(profile_failures)

    checked_records, record_failures = validate_record_sharing_scopes(root_path, policy)
    failures.extend(record_failures)

    return PolicyReport(
        source=str(policy_path),
        checked_profiles=checked_profiles,
        checked_sharing_records=checked_records,
        failures=failures,
    )


def format_policy_report(report: PolicyReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM policy source: {report.source}")
    lines.append(f"Profiles checked: {report.checked_profiles}")
    lines.append(f"Sharing records checked: {report.checked_sharing_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM policy validation failed.")
    else:
        lines.append("")
        lines.append("PFEM policy validation passed.")

    return "\n".join(lines)
