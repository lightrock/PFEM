"""PFEM integrity receipt helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_RECEIPT_PATH = Path("integrity") / "receipt-manifest.json"
DEFAULT_ALGORITHM = "sha256-canonical-json"


DEFAULT_RECEIPT_TARGETS = [
    ("adapters/adapter-registry.json", "adapter registry"),
    ("profiles/profile-registry.json", "profile registry"),
    ("nodes/node-registry.json", "node registry"),
    ("sources/source-registry.json", "source registry"),
    ("examples/example-registry.json", "example registry"),
    ("policy/sharing-policy.json", "sharing policy"),
    ("handling/handling-policy.json", "handling policy"),
    ("retention/retention-policy.json", "retention policy"),
    ("dispatch/dispatch-policy.json", "dispatch policy"),
    ("dispatch/dispatch-decisions.json", "dispatch decisions"),
    ("outbox/outbox-items.json", "outbox items"),
    ("inbox/inbox-items.json", "inbox items"),
    ("intake/intake-decisions.json", "intake decisions"),
    ("imports/import-records.json", "import records"),
    ("conflicts/conflict-records.json", "conflict records"),
    ("apply/apply-receipts.json", "apply receipts"),
    ("state/state-checkpoints.json", "state checkpoints"),
    ("state/state-transitions.json", "state transitions"),
    ("snapshots/snapshot-manifests.json", "snapshot manifests"),
    ("snapshots/snapshot-verification-receipts.json", "snapshot verification receipts"),
    ("recovery/recovery-points.json", "recovery points"),
    ("restore/restore-plans.json", "restore plans"),
    ("restore/restore-approvals.json", "restore approvals"),
    ("restore/restore-receipts.json", "restore receipts"),
    ("restore/restore-verification-receipts.json", "restore verification receipts"),
    ("restore/restore-closeout-records.json", "restore closeout records"),
    ("disposition/disposition-records.json", "disposition records"),
    ("disposition/disposition-receipts.json", "disposition receipts"),
    ("custody/custody-records.json", "custody records"),
    ("custody/custody-verification-receipts.json", "custody verification receipts"),
    ("custody/custody-transfer-records.json", "custody transfer records"),
    ("custody/custody-transfer-verification-receipts.json", "custody transfer verification receipts"),
    ("custody/custody-closeout-records.json", "custody closeout records"),
    ("custody/custody-chain-records.json", "custody chain records"),
    ("custody/custody-chain-verification-receipts.json", "custody chain verification receipts"),
    ("custody/custody-ledger-records.json", "custody ledger records"),
    ("custody/custody-ledger-verification-receipts.json", "custody ledger verification receipts"),
    ("custody/custody-release-requests.json", "custody release requests"),
    ("custody/custody-release-approvals.json", "custody release approvals"),
    ("custody/custody-release-receipts.json", "custody release receipts"),
    ("custody/custody-release-verification-receipts.json", "custody release verification receipts"),
    ("custody/custody-release-closeout-records.json", "custody release closeout records"),
    ("custody/custody-release-chain-records.json", "custody release chain records"),
    ("custody/custody-release-chain-verification-receipts.json", "custody release chain verification receipts"),
    ("custody/custody-lifecycle-records.json", "custody lifecycle records"),
    ("custody/custody-lifecycle-verification-receipts.json", "custody lifecycle verification receipts"),
    ("custody/custody-lifecycle-closeout-records.json", "custody lifecycle closeout records"),
    ("archive/archive-manifest-records.json", "archive manifest records"),
    ("archive/archive-receipts.json", "archive receipts"),
    ("archive/archive-verification-receipts.json", "archive verification receipts"),
    ("archive/archive-closeout-records.json", "archive closeout records"),
    ("archive/archive-chain-records.json", "archive chain records"),
    ("archive/archive-chain-verification-receipts.json", "archive chain verification receipts"),
    ("archive/archive-index-records.json", "archive index records"),
    ("archive/archive-index-verification-receipts.json", "archive index verification receipts"),
    ("archive/archive-index-closeout-records.json", "archive index closeout records"),
    ("archive/archive-lifecycle-records.json", "archive lifecycle records"),
    ("merge/merge-decisions.json", "merge decisions"),
    ("routing/routing-policy.json", "routing policy"),
    ("delivery/delivery-channel-registry.json", "delivery channel registry"),
    ("delivery/delivery-jobs.json", "delivery jobs"),
    ("transport/transport-adapter-registry.json", "transport adapter registry"),
    ("transport/transport-receipts.json", "transport receipts"),
    ("quality/quality-policy.json", "quality policy"),
    ("quality/quality-assessments.json", "quality assessments"),
    ("action/action-policy.json", "action policy"),
    ("action/action-records.json", "action records"),
    ("playbooks/examples/monitor-accepted-rollup.playbook.json", "accepted rollup monitoring playbook"),
    ("topology/federation-topology.json", "federation topology"),
    ("review/review-records.json", "review records"),
    ("audit/audit-journal.json", "audit journal"),
    ("exchange/exchange-receipts.json", "exchange receipts"),
    ("reconciliation/reconciliation-records.json", "reconciliation records"),
    ("bundles/examples/basic-rollup-exchange.bundle.json", "basic exchange bundle"),
    ("tests/fixtures/lifecycle/basic/raw_evidence.json", "basic lifecycle raw evidence"),
    ("tests/fixtures/lifecycle/basic/normalized_observation.json", "basic lifecycle normalized observation"),
    ("tests/fixtures/lifecycle/basic/finding.json", "basic lifecycle finding"),
    ("tests/fixtures/lifecycle/basic/alert.json", "basic lifecycle alert"),
    ("tests/fixtures/lifecycle/basic/evidence_package.json", "basic lifecycle evidence package"),
    ("tests/fixtures/rollup/basic/lifecycle/raw_evidence.json", "basic rollup raw evidence"),
    ("tests/fixtures/rollup/basic/lifecycle/normalized_observation.json", "basic rollup normalized observation"),
    ("tests/fixtures/rollup/basic/lifecycle/finding.json", "basic rollup finding"),
    ("tests/fixtures/rollup/basic/lifecycle/alert.json", "basic rollup alert"),
    ("tests/fixtures/rollup/basic/lifecycle/evidence_package.json", "basic rollup evidence package"),
    ("tests/fixtures/rollup/basic/rollup_summary.json", "basic rollup summary"),
    ("tests/fixtures/rollup/basic/federation_message.json", "basic federation message"),
]


@dataclass(frozen=True)
class IntegrityReceipt:
    path: str
    digest_algorithm: str
    digest: str
    purpose: str


@dataclass(frozen=True)
class IntegrityManifest:
    receipt_set_id: str
    version: str
    algorithm: str
    receipts: list[IntegrityReceipt]
    generated_by: str | None = None


@dataclass(frozen=True)
class IntegrityReport:
    source: str
    checked_receipts: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def canonical_json_bytes(path: Path) -> bytes:
    value: Any = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def compute_digest(path: str | Path, algorithm: str = DEFAULT_ALGORITHM) -> str:
    file_path = Path(path)

    if algorithm == "sha256-canonical-json":
        payload = canonical_json_bytes(file_path)
    elif algorithm == "sha256-bytes":
        payload = file_path.read_bytes()
    else:
        raise ValueError(f"unsupported digest algorithm: {algorithm}")

    return hashlib.sha256(payload).hexdigest()


def load_integrity_manifest(path: str | Path) -> IntegrityManifest:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    receipts = [
        IntegrityReceipt(
            path=str(item.get("path", "")),
            digest_algorithm=str(item.get("digest_algorithm", raw.get("algorithm", DEFAULT_ALGORITHM))),
            digest=str(item.get("digest", "")),
            purpose=str(item.get("purpose", "")),
        )
        for item in raw.get("receipts", [])
    ]
    return IntegrityManifest(
        receipt_set_id=str(raw.get("receipt_set_id", "")),
        version=str(raw.get("version", "")),
        algorithm=str(raw.get("algorithm", DEFAULT_ALGORITHM)),
        generated_by=str(raw["generated_by"]) if "generated_by" in raw else None,
        receipts=receipts,
    )


def build_integrity_manifest(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    receipts: list[dict[str, str]] = []

    for rel_path, purpose in DEFAULT_RECEIPT_TARGETS:
        target = root_path / rel_path
        if not target.exists():
            continue
        receipts.append(
            {
                "path": rel_path,
                "digest_algorithm": DEFAULT_ALGORITHM,
                "digest": compute_digest(target, DEFAULT_ALGORITHM),
                "purpose": purpose,
            }
        )

    return {
        "receipt_set_id": "pfem-integrity-receipts",
        "version": "0.1",
        "generated_by": "tools/pfem_integrity_update.py",
        "algorithm": DEFAULT_ALGORITHM,
        "receipts": receipts,
    }


def write_integrity_manifest(root: str | Path, manifest_path: str | Path = DEFAULT_RECEIPT_PATH) -> Path:
    root_path = Path(root)
    target = root_path / manifest_path
    target.parent.mkdir(parents=True, exist_ok=True)
    value = build_integrity_manifest(root_path)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return target


def validate_integrity_manifest(root: str | Path, manifest_path: str | Path = DEFAULT_RECEIPT_PATH) -> IntegrityReport:
    root_path = Path(root)
    source_path = root_path / manifest_path
    failures: list[str] = []

    if not source_path.exists():
        return IntegrityReport(source=str(source_path), failures=[f"missing integrity manifest: {manifest_path}"])

    manifest = load_integrity_manifest(source_path)
    if not manifest.receipt_set_id:
        failures.append("integrity manifest missing receipt_set_id")
    if not manifest.version:
        failures.append("integrity manifest missing version")
    if not manifest.algorithm:
        failures.append("integrity manifest missing algorithm")
    if not manifest.receipts:
        failures.append("integrity manifest has no receipts")

    seen_paths: set[str] = set()
    for receipt in manifest.receipts:
        if not receipt.path:
            failures.append("integrity receipt missing path")
            continue
        if receipt.path in seen_paths:
            failures.append(f"duplicate integrity receipt path: {receipt.path}")
        seen_paths.add(receipt.path)

        target = root_path / receipt.path
        if not target.exists():
            failures.append(f"integrity receipt target missing: {receipt.path}")
            continue

        if not receipt.digest:
            failures.append(f"integrity receipt missing digest: {receipt.path}")
            continue

        actual = compute_digest(target, receipt.digest_algorithm)
        if actual != receipt.digest:
            failures.append(f"integrity digest mismatch for {receipt.path}: expected={receipt.digest} actual={actual}")

    return IntegrityReport(source=str(source_path), checked_receipts=len(manifest.receipts), failures=failures)


def format_integrity_report(report: IntegrityReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM integrity source: {report.source}")
    lines.append(f"Receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM integrity validation failed.")
    else:
        lines.append("")
        lines.append("PFEM integrity validation passed.")

    return "\n".join(lines)
