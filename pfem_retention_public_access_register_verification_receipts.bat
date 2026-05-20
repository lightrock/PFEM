@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_public_access_register_verification_receipts.py
exit /b %ERRORLEVEL%
