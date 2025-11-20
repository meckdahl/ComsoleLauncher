#!/bin/bash
# ============================================================================
# ComsoleLauncher - Mac/Linux Installer
# Requires: Python 3.13, Java JDK
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo ""
echo "============================================================================"
echo "                  ComsoleLauncher - Setup"
echo "============================================================================"
echo ""

cd "$(dirname "$0")"

# ============================================================================
# Check Python 3.13
# ============================================================================
echo "[1/4] Checking Python 3.13..."

if ! command -v python3.13 &> /dev/null; then
    echo -e "${RED}[X] Python 3.13 not found!${NC}"
    echo ""
    echo "Download from: https://www.python.org/downloads/"
    echo "  - macOS: brew install python@3.13"
    echo "  - Linux: sudo apt install python3.13 python3.13-venv"
    echo ""
    exit 1
fi

PYVER=$(python3.13 --version 2>&1)
echo -e "${GREEN}[OK] $PYVER found${NC}"

# ============================================================================
# Check Java JDK
# ============================================================================
echo "[2/4] Checking Java JDK..."

if ! command -v java &> /dev/null; then
    echo -e "${RED}[X] Java JDK required!${NC}"
    echo ""
    echo "Download from: https://adoptium.net/"
    echo "Install Temurin JDK 17, restart terminal, run this again"
    echo ""
    exit 1
fi

echo -e "${GREEN}[OK] Java found${NC}"

# ============================================================================
# Create Python 3.13 virtual environment
# ============================================================================
echo "[3/4] Setting up environment..."

# Delete old venv if it exists
if [ -d ".venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf .venv
fi

# Create venv with Python 3.13
echo "Creating Python 3.13 virtual environment..."
python3.13 -m venv .venv

if [ ! -f ".venv/bin/python" ]; then
    echo -e "${RED}[X] Failed to create virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}[OK] Python 3.13 environment ready${NC}"

# ============================================================================
# Install dependencies
# ============================================================================
echo "[4/4] Installing dependencies..."

.venv/bin/python -m pip install --upgrade pip --quiet

echo "Installing JPype1..."
.venv/bin/pip install jpype1

if [ $? -ne 0 ]; then
    echo -e "${RED}[X] JPype1 installation failed${NC}"
    exit 1
fi

echo "Installing MPh and NumPy..."
.venv/bin/pip install mph numpy

if [ $? -ne 0 ]; then
    echo -e "${RED}[X] Installation failed${NC}"
    exit 1
fi

echo -e "${GREEN}[OK] All dependencies installed${NC}"

# ============================================================================
# Done - Launch
# ============================================================================
echo ""
echo "============================================================================"
echo "  Setup Complete!"
echo "============================================================================"
echo ""

mkdir -p comsol_projects

echo "Starting ComsoleLauncher..."
.venv/bin/python launcher.py
