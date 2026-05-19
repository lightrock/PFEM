"""Lightweight PFEM schema contract checks."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]


SCHEMA_TO_FIXTURE_FILES = {
    "finding.schema.json": ["tests/fixtures/**/finding.json"],
    "alert.schema.json": ["tests/fixtures/**/alert.json"],
    "evidence_package.schema.json": ["tests/fixtures/**/evidence_package.json"],
    "rollup_summary.schema.json": ["tests/fixtures/**/rollup_summary.json"],
    "federation_message.schema.json": ["tests/fixtures/**/federation_message.json"],
    "review_record.schema.json": ["review/review-records.json"],
    "audit_event.schema.json": ["audit/audit-journal.json"],
    "handling_policy.schema.json": ["handling/handling-policy.json"],
    "retention_policy.schema.json": ["retention/retention-policy.json"],
    "dispatch_policy.schema.json": ["dispatch/dispatch-policy.json"],
    "dispatch_decision.schema.json": ["dispatch/dispatch-decisions.json"],
    "outbox_item.schema.json": ["outbox/outbox-items.json"],
    "inbox_item.schema.json": ["inbox/inbox-items.json"],
    "delivery_channel_registry.schema.json": ["delivery/delivery-channel-registry.json"],
    "delivery_job.schema.json": ["delivery/delivery-jobs.json"],
    "transport_adapter_registry.schema.json": ["transport/transport-adapter-registry.json"],
    "transport_receipt.schema.json": ["transport/transport-receipts.json"],
    "routing_policy.schema.json": ["routing/routing-policy.json"],
    "exchange_bundle.schema.json": ["bundles/**/*.bundle.json"],
    "exchange_receipt.schema.json": ["exchange/exchange-receipts.json"],
    "reconciliation_record.schema.json": ["reconciliation/reconciliation-records.json"],
    "quality_policy.schema.json": ["quality/quality-policy.json"],
    "quality_assessment.schema.json": ["quality/quality-assessments.json"],
    "action_policy.schema.json": ["action/action-policy.json"],
    "action_record.schema.json": ["action/action-records.json"],
    "playbook.schema.json": ["playbooks/**/*.playbook.json"],
}


@dataclass(frozen=True)
class SchemaContractReport:
    root: Path
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_records(value: Any) -> list[JsonObject]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        records: list[JsonObject] = []
        for item in value:
            if not isinstance(item, dict):
                raise ValueError("record arrays must contain JSON objects")
            records.append(item)
        return records
    raise ValueError("expected JSON object or array")


def _required_fields(schema: JsonObject) -> list[str]:
    required = schema.get("required", [])
    if not isinstance(required, list):
        return []
    return [str(item) for item in required]


def validate_records_against_schema(schema_path: Path, record_paths: list[Path], root: Path) -> tuple[int, list[str]]:
    schema = _load_json(schema_path)
    required = _required_fields(schema)
    failures: list[str] = []
    checked = 0

    for record_path in sorted(set(record_paths)):
        records = _as_records(_load_json(record_path))
        for index, record in enumerate(records):
            checked += 1
            record_label = f"{record_path.relative_to(root)}[{index}]"
            for field in required:
                if field not in record or record[field] in (None, "", []):
                    failures.append(f"{record_label} missing required field {field!r} from {schema_path.name}")

    return checked, failures


def validate_schema_contracts(root: str | Path) -> SchemaContractReport:
    root_path = Path(root)
    failures: list[str] = []
    checked_records = 0

    for schema_name, patterns in SCHEMA_TO_FIXTURE_FILES.items():
        schema_path = root_path / "schemas" / schema_name
        if not schema_path.exists():
            failures.append(f"missing schema: schemas/{schema_name}")
            continue

        record_paths: list[Path] = []
        for pattern in patterns:
            record_paths.extend(root_path.glob(pattern))

        checked, schema_failures = validate_records_against_schema(schema_path, record_paths, root_path)
        checked_records += checked
        failures.extend(schema_failures)

    return SchemaContractReport(root=root_path, checked_records=checked_records, failures=failures)


def format_schema_contract_report(report: SchemaContractReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM schema contract root: {report.root}")
    lines.append(f"Records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM schema contract validation failed.")
    else:
        lines.append("")
        lines.append("PFEM schema contract validation passed.")

    return "\n".join(lines)
