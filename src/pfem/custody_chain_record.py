"""PFEM custody chain record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.custody_closeout_record import collect_custody_closeout_record_ids, load_custody_closeout_records
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_CHAIN_KINDS = {
    "closed_custody_chain_segment",
    "open_custody_chain_segment",
    "exception_custody_chain_segment",
}

KNOWN_WORKFLOW_KINDS = {
    "restore_workflow",
    "exchange_workflow",
    "delivery_workflow",
    "review_workflow",
    "general_workflow",
}

KNOWN_CHAIN_STATES = {
    "open",
    "closed",
    "closed_with_exceptions",
    "broken",
    "superseded",
}

KNOWN_FINAL_OUTCOMES = {
    "custody_verified_after_transfer",
    "custody_verified_with_exceptions",
    "custody_transfer_failed",
    "custody_chain_broken",
    "custody_chain_superseded",
}

KNOWN_LOCATION_KINDS = {
    "repository_path",
    "local_directory",
    "object_store",
    "external_archive",
    "export_package",
    "human_custodian",
}

KNOWN_DIGEST_ALGORITHMS = {
    "sha256-sorted-chain-ref-list",
}


@dataclass(frozen=True)
class CustodyChainRecord:
    custody_chain_record_id: str
    chain_kind: str
    created_time: str
    node_id: str
    source_workflow_kind: str
    source_closeout_ref: str
    chain_state: str
    start_ref: str
    terminal_ref: str
    final_outcome: str
    final_custodian_ref: str
    final_location_ref: str
    final_location_kind: str
    chain_refs: list[str]
    held_refs: list[str]
    basis_refs: list[str]
    digest_algorithm: str
    chain_ref_digest: str
    summarized_by_ref: str
    summary: str


@dataclass(frozen=True)
class CustodyChainRecordReport:
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


def load_custody_chain_records(path: str | Path) -> list[CustodyChainRecord]:
    return [
        CustodyChainRecord(
            custody_chain_record_id=str(record.get("custody_chain_record_id", "")),
            chain_kind=str(record.get("chain_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            source_workflow_kind=str(record.get("source_workflow_kind", "")),
            source_closeout_ref=str(record.get("source_closeout_ref", "")),
            chain_state=str(record.get("chain_state", "")),
            start_ref=str(record.get("start_ref", "")),
            terminal_ref=str(record.get("terminal_ref", "")),
            final_outcome=str(record.get("final_outcome", "")),
            final_custodian_ref=str(record.get("final_custodian_ref", "")),
            final_location_ref=str(record.get("final_location_ref", "")),
            final_location_kind=str(record.get("final_location_kind", "")),
            chain_refs=_as_list(record.get("chain_refs", [])),
            held_refs=_as_list(record.get("held_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            digest_algorithm=str(record.get("digest_algorithm", "")),
            chain_ref_digest=str(record.get("chain_ref_digest", "")),
            summarized_by_ref=str(record.get("summarized_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_custody_chain_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / "custody" / "custody-chain-records.json"
    if not records_path.exists():
        return set()
    return {
        record.custody_chain_record_id
        for record in load_custody_chain_records(records_path)
        if record.custody_chain_record_id
    }


def _closeout_states(root: Path) -> dict[str, str]:
    path = root / "custody" / "custody-closeout-records.json"
    if not path.exists():
        return {}
    return {
        record.custody_closeout_record_id: record.closeout_state
        for record in load_custody_closeout_records(path)
        if record.custody_closeout_record_id
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


def validate_custody_chain_records(root: str | Path) -> CustodyChainRecordReport:
    root_path = Path(root)
    records_path = root_path / "custody" / "custody-chain-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return CustodyChainRecordReport(
            source=str(records_path),
            failures=["missing custody chain records: custody/custody-chain-records.json"],
        )

    records = load_custody_chain_records(records_path)
    if not records:
        failures.append("custody chain records file has no records")

    node_ids = collect_node_ids(root_path)
    closeout_ids = collect_custody_closeout_record_ids(root_path)
    closeout_states = _closeout_states(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.custody_chain_record_id:
            failures.append("custody chain record missing custody_chain_record_id")
            continue
        if record.custody_chain_record_id in seen_ids:
            failures.append(f"duplicate custody_chain_record_id {record.custody_chain_record_id!r}")
        seen_ids.add(record.custody_chain_record_id)

        if record.chain_kind not in KNOWN_CHAIN_KINDS:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} uses unknown chain_kind {record.chain_kind!r}")
        if not record.created_time:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing created_time")
        if node_ids and record.node_id not in node_ids:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} references unknown node_id {record.node_id!r}")
        if record.source_workflow_kind not in KNOWN_WORKFLOW_KINDS:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} uses unknown source_workflow_kind {record.source_workflow_kind!r}")
        if not record.source_closeout_ref:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing source_closeout_ref")
        elif not _known_ref(record.source_closeout_ref, known_ids, known_paths):
            failures.append(f"custody chain record {record.custody_chain_record_id!r} references unknown source_closeout_ref {record.source_closeout_ref!r}")

        if record.chain_state not in KNOWN_CHAIN_STATES:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} uses unknown chain_state {record.chain_state!r}")
        if record.final_outcome not in KNOWN_FINAL_OUTCOMES:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} uses unknown final_outcome {record.final_outcome!r}")
        if not record.final_custodian_ref:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing final_custodian_ref")
        if not record.final_location_ref:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing final_location_ref")
        if record.final_location_kind not in KNOWN_LOCATION_KINDS:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} uses unknown final_location_kind {record.final_location_kind!r}")

        if not record.start_ref:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing start_ref")
        elif not _known_ref(record.start_ref, known_ids, known_paths):
            failures.append(f"custody chain record {record.custody_chain_record_id!r} references unknown start_ref {record.start_ref!r}")

        if not record.terminal_ref:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing terminal_ref")
        elif closeout_ids and record.terminal_ref not in closeout_ids:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} terminal_ref is not a known custody closeout record")
        if closeout_states.get(record.terminal_ref) not in {None, "closed"}:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} terminal closeout is not closed")

        if not record.chain_refs:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} has no chain_refs")
        for ref in record.chain_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain record {record.custody_chain_record_id!r} references unknown chain_ref {ref!r}")
        if record.start_ref and record.start_ref not in record.chain_refs:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} start_ref is not in chain_refs")
        if record.terminal_ref and record.terminal_ref not in record.chain_refs:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} terminal_ref is not in chain_refs")

        if not record.held_refs:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} has no held_refs")
        for ref in record.held_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain record {record.custody_chain_record_id!r} references unknown held_ref {ref!r}")

        if not record.basis_refs:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody chain record {record.custody_chain_record_id!r} references unknown basis_ref {ref!r}")

        if record.digest_algorithm not in KNOWN_DIGEST_ALGORITHMS:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} uses unknown digest_algorithm {record.digest_algorithm!r}")
        elif record.chain_ref_digest != compute_chain_ref_digest(record.chain_refs):
            failures.append(f"custody chain record {record.custody_chain_record_id!r} chain_ref_digest does not match chain_refs")

        if not record.summarized_by_ref:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing summarized_by_ref")
        if not record.summary:
            failures.append(f"custody chain record {record.custody_chain_record_id!r} missing summary")

    return CustodyChainRecordReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_custody_chain_record_report(report: CustodyChainRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM custody chain record source: {report.source}")
    lines.append(f"Custody chain records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM custody chain record validation failed.")
    else:
        lines.append("")
        lines.append("PFEM custody chain record validation passed.")

    return "\n".join(lines)
