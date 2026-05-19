"""PFEM snapshot verification receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.snapshot_manifest import collect_snapshot_manifest_ids, compute_snapshot_digest, load_snapshot_manifests
from pfem.state_checkpoint import collect_state_checkpoint_ids
from pfem.state_transition import collect_state_transition_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "snapshot_manifest_verification",
    "snapshot_item_verification",
}

KNOWN_VERIFICATION_STATES = {
    "passed",
    "failed",
    "partially_passed",
    "skipped",
    "stale",
}

KNOWN_DIGEST_ALGORITHMS = {
    "sha256-canonical-snapshot-items",
}


@dataclass(frozen=True)
class SnapshotVerificationReceipt:
    snapshot_verification_receipt_id: str
    receipt_kind: str
    created_time: str
    node_id: str
    snapshot_manifest_id: str
    state_checkpoint_id: str
    state_transition_id: str | None
    verification_state: str
    checked_item_refs: list[str]
    checked_source_paths: list[str]
    basis_refs: list[str]
    digest_algorithm: str
    expected_snapshot_digest: str
    actual_snapshot_digest: str
    verified_by_ref: str
    summary: str


@dataclass(frozen=True)
class SnapshotVerificationReceiptReport:
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


def load_snapshot_verification_receipts(path: str | Path) -> list[SnapshotVerificationReceipt]:
    return [
        SnapshotVerificationReceipt(
            snapshot_verification_receipt_id=str(record.get("snapshot_verification_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            snapshot_manifest_id=str(record.get("snapshot_manifest_id", "")),
            state_checkpoint_id=str(record.get("state_checkpoint_id", "")),
            state_transition_id=_optional_str(record.get("state_transition_id")),
            verification_state=str(record.get("verification_state", "")),
            checked_item_refs=_as_list(record.get("checked_item_refs", [])),
            checked_source_paths=_as_list(record.get("checked_source_paths", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            digest_algorithm=str(record.get("digest_algorithm", "")),
            expected_snapshot_digest=str(record.get("expected_snapshot_digest", "")),
            actual_snapshot_digest=str(record.get("actual_snapshot_digest", "")),
            verified_by_ref=str(record.get("verified_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_snapshot_verification_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "snapshots" / "snapshot-verification-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.snapshot_verification_receipt_id
        for receipt in load_snapshot_verification_receipts(receipts_path)
        if receipt.snapshot_verification_receipt_id
    }


def _manifest_by_id(root: Path) -> dict[str, Any]:
    path = root / "snapshots" / "snapshot-manifests.json"
    if not path.exists():
        return {}
    return {manifest.snapshot_manifest_id: manifest for manifest in load_snapshot_manifests(path)}


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


def validate_snapshot_verification_receipts(root: str | Path) -> SnapshotVerificationReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "snapshots" / "snapshot-verification-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return SnapshotVerificationReceiptReport(
            source=str(receipts_path),
            failures=["missing snapshot verification receipts: snapshots/snapshot-verification-receipts.json"],
        )

    receipts = load_snapshot_verification_receipts(receipts_path)
    if not receipts:
        failures.append("snapshot verification receipts file has no receipts")

    node_ids = collect_node_ids(root_path)
    manifest_ids = collect_snapshot_manifest_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    transition_ids = collect_state_transition_ids(root_path)
    manifests = _manifest_by_id(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.snapshot_verification_receipt_id:
            failures.append("snapshot verification receipt missing snapshot_verification_receipt_id")
            continue
        if receipt.snapshot_verification_receipt_id in seen_ids:
            failures.append(f"duplicate snapshot_verification_receipt_id {receipt.snapshot_verification_receipt_id!r}")
        seen_ids.add(receipt.snapshot_verification_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} missing created_time")
        if node_ids and receipt.node_id not in node_ids:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references unknown node_id {receipt.node_id!r}")
        if manifest_ids and receipt.snapshot_manifest_id not in manifest_ids:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references unknown snapshot_manifest_id {receipt.snapshot_manifest_id!r}")
        if checkpoint_ids and receipt.state_checkpoint_id not in checkpoint_ids:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references unknown state_checkpoint_id {receipt.state_checkpoint_id!r}")
        if receipt.state_transition_id and transition_ids and receipt.state_transition_id not in transition_ids:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references unknown state_transition_id {receipt.state_transition_id!r}")
        if receipt.verification_state not in KNOWN_VERIFICATION_STATES:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} uses unknown verification_state {receipt.verification_state!r}")

        if not receipt.checked_item_refs:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} has no checked_item_refs")
        for ref in receipt.checked_item_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references unknown checked_item_ref {ref!r}")

        for path in receipt.checked_source_paths:
            if path.replace("\\", "/") not in known_paths:
                failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references missing checked_source_path {path!r}")

        if not receipt.basis_refs:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} has no basis_refs")
        for ref in receipt.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} references unknown basis_ref {ref!r}")

        if receipt.digest_algorithm not in KNOWN_DIGEST_ALGORITHMS:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} uses unknown digest_algorithm {receipt.digest_algorithm!r}")
        if receipt.expected_snapshot_digest != receipt.actual_snapshot_digest:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} expected/actual digest mismatch")

        manifest = manifests.get(receipt.snapshot_manifest_id)
        if manifest is not None:
            manifest_digest = compute_snapshot_digest(manifest.items)
            if receipt.expected_snapshot_digest != manifest.snapshot_digest:
                failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} expected digest does not match manifest digest")
            if receipt.actual_snapshot_digest != manifest_digest:
                failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} actual digest does not match recomputed manifest digest")

        if not receipt.verified_by_ref:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} missing verified_by_ref")
        if not receipt.summary:
            failures.append(f"snapshot verification receipt {receipt.snapshot_verification_receipt_id!r} missing summary")

    return SnapshotVerificationReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_snapshot_verification_receipt_report(report: SnapshotVerificationReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM snapshot verification receipt source: {report.source}")
    lines.append(f"Snapshot verification receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM snapshot verification receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM snapshot verification receipt validation passed.")

    return "\n".join(lines)
