"""PFEM restore verification receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.recovery_point import collect_recovery_point_ids
from pfem.restore_approval import collect_restore_approval_ids
from pfem.restore_plan import collect_restore_plan_ids
from pfem.restore_receipt import collect_restore_receipt_ids, load_restore_receipts
from pfem.snapshot_manifest import collect_snapshot_manifest_ids
from pfem.state_checkpoint import collect_state_checkpoint_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "post_restore_state_verification",
    "post_restore_item_verification",
}

KNOWN_VERIFICATION_STATES = {
    "passed",
    "failed",
    "partially_passed",
    "skipped",
    "stale",
}

KNOWN_DIGEST_ALGORITHMS = {
    "sha256-sorted-ref-list",
}


@dataclass(frozen=True)
class RestoreVerificationReceipt:
    restore_verification_receipt_id: str
    receipt_kind: str
    created_time: str
    node_id: str
    restore_receipt_id: str
    restore_approval_id: str
    restore_plan_id: str
    recovery_point_id: str
    state_checkpoint_id: str | None
    snapshot_manifest_id: str | None
    verification_state: str
    checked_refs: list[str]
    basis_refs: list[str]
    digest_algorithm: str
    expected_restored_ref_digest: str
    actual_restored_ref_digest: str
    verified_by_ref: str
    summary: str


@dataclass(frozen=True)
class RestoreVerificationReceiptReport:
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


def compute_ref_digest(refs: list[str]) -> str:
    payload = json.dumps(sorted(refs), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def load_restore_verification_receipts(path: str | Path) -> list[RestoreVerificationReceipt]:
    return [
        RestoreVerificationReceipt(
            restore_verification_receipt_id=str(record.get("restore_verification_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            restore_receipt_id=str(record.get("restore_receipt_id", "")),
            restore_approval_id=str(record.get("restore_approval_id", "")),
            restore_plan_id=str(record.get("restore_plan_id", "")),
            recovery_point_id=str(record.get("recovery_point_id", "")),
            state_checkpoint_id=_optional_str(record.get("state_checkpoint_id")),
            snapshot_manifest_id=_optional_str(record.get("snapshot_manifest_id")),
            verification_state=str(record.get("verification_state", "")),
            checked_refs=_as_list(record.get("checked_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            digest_algorithm=str(record.get("digest_algorithm", "")),
            expected_restored_ref_digest=str(record.get("expected_restored_ref_digest", "")),
            actual_restored_ref_digest=str(record.get("actual_restored_ref_digest", "")),
            verified_by_ref=str(record.get("verified_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_restore_verification_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "restore" / "restore-verification-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.restore_verification_receipt_id
        for receipt in load_restore_verification_receipts(receipts_path)
        if receipt.restore_verification_receipt_id
    }


def _restore_receipt_states(root: Path) -> dict[str, str]:
    path = root / "restore" / "restore-receipts.json"
    if not path.exists():
        return {}
    return {
        receipt.restore_receipt_id: receipt.restore_state
        for receipt in load_restore_receipts(path)
        if receipt.restore_receipt_id
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


def validate_restore_verification_receipts(root: str | Path) -> RestoreVerificationReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "restore" / "restore-verification-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return RestoreVerificationReceiptReport(
            source=str(receipts_path),
            failures=["missing restore verification receipts: restore/restore-verification-receipts.json"],
        )

    receipts = load_restore_verification_receipts(receipts_path)
    if not receipts:
        failures.append("restore verification receipts file has no receipts")

    node_ids = collect_node_ids(root_path)
    restore_receipt_ids = collect_restore_receipt_ids(root_path)
    restore_approval_ids = collect_restore_approval_ids(root_path)
    restore_plan_ids = collect_restore_plan_ids(root_path)
    recovery_point_ids = collect_recovery_point_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    manifest_ids = collect_snapshot_manifest_ids(root_path)
    restore_receipt_states = _restore_receipt_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.restore_verification_receipt_id:
            failures.append("restore verification receipt missing restore_verification_receipt_id")
            continue
        if receipt.restore_verification_receipt_id in seen_ids:
            failures.append(f"duplicate restore_verification_receipt_id {receipt.restore_verification_receipt_id!r}")
        seen_ids.add(receipt.restore_verification_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} missing created_time")
        if node_ids and receipt.node_id not in node_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown node_id {receipt.node_id!r}")
        if restore_receipt_ids and receipt.restore_receipt_id not in restore_receipt_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown restore_receipt_id {receipt.restore_receipt_id!r}")
        if restore_receipt_states.get(receipt.restore_receipt_id) not in {None, "completed"}:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references restore receipt that is not completed")
        if restore_approval_ids and receipt.restore_approval_id not in restore_approval_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown restore_approval_id {receipt.restore_approval_id!r}")
        if restore_plan_ids and receipt.restore_plan_id not in restore_plan_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown restore_plan_id {receipt.restore_plan_id!r}")
        if recovery_point_ids and receipt.recovery_point_id not in recovery_point_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown recovery_point_id {receipt.recovery_point_id!r}")
        if receipt.state_checkpoint_id and checkpoint_ids and receipt.state_checkpoint_id not in checkpoint_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown state_checkpoint_id {receipt.state_checkpoint_id!r}")
        if receipt.snapshot_manifest_id and manifest_ids and receipt.snapshot_manifest_id not in manifest_ids:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown snapshot_manifest_id {receipt.snapshot_manifest_id!r}")

        if receipt.verification_state not in KNOWN_VERIFICATION_STATES:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} uses unknown verification_state {receipt.verification_state!r}")
        if not receipt.checked_refs:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} has no checked_refs")
        for ref in receipt.checked_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown checked_ref {ref!r}")

        if not receipt.basis_refs:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} has no basis_refs")
        for ref in receipt.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} references unknown basis_ref {ref!r}")

        if receipt.digest_algorithm not in KNOWN_DIGEST_ALGORITHMS:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} uses unknown digest_algorithm {receipt.digest_algorithm!r}")
        else:
            actual = compute_ref_digest(receipt.checked_refs)
            if receipt.expected_restored_ref_digest != receipt.actual_restored_ref_digest:
                failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} expected/actual digest mismatch")
            if receipt.actual_restored_ref_digest != actual:
                failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} actual digest does not match checked_refs")

        if not receipt.verified_by_ref:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} missing verified_by_ref")
        if not receipt.summary:
            failures.append(f"restore verification receipt {receipt.restore_verification_receipt_id!r} missing summary")

    return RestoreVerificationReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_restore_verification_receipt_report(report: RestoreVerificationReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM restore verification receipt source: {report.source}")
    lines.append(f"Restore verification receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM restore verification receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM restore verification receipt validation passed.")

    return "\n".join(lines)
