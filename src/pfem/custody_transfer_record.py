"""PFEM custody transfer record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.custody_record import collect_custody_record_ids
from pfem.custody_verification_receipt import (
    collect_custody_verification_receipt_ids,
    load_custody_verification_receipts,
)
from pfem.disposition_receipt import collect_disposition_receipt_ids
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_TRANSFER_KINDS = {
    "custody_location_transfer",
    "custody_custodian_transfer",
    "custody_reassertion",
    "manual_custody_transfer",
}

KNOWN_WORKFLOW_KINDS = {
    "restore_workflow",
    "exchange_workflow",
    "delivery_workflow",
    "review_workflow",
    "general_workflow",
}

KNOWN_TRANSFER_STATES = {
    "completed",
    "partially_completed",
    "failed",
    "skipped",
    "pending",
    "cancelled",
}

KNOWN_LOCATION_KINDS = {
    "repository_path",
    "local_directory",
    "object_store",
    "external_archive",
    "export_package",
    "human_custodian",
}


@dataclass(frozen=True)
class CustodyTransferRecord:
    custody_transfer_record_id: str
    transfer_kind: str
    created_time: str
    node_id: str
    custody_record_id: str
    custody_verification_receipt_id: str
    disposition_receipt_id: str
    source_workflow_kind: str
    source_closeout_ref: str
    transfer_state: str
    from_custodian_ref: str
    to_custodian_ref: str
    from_location_ref: str
    to_location_ref: str
    from_location_kind: str
    to_location_kind: str
    transferred_refs: list[str]
    skipped_refs: list[str]
    failed_refs: list[str]
    basis_refs: list[str]
    transferred_by_ref: str
    summary: str


@dataclass(frozen=True)
class CustodyTransferRecordReport:
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


def load_custody_transfer_records(path: str | Path) -> list[CustodyTransferRecord]:
    return [
        CustodyTransferRecord(
            custody_transfer_record_id=str(record.get("custody_transfer_record_id", "")),
            transfer_kind=str(record.get("transfer_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            custody_record_id=str(record.get("custody_record_id", "")),
            custody_verification_receipt_id=str(record.get("custody_verification_receipt_id", "")),
            disposition_receipt_id=str(record.get("disposition_receipt_id", "")),
            source_workflow_kind=str(record.get("source_workflow_kind", "")),
            source_closeout_ref=str(record.get("source_closeout_ref", "")),
            transfer_state=str(record.get("transfer_state", "")),
            from_custodian_ref=str(record.get("from_custodian_ref", "")),
            to_custodian_ref=str(record.get("to_custodian_ref", "")),
            from_location_ref=str(record.get("from_location_ref", "")),
            to_location_ref=str(record.get("to_location_ref", "")),
            from_location_kind=str(record.get("from_location_kind", "")),
            to_location_kind=str(record.get("to_location_kind", "")),
            transferred_refs=_as_list(record.get("transferred_refs", [])),
            skipped_refs=_as_list(record.get("skipped_refs", [])),
            failed_refs=_as_list(record.get("failed_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            transferred_by_ref=str(record.get("transferred_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_custody_transfer_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / "custody" / "custody-transfer-records.json"
    if not records_path.exists():
        return set()
    return {
        record.custody_transfer_record_id
        for record in load_custody_transfer_records(records_path)
        if record.custody_transfer_record_id
    }


def _verification_states(root: Path) -> dict[str, str]:
    path = root / "custody" / "custody-verification-receipts.json"
    if not path.exists():
        return {}
    return {
        receipt.custody_verification_receipt_id: receipt.verification_state
        for receipt in load_custody_verification_receipts(path)
        if receipt.custody_verification_receipt_id
    }


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
        ("apply/apply-receipts.json", "apply_receipt_id"),
        ("state/state-checkpoints.json", "state_checkpoint_id"),
        ("state/state-transitions.json", "state_transition_id"),
        ("snapshots/snapshot-manifests.json", "snapshot_manifest_id"),
        ("snapshots/snapshot-verification-receipts.json", "snapshot_verification_receipt_id"),
        ("recovery/recovery-points.json", "recovery_point_id"),
        ("restore/restore-plans.json", "restore_plan_id"),
        ("restore/restore-approvals.json", "restore_approval_id"),
        ("restore/restore-receipts.json", "restore_receipt_id"),
        ("restore/restore-verification-receipts.json", "restore_verification_receipt_id"),
        ("restore/restore-closeout-records.json", "restore_closeout_record_id"),
        ("disposition/disposition-records.json", "disposition_record_id"),
        ("disposition/disposition-receipts.json", "disposition_receipt_id"),
        ("custody/custody-records.json", "custody_record_id"),
        ("custody/custody-verification-receipts.json", "custody_verification_receipt_id"),
        ("custody/custody-transfer-records.json", "custody_transfer_record_id"),
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
        "inbox", "intake", "imports", "conflicts", "merge", "apply", "state",
        "snapshots", "recovery", "restore", "disposition", "custody", "transport",
        "topology", "review", "audit", "exchange", "reconciliation", "quality",
        "action", "playbooks", "integrity", "schemas", "contracts", "docs", "bundles", "tests",
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


def validate_custody_transfer_records(root: str | Path) -> CustodyTransferRecordReport:
    root_path = Path(root)
    records_path = root_path / "custody" / "custody-transfer-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return CustodyTransferRecordReport(
            source=str(records_path),
            failures=["missing custody transfer records: custody/custody-transfer-records.json"],
        )

    records = load_custody_transfer_records(records_path)
    if not records:
        failures.append("custody transfer records file has no records")

    node_ids = collect_node_ids(root_path)
    custody_record_ids = collect_custody_record_ids(root_path)
    verification_ids = collect_custody_verification_receipt_ids(root_path)
    disposition_receipt_ids = collect_disposition_receipt_ids(root_path)
    verification_states = _verification_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.custody_transfer_record_id:
            failures.append("custody transfer record missing custody_transfer_record_id")
            continue
        if record.custody_transfer_record_id in seen_ids:
            failures.append(f"duplicate custody_transfer_record_id {record.custody_transfer_record_id!r}")
        seen_ids.add(record.custody_transfer_record_id)

        if record.transfer_kind not in KNOWN_TRANSFER_KINDS:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} uses unknown transfer_kind {record.transfer_kind!r}")
        if not record.created_time:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} missing created_time")
        if node_ids and record.node_id not in node_ids:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references unknown node_id {record.node_id!r}")
        if custody_record_ids and record.custody_record_id not in custody_record_ids:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references unknown custody_record_id {record.custody_record_id!r}")
        if verification_ids and record.custody_verification_receipt_id not in verification_ids:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references unknown custody_verification_receipt_id {record.custody_verification_receipt_id!r}")
        if verification_states.get(record.custody_verification_receipt_id) not in {None, "passed"}:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references custody verification that did not pass")
        if disposition_receipt_ids and record.disposition_receipt_id not in disposition_receipt_ids:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references unknown disposition_receipt_id {record.disposition_receipt_id!r}")

        if record.source_workflow_kind not in KNOWN_WORKFLOW_KINDS:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} uses unknown source_workflow_kind {record.source_workflow_kind!r}")
        if not record.source_closeout_ref:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} missing source_closeout_ref")
        elif not _known_ref(record.source_closeout_ref, known_ids, known_paths):
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references unknown source_closeout_ref {record.source_closeout_ref!r}")

        if record.transfer_state not in KNOWN_TRANSFER_STATES:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} uses unknown transfer_state {record.transfer_state!r}")
        for label, value in [
            ("from_custodian_ref", record.from_custodian_ref),
            ("to_custodian_ref", record.to_custodian_ref),
            ("from_location_ref", record.from_location_ref),
            ("to_location_ref", record.to_location_ref),
        ]:
            if not value:
                failures.append(f"custody transfer record {record.custody_transfer_record_id!r} missing {label}")

        if record.from_location_kind not in KNOWN_LOCATION_KINDS:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} uses unknown from_location_kind {record.from_location_kind!r}")
        if record.to_location_kind not in KNOWN_LOCATION_KINDS:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} uses unknown to_location_kind {record.to_location_kind!r}")

        outcome_refs = [*record.transferred_refs, *record.skipped_refs, *record.failed_refs]
        if record.transfer_state == "completed" and not record.transferred_refs:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} completed but has no transferred_refs")
        if not outcome_refs:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} has no outcome refs")

        for label, refs in [
            ("transferred_ref", record.transferred_refs),
            ("skipped_ref", record.skipped_refs),
            ("failed_ref", record.failed_refs),
            ("basis_ref", record.basis_refs),
        ]:
            if label == "basis_ref" and not refs:
                failures.append(f"custody transfer record {record.custody_transfer_record_id!r} has no basis_refs")
            for ref in refs:
                if not _known_ref(ref, known_ids, known_paths):
                    failures.append(f"custody transfer record {record.custody_transfer_record_id!r} references unknown {label} {ref!r}")

        if not record.transferred_by_ref:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} missing transferred_by_ref")
        if not record.summary:
            failures.append(f"custody transfer record {record.custody_transfer_record_id!r} missing summary")

    return CustodyTransferRecordReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_custody_transfer_record_report(report: CustodyTransferRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM custody transfer record source: {report.source}")
    lines.append(f"Custody transfer records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM custody transfer record validation failed.")
    else:
        lines.append("")
        lines.append("PFEM custody transfer record validation passed.")

    return "\n".join(lines)
