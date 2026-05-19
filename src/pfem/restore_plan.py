"""PFEM restore plan validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.recovery_point import collect_recovery_point_ids, load_recovery_points
from pfem.snapshot_manifest import collect_snapshot_manifest_ids
from pfem.snapshot_verification_receipt import collect_snapshot_verification_receipt_ids
from pfem.state_checkpoint import collect_state_checkpoint_ids


JsonObject = dict[str, Any]

KNOWN_PLAN_KINDS = {
    "local_repository_restore",
    "node_state_restore",
    "rollup_state_restore",
}

KNOWN_RESTORE_SCOPES = {
    "local_repository_state",
    "node_state",
    "rollup_state",
}

KNOWN_PLAN_STATES = {
    "draft",
    "ready",
    "approved",
    "superseded",
    "cancelled",
    "executed",
    "failed",
}

KNOWN_PRECONDITIONS = {
    "recovery_point_available",
    "snapshot_verification_passed",
    "operator_review_required_before_execution",
    "exclusive_write_lock_required",
    "backup_before_restore_required",
}


@dataclass(frozen=True)
class RestorePlan:
    restore_plan_id: str
    plan_kind: str
    created_time: str
    node_id: str
    recovery_point_id: str
    state_checkpoint_id: str | None
    snapshot_manifest_id: str | None
    snapshot_verification_receipt_id: str | None
    restore_scope: str
    plan_state: str
    planned_restore_refs: list[str]
    preconditions: list[str]
    basis_refs: list[str]
    planned_by_ref: str
    summary: str


@dataclass(frozen=True)
class RestorePlanReport:
    source: str
    checked_plans: int = 0
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


def load_restore_plans(path: str | Path) -> list[RestorePlan]:
    return [
        RestorePlan(
            restore_plan_id=str(record.get("restore_plan_id", "")),
            plan_kind=str(record.get("plan_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            recovery_point_id=str(record.get("recovery_point_id", "")),
            state_checkpoint_id=_optional_str(record.get("state_checkpoint_id")),
            snapshot_manifest_id=_optional_str(record.get("snapshot_manifest_id")),
            snapshot_verification_receipt_id=_optional_str(record.get("snapshot_verification_receipt_id")),
            restore_scope=str(record.get("restore_scope", "")),
            plan_state=str(record.get("plan_state", "")),
            planned_restore_refs=_as_list(record.get("planned_restore_refs", [])),
            preconditions=_as_list(record.get("preconditions", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            planned_by_ref=str(record.get("planned_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_restore_plan_ids(root: str | Path) -> set[str]:
    plans_path = Path(root) / "restore" / "restore-plans.json"
    if not plans_path.exists():
        return set()
    return {
        plan.restore_plan_id
        for plan in load_restore_plans(plans_path)
        if plan.restore_plan_id
    }


def _recovery_point_states(root: Path) -> dict[str, str]:
    path = root / "recovery" / "recovery-points.json"
    if not path.exists():
        return {}
    return {
        point.recovery_point_id: point.recovery_state
        for point in load_recovery_points(path)
        if point.recovery_point_id
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


def validate_restore_plans(root: str | Path) -> RestorePlanReport:
    root_path = Path(root)
    plans_path = root_path / "restore" / "restore-plans.json"
    failures: list[str] = []

    if not plans_path.exists():
        return RestorePlanReport(source=str(plans_path), failures=["missing restore plans: restore/restore-plans.json"])

    plans = load_restore_plans(plans_path)
    if not plans:
        failures.append("restore plans file has no plans")

    node_ids = collect_node_ids(root_path)
    recovery_point_ids = collect_recovery_point_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    manifest_ids = collect_snapshot_manifest_ids(root_path)
    verification_ids = collect_snapshot_verification_receipt_ids(root_path)
    recovery_states = _recovery_point_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for plan in plans:
        if not plan.restore_plan_id:
            failures.append("restore plan missing restore_plan_id")
            continue
        if plan.restore_plan_id in seen_ids:
            failures.append(f"duplicate restore_plan_id {plan.restore_plan_id!r}")
        seen_ids.add(plan.restore_plan_id)

        if plan.plan_kind not in KNOWN_PLAN_KINDS:
            failures.append(f"restore plan {plan.restore_plan_id!r} uses unknown plan_kind {plan.plan_kind!r}")
        if not plan.created_time:
            failures.append(f"restore plan {plan.restore_plan_id!r} missing created_time")
        if node_ids and plan.node_id not in node_ids:
            failures.append(f"restore plan {plan.restore_plan_id!r} references unknown node_id {plan.node_id!r}")
        if recovery_point_ids and plan.recovery_point_id not in recovery_point_ids:
            failures.append(f"restore plan {plan.restore_plan_id!r} references unknown recovery_point_id {plan.recovery_point_id!r}")
        if recovery_states.get(plan.recovery_point_id) not in {None, "available"}:
            failures.append(f"restore plan {plan.restore_plan_id!r} references recovery point that is not available")
        if plan.state_checkpoint_id and checkpoint_ids and plan.state_checkpoint_id not in checkpoint_ids:
            failures.append(f"restore plan {plan.restore_plan_id!r} references unknown state_checkpoint_id {plan.state_checkpoint_id!r}")
        if plan.snapshot_manifest_id and manifest_ids and plan.snapshot_manifest_id not in manifest_ids:
            failures.append(f"restore plan {plan.restore_plan_id!r} references unknown snapshot_manifest_id {plan.snapshot_manifest_id!r}")
        if plan.snapshot_verification_receipt_id and verification_ids and plan.snapshot_verification_receipt_id not in verification_ids:
            failures.append(f"restore plan {plan.restore_plan_id!r} references unknown snapshot_verification_receipt_id {plan.snapshot_verification_receipt_id!r}")

        if plan.restore_scope not in KNOWN_RESTORE_SCOPES:
            failures.append(f"restore plan {plan.restore_plan_id!r} uses unknown restore_scope {plan.restore_scope!r}")
        if plan.plan_state not in KNOWN_PLAN_STATES:
            failures.append(f"restore plan {plan.restore_plan_id!r} uses unknown plan_state {plan.plan_state!r}")

        if not plan.planned_restore_refs:
            failures.append(f"restore plan {plan.restore_plan_id!r} has no planned_restore_refs")
        for ref in plan.planned_restore_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore plan {plan.restore_plan_id!r} references unknown planned_restore_ref {ref!r}")

        if not plan.preconditions:
            failures.append(f"restore plan {plan.restore_plan_id!r} has no preconditions")
        for precondition in plan.preconditions:
            if precondition not in KNOWN_PRECONDITIONS:
                failures.append(f"restore plan {plan.restore_plan_id!r} uses unknown precondition {precondition!r}")

        if not plan.basis_refs:
            failures.append(f"restore plan {plan.restore_plan_id!r} has no basis_refs")
        for ref in plan.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore plan {plan.restore_plan_id!r} references unknown basis_ref {ref!r}")

        if not plan.planned_by_ref:
            failures.append(f"restore plan {plan.restore_plan_id!r} missing planned_by_ref")
        if not plan.summary:
            failures.append(f"restore plan {plan.restore_plan_id!r} missing summary")

    return RestorePlanReport(source=str(plans_path), checked_plans=len(plans), failures=failures)


def format_restore_plan_report(report: RestorePlanReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM restore plan source: {report.source}")
    lines.append(f"Restore plans checked: {report.checked_plans}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM restore plan validation failed.")
    else:
        lines.append("")
        lines.append("PFEM restore plan validation passed.")

    return "\n".join(lines)
