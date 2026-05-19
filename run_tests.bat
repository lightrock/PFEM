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
echo Running PFEM retention decision record validation...
python tools\pfem_retention_decision_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention decision approval validation...
python tools\pfem_retention_decision_approvals.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention action receipt validation...
python tools\pfem_retention_action_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention action verification receipt validation...
python tools\pfem_retention_action_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention action closeout record validation...
python tools\pfem_retention_action_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention chain record validation...
python tools\pfem_retention_chain_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention chain verification receipt validation...
python tools\pfem_retention_chain_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention lifecycle record validation...
python tools\pfem_retention_lifecycle_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention lifecycle verification receipt validation...
python tools\pfem_retention_lifecycle_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention lifecycle closeout record validation...
python tools\pfem_retention_lifecycle_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention ledger record validation...
python tools\pfem_retention_ledger_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention ledger verification receipt validation...
python tools\pfem_retention_ledger_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention ledger closeout record validation...
python tools\pfem_retention_ledger_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention policy compliance record validation...
python tools\pfem_retention_policy_compliance_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention policy compliance verification receipt validation...
python tools\pfem_retention_policy_compliance_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention obligation record validation...
python tools\pfem_retention_obligation_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention obligation verification receipt validation...
python tools\pfem_retention_obligation_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention schedule record validation...
python tools\pfem_retention_schedule_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention schedule verification receipt validation...
python tools\pfem_retention_schedule_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention schedule closeout record validation...
python tools\pfem_retention_schedule_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention cycle record validation...
python tools\pfem_retention_cycle_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention cycle verification receipt validation...
python tools\pfem_retention_cycle_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention cycle closeout record validation...
python tools\pfem_retention_cycle_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention hold record validation...
python tools\pfem_retention_hold_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention hold verification receipt validation...
python tools\pfem_retention_hold_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention hold closeout record validation...
python tools\pfem_retention_hold_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention status snapshot record validation...
python tools\pfem_retention_status_snapshot_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention status snapshot verification receipt validation...
python tools\pfem_retention_status_snapshot_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention rollup record validation...
python tools\pfem_retention_rollup_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention rollup verification receipt validation...
python tools\pfem_retention_rollup_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention rollup closeout record validation...
python tools\pfem_retention_rollup_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention report record validation...
python tools\pfem_retention_report_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention report verification receipt validation...
python tools\pfem_retention_report_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention report closeout record validation...
python tools\pfem_retention_report_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention publication record validation...
python tools\pfem_retention_publication_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention publication verification receipt validation...
python tools\pfem_retention_publication_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention publication closeout record validation...
python tools\pfem_retention_publication_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention dashboard snapshot record validation...
python tools\pfem_retention_dashboard_snapshot_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention dashboard snapshot verification receipt validation...
python tools\pfem_retention_dashboard_snapshot_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention dashboard snapshot closeout record validation...
python tools\pfem_retention_dashboard_snapshot_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention summary record validation...
python tools\pfem_retention_summary_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention summary verification receipt validation...
python tools\pfem_retention_summary_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention summary closeout record validation...
python tools\pfem_retention_summary_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention export record validation...
python tools\pfem_retention_export_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention export verification receipt validation...
python tools\pfem_retention_export_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention export closeout record validation...
python tools\pfem_retention_export_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention handoff record validation...
python tools\pfem_retention_handoff_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention handoff verification receipt validation...
python tools\pfem_retention_handoff_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention handoff closeout record validation...
python tools\pfem_retention_handoff_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention acceptance record validation...
python tools\pfem_retention_acceptance_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention acceptance verification receipt validation...
python tools\pfem_retention_acceptance_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention acceptance closeout record validation...
python tools\pfem_retention_acceptance_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention package record validation...
python tools\pfem_retention_package_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention package verification receipt validation...
python tools\pfem_retention_package_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention package closeout record validation...
python tools\pfem_retention_package_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention finalization record validation...
python tools\pfem_retention_finalization_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention finalization verification receipt validation...
python tools\pfem_retention_finalization_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention finalization closeout record validation...
python tools\pfem_retention_finalization_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention terminal status record validation...
python tools\pfem_retention_terminal_status_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention terminal status verification receipt validation...
python tools\pfem_retention_terminal_status_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention terminal status closeout record validation...
python tools\pfem_retention_terminal_status_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention certificate record validation...
python tools\pfem_retention_certificate_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention certificate verification receipt validation...
python tools\pfem_retention_certificate_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention certificate closeout record validation...
python tools\pfem_retention_certificate_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention registry record validation...
python tools\pfem_retention_registry_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention registry verification receipt validation...
python tools\pfem_retention_registry_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention registry closeout record validation...
python tools\pfem_retention_registry_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention closure record validation...
python tools\pfem_retention_closure_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention closure verification receipt validation...
python tools\pfem_retention_closure_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention closure closeout record validation...
python tools\pfem_retention_closure_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention completion record validation...
python tools\pfem_retention_completion_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention completion verification receipt validation...
python tools\pfem_retention_completion_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention completion closeout record validation...
python tools\pfem_retention_completion_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention attestation record validation...
python tools\pfem_retention_attestation_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention attestation verification receipt validation...
python tools\pfem_retention_attestation_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention attestation closeout record validation...
python tools\pfem_retention_attestation_closeout_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention seal record validation...
python tools\pfem_retention_seal_records.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention seal verification receipt validation...
python tools\pfem_retention_seal_verification_receipts.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM retention seal closeout record validation...
python tools\pfem_retention_seal_closeout_records.py
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
