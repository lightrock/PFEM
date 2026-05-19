"""PFEM confidence and quality validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class ConfidenceLevel:
    confidence_level: str
    display_name: str
    rank: int
    description: str


@dataclass(frozen=True)
class QualityFlag:
    flag_id: str
    display_name: str
    description: str


@dataclass(frozen=True)
class QualityPolicy:
    policy_id: str
    version: str
    confidence_levels: list[ConfidenceLevel]
    quality_flags: list[QualityFlag]


@dataclass(frozen=True)
class QualityAssessment:
    quality_assessment_id: str
    created_time: str
    assessor_ref: str
    subject_refs: list[str]
    basis_refs: list[str]
    confidence_level: str
    quality_flags: list[str]
    uncertainty_summary: str
    recommended_use: str


@dataclass(frozen=True)
class QualityReport:
    source: str
    checked_policy_levels: int = 0
    checked_policy_flags: int = 0
    checked_assessments: int = 0
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


def load_quality_policy(path: str | Path) -> QualityPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    levels = [
        ConfidenceLevel(
            confidence_level=str(item.get("confidence_level", "")),
            display_name=str(item.get("display_name", "")),
            rank=int(item.get("rank", 0)),
            description=str(item.get("description", "")),
        )
        for item in raw.get("confidence_levels", [])
    ]
    flags = [
        QualityFlag(
            flag_id=str(item.get("flag_id", "")),
            display_name=str(item.get("display_name", "")),
            description=str(item.get("description", "")),
        )
        for item in raw.get("quality_flags", [])
    ]
    return QualityPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        confidence_levels=levels,
        quality_flags=flags,
    )


def load_quality_assessments(path: str | Path) -> list[QualityAssessment]:
    return [
        QualityAssessment(
            quality_assessment_id=str(record.get("quality_assessment_id", "")),
            created_time=str(record.get("created_time", "")),
            assessor_ref=str(record.get("assessor_ref", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            confidence_level=str(record.get("confidence_level", "")),
            quality_flags=_as_list(record.get("quality_flags", [])),
            uncertainty_summary=str(record.get("uncertainty_summary", "")),
            recommended_use=str(record.get("recommended_use", "")),
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
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "integrity", "schemas", "contracts",
        "docs", "tests", "bundles",
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


def validate_quality_repository(root: str | Path) -> QualityReport:
    root_path = Path(root)
    policy_path = root_path / "quality" / "quality-policy.json"
    assessments_path = root_path / "quality" / "quality-assessments.json"
    failures: list[str] = []

    if not policy_path.exists():
        return QualityReport(
            source=str(policy_path),
            failures=["missing quality policy: quality/quality-policy.json"],
        )

    if not assessments_path.exists():
        return QualityReport(
            source=str(assessments_path),
            failures=["missing quality assessments: quality/quality-assessments.json"],
        )

    policy = load_quality_policy(policy_path)
    assessments = load_quality_assessments(assessments_path)

    if not policy.policy_id:
        failures.append("quality policy missing policy_id")
    if not policy.version:
        failures.append("quality policy missing version")
    if not policy.confidence_levels:
        failures.append("quality policy has no confidence_levels")
    if not policy.quality_flags:
        failures.append("quality policy has no quality_flags")

    level_ids = [level.confidence_level for level in policy.confidence_levels]
    flag_ids = [flag.flag_id for flag in policy.quality_flags]

    if len(level_ids) != len(set(level_ids)):
        failures.append("quality policy has duplicate confidence_level values")
    if len(flag_ids) != len(set(flag_ids)):
        failures.append("quality policy has duplicate quality flag ids")

    known_levels = {level.confidence_level for level in policy.confidence_levels if level.confidence_level}
    known_flags = {flag.flag_id for flag in policy.quality_flags if flag.flag_id}
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    node_ids = collect_node_ids(root_path)
    seen_assessment_ids: set[str] = set()

    for assessment in assessments:
        if not assessment.quality_assessment_id:
            failures.append("quality assessment missing quality_assessment_id")
            continue
        if assessment.quality_assessment_id in seen_assessment_ids:
            failures.append(f"duplicate quality_assessment_id {assessment.quality_assessment_id!r}")
        seen_assessment_ids.add(assessment.quality_assessment_id)

        if not assessment.created_time:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} missing created_time")

        if not assessment.assessor_ref:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} missing assessor_ref")
        elif node_ids and assessment.assessor_ref not in node_ids and not _known_ref(assessment.assessor_ref, known_ids, known_paths):
            failures.append(
                f"quality assessment {assessment.quality_assessment_id!r} references unknown assessor_ref {assessment.assessor_ref!r}"
            )

        if assessment.confidence_level not in known_levels:
            failures.append(
                f"quality assessment {assessment.quality_assessment_id!r} uses unknown confidence_level {assessment.confidence_level!r}"
            )

        if not assessment.quality_flags:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} has no quality_flags")
        for flag in assessment.quality_flags:
            if flag not in known_flags:
                failures.append(
                    f"quality assessment {assessment.quality_assessment_id!r} uses unknown quality flag {flag!r}"
                )

        if not assessment.subject_refs:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} has no subject_refs")
        for ref in assessment.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"quality assessment {assessment.quality_assessment_id!r} references unknown subject_ref {ref!r}"
                )

        if not assessment.basis_refs:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} has no basis_refs")
        for ref in assessment.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"quality assessment {assessment.quality_assessment_id!r} references unknown basis_ref {ref!r}"
                )

        if not assessment.uncertainty_summary:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} missing uncertainty_summary")
        if not assessment.recommended_use:
            failures.append(f"quality assessment {assessment.quality_assessment_id!r} missing recommended_use")

    return QualityReport(
        source=str(root_path / "quality"),
        checked_policy_levels=len(policy.confidence_levels),
        checked_policy_flags=len(policy.quality_flags),
        checked_assessments=len(assessments),
        failures=failures,
    )


def format_quality_report(report: QualityReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM quality source: {report.source}")
    lines.append(f"Confidence levels checked: {report.checked_policy_levels}")
    lines.append(f"Quality flags checked: {report.checked_policy_flags}")
    lines.append(f"Quality assessments checked: {report.checked_assessments}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM quality validation failed.")
    else:
        lines.append("")
        lines.append("PFEM quality validation passed.")

    return "\n".join(lines)
