"""Audit the PFEM permanent-archive terminal tail.

This is a small stabilization check, not another generated record species batch.
It guards the final terminal-closure/endcap area where the schema-contract gate
caught repeated `missing_refs` required-field problems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


FINAL_ENDCAP_CLOSEOUT_PATH = Path(
    "retention/retention-permanent-archive-terminal-closure-final-endcap-closeout-records.json"
)
FINAL_ENDCAP_CLOSEOUT_ID = (
    "retention-permanent-archive-terminal-closure-final-endcap-closeout-basic-restore-001"
)

FINAL_VERIFICATION_SCHEMA_GLOB = (
    "retention_permanent_archive_terminal_closure_final_*_verification_receipt.schema.json"
)


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class RetentionTerminalTailAuditReport:
    root: str
    final_endcap_closeout_found: bool = False
    verification_schemas_checked: int = 0
    verification_receipts_checked: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_records(raw: Any, path: Path) -> list[JsonObject]:
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


def _hyphen_stem(schema_path: Path) -> str:
    name = schema_path.name
    prefix = "retention_"
    suffix = "_verification_receipt.schema.json"
    if not name.startswith(prefix) or not name.endswith(suffix):
        raise ValueError(f"unexpected verification schema name: {name}")
    stem = name[len(prefix) : -len(suffix)]
    return stem.replace("_", "-")


def _check_final_endcap(root: Path, failures: list[str]) -> bool:
    path = root / FINAL_ENDCAP_CLOSEOUT_PATH
    if not path.exists():
        failures.append(f"missing final endcap closeout records: {FINAL_ENDCAP_CLOSEOUT_PATH}")
        return False

    records = _as_records(_load_json(path), path)
    ids = {
        str(record.get("retention_permanent_archive_terminal_closure_final_endcap_closeout_record_id", ""))
        for record in records
    }
    if FINAL_ENDCAP_CLOSEOUT_ID not in ids:
        failures.append(f"missing final endcap closeout id: {FINAL_ENDCAP_CLOSEOUT_ID}")
        return False

    return True


def audit_retention_terminal_tail(root: str | Path) -> RetentionTerminalTailAuditReport:
    root_path = Path(root)
    failures: list[str] = []

    final_found = _check_final_endcap(root_path, failures)

    schema_paths = sorted((root_path / "schemas").glob(FINAL_VERIFICATION_SCHEMA_GLOB))
    if not schema_paths:
        failures.append(f"no final terminal closure verification schemas matched {FINAL_VERIFICATION_SCHEMA_GLOB}")

    schema_count = 0
    receipt_count = 0

    for schema_path in schema_paths:
        schema_count += 1
        schema = _load_json(schema_path)
        required = schema.get("required", [])
        properties = schema.get("properties", {})

        if isinstance(required, list) and "missing_refs" in required:
            failures.append(
                f"{schema_path.relative_to(root_path)} should not require missing_refs; "
                "empty diagnostic arrays are optional"
            )

        if not isinstance(properties, dict) or properties.get("missing_refs") != {"type": "array"}:
            failures.append(
                f"{schema_path.relative_to(root_path)} should define optional missing_refs as an array"
            )

        hyphen_stem = _hyphen_stem(schema_path)
        receipt_path = root_path / "retention" / f"retention-{hyphen_stem}-verification-receipts.json"
        if not receipt_path.exists():
            failures.append(f"missing verification receipts for schema {schema_path.name}: {receipt_path.relative_to(root_path)}")
            continue

        records = _as_records(_load_json(receipt_path), receipt_path)
        for index, record in enumerate(records):
            receipt_count += 1
            missing_refs = record.get("missing_refs")
            if missing_refs is None:
                failures.append(f"{receipt_path.relative_to(root_path)}[{index}] should include missing_refs diagnostic array")
            elif not isinstance(missing_refs, list):
                failures.append(f"{receipt_path.relative_to(root_path)}[{index}] missing_refs should be an array")
            elif record.get("verification_state") == "passed" and missing_refs:
                failures.append(f"{receipt_path.relative_to(root_path)}[{index}] passed but has non-empty missing_refs")

    return RetentionTerminalTailAuditReport(
        root=str(root_path),
        final_endcap_closeout_found=final_found,
        verification_schemas_checked=schema_count,
        verification_receipts_checked=receipt_count,
        failures=failures,
    )


def format_retention_terminal_tail_audit_report(report: RetentionTerminalTailAuditReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM retention terminal tail audit root: {report.root}")
    lines.append(f"Final endcap closeout found: {report.final_endcap_closeout_found}")
    lines.append(f"Verification schemas checked: {report.verification_schemas_checked}")
    lines.append(f"Verification receipts checked: {report.verification_receipts_checked}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM retention terminal tail audit failed.")
    else:
        lines.append("")
        lines.append("PFEM retention terminal tail audit passed.")

    return "\n".join(lines)
