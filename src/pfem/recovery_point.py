"""PFEM recovery point validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.snapshot_manifest import collect_snapshot_manifest_ids
from pfem.snapshot_verification_receipt import collect_snapshot_verification_receipt_ids, load_snapshot_verification_receipts
from pfem.state_checkpoint import collect_state_checkpoint_ids
from pfem.state_transition import collect_state_transition_ids


JsonObject = dict[str, Any]

KNOWN_RECOVERY_POINT_KINDS = {
    "verified_snapshot_restore_candidate",
    "manual_restore_candidate",
    "archival_restore_candidate",
}

KNOWN_RECOVERY_STATES = {
    "available",
    "superseded",
    "revoked",
    "archived",
    "failed",
}

KNOWN_RESTORE_SCOPES = {
    "local_repository_state",
    "node_state",
    "rollup_state",
}


@dataclass(frozen=True)
class RecoveryPoint:
    recovery_point_id: str
    recovery_point_kind: str
    created_time: str
    node_id: str
    state_checkpoint_id: str
    snapshot_manifest_id: str
    snapshot_verification_receipt_id: str
    state_transition_id: str | None
    recovery_state: str
    restore_scope: str
    restorable_refs: list[str]
    basis_refs: list[str]
    promoted_by_ref: str
    summary: str


@dataclass(frozen=True)
class RecoveryPointReport:
    source: str
    checked_points: int = 0
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


def load_recovery_points(path: str | Path) -> list[RecoveryPoint]:
    return [
        RecoveryPoint(
            recovery_point_id=str(record.get("recovery_point_id", "")),
            recovery_point_kind=str(record.get("recovery_point_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            state_checkpoint_id=str(record.get("state_checkpoint_id", "")),
            snapshot_manifest_id=str(record.get("snapshot_manifest_id", "")),
            snapshot_verification_receipt_id=str(record.get("snapshot_verification_receipt_id", "")),
            state_transition_id=_optional_str(record.get("state_transition_id")),
            recovery_state=str(record.get("recovery_state", "")),
            restore_scope=str(record.get("restore_scope", "")),
            restorable_refs=_as_list(record.get("restorable_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            promoted_by_ref=str(record.get("promoted_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_recovery_point_ids(root: str | Path) -> set[str]:
    points_path = Path(root) / "recovery" / "recovery-points.json"
    if not points_path.exists():
        return set()
    return {
        point.recovery_point_id
        for point in load_recovery_points(points_path)
        if point.recovery_point_id
    }


def _verification_receipt_states(root: Path) -> dict[str, str]:
    path = root / "snapshots" / "snapshot-verification-receipts.json"
    if not path.exists():
        return {}
    return {
        receipt.snapshot_verification_receipt_id: receipt.verification_state
        for receipt in load_snapshot_verification_receipts(path)
        if receipt.snapshot_verification_receipt_id
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
        "snapshots", "recovery", "transport", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "action", "playbooks", "integrity",
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


def validate_recovery_points(root: str | Path) -> RecoveryPointReport:
    root_path = Path(root)
    points_path = root_path / "recovery" / "recovery-points.json"
    failures: list[str] = []

    if not points_path.exists():
        return RecoveryPointReport(source=str(points_path), failures=["missing recovery points: recovery/recovery-points.json"])

    points = load_recovery_points(points_path)
    if not points:
        failures.append("recovery points file has no points")

    node_ids = collect_node_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    manifest_ids = collect_snapshot_manifest_ids(root_path)
    verification_ids = collect_snapshot_verification_receipt_ids(root_path)
    transition_ids = collect_state_transition_ids(root_path)
    verification_states = _verification_receipt_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for point in points:
        if not point.recovery_point_id:
            failures.append("recovery point missing recovery_point_id")
            continue
        if point.recovery_point_id in seen_ids:
            failures.append(f"duplicate recovery_point_id {point.recovery_point_id!r}")
        seen_ids.add(point.recovery_point_id)

        if point.recovery_point_kind not in KNOWN_RECOVERY_POINT_KINDS:
            failures.append(f"recovery point {point.recovery_point_id!r} uses unknown recovery_point_kind {point.recovery_point_kind!r}")
        if not point.created_time:
            failures.append(f"recovery point {point.recovery_point_id!r} missing created_time")
        if node_ids and point.node_id not in node_ids:
            failures.append(f"recovery point {point.recovery_point_id!r} references unknown node_id {point.node_id!r}")
        if checkpoint_ids and point.state_checkpoint_id not in checkpoint_ids:
            failures.append(f"recovery point {point.recovery_point_id!r} references unknown state_checkpoint_id {point.state_checkpoint_id!r}")
        if manifest_ids and point.snapshot_manifest_id not in manifest_ids:
            failures.append(f"recovery point {point.recovery_point_id!r} references unknown snapshot_manifest_id {point.snapshot_manifest_id!r}")
        if verification_ids and point.snapshot_verification_receipt_id not in verification_ids:
            failures.append(f"recovery point {point.recovery_point_id!r} references unknown snapshot_verification_receipt_id {point.snapshot_verification_receipt_id!r}")
        if point.state_transition_id and transition_ids and point.state_transition_id not in transition_ids:
            failures.append(f"recovery point {point.recovery_point_id!r} references unknown state_transition_id {point.state_transition_id!r}")

        if verification_states.get(point.snapshot_verification_receipt_id) not in {None, "passed"}:
            failures.append(f"recovery point {point.recovery_point_id!r} cannot promote a non-passed snapshot verification receipt")

        if point.recovery_state not in KNOWN_RECOVERY_STATES:
            failures.append(f"recovery point {point.recovery_point_id!r} uses unknown recovery_state {point.recovery_state!r}")
        if point.restore_scope not in KNOWN_RESTORE_SCOPES:
            failures.append(f"recovery point {point.recovery_point_id!r} uses unknown restore_scope {point.restore_scope!r}")

        if not point.restorable_refs:
            failures.append(f"recovery point {point.recovery_point_id!r} has no restorable_refs")
        for ref in point.restorable_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"recovery point {point.recovery_point_id!r} references unknown restorable_ref {ref!r}")

        if not point.basis_refs:
            failures.append(f"recovery point {point.recovery_point_id!r} has no basis_refs")
        for ref in point.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"recovery point {point.recovery_point_id!r} references unknown basis_ref {ref!r}")

        if not point.promoted_by_ref:
            failures.append(f"recovery point {point.recovery_point_id!r} missing promoted_by_ref")
        if not point.summary:
            failures.append(f"recovery point {point.recovery_point_id!r} missing summary")

    return RecoveryPointReport(source=str(points_path), checked_points=len(points), failures=failures)


def format_recovery_point_report(report: RecoveryPointReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM recovery point source: {report.source}")
    lines.append(f"Recovery points checked: {report.checked_points}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM recovery point validation failed.")
    else:
        lines.append("")
        lines.append("PFEM recovery point validation passed.")

    return "\n".join(lines)
