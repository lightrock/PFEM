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
echo Running PFEM review validation...
python tools\pfem_review.py
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
