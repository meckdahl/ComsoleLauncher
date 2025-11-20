#!/usr/bin/env python3
"""
Quick diagnostic script to test if all required modules can be imported.
Run this to diagnose installation issues.
"""

import sys

print("="*70)
print("ComsoleLauncher - Import Diagnostic Test")
print("="*70)
print(f"\nPython version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Test imports one by one
modules_to_test = [
    ("tkinter", "GUI framework (built-in)"),
    ("pathlib", "Path handling (built-in)"),
    ("threading", "Threading (built-in)"),
    ("ui", "UI package"),
    ("core", "Core package"),
    ("features", "Features package"),
    ("utils", "Utils package"),
]

failed = []
passed = []

for module_name, description in modules_to_test:
    try:
        __import__(module_name)
        print(f"✓ {module_name:20} - {description}")
        passed.append(module_name)
    except ImportError as e:
        print(f"✗ {module_name:20} - FAILED: {e}")
        failed.append((module_name, str(e)))
    except Exception as e:
        print(f"✗ {module_name:20} - ERROR: {e}")
        failed.append((module_name, str(e)))

print()
print("="*70)

if failed:
    print(f"RESULT: {len(passed)}/{len(modules_to_test)} imports succeeded")
    print()
    print("Failed imports:")
    for module, error in failed:
        print(f"  - {module}: {error}")
    print()
    print("Action required:")
    if "tkinter" in [m for m, _ in failed]:
        print("  - tkinter missing: Install python3-tk")
    if any(m in ["ui", "core", "features", "utils"] for m, _ in failed):
        print("  - Local packages missing: Check file structure")
    sys.exit(1)
else:
    print(f"SUCCESS: All {len(modules_to_test)} imports passed!")
    print()
    print("Your environment is correctly set up.")
    print("You can run the application with: python comsol_manager.py")
    sys.exit(0)
