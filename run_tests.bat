@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

echo Running PFEM smoke check...
python tools\pfem_smoke.py
if errorlevel 1 exit /b 1

echo.
echo Running PFEM unit tests...
python -m unittest discover -s tests\unit -p "test_*.py"
if errorlevel 1 exit /b 1

echo.
echo PFEM tests passed.
