@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_terminal_disposition_ledger_records.py
exit /b %ERRORLEVEL%
