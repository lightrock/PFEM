"""Audit PFEM contributor command protocol wiring."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REQUIRED_FILES = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/AI_START_HERE.md"),
    Path("docs/developer/pfem-contributor-command-protocol.md"),
    Path("docs/developer/pfem-new-tab-prompt.md"),
    Path("tools/pfem_check_manifest.json"),
]

OPTIONAL_FIRST_READ_FILES = [
    Path("docs/architecture/README.md"),
    Path("docs/developer/pfem-new-chat-handoff.md"),
    Path("docs/developer/pfem-ai-patch-safety-rules.md"),
    Path("docs/developer/pfem-boundary-language-generation-standard.md"),
    Path("docs/developer/pfem-boundary-generation-standard.md"),
    Path("docs/developer/pfem-architecture-theory-notes.md"),
    Path("docs/developer/pfem-adapters-and-subsystems.md"),
    Path("docs/developer/pfem-terminal-tail-stabilization.md"),
]

PROMPT_REQUIRED_PHRASES = [
    "lightrock/PFEM",
    "current repo state beats chat memory",
    "AGENTS.md",
    "docs/AI_START_HERE.md",
    "tools/pfem_check_manifest.json",
    "PFEM boundary",
    "Adapter",
    "Subsystem",
    "Mesh",
    "build/pfem-patch-status",
    "Do not generate more PFEM boundaries unless",
    "Do not invent fake refs",
    "start a new tab",
]

PROTOCOL_REQUIRED_PHRASES = [
    "When any developer says",
    "start a new tab",
    "do not continue implementation work",
    "copy/paste-ready handoff prompt",
    "Do not expose private chain-of-thought",
]

KEY_FILES_FOR_ANY_DEVELOPER_LANGUAGE = [
    Path("AGENTS.md"),
    Path("docs/AI_START_HERE.md"),
    Path("docs/developer/pfem-contributor-command-protocol.md"),
    Path("docs/developer/pfem-new-tab-prompt.md"),
]

@dataclass(frozen=True)
class ContributorCommandProtocolAuditReport:
    root: str
    required_files_checked: int = 0
    optional_first_read_files_found: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _missing_phrases(text: str, phrases: Iterable[str]) -> list[str]:
    lower = text.lower()
    return [phrase for phrase in phrases if phrase.lower() not in lower]


def audit_contributor_command_protocol(root: str | Path) -> ContributorCommandProtocolAuditReport:
    root_path = Path(root)
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root_path / rel).exists():
            failures.append(f"missing required contributor-command file: {rel}")

    optional_found = sum(1 for rel in OPTIONAL_FIRST_READ_FILES if (root_path / rel).exists())

    protocol_path = root_path / "docs" / "developer" / "pfem-contributor-command-protocol.md"
    if protocol_path.exists():
        text = _read(protocol_path)
        for phrase in _missing_phrases(text, PROTOCOL_REQUIRED_PHRASES):
            failures.append(f"{protocol_path.relative_to(root_path)} missing phrase: {phrase!r}")

    prompt_path = root_path / "docs" / "developer" / "pfem-new-tab-prompt.md"
    if prompt_path.exists():
        text = _read(prompt_path)
        for phrase in _missing_phrases(text, PROMPT_REQUIRED_PHRASES):
            failures.append(f"{prompt_path.relative_to(root_path)} missing phrase: {phrase!r}")

    for rel in KEY_FILES_FOR_ANY_DEVELOPER_LANGUAGE:
        path = root_path / rel
        if not path.exists():
            continue
        text = _read(path)
        if "When Allen says" in text or "Allen says" in text:
            failures.append(f"{rel} uses person-specific command language; use 'When any developer says'")

    manifest_path = root_path / "tools" / "pfem_check_manifest.json"
    if manifest_path.exists() and "pfem_contributor_command_protocol_audit.py" not in _read(manifest_path):
        failures.append("tools/pfem_check_manifest.json does not register the contributor command protocol audit")

    return ContributorCommandProtocolAuditReport(
        root=str(root_path),
        required_files_checked=len(REQUIRED_FILES),
        optional_first_read_files_found=optional_found,
        failures=failures,
    )


def format_contributor_command_protocol_audit_report(report: ContributorCommandProtocolAuditReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM contributor command protocol audit root: {report.root}")
    lines.append(f"Required files checked: {report.required_files_checked}")
    lines.append(f"Optional first-read files found: {report.optional_first_read_files_found}")
    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM contributor command protocol audit failed.")
    else:
        lines.append("")
        lines.append("PFEM contributor command protocol audit passed.")
    return "\n".join(lines)
