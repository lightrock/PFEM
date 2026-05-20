@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_release_access_verification_summary_records.py
exit /b %ERRORLEVEL%
