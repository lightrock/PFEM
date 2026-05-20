"""PFEM retention permanent archive terminal closeout access certificate records validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids

JsonObject = dict[str, Any]
ID_FIELD = 'retention_permanent_archive_terminal_closeout_access_certificate_record_id'
JSON_PATH = 'retention/retention-permanent-archive-terminal-closeout-access-certificate-records.json'
REQUIRED_FIELDS = [
    "retention_permanent_archive_terminal_closeout_access_certificate_record_id",
    "permanent_archive_terminal_closeout_access_certificate_kind",
    "created_time",
    "node_id",
    "retention_permanent_archive_terminal_closeout_integrity_certificate_closeout_record_id",
    "retention_permanent_archive_terminal_closeout_integrity_certificate_verification_receipt_id",
    "permanent_archive_terminal_closeout_access_certificate_state",
    "permanent_archive_terminal_closeout_access_certificate_scope",
    "permanent_archive_terminal_closeout_access_certificate_refs",
    "subject_refs",
    "basis_refs",
    "digest_algorithm",
    "permanent_archive_terminal_closeout_access_certificate_ref_digest",
    "permanent_archive_terminal_closeout_access_certificate_by_ref",
    "summary"
]
ENUMS = {
    "permanent_archive_terminal_closeout_access_certificate_kind": [
        "retention_permanent_archive_terminal_closeout_access_certificate",
        "manual_retention_permanent_archive_terminal_closeout_access_certificate"
    ],
    "permanent_archive_terminal_closeout_access_certificate_state": [
        "accepted",
        "accessioned",
        "approved",
        "archived",
        "attested",
        "certified",
        "closed",
        "completed",
        "deposited",
        "exported",
        "finalized",
        "frozen",
        "indexed",
        "locked",
        "pending",
        "published",
        "ready",
        "recorded",
        "registered",
        "released",
        "reported",
        "scheduled",
        "sealed",
        "snapshotted",
        "summarized",
        "superseded",
        "terminal",
        "transferred",
        "verified",
        "voided"
    ],
    "permanent_archive_terminal_closeout_access_certificate_scope": [
        "closed_retention_permanent_archive_terminal_closeout_integrity_certificate",
        "closed_retention_permanent_archive_terminal_final_rollup_report",
        "closed_retention_permanent_archive"
    ],
    "digest_algorithm": [
        "sha256-sorted-retention-permanent-archive-terminal-closeout-access-certificate-ref-list"
    ]
}
SINGLE_REF_FIELDS = [
    "retention_permanent_archive_terminal_closeout_integrity_certificate_closeout_record_id",
    "retention_permanent_archive_terminal_closeout_integrity_certificate_verification_receipt_id"
]
LIST_REF_FIELDS = [
    "permanent_archive_terminal_closeout_access_certificate_refs",
    "subject_refs",
    "basis_refs"
]
DIGEST_FIELD = 'permanent_archive_terminal_closeout_access_certificate_ref_digest'
EXPECTED_DIGEST_FIELD = None
DIGEST_SOURCE_FIELD = 'permanent_archive_terminal_closeout_access_certificate_refs'

@dataclass(frozen=True)
class RetentionPermanentArchiveTerminalCloseoutAccessCertificateRecordReport:
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

def load_retention_permanent_archive_terminal_closeout_access_certificate_records(path: str | Path) -> list[JsonObject]:
    return _load_records(Path(path))

def collect_retention_permanent_archive_terminal_closeout_access_certificate_record_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / JSON_PATH
    if not records_path.exists():
        return set()
    return {str(record.get(ID_FIELD, "")) for record in load_retention_permanent_archive_terminal_closeout_access_certificate_records(records_path) if record.get(ID_FIELD)}

def _iter_values(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from _iter_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_values(child)

def _collect_known_record_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for key, value in _iter_values(raw):
            if isinstance(value, str) and (key.endswith("_id") or key in {"message_id", "package_id", "route_id", "channel_id"}):
                ids.add(value)
    return ids

def _collect_known_artifact_paths(root: Path) -> set[str]:
    paths: set[str] = set()
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file():
            paths.add(str(path.relative_to(root)).replace("\\", "/"))
    return paths

def _known_ref(ref: str, known_ids: set[str], known_paths: set[str]) -> bool:
    return ref in known_ids or ref.replace("\\", "/") in known_paths

def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []

def _digest(refs: list[str]) -> str:
    payload = json.dumps(sorted(refs), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def validate_retention_permanent_archive_terminal_closeout_access_certificate_records(root: str | Path) -> RetentionPermanentArchiveTerminalCloseoutAccessCertificateRecordReport:
    root_path = Path(root)
    records_path = root_path / JSON_PATH
    failures: list[str] = []
    if not records_path.exists():
        return RetentionPermanentArchiveTerminalCloseoutAccessCertificateRecordReport(source=str(records_path), failures=[f"missing retention permanent archive terminal closeout access certificate records: {JSON_PATH}"])
    records = load_retention_permanent_archive_terminal_closeout_access_certificate_records(records_path)
    if not records:
        failures.append("retention permanent archive terminal closeout access certificate records file has no records")
    node_ids = collect_node_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()
    for record in records:
        record_id = str(record.get(ID_FIELD, ""))
        if not record_id:
            failures.append(f"retention permanent archive terminal closeout access certificate records record missing {ID_FIELD}")
            continue
        if record_id in seen_ids:
            failures.append(f"duplicate {ID_FIELD} {record_id!r}")
        seen_ids.add(record_id)
        for field in REQUIRED_FIELDS:
            if field not in record or record.get(field) in ("", None):
                failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} missing {field}")
        node_id = record.get("node_id")
        if node_ids and node_id and str(node_id) not in node_ids:
            failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} references unknown node_id {node_id!r}")
        for field, allowed in ENUMS.items():
            value = record.get(field)
            if value not in allowed:
                failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} uses unknown {field} {value!r}")
        for field in SINGLE_REF_FIELDS:
            ref = str(record.get(field, ""))
            if ref and not _known_ref(ref, known_ids, known_paths):
                failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} references unknown {field} {ref!r}")
        for field in LIST_REF_FIELDS:
            refs = _as_list(record.get(field, []))
            if field not in ("missing_refs", "skipped_refs", "failed_refs") and not refs:
                failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} has no {field}")
            for ref in refs:
                if ref and not _known_ref(ref, known_ids, known_paths):
                    failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} references unknown {field} {ref!r}")
        if record.get("verification_state") == "passed" and _as_list(record.get("missing_refs", [])):
            failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} passed but has missing_refs")
        if DIGEST_FIELD and DIGEST_SOURCE_FIELD:
            refs = _as_list(record.get(DIGEST_SOURCE_FIELD, []))
            actual = _digest(refs)
            if record.get(DIGEST_FIELD) != actual:
                failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} {DIGEST_FIELD} does not match {DIGEST_SOURCE_FIELD}")
            if EXPECTED_DIGEST_FIELD and record.get(EXPECTED_DIGEST_FIELD) != record.get(DIGEST_FIELD):
                failures.append(f"retention permanent archive terminal closeout access certificate records {record_id!r} expected/actual digest mismatch")
    return RetentionPermanentArchiveTerminalCloseoutAccessCertificateRecordReport(source=str(records_path), checked_records=len(records), failures=failures)

def format_retention_permanent_archive_terminal_closeout_access_certificate_record_report(report: RetentionPermanentArchiveTerminalCloseoutAccessCertificateRecordReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM retention permanent archive terminal closeout access certificate records source: {report.source}")
    lines.append(f"Retention Permanent Archive Terminal Closeout Access Certificate Records checked: {report.checked_records}")
    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM retention permanent archive terminal closeout access certificate records validation failed.")
    else:
        lines.append("")
        lines.append("PFEM retention permanent archive terminal closeout access certificate records validation passed.")
    return "\n".join(lines)
