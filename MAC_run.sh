#!/bin/bash

# ============================================================================
# Console Launcher - Mac/Linux Launcher Script
# Handles UV installation detection and graceful fallback to pip
# ============================================================================

set -e  # Exit on error (but we'll handle errors explicitly)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo ""
    echo "========================================"
    echo "  $1"
    echo "========================================"
    echo ""
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Main script
print_header "Console Launcher - Setup"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  - macOS: brew install python3"
    echo "  - Linux: sudo apt-get install python3 python3-pip"
    echo ""
    exit 1
fi

print_success "Python found: $(python3 --version)"

# Check for UV installation
echo ""
print_info "Checking for UV package manager..."

USE_UV=0

if command -v uv &> /dev/null; then
    print_success "UV found! Using UV for faster installation."
    USE_UV=1
else
    echo ""
    echo "UV is not installed."
    echo "UV is 10-100x faster than pip for installing packages."
    echo ""
    read -p "Would you like to install UV? (Y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        print_info "Installing UV..."
        
        if python3 -m pip install uv; then
            # Check if UV is now available
            if command -v uv &> /dev/null; then
                print_success "UV installed successfully!"
                USE_UV=1
            elif python3 -m uv --version &> /dev/null; then
                print_success "UV installed successfully!"
                USE_UV=1
                # Create alias for this session
                alias uv='python3 -m uv'
            else
                print_warning "UV installation failed. Using pip instead."
            fi
        else
            print_warning "UV installation failed. Using pip instead."
        fi
    else
        print_info "Using pip instead."
    fi
fi

# Install dependencies
print_header "Installing Dependencies"

install_with_uv() {
    print_info "Using UV for fast installation..."
    echo ""
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment with UV..."
        if uv venv; then
            print_success "Virtual environment created"
        else
            print_error "Failed to create virtual environment with UV"
            return 1
        fi
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        print_error "Failed to find activation script"
        return 1
    fi
    
    # Install packages
    print_info "Installing packages with UV..."
    if uv pip install mph numpy; then
        print_success "Dependencies installed successfully with UV"
        return 0
    else
        print_error "UV package installation failed"
        return 1
    fi
}

install_with_pip() {
    print_info "Using pip for installation..."
    echo ""
    
    # Upgrade pip first
    print_info "Upgrading pip..."
    python3 -m pip install --upgrade pip --quiet
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        if python3 -m venv venv; then
            print_success "Virtual environment created"
        else
            print_error "Failed to create virtual environment"
            exit 1
        fi
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        print_error "Failed to find activation script"
        exit 1
    fi
    
    # Install packages
    print_info "Installing packages with pip..."
    if pip install mph numpy; then
        print_success "Dependencies installed successfully with pip"
        return 0
    else
        print_error "Package installation failed"
        echo ""
        echo "Please check your internet connection and try again"
        exit 1
    fi
}

# Try installation based on selected method
if [ $USE_UV -eq 1 ]; then
    if ! install_with_uv; then
        print_warning "Falling back to pip..."
        install_with_pip
    fi
else
    install_with_pip
fi

# Run the application
print_header "Starting Console Launcher"

# Check if comsol_manager.py exists
if [ ! -f "comsol_manager.py" ]; then
    print_error "comsol_manager.py not found in current directory"
    echo ""
    echo "Please run this script from the ComsoleLauncher directory"
    exit 1
fi

# Make sure we're in the virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run the application
if python3 comsol_manager.py; then
    echo ""
    print_success "Application closed successfully"
else
    EXIT_CODE=$?
    echo ""
    print_error "Application exited with error code: $EXIT_CODE"
    echo ""
    echo "Common issues:"
    echo "  - COMSOL not installed"
    echo "  - Java not available"
    echo "  - Missing .mph files in comsol_projects folder"
    echo ""
    echo "Try using \"Inspect & Edit\" mode which doesn't require COMSOL"
    exit $EXIT_CODE
fi
