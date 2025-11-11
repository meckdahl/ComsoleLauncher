#!/bin/bash
# Comsol Project Manager - Unix/Mac Launcher
# Easy launch script with automatic UV setup

echo "============================================================"
echo "  Comsol Project Manager - Starting..."
echo "============================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Create log file
LOGFILE="launcher.log"
echo "[$(date)] Comsol Project Manager Starting..." > "$LOGFILE"
echo "[$(date)] Working directory: $(pwd)" >> "$LOGFILE"

# Check for UV
if command -v uv &> /dev/null; then
    echo "[*] UV detected - using fast dependency management"
    echo "[$(date)] UV detected" >> "$LOGFILE"
    echo ""

    # Create venv if needed
    if [ ! -d ".venv" ]; then
        echo "[*] Creating UV virtual environment..."
        echo "[$(date)] Creating UV venv..." >> "$LOGFILE"
        uv venv 2>> "$LOGFILE"
        if [ $? -ne 0 ]; then
            echo "[!] Failed to create virtual environment"
            echo "[$(date)] ERROR: Failed to create venv" >> "$LOGFILE"
            echo ""
            echo "Check launcher.log for details"
            exit 1
        fi
        echo "[+] Virtual environment created"
        echo "[$(date)] Venv created successfully" >> "$LOGFILE"
        echo ""
    fi

    # Install dependencies
    echo "[*] Installing/updating dependencies..."
    echo "[$(date)] Installing dependencies..." >> "$LOGFILE"
    uv pip install mph numpy 2>> "$LOGFILE"
    if [ $? -ne 0 ]; then
        echo "[!] Failed to install dependencies"
        echo "[$(date)] ERROR: Dependency installation failed" >> "$LOGFILE"
        echo ""
        echo "Check launcher.log for details"
        exit 1
    fi
    echo "[+] Dependencies ready"
    echo "[$(date)] Dependencies installed" >> "$LOGFILE"
    echo ""

    # Run the application
    echo "[*] Launching Comsol Project Manager..."
    echo "[$(date)] Launching application..." >> "$LOGFILE"
    echo ""
    echo "NOTE: First-time Java/Comsol connection may show warnings - this is normal"
    echo "      The application will continue loading..."
    echo ""
    uv run python comsol_manager.py 2>> "$LOGFILE"
    APP_EXIT_CODE=$?
    echo "[$(date)] Application exited with code $APP_EXIT_CODE" >> "$LOGFILE"

else
    echo "[*] UV not found - using system Python"
    echo "[$(date)] UV not found, using system Python" >> "$LOGFILE"
    echo "[i] Install UV for faster setup: pip install uv"
    echo ""

    # Detect Python command
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
    else
        echo "[!] Python not found"
        echo "[$(date)] ERROR: Python not found" >> "$LOGFILE"
        echo "[!] Please install Python 3.8 or higher"
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo "[*] Using Python $PYTHON_VERSION"
    echo "[$(date)] Using Python $PYTHON_VERSION" >> "$LOGFILE"

    # Check/install dependencies
    echo "[*] Checking dependencies..."
    echo "[$(date)] Checking dependencies..." >> "$LOGFILE"
    $PYTHON_CMD -c "import mph" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[*] Installing mph library..."
        echo "[$(date)] Installing mph..." >> "$LOGFILE"
        $PYTHON_CMD -m pip install mph numpy 2>> "$LOGFILE"
        if [ $? -ne 0 ]; then
            echo "[!] Failed to install dependencies"
            echo "[$(date)] ERROR: pip install failed" >> "$LOGFILE"
            echo ""
            echo "Check launcher.log for details"
            exit 1
        fi
    fi
    echo "[$(date)] Dependencies ready" >> "$LOGFILE"

    # Run the application
    echo "[*] Launching Comsol Project Manager..."
    echo "[$(date)] Launching application..." >> "$LOGFILE"
    echo ""
    echo "NOTE: First-time Java/Comsol connection may show warnings - this is normal"
    echo "      The application will continue loading..."
    echo ""
    $PYTHON_CMD comsol_manager.py 2>> "$LOGFILE"
    APP_EXIT_CODE=$?
    echo "[$(date)] Application exited with code $APP_EXIT_CODE" >> "$LOGFILE"
fi

# Check exit status
if [ $APP_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "[!] Application exited with error code $APP_EXIT_CODE"
    echo "[!] Check launcher.log for error details"
    echo ""
    exit $APP_EXIT_CODE
fi

echo ""
echo "[*] Application closed normally"
