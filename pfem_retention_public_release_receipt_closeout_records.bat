@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_public_release_receipt_closeout_records.py
exit /b %ERRORLEVEL%
