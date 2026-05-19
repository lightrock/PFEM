@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_restore_receipts.py
exit /b %ERRORLEVEL%
