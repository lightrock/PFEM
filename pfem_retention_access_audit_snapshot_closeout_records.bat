@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_access_audit_snapshot_closeout_records.py
exit /b %ERRORLEVEL%
