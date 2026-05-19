"""PFEM repository doctor."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from pfem.adapter_runtime import load_adapter_manifest, validate_adapter_registry
from pfem.audit import validate_audit_repository
from pfem.capability_runtime import load_capability_manifest
from pfem.example_runtime import validate_example_registry
from pfem.handling import validate_handling_policy
from pfem.integrity import validate_integrity_manifest
from pfem.node_runtime import validate_node_registry
from pfem.policy import validate_policy_repository
from pfem.profile_runtime import load_node_profile, validate_profile_registry
from pfem.review import validate_review_repository
from pfem.schema_contracts import validate_schema_contracts
from pfem.source_runtime import validate_source_provenance_repository
from pfem.topology import validate_topology_repository


EXPECTED_PATHS = [
    "README.md", "AGENTS.md", "docs/AI_START_HERE.md",
    "docs/architecture/neutral-language.md", "docs/architecture/architecture-stack.md",
    "docs/architecture/capability-model.md", "docs/architecture/evidence-lifecycle.md",
    "docs/architecture/examples.md", "docs/architecture/example-registry.md",
    "docs/architecture/sharing-policy.md", "docs/architecture/record-schemas.md",
    "docs/architecture/node-identity.md", "docs/architecture/federation-topology.md",
    "docs/architecture/source-provenance.md", "docs/architecture/review-decisions.md",
    "docs/architecture/integrity-receipts.md", "docs/architecture/audit-journal.md",
    "docs/architecture/handling-redaction.md",
    "ai/architecture-rules.md", "ai/adapter-rules.md", "ai/evidence-rules.md",
    "ai/node-profile-rules.md", "ai/review-checklist.md",
    "contracts/adapter-contract.md", "contracts/evidence-contract.md",
    "contracts/node-profile-contract.md", "contracts/lifecycle-contract.md",
    "contracts/federation-contract.md", "contracts/node-identity-contract.md",
    "contracts/federation-topology-contract.md", "contracts/source-provenance-contract.md",
    "contracts/review-contract.md", "contracts/integrity-receipt-contract.md",
    "contracts/audit-journal-contract.md", "contracts/handling-redaction-contract.md",
    "schemas/adapter_manifest.schema.json", "schemas/adapter_registry.schema.json",
    "schemas/example_registry.schema.json", "schemas/node_manifest.schema.json",
    "schemas/node_registry.schema.json", "schemas/node_profile.schema.json",
    "schemas/profile_registry.schema.json", "schemas/source_registry.schema.json",
    "schemas/review_record.schema.json", "schemas/integrity_receipt_manifest.schema.json",
    "schemas/audit_event.schema.json", "schemas/handling_policy.schema.json",
    "schemas/raw_evidence.schema.json", "schemas/normalized_observation.schema.json",
    "schemas/finding.schema.json", "schemas/alert.schema.json",
    "schemas/evidence_package.schema.json", "schemas/rollup_summary.schema.json",
    "schemas/federation_message.schema.json", "schemas/federation_topology.schema.json",
    "schemas/sharing_policy.schema.json",
    "capabilities/README.md", "adapters/adapter-registry.json",
    "profiles/profile-registry.json", "nodes/README.md", "nodes/node-registry.json",
    "sources/README.md", "sources/source-registry.json",
    "review/README.md", "review/review-records.json",
    "audit/README.md", "audit/audit-journal.json",
    "handling/README.md", "handling/handling-policy.json",
    "integrity/README.md", "integrity/receipt-manifest.json",
    "topology/README.md", "topology/federation-topology.json",
    "examples/README.md", "examples/example-registry.json",
    "policy/README.md", "policy/sharing-policy.json", "src/pfem/__init__.py",
]

JSON_CHECK_DIRS = ["schemas", "tests/fixtures", "adapters", "profiles", "nodes", "sources", "review", "audit", "handling", "integrity", "topology", "examples", "policy"]
NEUTRAL_LANGUAGE_SCAN_DIRS = ["README.md", "docs", "ai", "contracts", "profiles", "nodes", "sources", "review", "audit", "handling", "integrity", "topology", "schemas", "adapters", "capabilities", "examples", "policy", ".github"]
DISCOURAGED_PUBLIC_TERMS = ["DARPA", "DOD", "DoD", "Department of Defense"]


@dataclass
class DoctorReport:
    root: Path
    checked_json_files: int = 0
    checked_adapter_manifests: int = 0
    checked_capability_manifests: int = 0
    checked_node_profiles: int = 0
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return current


def _iter_json_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for rel in JSON_CHECK_DIRS:
        base = root / rel
        if base.exists():
            files.extend(sorted(base.rglob("*.json")))
    return files


def _iter_public_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    extensions = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".bat"}
    for rel in NEUTRAL_LANGUAGE_SCAN_DIRS:
        path = root / rel
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(path)
        elif path.is_dir():
            files.extend(file for file in sorted(path.rglob("*")) if file.is_file() and file.suffix.lower() in extensions)
    return files


def check_expected_paths(root: Path, report: DoctorReport) -> None:
    for rel in EXPECTED_PATHS:
        if not (root / rel).exists():
            report.failures.append(f"missing expected path: {rel}")


def check_json_syntax(root: Path, report: DoctorReport) -> None:
    for path in _iter_json_files(root):
        report.checked_json_files += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            report.failures.append(f"invalid JSON: {path.relative_to(root)}: {exc}")


def check_adapter_manifests(root: Path, report: DoctorReport) -> None:
    adapters_dir = root / "adapters"
    if not adapters_dir.exists():
        return
    for path in sorted(adapters_dir.rglob("adapter.yaml")):
        report.checked_adapter_manifests += 1
        try:
            manifest = load_adapter_manifest(path)
        except Exception as exc:
            report.failures.append(f"adapter manifest failed to load: {path.relative_to(root)}: {exc}")
            continue
        if not manifest.adapter_id:
            report.failures.append(f"adapter manifest missing adapter_id: {path.relative_to(root)}")
        if not manifest.display_name:
            report.failures.append(f"adapter manifest missing display_name: {path.relative_to(root)}")


def collect_capability_ids(root: Path, report: DoctorReport) -> set[str]:
    capability_ids: set[str] = set()
    capabilities_dir = root / "capabilities"
    if not capabilities_dir.exists():
        return capability_ids
    for path in sorted(capabilities_dir.rglob("*.capability.yaml")):
        report.checked_capability_manifests += 1
        try:
            manifest = load_capability_manifest(path)
        except Exception as exc:
            report.failures.append(f"capability manifest failed to load: {path.relative_to(root)}: {exc}")
            continue
        if not manifest.capability_id:
            report.failures.append(f"capability manifest missing capability_id: {path.relative_to(root)}")
        if not manifest.display_name:
            report.failures.append(f"capability manifest missing display_name: {path.relative_to(root)}")
        if not manifest.capability_kind:
            report.failures.append(f"capability manifest missing capability_kind: {path.relative_to(root)}")
        if manifest.capability_id in capability_ids:
            report.failures.append(f"duplicate capability_id {manifest.capability_id!r}: {path.relative_to(root)}")
        capability_ids.add(manifest.capability_id)
    return capability_ids


def check_node_profiles(root: Path, report: DoctorReport, capability_ids: set[str]) -> None:
    profiles_dir = root / "profiles"
    if not profiles_dir.exists():
        return
    for path in sorted(profiles_dir.rglob("*.profile.yaml")):
        report.checked_node_profiles += 1
        try:
            profile = load_node_profile(path)
        except Exception as exc:
            report.failures.append(f"node profile failed to load: {path.relative_to(root)}: {exc}")
            continue
        if not profile.profile_id:
            report.failures.append(f"node profile missing profile_id: {path.relative_to(root)}")
        if not profile.profile_kind:
            report.failures.append(f"node profile missing profile_kind: {path.relative_to(root)}")
        for capability in [*profile.enabled_capabilities, *profile.disabled_capabilities]:
            if capability and capability not in capability_ids:
                report.warnings.append(f"profile references unknown capability {capability!r}: {path.relative_to(root)}")


def check_neutral_language(root: Path, report: DoctorReport) -> None:
    for path in _iter_public_text_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            report.warnings.append(f"could not scan text file: {path.relative_to(root)}: {exc}")
            continue
        for term in DISCOURAGED_PUBLIC_TERMS:
            if term in text:
                report.warnings.append(f"discouraged public term {term!r} in {path.relative_to(root)}")


def run_doctor(start: str | Path | None = None) -> DoctorReport:
    root = find_repo_root(start)
    report = DoctorReport(root=root)

    check_expected_paths(root, report)
    check_json_syntax(root, report)
    check_adapter_manifests(root, report)
    report.failures.extend(validate_adapter_registry(root))
    report.failures.extend(validate_profile_registry(root))
    report.failures.extend(validate_node_registry(root))
    report.failures.extend(validate_source_provenance_repository(root).failures)
    report.failures.extend(validate_example_registry(root))
    report.failures.extend(validate_policy_repository(root).failures)
    report.failures.extend(validate_handling_policy(root).failures)
    report.failures.extend(validate_review_repository(root).failures)
    report.failures.extend(validate_audit_repository(root).failures)
    report.failures.extend(validate_schema_contracts(root).failures)
    report.failures.extend(validate_topology_repository(root).failures)
    report.failures.extend(validate_integrity_manifest(root).failures)
    capability_ids = collect_capability_ids(root, report)
    check_node_profiles(root, report, capability_ids)
    check_neutral_language(root, report)
    return report


def format_report(report: DoctorReport) -> str:
    lines = [
        f"PFEM doctor root: {report.root}",
        f"JSON files checked: {report.checked_json_files}",
        f"Adapter manifests checked: {report.checked_adapter_manifests}",
        f"Capability manifests checked: {report.checked_capability_manifests}",
        f"Node profiles checked: {report.checked_node_profiles}",
    ]
    if report.warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in report.warnings:
            lines.append(f"  - {warning}")
    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM doctor failed.")
    else:
        lines.append("")
        lines.append("PFEM doctor passed.")
    return "\n".join(lines)
