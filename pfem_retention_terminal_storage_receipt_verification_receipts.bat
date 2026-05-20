@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_terminal_storage_receipt_verification_receipts.py
exit /b %ERRORLEVEL%
