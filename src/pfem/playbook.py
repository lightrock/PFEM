"""PFEM playbook validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.action import load_action_policy
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_PLAYBOOK_STATUSES = {"draft", "active", "deprecated", "retired"}


@dataclass(frozen=True)
class PlaybookStep:
    step_id: str
    title: str
    instruction: str
    expected_output: str


@dataclass(frozen=True)
class Playbook:
    playbook_id: str
    playbook_kind: str
    version: str
    status: str
    owner_ref: str
    applies_to_action_kinds: list[str]
    required_inputs: list[str]
    summary: str
    steps: list[PlaybookStep]
    stop_conditions: list[str]


@dataclass(frozen=True)
class PlaybookReport:
    source: str
    checked_playbooks: int = 0
    checked_steps: int = 0
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


def _load_steps(value: object) -> list[PlaybookStep]:
    if not isinstance(value, list):
        return []
    steps: list[PlaybookStep] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        steps.append(
            PlaybookStep(
                step_id=str(item.get("step_id", "")),
                title=str(item.get("title", "")),
                instruction=str(item.get("instruction", "")),
                expected_output=str(item.get("expected_output", "")),
            )
        )
    return steps


def load_playbook(path: str | Path) -> Playbook:
    record = _load_records(Path(path))[0]
    return Playbook(
        playbook_id=str(record.get("playbook_id", "")),
        playbook_kind=str(record.get("playbook_kind", "")),
        version=str(record.get("version", "")),
        status=str(record.get("status", "")),
        owner_ref=str(record.get("owner_ref", "")),
        applies_to_action_kinds=_as_list(record.get("applies_to_action_kinds", [])),
        required_inputs=_as_list(record.get("required_inputs", [])),
        summary=str(record.get("summary", "")),
        steps=_load_steps(record.get("steps", [])),
        stop_conditions=_as_list(record.get("stop_conditions", [])),
    )


def load_playbooks(root: str | Path) -> list[tuple[Path, Playbook]]:
    root_path = Path(root)
    items: list[tuple[Path, Playbook]] = []
    for path in sorted(root_path.glob("playbooks/**/*.playbook.json")):
        items.append((path, load_playbook(path)))
    return items


def collect_playbook_ids(root: str | Path) -> set[str]:
    return {playbook.playbook_id for _, playbook in load_playbooks(root) if playbook.playbook_id}


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "action", "playbooks", "integrity",
        "schemas", "contracts", "docs", "tests", "bundles",
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


def validate_playbook_repository(root: str | Path) -> PlaybookReport:
    root_path = Path(root)
    failures: list[str] = []
    items = load_playbooks(root_path)

    if not items:
        return PlaybookReport(
            source=str(root_path / "playbooks"),
            failures=["no playbooks found under playbooks/**/*.playbook.json"],
        )

    action_policy_path = root_path / "action" / "action-policy.json"
    known_action_kinds: set[str] = set()
    if action_policy_path.exists():
        policy = load_action_policy(action_policy_path)
        known_action_kinds = {kind.action_kind for kind in policy.action_kinds if kind.action_kind}

    node_ids = collect_node_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()
    step_count = 0

    for path, playbook in items:
        rel = path.relative_to(root_path)

        if not playbook.playbook_id:
            failures.append(f"playbook missing playbook_id: {rel}")
            continue
        if playbook.playbook_id in seen_ids:
            failures.append(f"duplicate playbook_id {playbook.playbook_id!r}: {rel}")
        seen_ids.add(playbook.playbook_id)

        if not playbook.playbook_kind:
            failures.append(f"playbook {playbook.playbook_id!r} missing playbook_kind")
        if not playbook.version:
            failures.append(f"playbook {playbook.playbook_id!r} missing version")
        if playbook.status not in KNOWN_PLAYBOOK_STATUSES:
            failures.append(f"playbook {playbook.playbook_id!r} uses unknown status {playbook.status!r}")
        if not playbook.owner_ref:
            failures.append(f"playbook {playbook.playbook_id!r} missing owner_ref")
        elif node_ids and playbook.owner_ref not in node_ids and playbook.owner_ref not in known_paths:
            failures.append(f"playbook {playbook.playbook_id!r} references unknown owner_ref {playbook.owner_ref!r}")

        if not playbook.applies_to_action_kinds:
            failures.append(f"playbook {playbook.playbook_id!r} has no applies_to_action_kinds")
        for action_kind in playbook.applies_to_action_kinds:
            if known_action_kinds and action_kind not in known_action_kinds:
                failures.append(
                    f"playbook {playbook.playbook_id!r} references unknown action_kind {action_kind!r}"
                )

        if not playbook.required_inputs:
            failures.append(f"playbook {playbook.playbook_id!r} has no required_inputs")
        if not playbook.summary:
            failures.append(f"playbook {playbook.playbook_id!r} missing summary")
        if not playbook.steps:
            failures.append(f"playbook {playbook.playbook_id!r} has no steps")

        seen_steps: set[str] = set()
        for step in playbook.steps:
            step_count += 1
            if not step.step_id:
                failures.append(f"playbook {playbook.playbook_id!r} has a step missing step_id")
                continue
            if step.step_id in seen_steps:
                failures.append(f"playbook {playbook.playbook_id!r} has duplicate step_id {step.step_id!r}")
            seen_steps.add(step.step_id)

            if not step.title:
                failures.append(f"playbook {playbook.playbook_id!r} step {step.step_id!r} missing title")
            if not step.instruction:
                failures.append(f"playbook {playbook.playbook_id!r} step {step.step_id!r} missing instruction")
            if not step.expected_output:
                failures.append(f"playbook {playbook.playbook_id!r} step {step.step_id!r} missing expected_output")

    return PlaybookReport(
        source=str(root_path / "playbooks"),
        checked_playbooks=len(items),
        checked_steps=step_count,
        failures=failures,
    )


def format_playbook_report(report: PlaybookReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM playbook source: {report.source}")
    lines.append(f"Playbooks checked: {report.checked_playbooks}")
    lines.append(f"Playbook steps checked: {report.checked_steps}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM playbook validation failed.")
    else:
        lines.append("")
        lines.append("PFEM playbook validation passed.")

    return "\n".join(lines)
