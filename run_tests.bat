@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

call "%ROOT%pfem_check.bat" --full %*
exit /b %ERRORLEVEL%
