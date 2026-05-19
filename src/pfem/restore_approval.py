"""PFEM restore approval validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.recovery_point import collect_recovery_point_ids
from pfem.restore_plan import collect_restore_plan_ids, load_restore_plans


JsonObject = dict[str, Any]

KNOWN_APPROVAL_KINDS = {
    "operator_restore_approval",
    "automated_policy_restore_approval",
    "manual_override_restore_approval",
}

KNOWN_APPROVAL_STATES = {
    "approved",
    "rejected",
    "deferred",
    "revoked",
    "superseded",
}

KNOWN_APPROVED_SCOPES = {
    "local_repository_state",
    "node_state",
    "rollup_state",
}

KNOWN_APPROVAL_CONSTRAINTS = {
    "execute_only_if_current_state_matches_plan_preconditions",
    "write_restore_receipt_after_execution",
    "operator_present_required",
    "exclusive_write_lock_required",
}


@dataclass(frozen=True)
class RestoreApproval:
    restore_approval_id: str
    approval_kind: str
    created_time: str
    node_id: str
    restore_plan_id: str
    recovery_point_id: str
    approval_state: str
    approved_scope: str
    approved_refs: list[str]
    approver_ref: str
    approval_basis_refs: list[str]
    approval_constraints: list[str]
    summary: str


@dataclass(frozen=True)
class RestoreApprovalReport:
    source: str
    checked_approvals: int = 0
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


def load_restore_approvals(path: str | Path) -> list[RestoreApproval]:
    return [
        RestoreApproval(
            restore_approval_id=str(record.get("restore_approval_id", "")),
            approval_kind=str(record.get("approval_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            restore_plan_id=str(record.get("restore_plan_id", "")),
            recovery_point_id=str(record.get("recovery_point_id", "")),
            approval_state=str(record.get("approval_state", "")),
            approved_scope=str(record.get("approved_scope", "")),
            approved_refs=_as_list(record.get("approved_refs", [])),
            approver_ref=str(record.get("approver_ref", "")),
            approval_basis_refs=_as_list(record.get("approval_basis_refs", [])),
            approval_constraints=_as_list(record.get("approval_constraints", [])),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_restore_approval_ids(root: str | Path) -> set[str]:
    approvals_path = Path(root) / "restore" / "restore-approvals.json"
    if not approvals_path.exists():
        return set()
    return {
        approval.restore_approval_id
        for approval in load_restore_approvals(approvals_path)
        if approval.restore_approval_id
    }


def _restore_plan_states(root: Path) -> dict[str, str]:
    path = root / "restore" / "restore-plans.json"
    if not path.exists():
        return {}
    return {
        plan.restore_plan_id: plan.plan_state
        for plan in load_restore_plans(path)
        if plan.restore_plan_id
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


def validate_restore_approvals(root: str | Path) -> RestoreApprovalReport:
    root_path = Path(root)
    approvals_path = root_path / "restore" / "restore-approvals.json"
    failures: list[str] = []

    if not approvals_path.exists():
        return RestoreApprovalReport(source=str(approvals_path), failures=["missing restore approvals: restore/restore-approvals.json"])

    approvals = load_restore_approvals(approvals_path)
    if not approvals:
        failures.append("restore approvals file has no approvals")

    node_ids = collect_node_ids(root_path)
    restore_plan_ids = collect_restore_plan_ids(root_path)
    recovery_point_ids = collect_recovery_point_ids(root_path)
    plan_states = _restore_plan_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for approval in approvals:
        if not approval.restore_approval_id:
            failures.append("restore approval missing restore_approval_id")
            continue
        if approval.restore_approval_id in seen_ids:
            failures.append(f"duplicate restore_approval_id {approval.restore_approval_id!r}")
        seen_ids.add(approval.restore_approval_id)

        if approval.approval_kind not in KNOWN_APPROVAL_KINDS:
            failures.append(f"restore approval {approval.restore_approval_id!r} uses unknown approval_kind {approval.approval_kind!r}")
        if not approval.created_time:
            failures.append(f"restore approval {approval.restore_approval_id!r} missing created_time")
        if node_ids and approval.node_id not in node_ids:
            failures.append(f"restore approval {approval.restore_approval_id!r} references unknown node_id {approval.node_id!r}")
        if restore_plan_ids and approval.restore_plan_id not in restore_plan_ids:
            failures.append(f"restore approval {approval.restore_approval_id!r} references unknown restore_plan_id {approval.restore_plan_id!r}")
        if plan_states.get(approval.restore_plan_id) not in {None, "ready", "approved"}:
            failures.append(f"restore approval {approval.restore_approval_id!r} references restore plan that is not ready/approved")
        if recovery_point_ids and approval.recovery_point_id not in recovery_point_ids:
            failures.append(f"restore approval {approval.restore_approval_id!r} references unknown recovery_point_id {approval.recovery_point_id!r}")

        if approval.approval_state not in KNOWN_APPROVAL_STATES:
            failures.append(f"restore approval {approval.restore_approval_id!r} uses unknown approval_state {approval.approval_state!r}")
        if approval.approved_scope not in KNOWN_APPROVED_SCOPES:
            failures.append(f"restore approval {approval.restore_approval_id!r} uses unknown approved_scope {approval.approved_scope!r}")

        if not approval.approved_refs:
            failures.append(f"restore approval {approval.restore_approval_id!r} has no approved_refs")
        for ref in approval.approved_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore approval {approval.restore_approval_id!r} references unknown approved_ref {ref!r}")

        if not approval.approver_ref:
            failures.append(f"restore approval {approval.restore_approval_id!r} missing approver_ref")

        if not approval.approval_basis_refs:
            failures.append(f"restore approval {approval.restore_approval_id!r} has no approval_basis_refs")
        for ref in approval.approval_basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore approval {approval.restore_approval_id!r} references unknown approval_basis_ref {ref!r}")

        for constraint in approval.approval_constraints:
            if constraint not in KNOWN_APPROVAL_CONSTRAINTS:
                failures.append(f"restore approval {approval.restore_approval_id!r} uses unknown approval_constraint {constraint!r}")

        if not approval.summary:
            failures.append(f"restore approval {approval.restore_approval_id!r} missing summary")

    return RestoreApprovalReport(source=str(approvals_path), checked_approvals=len(approvals), failures=failures)


def format_restore_approval_report(report: RestoreApprovalReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM restore approval source: {report.source}")
    lines.append(f"Restore approvals checked: {report.checked_approvals}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM restore approval validation failed.")
    else:
        lines.append("")
        lines.append("PFEM restore approval validation passed.")

    return "\n".join(lines)
