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
    ("archive/archive-lifecycle-verification-receipts.json", "archive lifecycle verification receipts"),
    ("archive/archive-lifecycle-closeout-records.json", "archive lifecycle closeout records"),
    ("preservation/preservation-records.json", "preservation records"),
    ("preservation/preservation-verification-receipts.json", "preservation verification receipts"),
    ("preservation/preservation-closeout-records.json", "preservation closeout records"),
    ("preservation/preservation-chain-records.json", "preservation chain records"),
    ("preservation/preservation-chain-verification-receipts.json", "preservation chain verification receipts"),
    ("retention/retention-review-records.json", "retention review records"),
    ("retention/retention-review-verification-receipts.json", "retention review verification receipts"),
    ("retention/retention-decision-records.json", "retention decision records"),
    ("retention/retention-decision-approvals.json", "retention decision approvals"),
    ("retention/retention-action-receipts.json", "retention action receipts"),
    ("retention/retention-action-verification-receipts.json", "retention action verification receipts"),
    ("retention/retention-action-closeout-records.json", "retention action closeout records"),
    ("retention/retention-chain-records.json", "retention chain records"),
    ("retention/retention-chain-verification-receipts.json", "retention chain verification receipts"),
    ("retention/retention-lifecycle-records.json", "retention lifecycle records"),
    ("retention/retention-lifecycle-verification-receipts.json", "retention lifecycle verification receipts"),
    ("retention/retention-lifecycle-closeout-records.json", "retention lifecycle closeout records"),
    ("retention/retention-ledger-records.json", "retention ledger records"),
    ("retention/retention-ledger-verification-receipts.json", "retention ledger verification receipts"),
    ("retention/retention-ledger-closeout-records.json", "retention ledger closeout records"),
    ("retention/retention-policy-compliance-records.json", "retention policy compliance records"),
    ("retention/retention-policy-compliance-verification-receipts.json", "retention policy compliance verification receipts"),
    ("retention/retention-obligation-records.json", "retention obligation records"),
    ("retention/retention-obligation-verification-receipts.json", "retention obligation verification receipts"),
    ("retention/retention-schedule-records.json", "retention schedule records"),
    ("retention/retention-schedule-verification-receipts.json", "retention schedule verification receipts"),
    ("retention/retention-schedule-closeout-records.json", "retention schedule closeout records"),
    ("retention/retention-cycle-records.json", "retention cycle records"),
    ("retention/retention-cycle-verification-receipts.json", "retention cycle verification receipts"),
    ("retention/retention-cycle-closeout-records.json", "retention cycle closeout records"),
    ("retention/retention-hold-records.json", "retention hold records"),
    ("retention/retention-hold-verification-receipts.json", "retention hold verification receipts"),
    ("retention/retention-hold-closeout-records.json", "retention hold closeout records"),
    ("retention/retention-status-snapshot-records.json", "retention status snapshot records"),
    ("retention/retention-status-snapshot-verification-receipts.json", "retention status snapshot verification receipts"),
    ("retention/retention-rollup-records.json", "retention rollup records"),
    ("retention/retention-rollup-verification-receipts.json", "retention rollup verification receipts"),
    ("retention/retention-rollup-closeout-records.json", "retention rollup closeout records"),
    ("retention/retention-report-records.json", "retention report records"),
    ("retention/retention-report-verification-receipts.json", "retention report verification receipts"),
    ("retention/retention-report-closeout-records.json", "retention report closeout records"),
    ("retention/retention-publication-records.json", "retention publication records"),
    ("retention/retention-publication-verification-receipts.json", "retention publication verification receipts"),
    ("retention/retention-publication-closeout-records.json", "retention publication closeout records"),
    ("retention/retention-dashboard-snapshot-records.json", "retention dashboard snapshot records"),
    ("retention/retention-dashboard-snapshot-verification-receipts.json", "retention dashboard snapshot verification receipts"),
    ("retention/retention-dashboard-snapshot-closeout-records.json", "retention dashboard snapshot closeout records"),
    ("retention/retention-summary-records.json", "retention summary records"),
    ("retention/retention-summary-verification-receipts.json", "retention summary verification receipts"),
    ("retention/retention-summary-closeout-records.json", "retention summary closeout records"),
    ("retention/retention-export-records.json", "retention export records"),
    ("retention/retention-export-verification-receipts.json", "retention export verification receipts"),
    ("retention/retention-export-closeout-records.json", "retention export closeout records"),
    ("retention/retention-handoff-records.json", "retention handoff records"),
    ("retention/retention-handoff-verification-receipts.json", "retention handoff verification receipts"),
    ("retention/retention-handoff-closeout-records.json", "retention handoff closeout records"),
    ("retention/retention-acceptance-records.json", "retention acceptance records"),
    ("retention/retention-acceptance-verification-receipts.json", "retention acceptance verification receipts"),
    ("retention/retention-acceptance-closeout-records.json", "retention acceptance closeout records"),
    ("retention/retention-package-records.json", "retention package records"),
    ("retention/retention-package-verification-receipts.json", "retention package verification receipts"),
    ("retention/retention-package-closeout-records.json", "retention package closeout records"),
    ("retention/retention-finalization-records.json", "retention finalization records"),
    ("retention/retention-finalization-verification-receipts.json", "retention finalization verification receipts"),
    ("retention/retention-finalization-closeout-records.json", "retention finalization closeout records"),
    ("retention/retention-terminal-status-records.json", "retention terminal status records"),
    ("retention/retention-terminal-status-verification-receipts.json", "retention terminal status verification receipts"),
    ("retention/retention-terminal-status-closeout-records.json", "retention terminal status closeout records"),
    ("retention/retention-certificate-records.json", "retention certificate records"),
    ("retention/retention-certificate-verification-receipts.json", "retention certificate verification receipts"),
    ("retention/retention-certificate-closeout-records.json", "retention certificate closeout records"),
    ("retention/retention-registry-records.json", "retention registry records"),
    ("retention/retention-registry-verification-receipts.json", "retention registry verification receipts"),
    ("retention/retention-registry-closeout-records.json", "retention registry closeout records"),
    ("retention/retention-closure-records.json", "retention closure records"),
    ("retention/retention-closure-verification-receipts.json", "retention closure verification receipts"),
    ("retention/retention-closure-closeout-records.json", "retention closure closeout records"),
    ("retention/retention-completion-records.json", "retention completion records"),
    ("retention/retention-completion-verification-receipts.json", "retention completion verification receipts"),
    ("retention/retention-completion-closeout-records.json", "retention completion closeout records"),
    ("retention/retention-attestation-records.json", "retention attestation records"),
    ("retention/retention-attestation-verification-receipts.json", "retention attestation verification receipts"),
    ("retention/retention-attestation-closeout-records.json", "retention attestation closeout records"),
    ("retention/retention-seal-records.json", "retention seal records"),
    ("retention/retention-seal-verification-receipts.json", "retention seal verification receipts"),
    ("retention/retention-seal-closeout-records.json", "retention seal closeout records"),
    ("retention/retention-notarization-records.json", "retention notarization records"),
    ("retention/retention-notarization-verification-receipts.json", "retention notarization verification receipts"),
    ("retention/retention-notarization-closeout-records.json", "retention notarization closeout records"),
    ("retention/retention-archive-anchor-records.json", "retention archive anchor records"),
    ("retention/retention-archive-anchor-verification-receipts.json", "retention archive anchor verification receipts"),
    ("retention/retention-archive-anchor-closeout-records.json", "retention archive anchor closeout records"),
    ("retention/retention-endcap-records.json", "retention endcap records"),
    ("retention/retention-endcap-verification-receipts.json", "retention endcap verification receipts"),
    ("retention/retention-endcap-closeout-records.json", "retention endcap closeout records"),
    ("retention/retention-final-index-records.json", "retention final index records"),
    ("retention/retention-final-index-verification-receipts.json", "retention final index verification receipts"),
    ("retention/retention-final-index-closeout-records.json", "retention final index closeout records"),
    ("retention/retention-master-ledger-records.json", "retention master ledger records"),
    ("retention/retention-master-ledger-verification-receipts.json", "retention master ledger verification receipts"),
    ("retention/retention-master-ledger-closeout-records.json", "retention master ledger closeout records"),
    ("retention/retention-terminal-manifest-records.json", "retention terminal manifest records"),
    ("retention/retention-terminal-manifest-verification-receipts.json", "retention terminal manifest verification receipts"),
    ("retention/retention-terminal-manifest-closeout-records.json", "retention terminal manifest closeout records"),
    ("retention/retention-repository-release-records.json", "retention repository release records"),
    ("retention/retention-repository-release-verification-receipts.json", "retention repository release verification receipts"),
    ("retention/retention-repository-release-closeout-records.json", "retention repository release closeout records"),
    ("retention/retention-deployment-release-records.json", "retention deployment release records"),
    ("retention/retention-deployment-release-verification-receipts.json", "retention deployment release verification receipts"),
    ("retention/retention-deployment-release-closeout-records.json", "retention deployment release closeout records"),
    ("retention/retention-availability-notice-records.json", "retention availability notice records"),
    ("retention/retention-availability-notice-verification-receipts.json", "retention availability notice verification receipts"),
    ("retention/retention-availability-notice-closeout-records.json", "retention availability notice closeout records"),
    ("retention/retention-release-acknowledgement-records.json", "retention release acknowledgement records"),
    ("retention/retention-release-acknowledgement-verification-receipts.json", "retention release acknowledgement verification receipts"),
    ("retention/retention-release-acknowledgement-closeout-records.json", "retention release acknowledgement closeout records"),
    ("retention/retention-release-confirmation-records.json", "retention release confirmation records"),
    ("retention/retention-release-confirmation-verification-receipts.json", "retention release confirmation verification receipts"),
    ("retention/retention-release-confirmation-closeout-records.json", "retention release confirmation closeout records"),
    ("retention/retention-distribution-package-records.json", "retention distribution package records"),
    ("retention/retention-distribution-package-verification-receipts.json", "retention distribution package verification receipts"),
    ("retention/retention-distribution-package-closeout-records.json", "retention distribution package closeout records"),
    ("retention/retention-distribution-manifest-records.json", "retention distribution manifest records"),
    ("retention/retention-distribution-manifest-verification-receipts.json", "retention distribution manifest verification receipts"),
    ("retention/retention-distribution-manifest-closeout-records.json", "retention distribution manifest closeout records"),
    ("retention/retention-access-publication-records.json", "retention access publication records"),
    ("retention/retention-access-publication-verification-receipts.json", "retention access publication verification receipts"),
    ("retention/retention-access-publication-closeout-records.json", "retention access publication closeout records"),
    ("retention/retention-access-grant-records.json", "retention access grant records"),
    ("retention/retention-access-grant-verification-receipts.json", "retention access grant verification receipts"),
    ("retention/retention-access-grant-closeout-records.json", "retention access grant closeout records"),
    ("retention/retention-access-ledger-records.json", "retention access ledger records"),
    ("retention/retention-access-ledger-verification-receipts.json", "retention access ledger verification receipts"),
    ("retention/retention-access-ledger-closeout-records.json", "retention access ledger closeout records"),
    ("retention/retention-retrieval-catalog-records.json", "retention retrieval catalog records"),
    ("retention/retention-retrieval-catalog-verification-receipts.json", "retention retrieval catalog verification receipts"),
    ("retention/retention-retrieval-catalog-closeout-records.json", "retention retrieval catalog closeout records"),
    ("retention/retention-retrieval-endpoint-records.json", "retention retrieval endpoint records"),
    ("retention/retention-retrieval-endpoint-verification-receipts.json", "retention retrieval endpoint verification receipts"),
    ("retention/retention-retrieval-endpoint-closeout-records.json", "retention retrieval endpoint closeout records"),
    ("retention/retention-retrieval-token-records.json", "retention retrieval token records"),
    ("retention/retention-retrieval-token-verification-receipts.json", "retention retrieval token verification receipts"),
    ("retention/retention-retrieval-token-closeout-records.json", "retention retrieval token closeout records"),
    ("retention/retention-consumer-receipt-records.json", "retention consumer receipt records"),
    ("retention/retention-consumer-receipt-verification-receipts.json", "retention consumer receipt verification receipts"),
    ("retention/retention-consumer-receipt-closeout-records.json", "retention consumer receipt closeout records"),
    ("retention/retention-publication-rollup-records.json", "retention publication rollup records"),
    ("retention/retention-publication-rollup-verification-receipts.json", "retention publication rollup verification receipts"),
    ("retention/retention-publication-rollup-closeout-records.json", "retention publication rollup closeout records"),
    ("retention/retention-distribution-receipt-records.json", "retention distribution receipt records"),
    ("retention/retention-distribution-receipt-verification-receipts.json", "retention distribution receipt verification receipts"),
    ("retention/retention-distribution-receipt-closeout-records.json", "retention distribution receipt closeout records"),
    ("retention/retention-access-audit-snapshot-records.json", "retention access audit snapshot records"),
    ("retention/retention-access-audit-snapshot-verification-receipts.json", "retention access audit snapshot verification receipts"),
    ("retention/retention-access-audit-snapshot-closeout-records.json", "retention access audit snapshot closeout records"),
    ("retention/retention-release-health-snapshot-records.json", "retention release health snapshot records"),
    ("retention/retention-release-health-snapshot-verification-receipts.json", "retention release health snapshot verification receipts"),
    ("retention/retention-release-health-snapshot-closeout-records.json", "retention release health snapshot closeout records"),
    ("retention/retention-release-usage-summary-records.json", "retention release usage summary records"),
    ("retention/retention-release-usage-summary-verification-receipts.json", "retention release usage summary verification receipts"),
    ("retention/retention-release-usage-summary-closeout-records.json", "retention release usage summary closeout records"),
    ("retention/retention-retention-exposure-report-records.json", "retention retention exposure report records"),
    ("retention/retention-retention-exposure-report-verification-receipts.json", "retention retention exposure report verification receipts"),
    ("retention/retention-retention-exposure-report-closeout-records.json", "retention retention exposure report closeout records"),
    ("retention/retention-release-closeout-summary-records.json", "retention release closeout summary records"),
    ("retention/retention-release-closeout-summary-verification-receipts.json", "retention release closeout summary verification receipts"),
    ("retention/retention-release-closeout-summary-closeout-records.json", "retention release closeout summary closeout records"),
    ("retention/retention-public-record-index-records.json", "retention public record index records"),
    ("retention/retention-public-record-index-verification-receipts.json", "retention public record index verification receipts"),
    ("retention/retention-public-record-index-closeout-records.json", "retention public record index closeout records"),
    ("retention/retention-final-release-bundle-records.json", "retention final release bundle records"),
    ("retention/retention-final-release-bundle-verification-receipts.json", "retention final release bundle verification receipts"),
    ("retention/retention-final-release-bundle-closeout-records.json", "retention final release bundle closeout records"),
    ("retention/retention-terminal-access-notice-records.json", "retention terminal access notice records"),
    ("retention/retention-terminal-access-notice-verification-receipts.json", "retention terminal access notice verification receipts"),
    ("retention/retention-terminal-access-notice-closeout-records.json", "retention terminal access notice closeout records"),
    ("retention/retention-release-acceptance-records.json", "retention release acceptance records"),
    ("retention/retention-release-acceptance-verification-receipts.json", "retention release acceptance verification receipts"),
    ("retention/retention-release-acceptance-closeout-records.json", "retention release acceptance closeout records"),
    ("retention/retention-access-completion-records.json", "retention access completion records"),
    ("retention/retention-access-completion-verification-receipts.json", "retention access completion verification receipts"),
    ("retention/retention-access-completion-closeout-records.json", "retention access completion closeout records"),
    ("retention/retention-publication-certificate-records.json", "retention publication certificate records"),
    ("retention/retention-publication-certificate-verification-receipts.json", "retention publication certificate verification receipts"),
    ("retention/retention-publication-certificate-closeout-records.json", "retention publication certificate closeout records"),
    ("retention/retention-distribution-closure-notice-records.json", "retention distribution closure notice records"),
    ("retention/retention-distribution-closure-notice-verification-receipts.json", "retention distribution closure notice verification receipts"),
    ("retention/retention-distribution-closure-notice-closeout-records.json", "retention distribution closure notice closeout records"),
    ("retention/retention-public-access-register-records.json", "retention public access register records"),
    ("retention/retention-public-access-register-verification-receipts.json", "retention public access register verification receipts"),
    ("retention/retention-public-access-register-closeout-records.json", "retention public access register closeout records"),
    ("retention/retention-release-access-index-records.json", "retention release access index records"),
    ("retention/retention-release-access-index-verification-receipts.json", "retention release access index verification receipts"),
    ("retention/retention-release-access-index-closeout-records.json", "retention release access index closeout records"),
    ("retention/retention-release-access-verification-summary-records.json", "retention release access verification summary records"),
    ("retention/retention-release-access-verification-summary-verification-receipts.json", "retention release access verification summary verification receipts"),
    ("retention/retention-release-access-verification-summary-closeout-records.json", "retention release access verification summary closeout records"),
    ("retention/retention-release-access-closeout-summary-records.json", "retention release access closeout summary records"),
    ("retention/retention-release-access-closeout-summary-verification-receipts.json", "retention release access closeout summary verification receipts"),
    ("retention/retention-release-access-closeout-summary-closeout-records.json", "retention release access closeout summary closeout records"),
    ("retention/retention-archive-availability-rollup-records.json", "retention archive availability rollup records"),
    ("retention/retention-archive-availability-rollup-verification-receipts.json", "retention archive availability rollup verification receipts"),
    ("retention/retention-archive-availability-rollup-closeout-records.json", "retention archive availability rollup closeout records"),
    ("retention/retention-retrieval-readiness-snapshot-records.json", "retention retrieval readiness snapshot records"),
    ("retention/retention-retrieval-readiness-snapshot-verification-receipts.json", "retention retrieval readiness snapshot verification receipts"),
    ("retention/retention-retrieval-readiness-snapshot-closeout-records.json", "retention retrieval readiness snapshot closeout records"),
    ("retention/retention-consumer-availability-notice-records.json", "retention consumer availability notice records"),
    ("retention/retention-consumer-availability-notice-verification-receipts.json", "retention consumer availability notice verification receipts"),
    ("retention/retention-consumer-availability-notice-closeout-records.json", "retention consumer availability notice closeout records"),
    ("retention/retention-public-release-receipt-records.json", "retention public release receipt records"),
    ("retention/retention-public-release-receipt-verification-receipts.json", "retention public release receipt verification receipts"),
    ("retention/retention-public-release-receipt-closeout-records.json", "retention public release receipt closeout records"),
    ("retention/retention-release-exception-register-records.json", "retention release exception register records"),
    ("retention/retention-release-exception-register-verification-receipts.json", "retention release exception register verification receipts"),
    ("retention/retention-release-exception-register-closeout-records.json", "retention release exception register closeout records"),
    ("retention/retention-release-exception-summary-records.json", "retention release exception summary records"),
    ("retention/retention-release-exception-summary-verification-receipts.json", "retention release exception summary verification receipts"),
    ("retention/retention-release-exception-summary-closeout-records.json", "retention release exception summary closeout records"),
    ("retention/retention-release-metrics-snapshot-records.json", "retention release metrics snapshot records"),
    ("retention/retention-release-metrics-snapshot-verification-receipts.json", "retention release metrics snapshot verification receipts"),
    ("retention/retention-release-metrics-snapshot-closeout-records.json", "retention release metrics snapshot closeout records"),
    ("retention/retention-release-terminal-report-records.json", "retention release terminal report records"),
    ("retention/retention-release-terminal-report-verification-receipts.json", "retention release terminal report verification receipts"),
    ("retention/retention-release-terminal-report-closeout-records.json", "retention release terminal report closeout records"),
    ("retention/retention-final-publication-notice-records.json", "retention final publication notice records"),
    ("retention/retention-final-publication-notice-verification-receipts.json", "retention final publication notice verification receipts"),
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
