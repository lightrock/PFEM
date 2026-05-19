"""PFEM lineage validation.

Lineage validation checks that derived records point back to records that exist.
It is intentionally dependency-free and works on plain dictionaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


JsonRecord = dict[str, Any]


@dataclass(frozen=True)
class LineageReport:
    source: str
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_records(value: Any) -> list[JsonRecord]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        records: list[JsonRecord] = []
        for item in value:
            if not isinstance(item, dict):
                raise ValueError("record arrays must contain JSON objects")
            records.append(item)
        return records
    raise ValueError("expected a JSON object or array of JSON objects")


def load_records(path: str | Path) -> list[JsonRecord]:
    """Load one JSON record or an array of JSON records."""
    return _as_records(json.loads(Path(path).read_text(encoding="utf-8")))


def _ids(records: list[JsonRecord], key: str) -> set[str]:
    return {str(record[key]) for record in records if record.get(key)}


def validate_observation_lineage(evidence_records: list[JsonRecord], observation_records: list[JsonRecord]) -> list[str]:
    evidence_ids = _ids(evidence_records, "evidence_id")
    failures: list[str] = []

    for observation in observation_records:
        observation_id = observation.get("observation_id", "<missing observation_id>")
        for evidence_id in observation.get("source_evidence_ids", []):
            if evidence_id not in evidence_ids:
                failures.append(
                    f"observation {observation_id!r} references missing evidence {evidence_id!r}"
                )

    return failures


def validate_finding_lineage(observation_records: list[JsonRecord], finding_records: list[JsonRecord]) -> list[str]:
    observation_ids = _ids(observation_records, "observation_id")
    failures: list[str] = []

    for finding in finding_records:
        finding_id = finding.get("finding_id", "<missing finding_id>")
        for observation_id in finding.get("source_observation_ids", []):
            if observation_id not in observation_ids:
                failures.append(
                    f"finding {finding_id!r} references missing observation {observation_id!r}"
                )

    return failures


def validate_alert_lineage(finding_records: list[JsonRecord], alert_records: list[JsonRecord]) -> list[str]:
    finding_ids = _ids(finding_records, "finding_id")
    failures: list[str] = []

    for alert in alert_records:
        alert_id = alert.get("alert_id", "<missing alert_id>")
        finding_id = alert.get("finding_id")
        if finding_id and finding_id not in finding_ids:
            failures.append(
                f"alert {alert_id!r} references missing finding {finding_id!r}"
            )

    return failures


def validate_evidence_package_lineage(
    evidence_records: list[JsonRecord],
    observation_records: list[JsonRecord],
    finding_records: list[JsonRecord],
    alert_records: list[JsonRecord],
    package_records: list[JsonRecord],
) -> list[str]:
    known_ids = (
        _ids(evidence_records, "evidence_id")
        | _ids(observation_records, "observation_id")
        | _ids(finding_records, "finding_id")
        | _ids(alert_records, "alert_id")
    )
    failures: list[str] = []

    for package in package_records:
        package_id = package.get("package_id", "<missing package_id>")
        for included_ref in package.get("included_refs", []):
            if included_ref not in known_ids:
                failures.append(
                    f"evidence package {package_id!r} references missing record {included_ref!r}"
                )

    return failures


def validate_lifecycle_records(
    evidence_records: list[JsonRecord],
    observation_records: list[JsonRecord],
    finding_records: list[JsonRecord],
    alert_records: list[JsonRecord],
    package_records: list[JsonRecord] | None = None,
    source: str = "records",
) -> LineageReport:
    failures: list[str] = []
    package_records = package_records or []

    failures.extend(validate_observation_lineage(evidence_records, observation_records))
    failures.extend(validate_finding_lineage(observation_records, finding_records))
    failures.extend(validate_alert_lineage(finding_records, alert_records))
    failures.extend(
        validate_evidence_package_lineage(
            evidence_records,
            observation_records,
            finding_records,
            alert_records,
            package_records,
        )
    )

    checked_records = (
        len(evidence_records)
        + len(observation_records)
        + len(finding_records)
        + len(alert_records)
        + len(package_records)
    )

    return LineageReport(
        source=source,
        checked_records=checked_records,
        failures=failures,
    )


def validate_lifecycle_dir(path: str | Path) -> LineageReport:
    """Validate a lifecycle fixture directory.

    Expected files:

    - raw_evidence.json
    - normalized_observation.json
    - finding.json
    - alert.json
    - evidence_package.json, optional
    """
    root = Path(path)
    evidence_records = load_records(root / "raw_evidence.json")
    observation_records = load_records(root / "normalized_observation.json")
    finding_records = load_records(root / "finding.json")
    alert_records = load_records(root / "alert.json")

    package_path = root / "evidence_package.json"
    package_records = load_records(package_path) if package_path.exists() else []

    return validate_lifecycle_records(
        evidence_records=evidence_records,
        observation_records=observation_records,
        finding_records=finding_records,
        alert_records=alert_records,
        package_records=package_records,
        source=str(root),
    )


def format_lineage_report(report: LineageReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM lineage source: {report.source}")
    lines.append(f"Records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM lineage validation failed.")
    else:
        lines.append("")
        lines.append("PFEM lineage validation passed.")

    return "\n".join(lines)
