#!/usr/bin/env python3
"""
Comsol Project Manager - Python Launcher
Simple launcher that ensures dependencies are installed before running
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def log(message, logfile="launcher.log"):
    """Log message to file and print to console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    # Append to log file
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(log_entry)

    # Also print to console
    print(message)


def check_uv_available():
    """Check if UV is installed"""
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def setup_with_uv():
    """Setup environment using UV (fast)"""
    log("[*] Using UV for dependency management...")

    venv_path = Path(__file__).parent / ".venv"

    # Create venv if needed
    if not venv_path.exists():
        log("[*] Creating UV virtual environment...")
        result = subprocess.run(
            ["uv", "venv"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            log(f"ERROR: Failed to create venv: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, "uv venv")
        log("[+] Virtual environment created")

    # Install dependencies
    log("[*] Installing dependencies...")
    result = subprocess.run(
        ["uv", "pip", "install", "mph", "numpy"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        log(f"ERROR: Failed to install dependencies: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, "uv pip install")
    log("[+] Dependencies ready")

    # Run application
    log("[*] Launching Comsol Project Manager...")
    print()
    print("NOTE: First-time Java/Comsol connection may show warnings - this is normal")
    print("      The application will continue loading...")
    print()

    result = subprocess.run(
        ["uv", "run", "python", "comsol_manager.py"],
        capture_output=False  # Let output go to console
    )
    log(f"Application exited with code {result.returncode}")
    return result.returncode


def setup_with_pip():
    """Setup environment using regular pip"""
    log("[*] Using system Python...")
    print("[i] Install UV for faster setup: pip install uv")

    # Check if mph is installed
    try:
        import mph
        log("[+] Dependencies already installed")
    except ImportError:
        log("[*] Installing mph library...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "mph", "numpy"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            log(f"ERROR: pip install failed: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, "pip install")
        log("[+] Dependencies installed")

    # Run application
    log("[*] Launching Comsol Project Manager...")
    print()
    print("NOTE: First-time Java/Comsol connection may show warnings - this is normal")
    print("      The application will continue loading...")
    print()

    result = subprocess.run(
        [sys.executable, "comsol_manager.py"],
        capture_output=False  # Let output go to console
    )
    log(f"Application exited with code {result.returncode}")
    return result.returncode


def main():
    """Main entry point"""
    # Initialize log file
    logfile = Path(__file__).parent / "launcher.log"
    with open(logfile, "w", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Comsol Project Manager Starting...\n")

    print("=" * 60)
    print("  Comsol Project Manager - Starting...")
    print("=" * 60)
    print()

    # Change to script directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)

    log(f"Working directory: {script_dir}")

    try:
        if check_uv_available():
            log("UV detected")
            exit_code = setup_with_uv()
        else:
            log("UV not found, using system Python")
            exit_code = setup_with_pip()

        if exit_code != 0:
            print()
            print(f"[!] Application exited with error code {exit_code}")
            print("[!] Check launcher.log for error details")
            sys.exit(exit_code)
        else:
            print()
            print("[*] Application closed normally")

    except subprocess.CalledProcessError as e:
        print()
        print(f"[!] Error during setup: {e}")
        print("[!] Check launcher.log for details")
        log(f"ERROR: Setup failed - {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("[*] Cancelled by user")
        log("Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"[!] Unexpected error: {e}")
        print("[!] Check launcher.log for details")
        log(f"ERROR: Unexpected error - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
