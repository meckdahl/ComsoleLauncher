@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Console Launcher - Windows Launcher Script
REM Handles UV installation detection and graceful fallback to pip
REM ============================================================================

echo.
echo ========================================
echo  Console Launcher - Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found: 
python --version

REM Check for UV installation
echo.
echo Checking for UV package manager...
uv --version >nul 2>&1
if errorlevel 1 (
    echo UV is not installed.
    echo UV is 10-100x faster than pip for installing packages.
    echo.
    set /p INSTALL_UV="Would you like to install UV? (Y/N): "
    
    if /i "!INSTALL_UV!"=="Y" (
        echo.
        echo Installing UV...
        python -m pip install uv
        
        REM Check if UV installation succeeded
        uv --version >nul 2>&1
        if errorlevel 1 (
            echo UV installation failed. Using pip instead.
            set USE_PIP=1
        ) else (
            echo UV installed successfully!
            set USE_UV=1
        )
    ) else (
        echo Using pip instead.
        set USE_PIP=1
    )
) else (
    echo UV found! Using UV for faster installation.
    set USE_UV=1
)

REM Install dependencies
echo.
echo ========================================
echo  Installing Dependencies
echo ========================================
echo.

if defined USE_UV (
    echo Using UV for faster installation...
    echo.
    
    REM Check if virtual environment exists
    if not exist "venv" (
        echo Creating virtual environment with UV...
        uv venv
        if errorlevel 1 (
            echo [ERROR] Failed to create virtual environment with UV
            echo Falling back to pip...
            goto USE_PIP_INSTALL
        )
    )
    
    REM Activate virtual environment
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo [ERROR] Failed to activate virtual environment
        goto USE_PIP_INSTALL
    )
    
    echo Installing packages with UV...
    uv pip install mph numpy
    if errorlevel 1 (
        echo [ERROR] UV package installation failed
        echo Falling back to pip...
        goto USE_PIP_INSTALL
    )
    
    echo [OK] Dependencies installed successfully with UV
    goto RUN_APP
)

:USE_PIP_INSTALL
echo Using pip for installation...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing packages with pip...
pip install mph numpy
if errorlevel 1 (
    echo [ERROR] Package installation failed
    echo.
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully with pip

:RUN_APP
echo.
echo ========================================
echo  Starting Console Launcher
echo ========================================
echo.

REM Check if comsol_manager.py exists
if not exist "comsol_manager.py" (
    echo [ERROR] comsol_manager.py not found in current directory
    echo.
    echo Please run this script from the ComsoleLauncher directory
    pause
    exit /b 1
)

REM Run the application
python comsol_manager.py

REM Check if application exited with error
if errorlevel 1 (
    echo.
    echo [ERROR] Application exited with error code: !errorlevel!
    echo.
    echo Common issues:
    echo   - COMSOL not installed
    echo   - Java not available
    echo   - Missing .mph files in comsol_projects folder
    echo.
    echo Try using "Inspect & Edit" mode which doesn't require COMSOL
    pause
    exit /b 1
)

echo.
echo Application closed successfully
pause
