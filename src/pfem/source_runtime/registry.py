"""Source registry and provenance validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.adapter_runtime import load_adapter_registry
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class SourceRegistryEntry:
    source_id: str
    display_name: str
    source_kind: str
    adapter_id: str
    node_id: str
    status: str


@dataclass(frozen=True)
class SourceRegistry:
    registry_id: str
    version: str
    sources: list[SourceRegistryEntry]


@dataclass(frozen=True)
class SourceProvenanceReport:
    source: str
    checked_sources: int = 0
    checked_evidence_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def load_source_registry(path: str | Path) -> SourceRegistry:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [
        SourceRegistryEntry(
            source_id=str(item.get("source_id", "")),
            display_name=str(item.get("display_name", "")),
            source_kind=str(item.get("source_kind", "")),
            adapter_id=str(item.get("adapter_id", "")),
            node_id=str(item.get("node_id", "")),
            status=str(item.get("status", "")),
        )
        for item in raw.get("sources", [])
    ]
    return SourceRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        sources=entries,
    )


def collect_source_ids(root: str | Path) -> set[str]:
    root_path = Path(root)
    registry_path = root_path / "sources" / "source-registry.json"
    if not registry_path.exists():
        return set()
    registry = load_source_registry(registry_path)
    return {entry.source_id for entry in registry.sources if entry.source_id}


def _collect_adapter_ids(root: Path) -> set[str]:
    registry_path = root / "adapters" / "adapter-registry.json"
    if not registry_path.exists():
        return set()
    registry = load_adapter_registry(registry_path)
    return {entry.adapter_id for entry in registry.adapters if entry.adapter_id}


def validate_source_registry(root: str | Path) -> list[str]:
    root_path = Path(root)
    registry_path = root_path / "sources" / "source-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        failures.append("missing source registry: sources/source-registry.json")
        return failures

    registry = load_source_registry(registry_path)
    adapter_ids = _collect_adapter_ids(root_path)
    node_ids = collect_node_ids(root_path)
    seen: set[str] = set()

    if not registry.registry_id:
        failures.append("source registry missing registry_id")
    if not registry.version:
        failures.append("source registry missing version")

    for entry in registry.sources:
        if not entry.source_id:
            failures.append("source registry entry missing source_id")
            continue
        if entry.source_id in seen:
            failures.append(f"duplicate source registry source_id: {entry.source_id}")
        seen.add(entry.source_id)

        if not entry.display_name:
            failures.append(f"source {entry.source_id!r} missing display_name")
        if not entry.source_kind:
            failures.append(f"source {entry.source_id!r} missing source_kind")
        if adapter_ids and entry.adapter_id not in adapter_ids:
            failures.append(f"source {entry.source_id!r} references unknown adapter_id {entry.adapter_id!r}")
        if node_ids and entry.node_id not in node_ids:
            failures.append(f"source {entry.source_id!r} references unknown node_id {entry.node_id!r}")

    return failures


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


def _iter_raw_evidence_records(root: Path) -> list[tuple[Path, JsonObject]]:
    candidates = [
        *root.glob("tests/fixtures/**/raw_evidence.json"),
        *root.glob("examples/**/raw_evidence.json"),
        *root.glob("adapters/**/samples/raw/*.json"),
    ]
    records: list[tuple[Path, JsonObject]] = []
    for path in sorted(set(candidates)):
        # Adapter raw samples may be source payloads, not PFEM raw evidence records.
        # Only validate files that look like PFEM raw evidence.
        for record in _load_records(path):
            if "evidence_id" in record and "source_id" in record:
                records.append((path, record))
    return records


def validate_source_provenance_repository(root: str | Path) -> SourceProvenanceReport:
    root_path = Path(root)
    registry_path = root_path / "sources" / "source-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        return SourceProvenanceReport(
            source=str(registry_path),
            failures=["missing source registry: sources/source-registry.json"],
        )

    registry = load_source_registry(registry_path)
    registry_failures = validate_source_registry(root_path)
    failures.extend(registry_failures)

    known_sources = {entry.source_id for entry in registry.sources if entry.source_id}
    known_adapters = _collect_adapter_ids(root_path)

    records = _iter_raw_evidence_records(root_path)
    for path, record in records:
        evidence_id = record.get("evidence_id", "<missing evidence_id>")
        source_id = record.get("source_id")
        if source_id not in known_sources:
            failures.append(
                f"raw evidence {evidence_id!r} references unknown source_id {source_id!r}: {path.relative_to(root_path)}"
            )

        provenance = record.get("provenance", {})
        adapter_id = provenance.get("adapter_id") if isinstance(provenance, dict) else None
        if adapter_id and known_adapters and adapter_id not in known_adapters:
            failures.append(
                f"raw evidence {evidence_id!r} references unknown provenance.adapter_id {adapter_id!r}: {path.relative_to(root_path)}"
            )
        if not adapter_id:
            failures.append(
                f"raw evidence {evidence_id!r} missing provenance.adapter_id: {path.relative_to(root_path)}"
            )

    return SourceProvenanceReport(
        source=str(registry_path),
        checked_sources=len(registry.sources),
        checked_evidence_records=len(records),
        failures=failures,
    )


def format_source_provenance_report(report: SourceProvenanceReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM source registry: {report.source}")
    lines.append(f"Sources checked: {report.checked_sources}")
    lines.append(f"Raw evidence records checked: {report.checked_evidence_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM source provenance validation failed.")
    else:
        lines.append("")
        lines.append("PFEM source provenance validation passed.")

    return "\n".join(lines)
