"""PFEM restore closeout record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.recovery_point import collect_recovery_point_ids
from pfem.restore_approval import collect_restore_approval_ids
from pfem.restore_plan import collect_restore_plan_ids
from pfem.restore_receipt import collect_restore_receipt_ids
from pfem.restore_verification_receipt import (
    collect_restore_verification_receipt_ids,
    load_restore_verification_receipts,
)


JsonObject = dict[str, Any]

KNOWN_CLOSEOUT_KINDS = {
    "restore_workflow_closeout",
    "restore_exception_closeout",
    "restore_manual_closeout",
}

KNOWN_CLOSEOUT_STATES = {
    "closed",
    "closed_with_exceptions",
    "deferred",
    "escalated",
    "cancelled",
    "superseded",
}

KNOWN_OUTCOMES = {
    "restore_verified",
    "restore_verified_with_exceptions",
    "restore_failed",
    "restore_cancelled",
    "restore_escalated",
}


@dataclass(frozen=True)
class RestoreCloseoutRecord:
    restore_closeout_record_id: str
    closeout_kind: str
    created_time: str
    node_id: str
    restore_verification_receipt_id: str
    restore_receipt_id: str
    restore_approval_id: str
    restore_plan_id: str
    recovery_point_id: str
    closeout_state: str
    outcome: str
    closed_refs: list[str]
    basis_refs: list[str]
    closed_by_ref: str
    summary: str


@dataclass(frozen=True)
class RestoreCloseoutRecordReport:
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


def load_restore_closeout_records(path: str | Path) -> list[RestoreCloseoutRecord]:
    return [
        RestoreCloseoutRecord(
            restore_closeout_record_id=str(record.get("restore_closeout_record_id", "")),
            closeout_kind=str(record.get("closeout_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            restore_verification_receipt_id=str(record.get("restore_verification_receipt_id", "")),
            restore_receipt_id=str(record.get("restore_receipt_id", "")),
            restore_approval_id=str(record.get("restore_approval_id", "")),
            restore_plan_id=str(record.get("restore_plan_id", "")),
            recovery_point_id=str(record.get("recovery_point_id", "")),
            closeout_state=str(record.get("closeout_state", "")),
            outcome=str(record.get("outcome", "")),
            closed_refs=_as_list(record.get("closed_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            closed_by_ref=str(record.get("closed_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_restore_closeout_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / "restore" / "restore-closeout-records.json"
    if not records_path.exists():
        return set()
    return {
        record.restore_closeout_record_id
        for record in load_restore_closeout_records(records_path)
        if record.restore_closeout_record_id
    }


def _restore_verification_states(root: Path) -> dict[str, str]:
    path = root / "restore" / "restore-verification-receipts.json"
    if not path.exists():
        return {}
    return {
        receipt.restore_verification_receipt_id: receipt.verification_state
        for receipt in load_restore_verification_receipts(path)
        if receipt.restore_verification_receipt_id
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
        "snapshots", "recovery", "restore", "transport", "topology", "review",
        "audit", "exchange", "reconciliation", "quality", "action", "playbooks",
        "integrity", "schemas", "contracts", "docs", "bundles", "tests",
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


def validate_restore_closeout_records(root: str | Path) -> RestoreCloseoutRecordReport:
    root_path = Path(root)
    records_path = root_path / "restore" / "restore-closeout-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return RestoreCloseoutRecordReport(
            source=str(records_path),
            failures=["missing restore closeout records: restore/restore-closeout-records.json"],
        )

    records = load_restore_closeout_records(records_path)
    if not records:
        failures.append("restore closeout records file has no records")

    node_ids = collect_node_ids(root_path)
    verification_ids = collect_restore_verification_receipt_ids(root_path)
    receipt_ids = collect_restore_receipt_ids(root_path)
    approval_ids = collect_restore_approval_ids(root_path)
    plan_ids = collect_restore_plan_ids(root_path)
    recovery_ids = collect_recovery_point_ids(root_path)
    verification_states = _restore_verification_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.restore_closeout_record_id:
            failures.append("restore closeout record missing restore_closeout_record_id")
            continue
        if record.restore_closeout_record_id in seen_ids:
            failures.append(f"duplicate restore_closeout_record_id {record.restore_closeout_record_id!r}")
        seen_ids.add(record.restore_closeout_record_id)

        if record.closeout_kind not in KNOWN_CLOSEOUT_KINDS:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} uses unknown closeout_kind {record.closeout_kind!r}")
        if not record.created_time:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} missing created_time")
        if node_ids and record.node_id not in node_ids:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown node_id {record.node_id!r}")
        if verification_ids and record.restore_verification_receipt_id not in verification_ids:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown restore_verification_receipt_id {record.restore_verification_receipt_id!r}")
        if verification_states.get(record.restore_verification_receipt_id) not in {None, "passed"}:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references restore verification that did not pass")
        if receipt_ids and record.restore_receipt_id not in receipt_ids:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown restore_receipt_id {record.restore_receipt_id!r}")
        if approval_ids and record.restore_approval_id not in approval_ids:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown restore_approval_id {record.restore_approval_id!r}")
        if plan_ids and record.restore_plan_id not in plan_ids:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown restore_plan_id {record.restore_plan_id!r}")
        if recovery_ids and record.recovery_point_id not in recovery_ids:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown recovery_point_id {record.recovery_point_id!r}")

        if record.closeout_state not in KNOWN_CLOSEOUT_STATES:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} uses unknown closeout_state {record.closeout_state!r}")
        if record.outcome not in KNOWN_OUTCOMES:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} uses unknown outcome {record.outcome!r}")

        if record.closeout_state == "closed" and record.outcome != "restore_verified":
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} closed state should use outcome 'restore_verified'")

        if not record.closed_refs:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} has no closed_refs")
        for ref in record.closed_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown closed_ref {ref!r}")

        if not record.basis_refs:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore closeout record {record.restore_closeout_record_id!r} references unknown basis_ref {ref!r}")

        if not record.closed_by_ref:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} missing closed_by_ref")
        if not record.summary:
            failures.append(f"restore closeout record {record.restore_closeout_record_id!r} missing summary")

    return RestoreCloseoutRecordReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_restore_closeout_record_report(report: RestoreCloseoutRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM restore closeout record source: {report.source}")
    lines.append(f"Restore closeout records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM restore closeout record validation failed.")
    else:
        lines.append("")
        lines.append("PFEM restore closeout record validation passed.")

    return "\n".join(lines)
