"""PFEM repository doctor."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from pfem.action import validate_action_repository
from pfem.adapter_runtime import load_adapter_manifest, validate_adapter_registry
from pfem.audit import validate_audit_repository
from pfem.bundle import validate_bundle_repository
from pfem.conflict_record import validate_conflict_records
from pfem.capability_runtime import load_capability_manifest
from pfem.delivery import validate_delivery_channel_registry
from pfem.delivery_job import validate_delivery_jobs
from pfem.dispatch import validate_dispatch_policy
from pfem.dispatch_decision import validate_dispatch_decisions
from pfem.example_runtime import validate_example_registry
from pfem.exchange import validate_exchange_repository
from pfem.handling import validate_handling_policy
from pfem.inbox import validate_inbox_items
from pfem.import_record import validate_import_records
from pfem.merge_decision import validate_merge_decisions
from pfem.intake_decision import validate_intake_decisions
from pfem.integrity import validate_integrity_manifest
from pfem.node_runtime import validate_node_registry
from pfem.outbox import validate_outbox_items
from pfem.playbook import validate_playbook_repository
from pfem.policy import validate_policy_repository
from pfem.profile_runtime import load_node_profile, validate_profile_registry
from pfem.quality import validate_quality_repository
from pfem.reconciliation import validate_reconciliation_repository
from pfem.retention import validate_retention_policy
from pfem.review import validate_review_repository
from pfem.routing import validate_routing_policy
from pfem.schema_contracts import validate_schema_contracts
from pfem.source_runtime import validate_source_provenance_repository
from pfem.topology import validate_topology_repository
from pfem.transport import validate_transport_adapter_registry
from pfem.transport_receipt import validate_transport_receipts


EXPECTED_PATHS = [
    "README.md", "AGENTS.md", "docs/AI_START_HERE.md",
    "docs/architecture/dispatch-policy.md",
    "docs/architecture/dispatch-decisions.md",
    "docs/architecture/outbox-items.md",
    "docs/architecture/inbox-items.md",
    "docs/architecture/intake-decisions.md",
    "docs/architecture/import-records.md",
    "docs/architecture/conflict-records.md",
    "docs/architecture/merge-decisions.md",
    "docs/architecture/exchange-receipt-intake-linkage.md",
    "docs/architecture/routing-policy.md", "docs/architecture/delivery-channels.md",
    "docs/architecture/delivery-jobs.md",
    "docs/architecture/transport-adapters.md", "docs/architecture/transport-receipts.md",
    "contracts/dispatch-policy-contract.md",
    "contracts/dispatch-decision-contract.md",
    "contracts/outbox-item-contract.md",
    "contracts/inbox-item-contract.md",
    "contracts/intake-decision-contract.md",
    "contracts/import-record-contract.md",
    "contracts/conflict-record-contract.md",
    "contracts/merge-decision-contract.md",
    "contracts/exchange-receipt-intake-linkage-contract.md",
    "contracts/routing-contract.md", "contracts/delivery-channel-contract.md",
    "contracts/delivery-job-contract.md",
    "contracts/transport-adapter-contract.md", "contracts/transport-receipt-contract.md",
    "schemas/dispatch_policy.schema.json",
    "schemas/dispatch_decision.schema.json",
    "schemas/outbox_item.schema.json",
    "schemas/inbox_item.schema.json",
    "schemas/intake_decision.schema.json",
    "schemas/import_record.schema.json",
    "schemas/conflict_record.schema.json",
    "schemas/merge_decision.schema.json",
    "schemas/delivery_channel_registry.schema.json",
    "schemas/delivery_job.schema.json",
    "schemas/transport_adapter_registry.schema.json",
    "schemas/transport_receipt.schema.json",
    "dispatch/README.md", "dispatch/dispatch-policy.json",
    "dispatch/dispatch-decisions.json",
    "outbox/README.md", "outbox/outbox-items.json",
    "inbox/README.md", "inbox/inbox-items.json",
    "intake/README.md", "intake/intake-decisions.json",
    "imports/README.md", "imports/import-records.json",
    "conflicts/README.md", "conflicts/conflict-records.json",
    "merge/README.md", "merge/merge-decisions.json",
    "delivery/README.md", "delivery/delivery-channel-registry.json",
    "delivery/delivery-jobs.json",
    "transport/README.md", "transport/transport-adapter-registry.json",
    "transport/transport-receipts.json",
    "routing/README.md", "routing/routing-policy.json",
    "src/pfem/__init__.py",
]

JSON_CHECK_DIRS = ["schemas", "tests/fixtures", "adapters", "profiles", "nodes", "sources", "review", "audit", "exchange", "reconciliation", "quality", "action", "playbooks", "dispatch", "routing", "delivery", "outbox", "inbox", "intake", "imports", "conflicts", "merge", "transport", "handling", "retention", "bundles", "integrity", "topology", "examples", "policy"]
NEUTRAL_LANGUAGE_SCAN_DIRS = ["README.md", "docs", "ai", "contracts", "profiles", "nodes", "sources", "review", "audit", "exchange", "reconciliation", "quality", "action", "playbooks", "dispatch", "routing", "delivery", "outbox", "inbox", "transport", "handling", "retention", "bundles", "integrity", "topology", "schemas", "adapters", "capabilities", "examples", "policy", ".github"]
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
    report.failures.extend(validate_retention_policy(root).failures)
    report.failures.extend(validate_dispatch_policy(root).failures)
    report.failures.extend(validate_dispatch_decisions(root).failures)
    report.failures.extend(validate_outbox_items(root).failures)
    report.failures.extend(validate_inbox_items(root).failures)
    report.failures.extend(validate_import_records(root).failures)
    report.failures.extend(validate_conflict_records(root).failures)
    report.failures.extend(validate_merge_decisions(root).failures)
    report.failures.extend(validate_intake_decisions(root).failures)
    report.failures.extend(validate_delivery_channel_registry(root).failures)
    report.failures.extend(validate_delivery_jobs(root).failures)
    report.failures.extend(validate_transport_adapter_registry(root).failures)
    report.failures.extend(validate_transport_receipts(root).failures)
    report.failures.extend(validate_routing_policy(root).failures)
    report.failures.extend(validate_quality_repository(root).failures)
    report.failures.extend(validate_action_repository(root).failures)
    report.failures.extend(validate_playbook_repository(root).failures)
    report.failures.extend(validate_review_repository(root).failures)
    report.failures.extend(validate_audit_repository(root).failures)
    report.failures.extend(validate_bundle_repository(root).failures)
    report.failures.extend(validate_exchange_repository(root).failures)
    report.failures.extend(validate_reconciliation_repository(root).failures)
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
