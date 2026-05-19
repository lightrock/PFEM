"""PFEM handling and redaction validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.policy import load_sharing_policy, known_scope_ids


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class HandlingLabel:
    label_id: str
    display_name: str
    description: str
    allowed_sharing_scopes: list[str]
    requires_redaction_before_share: bool
    allowed_redaction_states: list[str]


@dataclass(frozen=True)
class HandlingPolicy:
    policy_id: str
    version: str
    handling_labels: list[HandlingLabel]


@dataclass(frozen=True)
class HandlingReport:
    source: str
    checked_labels: int = 0
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_handling_policy(path: str | Path) -> HandlingPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    labels = [
        HandlingLabel(
            label_id=str(item.get("label_id", "")),
            display_name=str(item.get("display_name", "")),
            description=str(item.get("description", "")),
            allowed_sharing_scopes=_as_list(item.get("allowed_sharing_scopes", [])),
            requires_redaction_before_share=bool(item.get("requires_redaction_before_share", False)),
            allowed_redaction_states=_as_list(item.get("allowed_redaction_states", [])),
        )
        for item in raw.get("handling_labels", [])
    ]
    return HandlingPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        handling_labels=labels,
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


def _iter_shared_records(root: Path) -> list[tuple[Path, JsonObject]]:
    candidates = [
        *root.glob("tests/fixtures/**/rollup_summary.json"),
        *root.glob("tests/fixtures/**/federation_message.json"),
        *root.glob("examples/**/rollup_summary.json"),
        *root.glob("examples/**/federation_message.json"),
    ]
    records: list[tuple[Path, JsonObject]] = []
    for path in sorted(set(candidates)):
        for record in _load_records(path):
            records.append((path, record))
    return records


def validate_handling_policy(root: str | Path) -> HandlingReport:
    root_path = Path(root)
    policy_path = root_path / "handling" / "handling-policy.json"
    failures: list[str] = []

    if not policy_path.exists():
        return HandlingReport(
            source=str(policy_path),
            failures=["missing handling policy: handling/handling-policy.json"],
        )

    policy = load_handling_policy(policy_path)
    labels_by_id = {label.label_id: label for label in policy.handling_labels if label.label_id}
    seen_labels: set[str] = set()

    if not policy.policy_id:
        failures.append("handling policy missing policy_id")
    if not policy.version:
        failures.append("handling policy missing version")
    if not policy.handling_labels:
        failures.append("handling policy has no handling_labels")

    sharing_scope_ids: set[str] = set()
    sharing_policy_path = root_path / "policy" / "sharing-policy.json"
    if sharing_policy_path.exists():
        sharing_scope_ids = known_scope_ids(load_sharing_policy(sharing_policy_path))

    for label in policy.handling_labels:
        if not label.label_id:
            failures.append("handling label missing label_id")
            continue
        if label.label_id in seen_labels:
            failures.append(f"duplicate handling label {label.label_id!r}")
        seen_labels.add(label.label_id)

        if not label.allowed_sharing_scopes:
            failures.append(f"handling label {label.label_id!r} has no allowed_sharing_scopes")
        if not label.allowed_redaction_states:
            failures.append(f"handling label {label.label_id!r} has no allowed_redaction_states")

        for scope in label.allowed_sharing_scopes:
            if sharing_scope_ids and scope not in sharing_scope_ids:
                failures.append(f"handling label {label.label_id!r} references unknown sharing scope {scope!r}")

    shared_records = _iter_shared_records(root_path)
    for path, record in shared_records:
        record_id = record.get("rollup_id") or record.get("message_id") or "<missing id>"
        handling_label = record.get("handling_label")
        sharing_scope = record.get("sharing_scope")
        redaction_state = record.get("redaction_state")

        if not handling_label:
            failures.append(f"shared record {record_id!r} missing handling_label: {path.relative_to(root_path)}")
            continue
        if handling_label not in labels_by_id:
            failures.append(f"shared record {record_id!r} uses unknown handling_label {handling_label!r}: {path.relative_to(root_path)}")
            continue

        label = labels_by_id[handling_label]
        if sharing_scope not in label.allowed_sharing_scopes:
            failures.append(
                f"shared record {record_id!r} uses sharing_scope {sharing_scope!r} not allowed by handling_label {handling_label!r}: {path.relative_to(root_path)}"
            )

        if not redaction_state:
            failures.append(f"shared record {record_id!r} missing redaction_state: {path.relative_to(root_path)}")
            continue

        if redaction_state not in label.allowed_redaction_states:
            failures.append(
                f"shared record {record_id!r} uses redaction_state {redaction_state!r} not allowed by handling_label {handling_label!r}: {path.relative_to(root_path)}"
            )

        if label.requires_redaction_before_share and redaction_state in {"not-required", "not-shared"} and sharing_scope != "local":
            failures.append(
                f"shared record {record_id!r} requires redaction before sharing but redaction_state is {redaction_state!r}: {path.relative_to(root_path)}"
            )

    return HandlingReport(
        source=str(policy_path),
        checked_labels=len(policy.handling_labels),
        checked_records=len(shared_records),
        failures=failures,
    )


def format_handling_report(report: HandlingReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM handling source: {report.source}")
    lines.append(f"Handling labels checked: {report.checked_labels}")
    lines.append(f"Shared records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM handling validation failed.")
    else:
        lines.append("")
        lines.append("PFEM handling validation passed.")

    return "\n".join(lines)
