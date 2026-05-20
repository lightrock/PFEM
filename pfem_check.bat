@echo off
rem PFEM_CHECK_LAUNCHER_VERSION=1
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"
python tools\pfem_check.py %*
exit /b %ERRORLEVEL%
