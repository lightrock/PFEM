@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHONPATH=%ROOT%src"

python tools\pfem_retention_retrieval_token_closeout_records.py
exit /b %ERRORLEVEL%
