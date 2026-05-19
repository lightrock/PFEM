"""PFEM custody chain verification receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.custody_chain_record import collect_custody_chain_record_ids, load_custody_chain_records
from pfem.custody_closeout_record import collect_custody_closeout_record_ids
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "custody_chain_summary_verification",
    "manual_custody_chain_verification",
}

KNOWN_WORKFLOW_KINDS = {
    "restore_workflow",
    "exchange_workflow",
    "delivery_workflow",
    "review_workflow",
    "general_workflow",
}

KNOWN_VERIFICATION_STATES = {
    "passed",
    "failed",
    "partially_passed",
    "skipped",
    "stale",
}

KNOWN_DIGEST_ALGORITHMS = {
    "sha256-sorted-chain-ref-list",
}


@dataclass(frozen=True)
class CustodyChainVerificationReceipt:
    custody_chain_verification_receipt_id: str
    receipt_kind: str
    created_time: str
    node_id: str
    custody_chain_record_id: str
    terminal_ref: str
    source_workflow_kind: str
    source_closeout_ref: str
    verification_state: str
    checked_chain_refs: list[str]
    checked_held_refs: list[str]
    missing_refs: list[str]
    basis_refs: list[str]
    digest_algorithm: str
    expected_chain_ref_digest: str
    actual_chain_ref_digest: str
    verified_by_ref: str
    summary: str


@dataclass(frozen=True)
class CustodyChainVerificationReceiptReport:
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


def compute_chain_ref_digest(refs: list[str]) -> str:
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


def load_custody_chain_verification_receipts(path: str | Path) -> list[CustodyChainVerificationReceipt]:
    return [
        CustodyChainVerificationReceipt(
            custody_chain_verification_receipt_id=str(record.get("custody_chain_verification_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            custody_chain_record_id=str(record.get("custody_chain_record_id", "")),
            terminal_ref=str(record.get("terminal_ref", "")),
            source_workflow_kind=str(record.get("source_workflow_kind", "")),
            source_closeout_ref=str(record.get("source_closeout_ref", "")),
            verification_state=str(record.get("verification_state", "")),
            checked_chain_refs=_as_list(record.get("checked_chain_refs", [])),
            checked_held_refs=_as_list(record.get("checked_held_refs", [])),
            missing_refs=_as_list(record.get("missing_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            digest_algorithm=str(record.get("digest_algorithm", "")),
            expected_chain_ref_digest=str(record.get("expected_chain_ref_digest", "")),
            actual_chain_ref_digest=str(record.get("actual_chain_ref_digest", "")),
            verified_by_ref=str(record.get("verified_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_custody_chain_verification_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "custody" / "custody-chain-verification-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.custody_chain_verification_receipt_id
        for receipt in load_custody_chain_verification_receipts(receipts_path)
        if receipt.custody_chain_verification_receipt_id
    }


def _chain_states(root: Path) -> dict[str, str]:
    path = root / "custody" / "custody-chain-records.json"
    if not path.exists():
        return {}
    return {
        record.custody_chain_record_id: record.chain_state
        for record in load_custody_chain_records(path)
        if record.custody_chain_record_id
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
        ("custody/custody-transfer-verification-receipts.json", "custody_transfer_verification_receipt_id"),
        ("custody/custody-closeout-records.json", "custody_closeout_record_id"),
        ("custody/custody-chain-records.json", "custody_chain_record_id"),
        ("custody/custody-chain-verification-receipts.json", "custody_chain_verification_receipt_id"),
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


def validate_custody_chain_verification_receipts(root: str | Path) -> CustodyChainVerificationReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "custody" / "custody-chain-verification-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return CustodyChainVerificationReceiptReport(
            source=str(receipts_path),
            failures=["missing custody chain verification receipts: custody/custody-chain-verification-receipts.json"],
        )

    receipts = load_custody_chain_verification_receipts(receipts_path)
    if not receipts:
        failures.append("custody chain verification receipts file has no receipts")

    node_ids = collect_node_ids(root_path)
    chain_ids = collect_custody_chain_record_ids(root_path)
    closeout_ids = collect_custody_closeout_record_ids(root_path)
    chain_states = _chain_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.custody_chain_verification_receipt_id:
            failures.append("custody chain verification receipt missing custody_chain_verification_receipt_id")
            continue
        if receipt.custody_chain_verification_receipt_id in seen_ids:
            failures.append(f"duplicate custody_chain_verification_receipt_id {receipt.custody_chain_verification_receipt_id!r}")
        seen_ids.add(receipt.custody_chain_verification_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} missing created_time")
        if node_ids and receipt.node_id not in node_ids:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown node_id {receipt.node_id!r}")
        if chain_ids and receipt.custody_chain_record_id not in chain_ids:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown custody_chain_record_id {receipt.custody_chain_record_id!r}")
        if chain_states.get(receipt.custody_chain_record_id) not in {None, "closed"}:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references custody chain that is not closed")
        if closeout_ids and receipt.terminal_ref not in closeout_ids:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} terminal_ref is not a known custody closeout record")

        if receipt.source_workflow_kind not in KNOWN_WORKFLOW_KINDS:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} uses unknown source_workflow_kind {receipt.source_workflow_kind!r}")
        if not receipt.source_closeout_ref:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} missing source_closeout_ref")
        elif not _known_ref(receipt.source_closeout_ref, known_ids, known_paths):
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown source_closeout_ref {receipt.source_closeout_ref!r}")

        if receipt.verification_state not in KNOWN_VERIFICATION_STATES:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} uses unknown verification_state {receipt.verification_state!r}")

        if not receipt.checked_chain_refs:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} has no checked_chain_refs")
        for ref in receipt.checked_chain_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown checked_chain_ref {ref!r}")
        if receipt.terminal_ref and receipt.terminal_ref not in receipt.checked_chain_refs:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} terminal_ref is not in checked_chain_refs")

        if not receipt.checked_held_refs:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} has no checked_held_refs")
        for ref in receipt.checked_held_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown checked_held_ref {ref!r}")

        for ref in receipt.missing_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown missing_ref {ref!r}")
        if receipt.verification_state == "passed" and receipt.missing_refs:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} passed but has missing_refs")

        if not receipt.basis_refs:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} has no basis_refs")
        for ref in receipt.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} references unknown basis_ref {ref!r}")

        if receipt.digest_algorithm not in KNOWN_DIGEST_ALGORITHMS:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} uses unknown digest_algorithm {receipt.digest_algorithm!r}")
        else:
            actual = compute_chain_ref_digest(receipt.checked_chain_refs)
            if receipt.expected_chain_ref_digest != receipt.actual_chain_ref_digest:
                failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} expected/actual digest mismatch")
            if receipt.actual_chain_ref_digest != actual:
                failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} actual digest does not match checked_chain_refs")

        if not receipt.verified_by_ref:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} missing verified_by_ref")
        if not receipt.summary:
            failures.append(f"custody chain verification receipt {receipt.custody_chain_verification_receipt_id!r} missing summary")

    return CustodyChainVerificationReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_custody_chain_verification_receipt_report(report: CustodyChainVerificationReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM custody chain verification receipt source: {report.source}")
    lines.append(f"Custody chain verification receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM custody chain verification receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM custody chain verification receipt validation passed.")

    return "\n".join(lines)
