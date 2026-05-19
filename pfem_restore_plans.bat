@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_restore_plans.py
exit /b %ERRORLEVEL%
