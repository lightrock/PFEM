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
