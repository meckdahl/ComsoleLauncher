@echo off
REM ============================================================================
REM ComsoleLauncher - Windows Installer
REM Requires: Python 3.13, Java JDK
REM ============================================================================

setlocal

cls
echo.
echo ============================================================================
echo                   ComsoleLauncher - Setup
echo ============================================================================
echo.

cd /d "%~dp0"

REM ============================================================================
REM Check Python 3.13 using py launcher
REM ============================================================================
echo [1/4] Checking Python 3.13...

py -3.13 --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [X] Python 3.13 not found!
    echo.
    echo Download from: https://www.python.org/downloads/
    echo Check "Add Python to PATH" during install
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('py -3.13 --version 2^>^&1') do echo [OK] %%i found

REM ============================================================================
REM Check Java JDK
REM ============================================================================
echo [2/4] Checking Java JDK...

java -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [X] Java JDK required!
    echo.
    echo Download from: https://adoptium.net/
    echo Install Temurin JDK 17, restart computer, run this again
    echo.
    pause
    exit /b 1
)
echo [OK] Java found

REM ============================================================================
REM Create Python 3.13 virtual environment
REM ============================================================================
echo [3/4] Setting up environment...

REM Delete old venv if it exists
if exist ".venv" (
    echo Removing old virtual environment...
    rmdir /s /q .venv
)

REM Create venv with Python 3.13
echo Creating Python 3.13 virtual environment...
py -3.13 -m venv .venv

if not exist ".venv\Scripts\python.exe" (
    echo [X] Failed to create virtual environment
    pause
    exit /b 1
)

echo [OK] Python 3.13 environment ready

REM ============================================================================
REM Install dependencies using venv's pip
REM ============================================================================
echo [4/4] Installing dependencies...

.venv\Scripts\python -m pip install --upgrade pip --quiet

echo Installing JPype1 from wheel...
.venv\Scripts\pip install wheels\jpype1-1.6.0-cp313-cp313-win_amd64.whl

if %ERRORLEVEL% neq 0 (
    echo [X] JPype1 installation failed
    pause
    exit /b 1
)

echo Installing MPh and NumPy...
.venv\Scripts\pip install mph numpy

if %ERRORLEVEL% neq 0 (
    echo [X] Installation failed
    pause
    exit /b 1
)

echo [OK] All dependencies installed

REM ============================================================================
REM Done - Launch
REM ============================================================================
echo.
echo ============================================================================
echo   Setup Complete!
echo ============================================================================
echo.

if not exist "comsol_projects" mkdir comsol_projects

echo Starting ComsoleLauncher...
.venv\Scripts\python.exe launcher.py

endlocal
