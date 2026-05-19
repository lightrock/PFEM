"""PFEM rollup and federation validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.lineage import load_records


JsonRecord = dict[str, Any]


@dataclass(frozen=True)
class RollupReport:
    source: str
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _ids(records: list[JsonRecord], key: str) -> set[str]:
    return {str(record[key]) for record in records if record.get(key)}


def known_lifecycle_ids(
    evidence_records: list[JsonRecord],
    observation_records: list[JsonRecord],
    finding_records: list[JsonRecord],
    alert_records: list[JsonRecord],
    package_records: list[JsonRecord],
) -> set[str]:
    """Return ids that may be referenced by rollups and federation messages."""
    return (
        _ids(evidence_records, "evidence_id")
        | _ids(observation_records, "observation_id")
        | _ids(finding_records, "finding_id")
        | _ids(alert_records, "alert_id")
        | _ids(package_records, "package_id")
    )


def validate_rollup_summaries(
    known_ids: set[str],
    rollup_records: list[JsonRecord],
) -> list[str]:
    failures: list[str] = []

    for rollup in rollup_records:
        rollup_id = rollup.get("rollup_id", "<missing rollup_id>")
        if not rollup.get("producer_node_id"):
            failures.append(f"rollup {rollup_id!r} missing producer_node_id")
        if not rollup.get("summary_kind"):
            failures.append(f"rollup {rollup_id!r} missing summary_kind")

        for ref in rollup.get("source_lineage_refs", []):
            if ref not in known_ids:
                failures.append(
                    f"rollup {rollup_id!r} references missing lifecycle record {ref!r}"
                )

    return failures


def validate_federation_messages(
    known_ids: set[str],
    rollup_records: list[JsonRecord],
    federation_records: list[JsonRecord],
) -> list[str]:
    rollup_ids = _ids(rollup_records, "rollup_id")
    valid_refs = known_ids | rollup_ids
    failures: list[str] = []

    for message in federation_records:
        message_id = message.get("message_id", "<missing message_id>")
        if not message.get("sender_node_id"):
            failures.append(f"federation message {message_id!r} missing sender_node_id")
        if not message.get("message_kind"):
            failures.append(f"federation message {message_id!r} missing message_kind")

        for ref in message.get("lineage_refs", []):
            if ref not in valid_refs:
                failures.append(
                    f"federation message {message_id!r} references missing lineage record {ref!r}"
                )

    return failures


def validate_rollup_records(
    evidence_records: list[JsonRecord],
    observation_records: list[JsonRecord],
    finding_records: list[JsonRecord],
    alert_records: list[JsonRecord],
    package_records: list[JsonRecord],
    rollup_records: list[JsonRecord],
    federation_records: list[JsonRecord],
    source: str = "records",
) -> RollupReport:
    known_ids = known_lifecycle_ids(
        evidence_records,
        observation_records,
        finding_records,
        alert_records,
        package_records,
    )

    failures: list[str] = []
    failures.extend(validate_rollup_summaries(known_ids, rollup_records))
    failures.extend(validate_federation_messages(known_ids, rollup_records, federation_records))

    checked_records = (
        len(evidence_records)
        + len(observation_records)
        + len(finding_records)
        + len(alert_records)
        + len(package_records)
        + len(rollup_records)
        + len(federation_records)
    )

    return RollupReport(
        source=source,
        checked_records=checked_records,
        failures=failures,
    )


def validate_rollup_dir(path: str | Path) -> RollupReport:
    """Validate rollup/federation fixture directory."""
    root = Path(path)
    lifecycle_root = root / "lifecycle"

    evidence_records = load_records(lifecycle_root / "raw_evidence.json")
    observation_records = load_records(lifecycle_root / "normalized_observation.json")
    finding_records = load_records(lifecycle_root / "finding.json")
    alert_records = load_records(lifecycle_root / "alert.json")
    package_records = load_records(lifecycle_root / "evidence_package.json")
    rollup_records = load_records(root / "rollup_summary.json")
    federation_records = load_records(root / "federation_message.json")

    return validate_rollup_records(
        evidence_records=evidence_records,
        observation_records=observation_records,
        finding_records=finding_records,
        alert_records=alert_records,
        package_records=package_records,
        rollup_records=rollup_records,
        federation_records=federation_records,
        source=str(root),
    )


def format_rollup_report(report: RollupReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM rollup source: {report.source}")
    lines.append(f"Records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM rollup validation failed.")
    else:
        lines.append("")
        lines.append("PFEM rollup validation passed.")

    return "\n".join(lines)
