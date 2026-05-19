"""PFEM import record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.exchange import load_exchange_receipts
from pfem.inbox import collect_inbox_item_ids
from pfem.intake_decision import collect_intake_decision_ids
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_IMPORT_KINDS = {
    "exchange_bundle_import",
    "message_import",
    "report_import",
    "manual_import",
}

KNOWN_IMPORT_STATES = {
    "staged",
    "imported",
    "skipped",
    "failed",
    "superseded",
    "rejected",
}


@dataclass(frozen=True)
class ImportRecord:
    import_record_id: str
    import_kind: str
    created_time: str
    exchange_receipt_id: str
    bundle_id: str
    inbox_item_id: str | None
    intake_decision_id: str | None
    source_node_id: str
    destination_node_id: str
    subject_refs: list[str]
    artifact_refs: list[str]
    basis_refs: list[str]
    created_or_updated_refs: list[str]
    import_state: str
    imported_by_ref: str
    summary: str


@dataclass(frozen=True)
class ImportRecordReport:
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


def load_import_records(path: str | Path) -> list[ImportRecord]:
    return [
        ImportRecord(
            import_record_id=str(record.get("import_record_id", "")),
            import_kind=str(record.get("import_kind", "")),
            created_time=str(record.get("created_time", "")),
            exchange_receipt_id=str(record.get("exchange_receipt_id", "")),
            bundle_id=str(record.get("bundle_id", "")),
            inbox_item_id=str(record["inbox_item_id"]) if "inbox_item_id" in record else None,
            intake_decision_id=str(record["intake_decision_id"]) if "intake_decision_id" in record else None,
            source_node_id=str(record.get("source_node_id", "")),
            destination_node_id=str(record.get("destination_node_id", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            artifact_refs=_as_list(record.get("artifact_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            created_or_updated_refs=_as_list(record.get("created_or_updated_refs", [])),
            import_state=str(record.get("import_state", "")),
            imported_by_ref=str(record.get("imported_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_import_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / "imports" / "import-records.json"
    if not records_path.exists():
        return set()
    return {
        record.import_record_id
        for record in load_import_records(records_path)
        if record.import_record_id
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
        "inbox", "intake", "imports", "transport", "topology", "review", "audit",
        "exchange", "reconciliation", "quality", "action", "playbooks", "integrity",
        "schemas", "contracts", "docs", "bundles", "tests",
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


def validate_import_records(root: str | Path) -> ImportRecordReport:
    root_path = Path(root)
    records_path = root_path / "imports" / "import-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return ImportRecordReport(source=str(records_path), failures=["missing import records: imports/import-records.json"])

    records = load_import_records(records_path)
    if not records:
        failures.append("import records file has no records")

    exchange_receipt_ids = _collect_exchange_receipt_ids(root_path)
    bundle_ids = _collect_bundle_ids(root_path)
    inbox_item_ids = collect_inbox_item_ids(root_path)
    intake_decision_ids = collect_intake_decision_ids(root_path)
    node_ids = collect_node_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.import_record_id:
            failures.append("import record missing import_record_id")
            continue
        if record.import_record_id in seen_ids:
            failures.append(f"duplicate import_record_id {record.import_record_id!r}")
        seen_ids.add(record.import_record_id)

        if record.import_kind not in KNOWN_IMPORT_KINDS:
            failures.append(f"import record {record.import_record_id!r} uses unknown import_kind {record.import_kind!r}")
        if not record.created_time:
            failures.append(f"import record {record.import_record_id!r} missing created_time")
        if exchange_receipt_ids and record.exchange_receipt_id not in exchange_receipt_ids:
            failures.append(f"import record {record.import_record_id!r} references unknown exchange_receipt_id {record.exchange_receipt_id!r}")
        if bundle_ids and record.bundle_id not in bundle_ids:
            failures.append(f"import record {record.import_record_id!r} references unknown bundle_id {record.bundle_id!r}")
        if record.inbox_item_id and inbox_item_ids and record.inbox_item_id not in inbox_item_ids:
            failures.append(f"import record {record.import_record_id!r} references unknown inbox_item_id {record.inbox_item_id!r}")
        if record.intake_decision_id and intake_decision_ids and record.intake_decision_id not in intake_decision_ids:
            failures.append(f"import record {record.import_record_id!r} references unknown intake_decision_id {record.intake_decision_id!r}")
        if node_ids and record.source_node_id not in node_ids:
            failures.append(f"import record {record.import_record_id!r} references unknown source_node_id {record.source_node_id!r}")
        if node_ids and record.destination_node_id not in node_ids:
            failures.append(f"import record {record.import_record_id!r} references unknown destination_node_id {record.destination_node_id!r}")
        if record.import_state not in KNOWN_IMPORT_STATES:
            failures.append(f"import record {record.import_record_id!r} uses unknown import_state {record.import_state!r}")
        if not record.imported_by_ref:
            failures.append(f"import record {record.import_record_id!r} missing imported_by_ref")
        if not record.summary:
            failures.append(f"import record {record.import_record_id!r} missing summary")

        if not record.subject_refs:
            failures.append(f"import record {record.import_record_id!r} has no subject_refs")
        for ref in record.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"import record {record.import_record_id!r} references unknown subject_ref {ref!r}")

        if not record.artifact_refs:
            failures.append(f"import record {record.import_record_id!r} has no artifact_refs")
        for ref in record.artifact_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"import record {record.import_record_id!r} references unknown artifact_ref {ref!r}")

        if not record.basis_refs:
            failures.append(f"import record {record.import_record_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"import record {record.import_record_id!r} references unknown basis_ref {ref!r}")

        for ref in record.created_or_updated_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"import record {record.import_record_id!r} references unknown created_or_updated_ref {ref!r}")

    return ImportRecordReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_import_record_report(report: ImportRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM import record source: {report.source}")
    lines.append(f"Import records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM import record validation failed.")
    else:
        lines.append("")
        lines.append("PFEM import record validation passed.")

    return "\n".join(lines)
