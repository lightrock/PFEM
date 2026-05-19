"""PFEM exchange receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.inbox import collect_inbox_item_ids
from pfem.intake_decision import collect_intake_decision_ids
from pfem.node_runtime import collect_node_ids
from pfem.outbox import collect_outbox_item_ids
from pfem.transport_receipt import collect_transport_receipt_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "exported",
    "transmitted",
    "received",
    "accepted",
    "rejected",
    "superseded",
}

KNOWN_DECISIONS = {
    "prepared",
    "sent",
    "received",
    "accepted",
    "rejected",
    "superseded",
    "needs-review",
}


@dataclass(frozen=True)
class ExchangeReceipt:
    exchange_receipt_id: str
    receipt_kind: str
    bundle_id: str
    created_time: str
    from_node_id: str
    to_node_id: str
    decision: str
    subject_refs: list[str]
    artifact_refs: list[str]
    summary: str
    transport_receipt_id: str | None = None
    outbox_item_id: str | None = None
    inbox_item_id: str | None = None
    intake_decision_id: str | None = None
    basis_refs: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ExchangeReport:
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


def load_exchange_receipts(path: str | Path) -> list[ExchangeReceipt]:
    return [
        ExchangeReceipt(
            exchange_receipt_id=str(record.get("exchange_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            bundle_id=str(record.get("bundle_id", "")),
            created_time=str(record.get("created_time", "")),
            from_node_id=str(record.get("from_node_id", "")),
            to_node_id=str(record.get("to_node_id", "")),
            decision=str(record.get("decision", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            artifact_refs=_as_list(record.get("artifact_refs", [])),
            summary=str(record.get("summary", "")),
            transport_receipt_id=str(record["transport_receipt_id"]) if "transport_receipt_id" in record else None,
            outbox_item_id=str(record["outbox_item_id"]) if "outbox_item_id" in record else None,
            inbox_item_id=str(record["inbox_item_id"]) if "inbox_item_id" in record else None,
            intake_decision_id=str(record["intake_decision_id"]) if "intake_decision_id" in record else None,
            basis_refs=_as_list(record.get("basis_refs", [])),
        )
        for record in _load_records(Path(path))
    ]


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
    return ids


def _collect_bundle_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in root.glob("bundles/**/*.bundle.json"):
        for record in _load_records(path):
            if record.get("bundle_id"):
                ids.add(str(record["bundle_id"]))
    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "dispatch", "routing", "delivery", "outbox",
        "inbox", "intake", "transport", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "action", "playbooks", "integrity",
        "schemas", "contracts", "docs", "tests", "bundles",
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


def validate_exchange_repository(root: str | Path) -> ExchangeReport:
    root_path = Path(root)
    receipts_path = root_path / "exchange" / "exchange-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return ExchangeReport(
            source=str(receipts_path),
            failures=["missing exchange receipts: exchange/exchange-receipts.json"],
        )

    receipts = load_exchange_receipts(receipts_path)
    node_ids = collect_node_ids(root_path)
    bundle_ids = _collect_bundle_ids(root_path)
    known_record_ids = _collect_known_record_ids(root_path)
    known_artifact_paths = _collect_known_artifact_paths(root_path)
    transport_receipt_ids = collect_transport_receipt_ids(root_path)
    outbox_item_ids = collect_outbox_item_ids(root_path)
    inbox_item_ids = collect_inbox_item_ids(root_path)
    intake_decision_ids = collect_intake_decision_ids(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.exchange_receipt_id:
            failures.append("exchange receipt missing exchange_receipt_id")
            continue
        if receipt.exchange_receipt_id in seen_ids:
            failures.append(f"duplicate exchange_receipt_id {receipt.exchange_receipt_id!r}")
        seen_ids.add(receipt.exchange_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}"
            )
        if receipt.decision not in KNOWN_DECISIONS:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} uses unknown decision {receipt.decision!r}"
            )
        if receipt.bundle_id not in bundle_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown bundle_id {receipt.bundle_id!r}"
            )
        if node_ids and receipt.from_node_id not in node_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown from_node_id {receipt.from_node_id!r}"
            )
        if node_ids and receipt.to_node_id not in node_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown to_node_id {receipt.to_node_id!r}"
            )
        if receipt.transport_receipt_id and transport_receipt_ids and receipt.transport_receipt_id not in transport_receipt_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown transport_receipt_id {receipt.transport_receipt_id!r}"
            )
        if receipt.outbox_item_id and outbox_item_ids and receipt.outbox_item_id not in outbox_item_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown outbox_item_id {receipt.outbox_item_id!r}"
            )
        if receipt.inbox_item_id and inbox_item_ids and receipt.inbox_item_id not in inbox_item_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown inbox_item_id {receipt.inbox_item_id!r}"
            )
        if receipt.intake_decision_id and intake_decision_ids and receipt.intake_decision_id not in intake_decision_ids:
            failures.append(
                f"exchange receipt {receipt.exchange_receipt_id!r} references unknown intake_decision_id {receipt.intake_decision_id!r}"
            )

        if receipt.receipt_kind in {"accepted", "rejected"}:
            if not receipt.inbox_item_id:
                failures.append(f"exchange receipt {receipt.exchange_receipt_id!r} missing inbox_item_id for inbound decision")
            if not receipt.intake_decision_id:
                failures.append(f"exchange receipt {receipt.exchange_receipt_id!r} missing intake_decision_id for inbound decision")

        if not receipt.created_time:
            failures.append(f"exchange receipt {receipt.exchange_receipt_id!r} missing created_time")
        if not receipt.summary:
            failures.append(f"exchange receipt {receipt.exchange_receipt_id!r} missing summary")

        if not receipt.subject_refs:
            failures.append(f"exchange receipt {receipt.exchange_receipt_id!r} has no subject_refs")
        for ref in receipt.subject_refs:
            if ref not in known_record_ids:
                failures.append(
                    f"exchange receipt {receipt.exchange_receipt_id!r} references unknown subject_ref {ref!r}"
                )

        for ref in receipt.basis_refs:
            if not _known_ref(ref, known_record_ids, known_artifact_paths):
                failures.append(
                    f"exchange receipt {receipt.exchange_receipt_id!r} references unknown basis_ref {ref!r}"
                )

        for artifact in receipt.artifact_refs:
            normalized = artifact.replace("\\", "/")
            if normalized not in known_artifact_paths:
                failures.append(
                    f"exchange receipt {receipt.exchange_receipt_id!r} references missing artifact_ref {artifact!r}"
                )

    return ExchangeReport(
        source=str(receipts_path),
        checked_receipts=len(receipts),
        failures=failures,
    )


def format_exchange_report(report: ExchangeReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM exchange source: {report.source}")
    lines.append(f"Exchange receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM exchange validation failed.")
    else:
        lines.append("")
        lines.append("PFEM exchange validation passed.")

    return "\n".join(lines)
