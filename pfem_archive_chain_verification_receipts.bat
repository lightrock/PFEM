@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_archive_chain_verification_receipts.py
exit /b %ERRORLEVEL%
