@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_custody_release_verification_receipts.py
exit /b %ERRORLEVEL%
