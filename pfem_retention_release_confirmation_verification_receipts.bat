@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_release_confirmation_verification_receipts.py
exit /b %ERRORLEVEL%
