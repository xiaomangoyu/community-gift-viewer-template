@echo off
setlocal
cd /d "%~dp0"

set "PORT=8000"
if not "%~1"=="" set "PORT=%~1"
set "PYTHON_CMD="

py -3 -c "import sys" >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"
if defined PYTHON_CMD goto :start

python -c "import sys" >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=python"
if not defined PYTHON_CMD goto :python_error

:start
echo.
echo Community Gifts Viewer is starting on port %PORT%.
echo Local: http://127.0.0.1:%PORT%/
echo LAN:   http://YOUR-WINDOWS-IP:%PORT%/
echo.
echo Windows IPv4 addresses:
ipconfig | findstr /i "IPv4"
echo.
echo Keep this window open. Press Ctrl+C to stop the server.
start "" "http://127.0.0.1:%PORT%/"
%PYTHON_CMD% -m http.server %PORT% --bind 0.0.0.0
exit /b %errorlevel%

:python_error
echo.
echo Python 3 was not found.
echo Install 64-bit Python 3.12 and enable Add Python to PATH, then run this file again.
pause
exit /b 2
