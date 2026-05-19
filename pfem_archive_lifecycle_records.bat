@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_archive_lifecycle_records.py
exit /b %ERRORLEVEL%
