"""PFEM reconciliation record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_RECONCILIATION_KINDS = {
    "conflict",
    "correction",
    "merge",
    "supersession",
    "rejection",
    "unresolved_conflict",
}

KNOWN_DECISIONS = {
    "accepted",
    "rejected",
    "merged",
    "superseded",
    "corrected",
    "unresolved",
    "needs-review",
}

KNOWN_RESULT_STATES = {
    "active",
    "superseded",
    "corrected",
    "merged",
    "rejected",
    "unresolved",
    "needs-review",
}


@dataclass(frozen=True)
class ReconciliationRecord:
    reconciliation_id: str
    reconciliation_kind: str
    created_time: str
    created_by_ref: str
    subject_refs: list[str]
    basis_refs: list[str]
    decision: str
    result_state: str
    summary: str
    notes: str | None = None


@dataclass(frozen=True)
class ReconciliationReport:
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


def load_reconciliation_records(path: str | Path) -> list[ReconciliationRecord]:
    return [
        ReconciliationRecord(
            reconciliation_id=str(record.get("reconciliation_id", "")),
            reconciliation_kind=str(record.get("reconciliation_kind", "")),
            created_time=str(record.get("created_time", "")),
            created_by_ref=str(record.get("created_by_ref", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            decision=str(record.get("decision", "")),
            result_state=str(record.get("result_state", "")),
            summary=str(record.get("summary", "")),
            notes=str(record["notes"]) if "notes" in record else None,
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
    ]
    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))
    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters",
        "profiles",
        "nodes",
        "sources",
        "examples",
        "policy",
        "handling",
        "retention",
        "topology",
        "review",
        "audit",
        "exchange",
        "reconciliation",
        "integrity",
        "schemas",
        "contracts",
        "docs",
        "tests",
        "bundles",
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


def validate_reconciliation_repository(root: str | Path) -> ReconciliationReport:
    root_path = Path(root)
    records_path = root_path / "reconciliation" / "reconciliation-records.json"
    failures: list[str] = []

    if not records_path.exists():
        return ReconciliationReport(
            source=str(records_path),
            failures=["missing reconciliation records: reconciliation/reconciliation-records.json"],
        )

    records = load_reconciliation_records(records_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    node_ids = collect_node_ids(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.reconciliation_id:
            failures.append("reconciliation record missing reconciliation_id")
            continue
        if record.reconciliation_id in seen_ids:
            failures.append(f"duplicate reconciliation_id {record.reconciliation_id!r}")
        seen_ids.add(record.reconciliation_id)

        if record.reconciliation_kind not in KNOWN_RECONCILIATION_KINDS:
            failures.append(
                f"reconciliation {record.reconciliation_id!r} uses unknown reconciliation_kind {record.reconciliation_kind!r}"
            )
        if record.decision not in KNOWN_DECISIONS:
            failures.append(
                f"reconciliation {record.reconciliation_id!r} uses unknown decision {record.decision!r}"
            )
        if record.result_state not in KNOWN_RESULT_STATES:
            failures.append(
                f"reconciliation {record.reconciliation_id!r} uses unknown result_state {record.result_state!r}"
            )

        if not record.created_time:
            failures.append(f"reconciliation {record.reconciliation_id!r} missing created_time")
        if not record.created_by_ref:
            failures.append(f"reconciliation {record.reconciliation_id!r} missing created_by_ref")
        elif node_ids and record.created_by_ref not in node_ids and not _known_ref(record.created_by_ref, known_ids, known_paths):
            failures.append(
                f"reconciliation {record.reconciliation_id!r} references unknown created_by_ref {record.created_by_ref!r}"
            )

        if not record.subject_refs:
            failures.append(f"reconciliation {record.reconciliation_id!r} has no subject_refs")
        for ref in record.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"reconciliation {record.reconciliation_id!r} references unknown subject_ref {ref!r}"
                )

        if not record.basis_refs:
            failures.append(f"reconciliation {record.reconciliation_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"reconciliation {record.reconciliation_id!r} references unknown basis_ref {ref!r}"
                )

        if not record.summary:
            failures.append(f"reconciliation {record.reconciliation_id!r} missing summary")

    return ReconciliationReport(
        source=str(records_path),
        checked_records=len(records),
        failures=failures,
    )


def format_reconciliation_report(report: ReconciliationReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM reconciliation source: {report.source}")
    lines.append(f"Reconciliation records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM reconciliation validation failed.")
    else:
        lines.append("")
        lines.append("PFEM reconciliation validation passed.")

    return "\n".join(lines)
