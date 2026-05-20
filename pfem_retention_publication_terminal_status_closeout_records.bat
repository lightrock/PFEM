@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_publication_terminal_status_closeout_records.py
exit /b %ERRORLEVEL%
