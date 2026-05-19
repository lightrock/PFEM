"""PFEM retention and disposition validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class RetentionClass:
    retention_class: str
    display_name: str
    description: str
    default_duration: str
    allowed_disposition_states: list[str]


@dataclass(frozen=True)
class RecordTypeDefault:
    record_type: str
    retention_class: str


@dataclass(frozen=True)
class RetentionPolicy:
    policy_id: str
    version: str
    retention_classes: list[RetentionClass]
    record_type_defaults: list[RecordTypeDefault]


@dataclass(frozen=True)
class RetentionReport:
    source: str
    checked_classes: int = 0
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_retention_policy(path: str | Path) -> RetentionPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    classes = [
        RetentionClass(
            retention_class=str(item.get("retention_class", "")),
            display_name=str(item.get("display_name", "")),
            description=str(item.get("description", "")),
            default_duration=str(item.get("default_duration", "")),
            allowed_disposition_states=_as_list(item.get("allowed_disposition_states", [])),
        )
        for item in raw.get("retention_classes", [])
    ]
    defaults = [
        RecordTypeDefault(
            record_type=str(item.get("record_type", "")),
            retention_class=str(item.get("retention_class", "")),
        )
        for item in raw.get("record_type_defaults", [])
    ]
    return RetentionPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        retention_classes=classes,
        record_type_defaults=defaults,
    )


def _load_records(path: Path) -> list[JsonObject]:
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


def _iter_retained_records(root: Path) -> list[tuple[Path, JsonObject]]:
    candidates = [
        *root.glob("tests/fixtures/**/evidence_package.json"),
        *root.glob("tests/fixtures/**/rollup_summary.json"),
        *root.glob("tests/fixtures/**/federation_message.json"),
        *root.glob("examples/**/evidence_package.json"),
        *root.glob("examples/**/rollup_summary.json"),
        *root.glob("examples/**/federation_message.json"),
    ]
    records: list[tuple[Path, JsonObject]] = []
    for path in sorted(set(candidates)):
        for record in _load_records(path):
            records.append((path, record))
    return records


def validate_retention_policy(root: str | Path) -> RetentionReport:
    root_path = Path(root)
    policy_path = root_path / "retention" / "retention-policy.json"
    failures: list[str] = []

    if not policy_path.exists():
        return RetentionReport(
            source=str(policy_path),
            failures=["missing retention policy: retention/retention-policy.json"],
        )

    policy = load_retention_policy(policy_path)
    class_by_id = {item.retention_class: item for item in policy.retention_classes if item.retention_class}
    seen_classes: set[str] = set()

    if not policy.policy_id:
        failures.append("retention policy missing policy_id")
    if not policy.version:
        failures.append("retention policy missing version")
    if not policy.retention_classes:
        failures.append("retention policy has no retention_classes")

    for item in policy.retention_classes:
        if not item.retention_class:
            failures.append("retention class missing retention_class")
            continue
        if item.retention_class in seen_classes:
            failures.append(f"duplicate retention_class {item.retention_class!r}")
        seen_classes.add(item.retention_class)
        if not item.default_duration:
            failures.append(f"retention class {item.retention_class!r} missing default_duration")
        if not item.allowed_disposition_states:
            failures.append(f"retention class {item.retention_class!r} has no allowed_disposition_states")

    for item in policy.record_type_defaults:
        if item.retention_class not in class_by_id:
            failures.append(
                f"record type default {item.record_type!r} references unknown retention_class {item.retention_class!r}"
            )

    retained_records = _iter_retained_records(root_path)
    for path, record in retained_records:
        record_id = record.get("package_id") or record.get("rollup_id") or record.get("message_id") or "<missing id>"
        retention_class = record.get("retention_class")
        disposition_state = record.get("disposition_state")

        if not retention_class:
            failures.append(f"record {record_id!r} missing retention_class: {path.relative_to(root_path)}")
            continue
        if retention_class not in class_by_id:
            failures.append(
                f"record {record_id!r} uses unknown retention_class {retention_class!r}: {path.relative_to(root_path)}"
            )
            continue

        if not disposition_state:
            failures.append(f"record {record_id!r} missing disposition_state: {path.relative_to(root_path)}")
            continue

        allowed_states = class_by_id[retention_class].allowed_disposition_states
        if disposition_state not in allowed_states:
            failures.append(
                f"record {record_id!r} uses disposition_state {disposition_state!r} not allowed by retention_class {retention_class!r}: {path.relative_to(root_path)}"
            )

    return RetentionReport(
        source=str(policy_path),
        checked_classes=len(policy.retention_classes),
        checked_records=len(retained_records),
        failures=failures,
    )


def format_retention_report(report: RetentionReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM retention source: {report.source}")
    lines.append(f"Retention classes checked: {report.checked_classes}")
    lines.append(f"Retained records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM retention validation failed.")
    else:
        lines.append("")
        lines.append("PFEM retention validation passed.")

    return "\n".join(lines)
