#!/usr/bin/env python3
"""
Comsol Project Manager - Setup Verification Script

Checks if your system has all required components to run the application.
Run this before starting the main application for the first time.
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_check(text, passed, details=""):
    """Print a check result"""
    symbol = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"  # Green or Red
    reset = "\033[0m"
    
    print(f"{color}{symbol}{reset} {text}")
    if details:
        print(f"  → {details}")


def check_python_version():
    """Check if Python version is adequate"""
    print_header("Python Version Check")
    
    version = sys.version_info
    required = (3, 8)
    
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    passed = (version.major, version.minor) >= required
    
    print_check(
        f"Python {version_str}",
        passed,
        f"Required: Python {required[0]}.{required[1]}+" if not passed else "Good!"
    )
    
    return passed


def check_pip():
    """Check if pip is available"""
    print_header("Package Manager Check")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print_check("pip available", True, result.stdout.strip())
        return True
    except subprocess.CalledProcessError:
        print_check("pip available", False, "pip not found")
        return False


def check_module(module_name):
    """Check if a Python module is installed"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def check_required_modules():
    """Check all required Python modules"""
    print_header("Required Python Packages")
    
    modules = {
        'tkinter': 'Built-in GUI framework',
        'mph': 'Comsol interface library',
        'numpy': 'Numerical computing'
    }
    
    all_passed = True
    
    for module_name, description in modules.items():
        passed = check_module(module_name)
        print_check(f"{module_name:12} - {description}", passed)
        
        if not passed:
            all_passed = False
            if module_name == 'tkinter':
                print("     Install: sudo apt-get install python3-tk (Linux)")
                print("              Already included (Windows/Mac)")
            elif module_name == 'mph':
                print(f"     Install: pip install {module_name}")
            else:
                print(f"     Install: pip install {module_name}")
    
    return all_passed


def check_java():
    """Check if Java is available (required for mph/JPype)"""
    print_header("Java Runtime Environment Check")
    
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        # Java prints version to stderr
        version_info = result.stderr.split('\n')[0] if result.stderr else "Unknown"
        print_check("Java available", True, version_info)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_check("Java available", False, "Java not found")
        print("     Required for mph library (JPype bridge)")
        print("     Usually installed with Comsol Multiphysics")
        return False


def check_comsol():
    """Check if Comsol appears to be installed"""
    print_header("Comsol Multiphysics Check")
    
    # Common Comsol installation paths
    comsol_paths = [
        Path(r"C:\Program Files\COMSOL"),  # Windows
        Path(r"C:\COMSOL"),  # Windows alternative
        Path("/usr/local/comsol"),  # Linux
        Path("/Applications/COMSOL"),  # macOS
        Path.home() / "comsol"  # User installation
    ]
    
    found = False
    for path in comsol_paths:
        if path.exists():
            print_check(f"Comsol found at {path}", True)
            found = True
            break
    
    if not found:
        print_check(
            "Comsol installation",
            False,
            "Could not detect Comsol (may be installed elsewhere)"
        )
        print("     This check is informational - Comsol may still work")
    
    return True  # Don't fail on this


def check_project_structure():
    """Check if project structure is correct"""
    print_header("Project Structure Check")
    
    base_path = Path(__file__).parent
    
    required_files = {
        'comsol_manager.py': 'Main application',
        'README.md': 'Documentation',
        'requirements.txt': 'Dependencies list'
    }
    
    all_passed = True
    
    for filename, description in required_files.items():
        file_path = base_path / filename
        passed = file_path.exists()
        print_check(f"{filename:25} - {description}", passed)
        
        if not passed:
            all_passed = False
    
    # Check directories
    projects_path = base_path / "comsol_projects"
    projects_exists = projects_path.exists()
    
    print_check("comsol_projects/         - Project folder", projects_exists)
    
    if not projects_exists:
        print("     Creating comsol_projects directory...")
        try:
            projects_path.mkdir(exist_ok=True)
            print("     ✓ Created successfully")
        except Exception as e:
            print(f"     ✗ Failed to create: {e}")
            all_passed = False
    
    return all_passed


def check_permissions():
    """Check if we have necessary permissions"""
    print_header("Permissions Check")
    
    base_path = Path(__file__).parent
    
    # Try to create a test file
    test_file = base_path / "comsol_projects" / ".permission_test"
    
    try:
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_text("test")
        test_file.unlink()
        print_check("Write permissions", True, f"Can write to {base_path}")
        return True
    except Exception as e:
        print_check("Write permissions", False, f"Cannot write to {base_path}")
        print(f"     Error: {e}")
        return False


def print_summary(results):
    """Print summary and recommendations"""
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run Comsol Project Manager.")
        print("\nNext steps:")
        print("  1. Run: python comsol_manager.py")
        print("  2. Place .mph files in the comsol_projects/ folder")
        print("  3. Click 'Refresh' to scan for projects")
        print("  4. Select a project and click 'Connect to Comsol'")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("\nCommon solutions:")
        
        if not results.get('modules', True):
            print("\n  Missing Python packages:")
            print("    pip install mph numpy")
        
        if not results.get('java', True):
            print("\n  Java not found:")
            print("    - Install Java Runtime Environment (JRE)")
            print("    - Usually included with Comsol Multiphysics")
            print("    - Restart terminal/computer after installation")
        
        if not results.get('python', True):
            print("\n  Python version too old:")
            print("    - Install Python 3.8 or higher")
            print("    - Download from: https://www.python.org/")
        
        print("\n  After fixing issues, run this script again:")
        print("    python verify_setup.py")


def main():
    """Main verification function"""
    print("\n" + "🔍 " * 20)
    print("  COMSOL PROJECT MANAGER - SETUP VERIFICATION")
    print("🔍 " * 20)
    
    results = {}
    
    # Run all checks
    results['python'] = check_python_version()
    results['pip'] = check_pip()
    results['modules'] = check_required_modules()
    results['java'] = check_java()
    results['comsol'] = check_comsol()
    results['structure'] = check_project_structure()
    results['permissions'] = check_permissions()
    
    # Print summary
    print_summary(results)
    
    # Return exit code
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
