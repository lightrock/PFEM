"""Audit PFEM boundary-language generation standards.

This audit is intentionally about process guardrails, not another PFEM
record species. It keeps future generated boundaries from drifting away from
the standards that make retention, verification, closeout, and terminal
archive chains testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


REQUIRED_GUIDE_PATHS = [
    Path("docs/developer/pfem-boundary-language-generation-standard.md"),
    Path("docs/developer/pfem-new-chat-handoff.md"),
    Path("docs/developer/pfem-terminal-tail-stabilization.md"),
    Path("docs/developer/pfem-architecture-theory-notes.md"),
    Path("docs/developer/pfem-ai-patch-safety-rules.md"),
]

ALLOWED_ROOT_PFEM_BATS = {
    "pfem_check.bat",
}


@dataclass(frozen=True)
class BoundaryLanguageStandardsAuditReport:
    root: str
    manifest_steps_checked: int = 0
    verification_schemas_checked: int = 0
    verification_receipts_checked: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_records(raw: Any, path: Path) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        records: list[dict[str, Any]] = []
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError(f"expected JSON object records in {path}")
            records.append(item)
        return records
    raise ValueError(f"expected JSON object or array in {path}")


def _check_required_guides(root: Path, failures: list[str]) -> None:
    for rel in REQUIRED_GUIDE_PATHS:
        if not (root / rel).exists():
            failures.append(f"missing PFEM boundary-language guide/handoff file: {rel}")


def _check_no_root_bat_churn(root: Path, failures: list[str]) -> None:
    for path in sorted(root.glob("pfem_*.bat")):
        if path.name not in ALLOWED_ROOT_PFEM_BATS:
            failures.append(
                f"root PFEM BAT wrapper should not exist: {path.name}; "
                "add Python tools under tools/ and register them in tools/pfem_check_manifest.json"
            )


def _check_manifest(root: Path, failures: list[str]) -> int:
    manifest_path = root / "tools" / "pfem_check_manifest.json"
    if not manifest_path.exists():
        failures.append("missing tools/pfem_check_manifest.json")
        return 0

    manifest = _load_json(manifest_path)
    steps = manifest.get("steps", [])
    if not isinstance(steps, list):
        failures.append("tools/pfem_check_manifest.json has no list-valued steps field")
        return 0

    checked = 0
    seen_args: set[tuple[str, ...]] = set()
    has_boundary_language_audit = False

    for index, step in enumerate(steps):
        checked += 1
        if not isinstance(step, dict):
            failures.append(f"manifest step {index} is not an object")
            continue

        label = step.get("label")
        args = step.get("args")

        if not isinstance(label, str) or not label.strip():
            failures.append(f"manifest step {index} is missing a label")

        if not isinstance(args, list) or not args:
            failures.append(f"manifest step {index} is missing args")
            continue

        args_tuple = tuple(str(arg) for arg in args)
        if args_tuple in seen_args:
            failures.append(f"duplicate manifest args entry: {args_tuple}")
        seen_args.add(args_tuple)

        first = str(args[0])
        if first == "tools/pfem_boundary_language_standards_audit.py":
            has_boundary_language_audit = True
        if "generated boundary" in first.lower() or (isinstance(label, str) and "generated boundary" in label.lower()):
            failures.append(f"manifest still contains deprecated placeholder language at step {index}")
        if first.lower().endswith(".bat"):
            failures.append(f"manifest step should not call BAT wrapper: {first}")
        if first.startswith("tools/") and first.endswith(".py") and not (root / first).exists():
            failures.append(f"manifest references missing tool: {first}")

    if not has_boundary_language_audit:
        failures.append("manifest is missing tools/pfem_boundary_language_standards_audit.py")

    return checked


def _check_verification_receipt_schemas(root: Path, failures: list[str]) -> int:
    checked = 0
    schemas_dir = root / "schemas"
    if not schemas_dir.exists():
        return checked

    for schema_path in sorted(schemas_dir.glob("*_verification_receipt.schema.json")):
        checked += 1
        schema = _load_json(schema_path)
        required = schema.get("required", [])
        properties = schema.get("properties", {})

        if isinstance(required, list) and "missing_refs" in required:
            failures.append(
                f"{schema_path.relative_to(root)} should not require missing_refs; "
                "missing_refs is an optional diagnostic array"
            )

        if isinstance(properties, dict) and "missing_refs" in properties:
            missing_refs_schema = properties.get("missing_refs")
            if not isinstance(missing_refs_schema, dict) or missing_refs_schema.get("type") != "array":
                failures.append(
                    f"{schema_path.relative_to(root)} should define missing_refs as an array property"
                )

    return checked


def _check_verification_receipts(root: Path, failures: list[str]) -> int:
    checked = 0
    retention_dir = root / "retention"
    if not retention_dir.exists():
        return checked

    for receipt_path in sorted(retention_dir.glob("retention-*-verification-receipts.json")):
        raw = _load_json(receipt_path)
        records = _as_records(raw, receipt_path)

        for index, record in enumerate(records):
            checked += 1
            state = record.get("verification_state")
            missing_refs = record.get("missing_refs")

            if missing_refs is not None and not isinstance(missing_refs, list):
                failures.append(
                    f"{receipt_path.relative_to(root)}[{index}] missing_refs should be an array when present"
                )

            if state == "passed" and isinstance(missing_refs, list) and missing_refs:
                failures.append(
                    f"{receipt_path.relative_to(root)}[{index}] passed but has non-empty missing_refs"
                )

    return checked


def audit_boundary_language_standards(root: str | Path) -> BoundaryLanguageStandardsAuditReport:
    root_path = Path(root)
    failures: list[str] = []

    _check_required_guides(root_path, failures)
    _check_no_root_bat_churn(root_path, failures)
    manifest_steps = _check_manifest(root_path, failures)
    schema_count = _check_verification_receipt_schemas(root_path, failures)
    receipt_count = _check_verification_receipts(root_path, failures)

    return BoundaryLanguageStandardsAuditReport(
        root=str(root_path),
        manifest_steps_checked=manifest_steps,
        verification_schemas_checked=schema_count,
        verification_receipts_checked=receipt_count,
        failures=failures,
    )


def format_boundary_language_standards_audit_report(report: BoundaryLanguageStandardsAuditReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM boundary-language standards audit root: {report.root}")
    lines.append(f"Manifest steps checked: {report.manifest_steps_checked}")
    lines.append(f"Verification schemas checked: {report.verification_schemas_checked}")
    lines.append(f"Verification receipts checked: {report.verification_receipts_checked}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM boundary-language standards audit failed.")
    else:
        lines.append("")
        lines.append("PFEM boundary-language standards audit passed.")

    return "\n".join(lines)
