"""PFEM exchange bundle validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.handling import load_handling_policy
from pfem.node_runtime import collect_node_ids
from pfem.policy import load_sharing_policy, known_scope_ids
from pfem.retention import load_retention_policy


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class ExchangeBundle:
    bundle_id: str
    bundle_kind: str
    created_time: str
    producer_node_id: str
    recipient_node_ids: list[str]
    sharing_scope: str
    handling_label: str
    redaction_state: str
    retention_class: str
    disposition_state: str
    included_record_refs: list[str]
    included_artifact_paths: list[str]
    purpose: str
    notes: str | None = None


@dataclass(frozen=True)
class BundleReport:
    source: str
    checked_bundles: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


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


def load_exchange_bundle(path: str | Path) -> ExchangeBundle:
    record = _load_records(Path(path))[0]
    return ExchangeBundle(
        bundle_id=str(record.get("bundle_id", "")),
        bundle_kind=str(record.get("bundle_kind", "")),
        created_time=str(record.get("created_time", "")),
        producer_node_id=str(record.get("producer_node_id", "")),
        recipient_node_ids=_as_list(record.get("recipient_node_ids", [])),
        sharing_scope=str(record.get("sharing_scope", "")),
        handling_label=str(record.get("handling_label", "")),
        redaction_state=str(record.get("redaction_state", "")),
        retention_class=str(record.get("retention_class", "")),
        disposition_state=str(record.get("disposition_state", "")),
        included_record_refs=_as_list(record.get("included_record_refs", [])),
        included_artifact_paths=_as_list(record.get("included_artifact_paths", [])),
        purpose=str(record.get("purpose", "")),
        notes=str(record["notes"]) if "notes" in record else None,
    )


def _collect_known_record_ids(root: Path) -> set[str]:
    patterns = [
        ("tests/fixtures/**/raw_evidence.json", "evidence_id"),
        ("tests/fixtures/**/normalized_observation.json", "observation_id"),
        ("tests/fixtures/**/finding.json", "finding_id"),
        ("tests/fixtures/**/alert.json", "alert_id"),
        ("tests/fixtures/**/evidence_package.json", "package_id"),
        ("tests/fixtures/**/rollup_summary.json", "rollup_id"),
        ("tests/fixtures/**/federation_message.json", "message_id"),
        ("review/review-records.json", "review_id"),
        ("audit/audit-journal.json", "audit_id"),
        ("bundles/**/*.bundle.json", "bundle_id"),
    ]
    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))
    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "topology", "review", "audit", "integrity",
        "schemas", "contracts", "docs", "tests", "bundles",
    ]
    paths: set[str] = set()
    for folder in folders:
        base = root / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                paths.add(str(path.relative_to(root)).replace("\\", "/"))
    return paths


def _iter_bundle_paths(root: Path) -> list[Path]:
    return sorted(root.glob("bundles/**/*.bundle.json"))


def validate_bundle_repository(root: str | Path) -> BundleReport:
    root_path = Path(root)
    failures: list[str] = []

    bundle_paths = _iter_bundle_paths(root_path)
    if not bundle_paths:
        return BundleReport(
            source=str(root_path / "bundles"),
            failures=["no exchange bundle files found under bundles/**/*.bundle.json"],
        )

    node_ids = collect_node_ids(root_path)
    known_record_ids = _collect_known_record_ids(root_path)
    known_artifact_paths = _collect_known_artifact_paths(root_path)

    sharing_scope_ids: set[str] = set()
    sharing_policy_path = root_path / "policy" / "sharing-policy.json"
    if sharing_policy_path.exists():
        sharing_scope_ids = known_scope_ids(load_sharing_policy(sharing_policy_path))

    handling_labels: dict[str, object] = {}
    handling_policy_path = root_path / "handling" / "handling-policy.json"
    if handling_policy_path.exists():
        handling_policy = load_handling_policy(handling_policy_path)
        handling_labels = {label.label_id: label for label in handling_policy.handling_labels if label.label_id}

    retention_classes: dict[str, object] = {}
    retention_policy_path = root_path / "retention" / "retention-policy.json"
    if retention_policy_path.exists():
        retention_policy = load_retention_policy(retention_policy_path)
        retention_classes = {
            item.retention_class: item
            for item in retention_policy.retention_classes
            if item.retention_class
        }

    seen_bundle_ids: set[str] = set()

    for path in bundle_paths:
        bundle = load_exchange_bundle(path)
        if not bundle.bundle_id:
            failures.append(f"bundle missing bundle_id: {path.relative_to(root_path)}")
            continue
        if bundle.bundle_id in seen_bundle_ids:
            failures.append(f"duplicate bundle_id {bundle.bundle_id!r}: {path.relative_to(root_path)}")
        seen_bundle_ids.add(bundle.bundle_id)

        if not bundle.bundle_kind:
            failures.append(f"bundle {bundle.bundle_id!r} missing bundle_kind")
        if not bundle.created_time:
            failures.append(f"bundle {bundle.bundle_id!r} missing created_time")
        if not bundle.purpose:
            failures.append(f"bundle {bundle.bundle_id!r} missing purpose")

        if node_ids and bundle.producer_node_id not in node_ids:
            failures.append(f"bundle {bundle.bundle_id!r} references unknown producer_node_id {bundle.producer_node_id!r}")

        if not bundle.recipient_node_ids:
            failures.append(f"bundle {bundle.bundle_id!r} has no recipient_node_ids")
        for recipient in bundle.recipient_node_ids:
            if node_ids and recipient not in node_ids:
                failures.append(f"bundle {bundle.bundle_id!r} references unknown recipient_node_id {recipient!r}")

        if sharing_scope_ids and bundle.sharing_scope not in sharing_scope_ids:
            failures.append(f"bundle {bundle.bundle_id!r} uses unknown sharing_scope {bundle.sharing_scope!r}")

        handling_label = handling_labels.get(bundle.handling_label)
        if handling_labels and not handling_label:
            failures.append(f"bundle {bundle.bundle_id!r} uses unknown handling_label {bundle.handling_label!r}")
        elif handling_label:
            allowed_scopes = getattr(handling_label, "allowed_sharing_scopes", [])
            allowed_redaction = getattr(handling_label, "allowed_redaction_states", [])
            if bundle.sharing_scope not in allowed_scopes:
                failures.append(
                    f"bundle {bundle.bundle_id!r} uses sharing_scope {bundle.sharing_scope!r} "
                    f"not allowed by handling_label {bundle.handling_label!r}"
                )
            if bundle.redaction_state not in allowed_redaction:
                failures.append(
                    f"bundle {bundle.bundle_id!r} uses redaction_state {bundle.redaction_state!r} "
                    f"not allowed by handling_label {bundle.handling_label!r}"
                )

        retention_class = retention_classes.get(bundle.retention_class)
        if retention_classes and not retention_class:
            failures.append(f"bundle {bundle.bundle_id!r} uses unknown retention_class {bundle.retention_class!r}")
        elif retention_class:
            allowed_states = getattr(retention_class, "allowed_disposition_states", [])
            if bundle.disposition_state not in allowed_states:
                failures.append(
                    f"bundle {bundle.bundle_id!r} uses disposition_state {bundle.disposition_state!r} "
                    f"not allowed by retention_class {bundle.retention_class!r}"
                )

        if not bundle.included_record_refs:
            failures.append(f"bundle {bundle.bundle_id!r} has no included_record_refs")
        for ref in bundle.included_record_refs:
            if ref not in known_record_ids:
                failures.append(f"bundle {bundle.bundle_id!r} references unknown included_record_ref {ref!r}")

        if not bundle.included_artifact_paths:
            failures.append(f"bundle {bundle.bundle_id!r} has no included_artifact_paths")
        for artifact_path in bundle.included_artifact_paths:
            normalized = artifact_path.replace("\\", "/")
            if normalized not in known_artifact_paths:
                failures.append(f"bundle {bundle.bundle_id!r} references missing included_artifact_path {artifact_path!r}")

    return BundleReport(
        source=str(root_path / "bundles"),
        checked_bundles=len(bundle_paths),
        failures=failures,
    )


def format_bundle_report(report: BundleReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM bundle source: {report.source}")
    lines.append(f"Exchange bundles checked: {report.checked_bundles}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM bundle validation failed.")
    else:
        lines.append("")
        lines.append("PFEM bundle validation passed.")

    return "\n".join(lines)
