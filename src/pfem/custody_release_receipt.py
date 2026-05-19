"""PFEM custody release receipts validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]
ID_FIELD = 'custody_release_receipt_id'
JSON_PATH = 'custody/custody-release-receipts.json'
REQUIRED_FIELDS = [
    "custody_release_receipt_id",
    "receipt_kind",
    "created_time",
    "node_id",
    "custody_release_approval_id",
    "custody_release_request_id",
    "release_state",
    "release_scope",
    "released_refs",
    "basis_refs",
    "released_by_ref",
    "summary"
]
ENUMS = {
    "receipt_kind": [
        "custody_release_execution_receipt",
        "manual_custody_release_receipt"
    ],
    "release_state": [
        "completed",
        "partially_completed",
        "failed",
        "skipped",
        "pending"
    ],
    "release_scope": [
        "closed_custody_chain_artifacts",
        "evidence_package",
        "archived_records"
    ]
}
SINGLE_REF_FIELDS = [
    "custody_release_approval_id",
    "custody_release_request_id"
]
LIST_REF_FIELDS = [
    "released_refs",
    "skipped_refs",
    "failed_refs",
    "basis_refs"
]
DIGEST_FIELD = None
EXPECTED_DIGEST_FIELD = None
DIGEST_SOURCE_FIELD = None
DIGEST_ALGORITHM = None


@dataclass(frozen=True)
class CustodyReleaseReceiptReport:
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


def load_custody_release_receipts(path: str | Path) -> list[JsonObject]:
    return _load_records(Path(path))


def collect_custody_release_receipt_ids(root: str | Path) -> set[str]:
    records_path = Path(root) / JSON_PATH
    if not records_path.exists():
        return set()
    return {
        str(record.get(ID_FIELD, ""))
        for record in load_custody_release_receipts(records_path)
        if record.get(ID_FIELD)
    }


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


def validate_custody_release_receipts(root: str | Path) -> CustodyReleaseReceiptReport:
    root_path = Path(root)
    records_path = root_path / JSON_PATH
    failures: list[str] = []

    if not records_path.exists():
        return CustodyReleaseReceiptReport(source=str(records_path), failures=[f"missing custody release receipts: {JSON_PATH}"])

    records = load_custody_release_receipts(records_path)
    if not records:
        failures.append("custody release receipts file has no records")

    node_ids = collect_node_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for record in records:
        record_id = str(record.get(ID_FIELD, ""))
        if not record_id:
            failures.append(f"custody release receipts record missing {ID_FIELD}")
            continue
        if record_id in seen_ids:
            failures.append(f"duplicate {ID_FIELD} {record_id!r}")
        seen_ids.add(record_id)

        for field in REQUIRED_FIELDS:
            if field not in record or record.get(field) in ("", None):
                failures.append(f"custody release receipts {record_id!r} missing {field}")

        node_id = record.get("node_id")
        if node_ids and node_id and str(node_id) not in node_ids:
            failures.append(f"custody release receipts {record_id!r} references unknown node_id {node_id!r}")

        for field, allowed in ENUMS.items():
            value = record.get(field)
            if value not in allowed:
                failures.append(f"custody release receipts {record_id!r} uses unknown {field} {value!r}")

        for field in SINGLE_REF_FIELDS:
            ref = str(record.get(field, ""))
            if ref and not _known_ref(ref, known_ids, known_paths):
                failures.append(f"custody release receipts {record_id!r} references unknown {field} {ref!r}")

        for field in LIST_REF_FIELDS:
            refs = _as_list(record.get(field, []))
            if field not in ("missing_refs", "skipped_refs", "failed_refs") and not refs:
                failures.append(f"custody release receipts {record_id!r} has no {field}")
            for ref in refs:
                if ref and not _known_ref(ref, known_ids, known_paths):
                    failures.append(f"custody release receipts {record_id!r} references unknown {field} {ref!r}")

        if record.get("verification_state") == "passed" and _as_list(record.get("missing_refs", [])):
            failures.append(f"custody release receipts {record_id!r} passed but has missing_refs")
        if record.get("release_state") == "completed" and not _as_list(record.get("released_refs", [])):
            failures.append(f"custody release receipts {record_id!r} completed but has no released_refs")

        if DIGEST_FIELD and DIGEST_SOURCE_FIELD:
            refs = _as_list(record.get(DIGEST_SOURCE_FIELD, []))
            actual = _digest(refs)
            if record.get(DIGEST_FIELD) != actual:
                failures.append(f"custody release receipts {record_id!r} {DIGEST_FIELD} does not match {DIGEST_SOURCE_FIELD}")
            if EXPECTED_DIGEST_FIELD and record.get(EXPECTED_DIGEST_FIELD) != record.get(DIGEST_FIELD):
                failures.append(f"custody release receipts {record_id!r} expected/actual digest mismatch")

    return CustodyReleaseReceiptReport(source=str(records_path), checked_records=len(records), failures=failures)


def format_custody_release_receipt_report(report: CustodyReleaseReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM custody release receipts source: {report.source}")
    lines.append(f"Custody Release Receipts checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM custody release receipts validation failed.")
    else:
        lines.append("")
        lines.append("PFEM custody release receipts validation passed.")

    return "\n".join(lines)
