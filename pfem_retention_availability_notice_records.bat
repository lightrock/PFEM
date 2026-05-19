@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_availability_notice_records.py
exit /b %ERRORLEVEL%
