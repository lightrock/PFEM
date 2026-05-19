"""PFEM disposition record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_DISPOSITION_KINDS = {
    "closed_workflow_artifact_disposition",
    "manual_artifact_disposition",
    "retention_policy_disposition",
}

KNOWN_WORKFLOW_KINDS = {
    "restore_workflow",
    "exchange_workflow",
    "delivery_workflow",
    "review_workflow",
    "general_workflow",
}

KNOWN_DISPOSITION_STATES = {
    "retained",
    "archived",
    "exported",
    "removed",
    "held",
    "pending",
    "superseded",
}

KNOWN_ACTIONS = {
    "retain",
    "archive",
    "export",
    "remove",
    "hold",
    "skip",
}


@dataclass(frozen=True)
class DispositionAction:
    action: str
    target_ref: str
    reason: str


@dataclass(frozen=True)
class DispositionRecord:
    disposition_record_id: str
    disposition_kind: str
    created_time: str
    node_id: str
    source_workflow_kind: str
    source_closeout_ref: str
    disposition_state: str
    retention_basis: str | None
    retention_policy_ref: str | None
    subject_refs: list[str]
    actions: list[DispositionAction]
    basis_refs: list[str]
    disposed_by_ref: str
    summary: str


@dataclass(frozen=True)
class DispositionRecordReport:
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


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _as_actions(value: object) -> list[DispositionAction]:
    if not isinstance(value, list):
        return []
    actions: list[DispositionAction] = []
    for item in value:
        if isinstance(item, dict):
            actions.append(
                DispositionAction(
                    action=str(item.get("action", "")),
                    target_ref=str(item.get("target_ref", "")),
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


def load_disposition_records(path: str | Path) -> list[DispositionRecord]:
    return [
        DispositionRecord(
            disposition_record_id=str(record.get("disposition_record_id", "")),
            disposition_kind=str(record.get("disposition_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            source_workflow_kind=str(record.get("source_workflow_kind", "")),
            source_closeout_ref=str(record.get("source_closeout_ref", "")),
            disposition_state=str(record.get("disposition_state", "")),
            retention_basis=_optional_str(record.get("retention_basis")),
            retention_policy_ref=_optional_str(record.get("retention_policy_ref")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            actions=_as_actions(record.get("actions", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            disposed_by_ref=str(record.get("disposed_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_disposition_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / "disposition" / "disposition-records.json"
    if not records_path.exists():
        return set()
    return {
        record.disposition_record_id
        for record in load_disposition_records(records_path)
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
        "snapshots", "recovery", "restore", "disposition", "transport", "topology",
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


def validate_disposition_records(root: str | Path) -> DispositionRecordReport:
    root_path = Path(root)
    records_path = root_path / "disposition" / "disposition-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return DispositionRecordReport(
            source=str(records_path),
            failures=["missing disposition records: disposition/disposition-records.json"],
        )

    records = load_disposition_records(records_path)
    if not records:
        failures.append("disposition records file has no records")

    node_ids = collect_node_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.disposition_record_id:
            failures.append("disposition record missing disposition_record_id")
            continue
        if record.disposition_record_id in seen_ids:
            failures.append(f"duplicate disposition_record_id {record.disposition_record_id!r}")
        seen_ids.add(record.disposition_record_id)

        if record.disposition_kind not in KNOWN_DISPOSITION_KINDS:
            failures.append(f"disposition record {record.disposition_record_id!r} uses unknown disposition_kind {record.disposition_kind!r}")
        if not record.created_time:
            failures.append(f"disposition record {record.disposition_record_id!r} missing created_time")
        if node_ids and record.node_id not in node_ids:
            failures.append(f"disposition record {record.disposition_record_id!r} references unknown node_id {record.node_id!r}")
        if record.source_workflow_kind not in KNOWN_WORKFLOW_KINDS:
            failures.append(f"disposition record {record.disposition_record_id!r} uses unknown source_workflow_kind {record.source_workflow_kind!r}")
        if not record.source_closeout_ref:
            failures.append(f"disposition record {record.disposition_record_id!r} missing source_closeout_ref")
        elif not _known_ref(record.source_closeout_ref, known_ids, known_paths):
            failures.append(f"disposition record {record.disposition_record_id!r} references unknown source_closeout_ref {record.source_closeout_ref!r}")

        if record.disposition_state not in KNOWN_DISPOSITION_STATES:
            failures.append(f"disposition record {record.disposition_record_id!r} uses unknown disposition_state {record.disposition_state!r}")

        if record.retention_policy_ref and not _known_ref(record.retention_policy_ref, known_ids, known_paths):
            failures.append(f"disposition record {record.disposition_record_id!r} references unknown retention_policy_ref {record.retention_policy_ref!r}")

        if not record.subject_refs:
            failures.append(f"disposition record {record.disposition_record_id!r} has no subject_refs")
        for ref in record.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"disposition record {record.disposition_record_id!r} references unknown subject_ref {ref!r}")

        if not record.actions:
            failures.append(f"disposition record {record.disposition_record_id!r} has no actions")
        for action in record.actions:
            if action.action not in KNOWN_ACTIONS:
                failures.append(f"disposition record {record.disposition_record_id!r} uses unknown action {action.action!r}")
            if not action.target_ref:
                failures.append(f"disposition record {record.disposition_record_id!r} has action without target_ref")
            elif not _known_ref(action.target_ref, known_ids, known_paths):
                failures.append(f"disposition record {record.disposition_record_id!r} references unknown action target_ref {action.target_ref!r}")
            if not action.reason:
                failures.append(f"disposition record {record.disposition_record_id!r} has action without reason")

        if not record.basis_refs:
            failures.append(f"disposition record {record.disposition_record_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"disposition record {record.disposition_record_id!r} references unknown basis_ref {ref!r}")

        if not record.disposed_by_ref:
            failures.append(f"disposition record {record.disposition_record_id!r} missing disposed_by_ref")
        if not record.summary:
            failures.append(f"disposition record {record.disposition_record_id!r} missing summary")

    return DispositionRecordReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_disposition_record_report(report: DispositionRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM disposition record source: {report.source}")
    lines.append(f"Disposition records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM disposition record validation failed.")
    else:
        lines.append("")
        lines.append("PFEM disposition record validation passed.")

    return "\n".join(lines)
