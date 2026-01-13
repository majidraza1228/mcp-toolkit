@echo off
REM MCP Toolkit Launcher for Windows
REM Automatically uses the correct Python version (3.11+)

echo Starting MCP Toolkit...
echo.

REM Check for Python 3.11+
python --version 2>nul | findstr /R "3\.1[1-9]" >nul
if %errorlevel% equ 0 (
    echo Found Python 3.11+
    python run.py
    goto :end
)

python3 --version 2>nul | findstr /R "3\.1[1-9]" >nul
if %errorlevel% equ 0 (
    echo Found Python 3.11+
    python3 run.py
    goto :end
)

py -3.11 --version 2>nul
if %errorlevel% equ 0 (
    echo Found Python 3.11+
    py -3.11 run.py
    goto :end
)

echo ERROR: Python 3.11+ not found!
echo.
echo Please install Python 3.11 or higher from python.org
echo.
pause

:end
