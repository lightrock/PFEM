@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

echo Running PFEM catalog...
python tools\pfem_catalog.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM source provenance validation...
python tools\pfem_sources.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM topology validation...
python tools\pfem_topology.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM dispatch validation...
python tools\pfem_dispatch.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM dispatch decision validation...
python tools\pfem_dispatch_decisions.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM outbox validation...
python tools\pfem_outbox.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM inbox validation...
python tools\pfem_inbox.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM intake decision validation...
python tools\pfem_intake_decisions.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM import record validation...
python tools\pfem_import_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM merge decision validation...
python tools\pfem_merge_decisions.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM conflict record validation...
python tools\pfem_conflict_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM apply receipt validation...
python tools\pfem_apply_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM state checkpoint validation...
python tools\pfem_state_checkpoints.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM state transition validation...
python tools\pfem_state_transitions.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM snapshot manifest validation...
python tools\pfem_snapshot_manifests.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM snapshot verification receipt validation...
python tools\pfem_snapshot_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM recovery point validation...
python tools\pfem_recovery_points.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM restore plan validation...
python tools\pfem_restore_plans.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM restore approval validation...
python tools\pfem_restore_approvals.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM restore receipt validation...
python tools\pfem_restore_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM restore verification receipt validation...
python tools\pfem_restore_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM restore closeout record validation...
python tools\pfem_restore_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM disposition record validation...
python tools\pfem_disposition_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM disposition receipt validation...
python tools\pfem_disposition_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody record validation...
python tools\pfem_custody_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody verification receipt validation...
python tools\pfem_custody_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody transfer record validation...
python tools\pfem_custody_transfer_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody transfer verification receipt validation...
python tools\pfem_custody_transfer_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody closeout record validation...
python tools\pfem_custody_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody chain record validation...
python tools\pfem_custody_chain_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody chain verification receipt validation...
python tools\pfem_custody_chain_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody ledger record validation...
python tools\pfem_custody_ledger_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody ledger verification receipt validation...
python tools\pfem_custody_ledger_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release request validation...
python tools\pfem_custody_release_requests.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release approval validation...
python tools\pfem_custody_release_approvals.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release receipt validation...
python tools\pfem_custody_release_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release verification receipt validation...
python tools\pfem_custody_release_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release closeout record validation...
python tools\pfem_custody_release_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release chain record validation...
python tools\pfem_custody_release_chain_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody release chain verification receipt validation...
python tools\pfem_custody_release_chain_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody lifecycle record validation...
python tools\pfem_custody_lifecycle_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody lifecycle verification receipt validation...
python tools\pfem_custody_lifecycle_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM custody lifecycle closeout record validation...
python tools\pfem_custody_lifecycle_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive manifest record validation...
python tools\pfem_archive_manifest_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive receipt validation...
python tools\pfem_archive_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive verification receipt validation...
python tools\pfem_archive_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive closeout record validation...
python tools\pfem_archive_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive chain record validation...
python tools\pfem_archive_chain_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive chain verification receipt validation...
python tools\pfem_archive_chain_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive index record validation...
python tools\pfem_archive_index_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive index verification receipt validation...
python tools\pfem_archive_index_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive index closeout record validation...
python tools\pfem_archive_index_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive lifecycle record validation...
python tools\pfem_archive_lifecycle_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive lifecycle verification receipt validation...
python tools\pfem_archive_lifecycle_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM archive lifecycle closeout record validation...
python tools\pfem_archive_lifecycle_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM preservation record validation...
python tools\pfem_preservation_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM preservation verification receipt validation...
python tools\pfem_preservation_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM preservation closeout record validation...
python tools\pfem_preservation_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM preservation chain record validation...
python tools\pfem_preservation_chain_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM preservation chain verification receipt validation...
python tools\pfem_preservation_chain_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention review record validation...
python tools\pfem_retention_review_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention review verification receipt validation...
python tools\pfem_retention_review_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM delivery validation...
python tools\pfem_delivery.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM delivery job validation...
python tools\pfem_delivery_jobs.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM transport validation...
python tools\pfem_transport.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM transport receipt validation...
python tools\pfem_transport_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM routing validation...
python tools\pfem_routing.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM handling validation...
python tools\pfem_handling.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention validation...
python tools\pfem_retention.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM quality validation...
python tools\pfem_quality.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM action validation...
python tools\pfem_actions.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM playbook validation...
python tools\pfem_playbooks.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM review validation...
python tools\pfem_review.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM audit validation...
python tools\pfem_audit.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM bundle validation...
python tools\pfem_bundles.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM exchange validation...
python tools\pfem_exchange.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM reconciliation validation...
python tools\pfem_reconciliation.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM schema contract validation...
python tools\pfem_schema_contracts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM policy validation...
python tools\pfem_policy.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM lineage validation...
python tools\pfem_lineage.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM rollup validation...
python tools\pfem_rollup.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM integrity validation...
python tools\pfem_integrity.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM doctor...
python tools\pfem_doctor.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM smoke check...
python tools\pfem_smoke.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM unit tests...
python -m unittest discover -s tests\unit -p "test_*.py"
if errorlevel 1 exit /b 1

echo.
echo PFEM tests passed.
