"""PFEM restore receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.recovery_point import collect_recovery_point_ids
from pfem.restore_approval import collect_restore_approval_ids, load_restore_approvals
from pfem.restore_plan import collect_restore_plan_ids
from pfem.snapshot_manifest import collect_snapshot_manifest_ids
from pfem.snapshot_verification_receipt import collect_snapshot_verification_receipt_ids
from pfem.state_checkpoint import collect_state_checkpoint_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "local_repository_restore_execution",
    "node_state_restore_execution",
    "rollup_state_restore_execution",
}

KNOWN_RESTORE_STATES = {
    "completed",
    "partially_completed",
    "failed",
    "skipped",
    "rolled_back",
}

KNOWN_RESTORE_SCOPES = {
    "local_repository_state",
    "node_state",
    "rollup_state",
}


@dataclass(frozen=True)
class RestoreReceipt:
    restore_receipt_id: str
    receipt_kind: str
    created_time: str
    node_id: str
    restore_plan_id: str
    restore_approval_id: str
    recovery_point_id: str
    state_checkpoint_id: str | None
    snapshot_manifest_id: str | None
    snapshot_verification_receipt_id: str | None
    restore_state: str
    restore_scope: str
    restored_refs: list[str]
    skipped_refs: list[str]
    failed_refs: list[str]
    basis_refs: list[str]
    restored_by_ref: str
    summary: str


@dataclass(frozen=True)
class RestoreReceiptReport:
    source: str
    checked_receipts: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


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


def load_restore_receipts(path: str | Path) -> list[RestoreReceipt]:
    return [
        RestoreReceipt(
            restore_receipt_id=str(record.get("restore_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            restore_plan_id=str(record.get("restore_plan_id", "")),
            restore_approval_id=str(record.get("restore_approval_id", "")),
            recovery_point_id=str(record.get("recovery_point_id", "")),
            state_checkpoint_id=_optional_str(record.get("state_checkpoint_id")),
            snapshot_manifest_id=_optional_str(record.get("snapshot_manifest_id")),
            snapshot_verification_receipt_id=_optional_str(record.get("snapshot_verification_receipt_id")),
            restore_state=str(record.get("restore_state", "")),
            restore_scope=str(record.get("restore_scope", "")),
            restored_refs=_as_list(record.get("restored_refs", [])),
            skipped_refs=_as_list(record.get("skipped_refs", [])),
            failed_refs=_as_list(record.get("failed_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            restored_by_ref=str(record.get("restored_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_restore_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "restore" / "restore-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.restore_receipt_id
        for receipt in load_restore_receipts(receipts_path)
        if receipt.restore_receipt_id
    }


def _restore_approval_states(root: Path) -> dict[str, str]:
    path = root / "restore" / "restore-approvals.json"
    if not path.exists():
        return {}
    return {
        approval.restore_approval_id: approval.approval_state
        for approval in load_restore_approvals(path)
        if approval.restore_approval_id
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


def validate_restore_receipts(root: str | Path) -> RestoreReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "restore" / "restore-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return RestoreReceiptReport(source=str(receipts_path), failures=["missing restore receipts: restore/restore-receipts.json"])

    receipts = load_restore_receipts(receipts_path)
    if not receipts:
        failures.append("restore receipts file has no receipts")

    node_ids = collect_node_ids(root_path)
    restore_plan_ids = collect_restore_plan_ids(root_path)
    restore_approval_ids = collect_restore_approval_ids(root_path)
    recovery_point_ids = collect_recovery_point_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    manifest_ids = collect_snapshot_manifest_ids(root_path)
    verification_ids = collect_snapshot_verification_receipt_ids(root_path)
    approval_states = _restore_approval_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.restore_receipt_id:
            failures.append("restore receipt missing restore_receipt_id")
            continue
        if receipt.restore_receipt_id in seen_ids:
            failures.append(f"duplicate restore_receipt_id {receipt.restore_receipt_id!r}")
        seen_ids.add(receipt.restore_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} missing created_time")
        if node_ids and receipt.node_id not in node_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown node_id {receipt.node_id!r}")
        if restore_plan_ids and receipt.restore_plan_id not in restore_plan_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown restore_plan_id {receipt.restore_plan_id!r}")
        if restore_approval_ids and receipt.restore_approval_id not in restore_approval_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown restore_approval_id {receipt.restore_approval_id!r}")
        if approval_states.get(receipt.restore_approval_id) not in {None, "approved"}:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references restore approval that is not approved")
        if recovery_point_ids and receipt.recovery_point_id not in recovery_point_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown recovery_point_id {receipt.recovery_point_id!r}")
        if receipt.state_checkpoint_id and checkpoint_ids and receipt.state_checkpoint_id not in checkpoint_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown state_checkpoint_id {receipt.state_checkpoint_id!r}")
        if receipt.snapshot_manifest_id and manifest_ids and receipt.snapshot_manifest_id not in manifest_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown snapshot_manifest_id {receipt.snapshot_manifest_id!r}")
        if receipt.snapshot_verification_receipt_id and verification_ids and receipt.snapshot_verification_receipt_id not in verification_ids:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown snapshot_verification_receipt_id {receipt.snapshot_verification_receipt_id!r}")

        if receipt.restore_state not in KNOWN_RESTORE_STATES:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} uses unknown restore_state {receipt.restore_state!r}")
        if receipt.restore_scope not in KNOWN_RESTORE_SCOPES:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} uses unknown restore_scope {receipt.restore_scope!r}")

        outcome_refs = [*receipt.restored_refs, *receipt.skipped_refs, *receipt.failed_refs]
        if receipt.restore_state == "completed" and not receipt.restored_refs:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} is completed but has no restored_refs")
        if not outcome_refs:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} has no outcome refs")

        for label, refs in [
            ("restored_ref", receipt.restored_refs),
            ("skipped_ref", receipt.skipped_refs),
            ("failed_ref", receipt.failed_refs),
            ("basis_ref", receipt.basis_refs),
        ]:
            if label == "basis_ref" and not refs:
                failures.append(f"restore receipt {receipt.restore_receipt_id!r} has no basis_refs")
            for ref in refs:
                if not _known_ref(ref, known_ids, known_paths):
                    failures.append(f"restore receipt {receipt.restore_receipt_id!r} references unknown {label} {ref!r}")

        if not receipt.restored_by_ref:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} missing restored_by_ref")
        if not receipt.summary:
            failures.append(f"restore receipt {receipt.restore_receipt_id!r} missing summary")

    return RestoreReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_restore_receipt_report(report: RestoreReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM restore receipt source: {report.source}")
    lines.append(f"Restore receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM restore receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM restore receipt validation passed.")

    return "\n".join(lines)
