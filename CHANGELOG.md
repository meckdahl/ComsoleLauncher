# Recent Changes

## 2025-11-17 - Python 3.13 Support & Installation Fixes

1. **Added Python 3.13 wheel** - Downloaded `jpype1-1.6.0-cp313-cp313-win_amd64.whl` for Windows Python 3.13 compatibility
2. **Simplified installers** - Rewrote WIN_run.bat and MAC_run.sh to explicitly require Python 3.13, eliminating version mismatch issues
3. **Fixed venv handling** - Installers now always recreate virtual environment to prevent corrupted or wrong-version venv problems
4. **Improved error handling** - Added comprehensive error messages to launcher.py and comsol_manager.py for better debugging
5. **Cleaned up codebase** - Removed duplicate files (WIN_install.bat, WIN_setup.bat) and unused scripts (dependency_checker.py, verify_setup.py, build_wheels.bat)
6. **Consolidated documentation** - Merged QUICKSTART.md into README.md, updated all references to Python 3.13
7. **Streamlined installation** - 4-step process: check Python 3.13 → check Java → create venv → install dependencies
8. **Fixed batch file bugs** - Resolved delayed expansion and nested parentheses issues causing silent failures on Windows

All changes ensure clean installation on Python 3.13 with proper error reporting.
