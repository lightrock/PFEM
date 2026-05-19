"""PFEM conflict record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.exchange import load_exchange_receipts
from pfem.import_record import collect_import_record_ids


JsonObject = dict[str, Any]

KNOWN_CONFLICT_KINDS = {
    "no_conflict",
    "version_collision",
    "duplicate_record",
    "stale_incoming",
    "policy_conflict",
    "identity_conflict",
    "schema_conflict",
}

KNOWN_SEVERITIES = {
    "none",
    "low",
    "medium",
    "high",
    "critical",
}

KNOWN_CONFLICT_STATES = {
    "none_detected",
    "observed",
    "under_review",
    "resolved",
    "waived",
    "superseded",
}


@dataclass(frozen=True)
class ConflictRecord:
    conflict_record_id: str
    conflict_kind: str
    created_time: str
    import_record_id: str
    exchange_receipt_id: str
    bundle_id: str
    incoming_refs: list[str]
    local_target_refs: list[str]
    basis_refs: list[str]
    severity: str
    conflict_state: str
    detected_by_ref: str
    summary: str


@dataclass(frozen=True)
class ConflictRecordReport:
    source: str
    checked_records: int = 0
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


def load_conflict_records(path: str | Path) -> list[ConflictRecord]:
    return [
        ConflictRecord(
            conflict_record_id=str(record.get("conflict_record_id", "")),
            conflict_kind=str(record.get("conflict_kind", "")),
            created_time=str(record.get("created_time", "")),
            import_record_id=str(record.get("import_record_id", "")),
            exchange_receipt_id=str(record.get("exchange_receipt_id", "")),
            bundle_id=str(record.get("bundle_id", "")),
            incoming_refs=_as_list(record.get("incoming_refs", [])),
            local_target_refs=_as_list(record.get("local_target_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            severity=str(record.get("severity", "")),
            conflict_state=str(record.get("conflict_state", "")),
            detected_by_ref=str(record.get("detected_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_conflict_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / "conflicts" / "conflict-records.json"
    if not records_path.exists():
        return set()
    return {
        record.conflict_record_id
        for record in load_conflict_records(records_path)
        if record.conflict_record_id
    }


def _collect_exchange_receipt_ids(root: Path) -> set[str]:
    path = root / "exchange" / "exchange-receipts.json"
    if not path.exists():
        return set()
    return {
        receipt.exchange_receipt_id
        for receipt in load_exchange_receipts(path)
        if receipt.exchange_receipt_id
    }


def _collect_bundle_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in root.glob("bundles/**/*.bundle.json"):
        for record in _load_records(path):
            if record.get("bundle_id"):
                ids.add(str(record["bundle_id"]))
    return ids


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
        ("exchange/exchange-receipts.json", "exchange_receipt_id"),
        ("imports/import-records.json", "import_record_id"),
        ("conflicts/conflict-records.json", "conflict_record_id"),
        ("merge/merge-decisions.json", "merge_decision_id"),
        ("reconciliation/reconciliation-records.json", "reconciliation_id"),
        ("quality/quality-assessments.json", "quality_assessment_id"),
        ("action/action-records.json", "action_id"),
        ("playbooks/**/*.playbook.json", "playbook_id"),
        ("delivery/delivery-jobs.json", "delivery_job_id"),
        ("dispatch/dispatch-decisions.json", "dispatch_decision_id"),
        ("outbox/outbox-items.json", "outbox_item_id"),
        ("inbox/inbox-items.json", "inbox_item_id"),
        ("intake/intake-decisions.json", "intake_decision_id"),
        ("transport/transport-receipts.json", "transport_receipt_id"),
    ]
    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))

    for path, array_key, id_key in [
        (root / "dispatch" / "dispatch-policy.json", "rules", "dispatch_rule_id"),
        (root / "routing" / "routing-policy.json", "routes", "route_id"),
        (root / "delivery" / "delivery-channel-registry.json", "channels", "channel_id"),
        (root / "transport" / "transport-adapter-registry.json", "adapters", "transport_adapter_id"),
    ]:
        if not path.exists():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            for item in raw.get(array_key, []):
                if isinstance(item, dict) and item.get(id_key):
                    ids.add(str(item[id_key]))

    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "dispatch", "routing", "delivery", "outbox",
        "inbox", "intake", "imports", "conflicts", "merge", "transport",
        "topology", "review", "audit", "exchange", "reconciliation", "quality",
        "action", "playbooks", "integrity", "schemas", "contracts", "docs",
        "bundles", "tests",
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


def _known_ref(ref: str, known_ids: set[str], known_paths: set[str]) -> bool:
    return ref in known_ids or ref.replace("\\", "/") in known_paths


def validate_conflict_records(root: str | Path) -> ConflictRecordReport:
    root_path = Path(root)
    records_path = root_path / "conflicts" / "conflict-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return ConflictRecordReport(source=str(records_path), failures=["missing conflict records: conflicts/conflict-records.json"])

    records = load_conflict_records(records_path)
    if not records:
        failures.append("conflict records file has no records")

    import_record_ids = collect_import_record_ids(root_path)
    exchange_receipt_ids = _collect_exchange_receipt_ids(root_path)
    bundle_ids = _collect_bundle_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.conflict_record_id:
            failures.append("conflict record missing conflict_record_id")
            continue
        if record.conflict_record_id in seen_ids:
            failures.append(f"duplicate conflict_record_id {record.conflict_record_id!r}")
        seen_ids.add(record.conflict_record_id)

        if record.conflict_kind not in KNOWN_CONFLICT_KINDS:
            failures.append(f"conflict record {record.conflict_record_id!r} uses unknown conflict_kind {record.conflict_kind!r}")
        if not record.created_time:
            failures.append(f"conflict record {record.conflict_record_id!r} missing created_time")
        if import_record_ids and record.import_record_id not in import_record_ids:
            failures.append(f"conflict record {record.conflict_record_id!r} references unknown import_record_id {record.import_record_id!r}")
        if exchange_receipt_ids and record.exchange_receipt_id not in exchange_receipt_ids:
            failures.append(f"conflict record {record.conflict_record_id!r} references unknown exchange_receipt_id {record.exchange_receipt_id!r}")
        if bundle_ids and record.bundle_id not in bundle_ids:
            failures.append(f"conflict record {record.conflict_record_id!r} references unknown bundle_id {record.bundle_id!r}")

        if not record.incoming_refs:
            failures.append(f"conflict record {record.conflict_record_id!r} has no incoming_refs")
        for ref in record.incoming_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"conflict record {record.conflict_record_id!r} references unknown incoming_ref {ref!r}")

        for ref in record.local_target_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"conflict record {record.conflict_record_id!r} references unknown local_target_ref {ref!r}")

        if not record.basis_refs:
            failures.append(f"conflict record {record.conflict_record_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"conflict record {record.conflict_record_id!r} references unknown basis_ref {ref!r}")

        if record.severity not in KNOWN_SEVERITIES:
            failures.append(f"conflict record {record.conflict_record_id!r} uses unknown severity {record.severity!r}")
        if record.conflict_state not in KNOWN_CONFLICT_STATES:
            failures.append(f"conflict record {record.conflict_record_id!r} uses unknown conflict_state {record.conflict_state!r}")
        if record.conflict_kind == "no_conflict" and record.conflict_state != "none_detected":
            failures.append(f"conflict record {record.conflict_record_id!r} no_conflict should use conflict_state 'none_detected'")
        if record.conflict_state == "none_detected" and record.severity != "none":
            failures.append(f"conflict record {record.conflict_record_id!r} none_detected should use severity 'none'")
        if not record.detected_by_ref:
            failures.append(f"conflict record {record.conflict_record_id!r} missing detected_by_ref")
        if not record.summary:
            failures.append(f"conflict record {record.conflict_record_id!r} missing summary")

    return ConflictRecordReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_conflict_record_report(report: ConflictRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM conflict record source: {report.source}")
    lines.append(f"Conflict records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM conflict record validation failed.")
    else:
        lines.append("")
        lines.append("PFEM conflict record validation passed.")

    return "\n".join(lines)
