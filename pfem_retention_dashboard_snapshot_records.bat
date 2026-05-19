@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_dashboard_snapshot_records.py
exit /b %ERRORLEVEL%
