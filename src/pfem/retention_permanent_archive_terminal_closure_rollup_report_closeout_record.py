# PFEM retention permanent archive terminal closure rollup report closeout records validation.

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]
ID_FIELD = 'retention_permanent_archive_terminal_closure_rollup_report_closeout_record_id'
JSON_PATH = 'retention/retention-permanent-archive-terminal-closure-rollup-report-closeout-records.json'
REQUIRED_FIELDS = [
    "retention_permanent_archive_terminal_closure_rollup_report_closeout_record_id",
    "closeout_kind",
    "created_time",
    "node_id",
    "retention_permanent_archive_terminal_closure_rollup_report_verification_receipt_id",
    "retention_permanent_archive_terminal_closure_rollup_report_record_id",
    "closeout_state",
    "outcome",
    "closed_refs",
    "subject_refs",
    "basis_refs",
    "closed_by_ref",
    "summary"
]
ENUMS = {
    "closeout_kind": [
        "retention_permanent_archive_terminal_closure_rollup_report_closeout",
        "manual_retention_permanent_archive_terminal_closure_rollup_report_closeout"
    ],
    "closeout_state": [
        "closed",
        "closed_with_exceptions",
        "deferred",
        "escalated",
        "cancelled",
        "superseded"
    ],
    "outcome": [
        "retention_permanent_archive_terminal_closure_rollup_report_verified_and_closed",
        "retention_permanent_archive_terminal_closure_rollup_report_closed_with_exceptions",
        "retention_permanent_archive_terminal_closure_rollup_report_failed"
    ]
}
DIGEST_FIELD = None
EXPECTED_DIGEST_FIELD = None
DIGEST_SOURCE_FIELD = None

@dataclass(frozen=True)
class RetentionPermanentArchiveTerminalClosureRollupReportCloseoutRecordReport:
    source: str
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures

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

def load_retention_permanent_archive_terminal_closure_rollup_report_closeout_records(path: str | Path) -> list[JsonObject]:
    return _load_records(Path(path))

def collect_retention_permanent_archive_terminal_closure_rollup_report_closeout_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / JSON_PATH
    if not records_path.exists():
        return set()
    return {str(record.get(ID_FIELD, "")) for record in load_retention_permanent_archive_terminal_closure_rollup_report_closeout_records(records_path) if record.get(ID_FIELD)}

def _as_list(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []

def _digest(refs: list[str]) -> str:
    payload = json.dumps(sorted(refs), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def validate_retention_permanent_archive_terminal_closure_rollup_report_closeout_records(root: str | Path) -> RetentionPermanentArchiveTerminalClosureRollupReportCloseoutRecordReport:
    root_path = Path(root)
    records_path = root_path / JSON_PATH
    failures: list[str] = []
    if not records_path.exists():
        return RetentionPermanentArchiveTerminalClosureRollupReportCloseoutRecordReport(source=str(records_path), failures=[f"missing retention permanent archive terminal closure rollup report closeout records: {JSON_PATH}"])
    records = load_retention_permanent_archive_terminal_closure_rollup_report_closeout_records(records_path)
    if not records:
        failures.append("retention permanent archive terminal closure rollup report closeout records file has no records")
    seen_ids: set[str] = set()
    for record in records:
        record_id = str(record.get(ID_FIELD, ""))
        if not record_id:
            failures.append(f"retention permanent archive terminal closure rollup report closeout records record missing {ID_FIELD}")
            continue
        if record_id in seen_ids:
            failures.append(f"duplicate {ID_FIELD} {record_id!r}")
        seen_ids.add(record_id)
        for field in REQUIRED_FIELDS:
            if field not in record or record.get(field) in ("", None):
                failures.append(f"retention permanent archive terminal closure rollup report closeout records {record_id!r} missing {field}")
        for field, allowed in ENUMS.items():
            value = record.get(field)
            if value not in allowed:
                failures.append(f"retention permanent archive terminal closure rollup report closeout records {record_id!r} uses unknown {field} {value!r}")
        if record.get("verification_state") == "passed" and _as_list(record.get("missing_refs", [])):
            failures.append(f"retention permanent archive terminal closure rollup report closeout records {record_id!r} passed but has missing_refs")
        if DIGEST_FIELD and DIGEST_SOURCE_FIELD:
            actual = _digest(_as_list(record.get(DIGEST_SOURCE_FIELD, [])))
            if record.get(DIGEST_FIELD) != actual:
                failures.append(f"retention permanent archive terminal closure rollup report closeout records {record_id!r} {DIGEST_FIELD} does not match {DIGEST_SOURCE_FIELD}")
            if EXPECTED_DIGEST_FIELD and record.get(EXPECTED_DIGEST_FIELD) != record.get(DIGEST_FIELD):
                failures.append(f"retention permanent archive terminal closure rollup report closeout records {record_id!r} expected/actual digest mismatch")
    return RetentionPermanentArchiveTerminalClosureRollupReportCloseoutRecordReport(source=str(records_path), checked_records=len(records), failures=failures)

def format_retention_permanent_archive_terminal_closure_rollup_report_closeout_record_report(report: RetentionPermanentArchiveTerminalClosureRollupReportCloseoutRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM retention permanent archive terminal closure rollup report closeout records source: {report.source}")
    lines.append(f"Retention Permanent Archive Terminal Closure Rollup Report Closeout Records checked: {report.checked_records}")
    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM retention permanent archive terminal closure rollup report closeout records validation failed.")
    else:
        lines.append("")
        lines.append("PFEM retention permanent archive terminal closure rollup report closeout records validation passed.")
    return "\n".join(lines)
