@echo off
REM Comsol Project Manager - Windows Launcher
REM Easy launch script with automatic UV setup

echo ============================================================
echo   Comsol Project Manager - Starting...
echo ============================================================
echo.

cd /d "%~dp0"

REM Create log file
set LOGFILE=launcher.log
echo [%date% %time%] Comsol Project Manager Starting... > %LOGFILE%
echo [%date% %time%] Working directory: %cd% >> %LOGFILE%

REM Check for UV
where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [*] UV detected - using fast dependency management
    echo [%date% %time%] UV detected >> %LOGFILE%
    echo.

    REM Create venv if needed
    if not exist ".venv" (
        echo [*] Creating UV virtual environment...
        echo [%date% %time%] Creating UV venv... >> %LOGFILE%
        uv venv 2>> %LOGFILE%
        if %ERRORLEVEL% neq 0 (
            echo [!] Failed to create virtual environment
            echo [%date% %time%] ERROR: Failed to create venv >> %LOGFILE%
            echo.
            echo Check launcher.log for details
            pause
            exit /b 1
        )
        echo [+] Virtual environment created
        echo [%date% %time%] Venv created successfully >> %LOGFILE%
        echo.
    )

    REM Install dependencies
    echo [*] Installing/updating dependencies...
    echo [%date% %time%] Installing dependencies... >> %LOGFILE%
    uv pip install mph numpy 2>> %LOGFILE%
    if %ERRORLEVEL% neq 0 (
        echo [!] Failed to install dependencies
        echo [%date% %time%] ERROR: Dependency installation failed >> %LOGFILE%
        echo.
        echo Check launcher.log for details
        pause
        exit /b 1
    )
    echo [+] Dependencies ready
    echo [%date% %time%] Dependencies installed >> %LOGFILE%
    echo.

    REM Run the application
    echo [*] Launching Comsol Project Manager...
    echo [%date% %time%] Launching application... >> %LOGFILE%
    echo.
    echo NOTE: First-time Java/Comsol connection may show warnings - this is normal
    echo       The application will continue loading...
    echo.
    uv run python comsol_manager.py 2>> %LOGFILE%
    set APP_EXIT_CODE=%ERRORLEVEL%
    echo [%date% %time%] Application exited with code %APP_EXIT_CODE% >> %LOGFILE%

) else (
    echo [*] UV not found - using system Python
    echo [%date% %time%] UV not found, using system Python >> %LOGFILE%
    echo [i] Install UV for faster setup: pip install uv
    echo.

    REM Check for Python
    where python >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo [!] Python not found in PATH
        echo [%date% %time%] ERROR: Python not found >> %LOGFILE%
        echo [!] Please install Python 3.8 or higher
        pause
        exit /b 1
    )

    REM Check/install dependencies
    echo [*] Checking dependencies...
    echo [%date% %time%] Checking dependencies... >> %LOGFILE%
    python -c "import mph" 2>nul
    if %ERRORLEVEL% neq 0 (
        echo [*] Installing mph library...
        echo [%date% %time%] Installing mph... >> %LOGFILE%
        python -m pip install mph numpy 2>> %LOGFILE%
        if %ERRORLEVEL% neq 0 (
            echo [!] Failed to install dependencies
            echo [%date% %time%] ERROR: pip install failed >> %LOGFILE%
            echo.
            echo Check launcher.log for details
            pause
            exit /b 1
        )
    )
    echo [%date% %time%] Dependencies ready >> %LOGFILE%

    REM Run the application
    echo [*] Launching Comsol Project Manager...
    echo [%date% %time%] Launching application... >> %LOGFILE%
    echo.
    echo NOTE: First-time Java/Comsol connection may show warnings - this is normal
    echo       The application will continue loading...
    echo.
    python comsol_manager.py 2>> %LOGFILE%
    set APP_EXIT_CODE=%ERRORLEVEL%
    echo [%date% %time%] Application exited with code %APP_EXIT_CODE% >> %LOGFILE%
)

REM Check exit status
if %APP_EXIT_CODE% neq 0 (
    echo.
    echo [!] Application exited with error code %APP_EXIT_CODE%
    echo [!] Check launcher.log for error details
    echo.
    pause
    exit /b %APP_EXIT_CODE%
)

REM Normal exit - brief pause to see final messages
timeout /t 2 /nobreak >nul
