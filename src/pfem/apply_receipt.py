"""PFEM apply receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.conflict_record import collect_conflict_record_ids
from pfem.exchange import load_exchange_receipts
from pfem.import_record import collect_import_record_ids
from pfem.merge_decision import collect_merge_decision_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "local_record_apply",
    "local_record_skip",
    "local_record_failure",
    "rollback",
}

KNOWN_APPLY_STATES = {
    "planned",
    "applied",
    "skipped",
    "failed",
    "partially_applied",
    "rolled_back",
}


@dataclass(frozen=True)
class ApplyReceipt:
    apply_receipt_id: str
    receipt_kind: str
    created_time: str
    merge_decision_id: str
    conflict_record_id: str | None
    import_record_id: str
    exchange_receipt_id: str | None
    bundle_id: str
    apply_state: str
    applied_by_ref: str
    created_refs: list[str]
    updated_refs: list[str]
    skipped_refs: list[str]
    failed_refs: list[str]
    basis_refs: list[str]
    summary: str


@dataclass(frozen=True)
class ApplyReceiptReport:
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


def load_apply_receipts(path: str | Path) -> list[ApplyReceipt]:
    return [
        ApplyReceipt(
            apply_receipt_id=str(record.get("apply_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            merge_decision_id=str(record.get("merge_decision_id", "")),
            conflict_record_id=str(record["conflict_record_id"]) if "conflict_record_id" in record else None,
            import_record_id=str(record.get("import_record_id", "")),
            exchange_receipt_id=str(record["exchange_receipt_id"]) if "exchange_receipt_id" in record else None,
            bundle_id=str(record.get("bundle_id", "")),
            apply_state=str(record.get("apply_state", "")),
            applied_by_ref=str(record.get("applied_by_ref", "")),
            created_refs=_as_list(record.get("created_refs", [])),
            updated_refs=_as_list(record.get("updated_refs", [])),
            skipped_refs=_as_list(record.get("skipped_refs", [])),
            failed_refs=_as_list(record.get("failed_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_apply_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "apply" / "apply-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.apply_receipt_id
        for receipt in load_apply_receipts(receipts_path)
        if receipt.apply_receipt_id
    }


def _collect_exchange_receipt_ids(root: Path) -> set[str]:
    path = root / "exchange" / "exchange-receipts.json"
    if not path.exists():
        return set()
    return {
        receipt.exchange_receipt_id
        for receipt in load_exchange_receipts(path)
        if receipt.exchange_receipt_id
    }


def _collect_bundle_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in root.glob("bundles/**/*.bundle.json"):
        for record in _load_records(path):
            if record.get("bundle_id"):
                ids.add(str(record["bundle_id"]))
    return ids


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
        "inbox", "intake", "imports", "conflicts", "merge", "apply", "transport",
        "topology", "review", "audit", "exchange", "reconciliation", "quality",
        "action", "playbooks", "integrity", "schemas", "contracts", "docs",
        "bundles", "tests",
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


def validate_apply_receipts(root: str | Path) -> ApplyReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "apply" / "apply-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return ApplyReceiptReport(source=str(receipts_path), failures=["missing apply receipts: apply/apply-receipts.json"])

    receipts = load_apply_receipts(receipts_path)
    if not receipts:
        failures.append("apply receipts file has no receipts")

    merge_decision_ids = collect_merge_decision_ids(root_path)
    conflict_record_ids = collect_conflict_record_ids(root_path)
    import_record_ids = collect_import_record_ids(root_path)
    exchange_receipt_ids = _collect_exchange_receipt_ids(root_path)
    bundle_ids = _collect_bundle_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.apply_receipt_id:
            failures.append("apply receipt missing apply_receipt_id")
            continue
        if receipt.apply_receipt_id in seen_ids:
            failures.append(f"duplicate apply_receipt_id {receipt.apply_receipt_id!r}")
        seen_ids.add(receipt.apply_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} missing created_time")
        if merge_decision_ids and receipt.merge_decision_id not in merge_decision_ids:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} references unknown merge_decision_id {receipt.merge_decision_id!r}")
        if receipt.conflict_record_id and conflict_record_ids and receipt.conflict_record_id not in conflict_record_ids:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} references unknown conflict_record_id {receipt.conflict_record_id!r}")
        if import_record_ids and receipt.import_record_id not in import_record_ids:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} references unknown import_record_id {receipt.import_record_id!r}")
        if receipt.exchange_receipt_id and exchange_receipt_ids and receipt.exchange_receipt_id not in exchange_receipt_ids:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} references unknown exchange_receipt_id {receipt.exchange_receipt_id!r}")
        if bundle_ids and receipt.bundle_id not in bundle_ids:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} references unknown bundle_id {receipt.bundle_id!r}")
        if receipt.apply_state not in KNOWN_APPLY_STATES:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} uses unknown apply_state {receipt.apply_state!r}")
        if not receipt.applied_by_ref:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} missing applied_by_ref")

        all_outcome_refs = [*receipt.created_refs, *receipt.updated_refs, *receipt.skipped_refs, *receipt.failed_refs]
        if receipt.apply_state == "applied" and not all_outcome_refs:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} is applied but has no created/updated/skipped/failed refs")

        for label, refs in [
            ("created_ref", receipt.created_refs),
            ("updated_ref", receipt.updated_refs),
            ("skipped_ref", receipt.skipped_refs),
            ("failed_ref", receipt.failed_refs),
            ("basis_ref", receipt.basis_refs),
        ]:
            if label == "basis_ref" and not refs:
                failures.append(f"apply receipt {receipt.apply_receipt_id!r} has no basis_refs")
            for ref in refs:
                if not _known_ref(ref, known_ids, known_paths):
                    failures.append(f"apply receipt {receipt.apply_receipt_id!r} references unknown {label} {ref!r}")

        if not receipt.summary:
            failures.append(f"apply receipt {receipt.apply_receipt_id!r} missing summary")

    return ApplyReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_apply_receipt_report(report: ApplyReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM apply receipt source: {report.source}")
    lines.append(f"Apply receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM apply receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM apply receipt validation passed.")

    return "\n".join(lines)
