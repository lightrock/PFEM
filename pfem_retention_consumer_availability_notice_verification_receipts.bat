@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_consumer_availability_notice_verification_receipts.py
exit /b %ERRORLEVEL%
