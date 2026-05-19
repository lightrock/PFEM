"""PFEM disposition receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.disposition_record import collect_disposition_record_ids, load_disposition_records
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "disposition_action_receipt",
    "manual_disposition_receipt",
    "retention_policy_disposition_receipt",
}

KNOWN_WORKFLOW_KINDS = {
    "restore_workflow",
    "exchange_workflow",
    "delivery_workflow",
    "review_workflow",
    "general_workflow",
}

KNOWN_RECEIPT_STATES = {
    "completed",
    "partially_completed",
    "failed",
    "skipped",
    "pending",
}

KNOWN_ACTIONS = {
    "retain",
    "archive",
    "export",
    "remove",
    "hold",
    "skip",
}

KNOWN_RESULTS = {
    "completed",
    "skipped",
    "failed",
    "pending",
}


@dataclass(frozen=True)
class DispositionExecutedAction:
    action: str
    target_ref: str
    result: str
    reason: str


@dataclass(frozen=True)
class DispositionReceipt:
    disposition_receipt_id: str
    receipt_kind: str
    created_time: str
    node_id: str
    disposition_record_id: str
    source_workflow_kind: str
    source_closeout_ref: str
    receipt_state: str
    executed_actions: list[DispositionExecutedAction]
    completed_refs: list[str]
    skipped_refs: list[str]
    failed_refs: list[str]
    basis_refs: list[str]
    executed_by_ref: str
    summary: str


@dataclass(frozen=True)
class DispositionReceiptReport:
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


def _as_actions(value: object) -> list[DispositionExecutedAction]:
    if not isinstance(value, list):
        return []
    actions: list[DispositionExecutedAction] = []
    for item in value:
        if isinstance(item, dict):
            actions.append(
                DispositionExecutedAction(
                    action=str(item.get("action", "")),
                    target_ref=str(item.get("target_ref", "")),
                    result=str(item.get("result", "")),
                    reason=str(item.get("reason", "")),
                )
            )
    return actions


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


def load_disposition_receipts(path: str | Path) -> list[DispositionReceipt]:
    return [
        DispositionReceipt(
            disposition_receipt_id=str(record.get("disposition_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            disposition_record_id=str(record.get("disposition_record_id", "")),
            source_workflow_kind=str(record.get("source_workflow_kind", "")),
            source_closeout_ref=str(record.get("source_closeout_ref", "")),
            receipt_state=str(record.get("receipt_state", "")),
            executed_actions=_as_actions(record.get("executed_actions", [])),
            completed_refs=_as_list(record.get("completed_refs", [])),
            skipped_refs=_as_list(record.get("skipped_refs", [])),
            failed_refs=_as_list(record.get("failed_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            executed_by_ref=str(record.get("executed_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_disposition_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "disposition" / "disposition-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.disposition_receipt_id
        for receipt in load_disposition_receipts(receipts_path)
        if receipt.disposition_receipt_id
    }


def _disposition_record_states(root: Path) -> dict[str, str]:
    path = root / "disposition" / "disposition-records.json"
    if not path.exists():
        return {}
    return {
        record.disposition_record_id: record.disposition_state
        for record in load_disposition_records(path)
        if record.disposition_record_id
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
        "snapshots", "recovery", "restore", "disposition", "custody", "transport", "topology",
        "review", "audit", "exchange", "reconciliation", "quality", "action",
        "playbooks", "integrity", "schemas", "contracts", "docs", "bundles", "tests",
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


def validate_disposition_receipts(root: str | Path) -> DispositionReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "disposition" / "disposition-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return DispositionReceiptReport(
            source=str(receipts_path),
            failures=["missing disposition receipts: disposition/disposition-receipts.json"],
        )

    receipts = load_disposition_receipts(receipts_path)
    if not receipts:
        failures.append("disposition receipts file has no receipts")

    node_ids = collect_node_ids(root_path)
    disposition_record_ids = collect_disposition_record_ids(root_path)
    disposition_states = _disposition_record_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.disposition_receipt_id:
            failures.append("disposition receipt missing disposition_receipt_id")
            continue
        if receipt.disposition_receipt_id in seen_ids:
            failures.append(f"duplicate disposition_receipt_id {receipt.disposition_receipt_id!r}")
        seen_ids.add(receipt.disposition_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} missing created_time")
        if node_ids and receipt.node_id not in node_ids:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} references unknown node_id {receipt.node_id!r}")
        if disposition_record_ids and receipt.disposition_record_id not in disposition_record_ids:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} references unknown disposition_record_id {receipt.disposition_record_id!r}")
        if disposition_states.get(receipt.disposition_record_id) not in {None, "retained", "archived", "exported", "removed", "held"}:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} references disposition record that is not actionable")
        if receipt.source_workflow_kind not in KNOWN_WORKFLOW_KINDS:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} uses unknown source_workflow_kind {receipt.source_workflow_kind!r}")
        if not receipt.source_closeout_ref:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} missing source_closeout_ref")
        elif not _known_ref(receipt.source_closeout_ref, known_ids, known_paths):
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} references unknown source_closeout_ref {receipt.source_closeout_ref!r}")
        if receipt.receipt_state not in KNOWN_RECEIPT_STATES:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} uses unknown receipt_state {receipt.receipt_state!r}")

        if not receipt.executed_actions:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} has no executed_actions")
        for action in receipt.executed_actions:
            if action.action not in KNOWN_ACTIONS:
                failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} uses unknown action {action.action!r}")
            if action.result not in KNOWN_RESULTS:
                failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} uses unknown action result {action.result!r}")
            if not action.target_ref:
                failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} has action without target_ref")
            elif not _known_ref(action.target_ref, known_ids, known_paths):
                failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} references unknown action target_ref {action.target_ref!r}")
            if not action.reason:
                failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} has action without reason")

        outcome_refs = [*receipt.completed_refs, *receipt.skipped_refs, *receipt.failed_refs]
        if receipt.receipt_state == "completed" and not receipt.completed_refs:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} is completed but has no completed_refs")
        if not outcome_refs:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} has no outcome refs")

        for label, refs in [
            ("completed_ref", receipt.completed_refs),
            ("skipped_ref", receipt.skipped_refs),
            ("failed_ref", receipt.failed_refs),
            ("basis_ref", receipt.basis_refs),
        ]:
            if label == "basis_ref" and not refs:
                failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} has no basis_refs")
            for ref in refs:
                if not _known_ref(ref, known_ids, known_paths):
                    failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} references unknown {label} {ref!r}")

        if not receipt.executed_by_ref:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} missing executed_by_ref")
        if not receipt.summary:
            failures.append(f"disposition receipt {receipt.disposition_receipt_id!r} missing summary")

    return DispositionReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_disposition_receipt_report(report: DispositionReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM disposition receipt source: {report.source}")
    lines.append(f"Disposition receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM disposition receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM disposition receipt validation passed.")

    return "\n".join(lines)
