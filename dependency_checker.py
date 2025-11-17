"""
Dependency Checker for Console Launcher
Verifies that all required dependencies are installed and provides
graceful error handling with helpful installation instructions.
"""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import Tuple, Optional, List


class DependencyChecker:
    """Check and manage project dependencies."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.has_uv = False
        self.has_mph = False
        self.has_numpy = False
        
    def check_python_version(self) -> bool:
        """Check if Python version meets requirements."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.errors.append(
                f"Python 3.8 or higher is required. "
                f"You have Python {version.major}.{version.minor}.{version.micro}"
            )
            return False
        return True
    
    def check_uv_installed(self) -> bool:
        """Check if UV package manager is installed."""
        # Check if 'uv' command is available
        if shutil.which('uv'):
            try:
                result = subprocess.run(
                    ['uv', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    self.has_uv = True
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        # Check if UV can be imported as module
        try:
            subprocess.run(
                [sys.executable, '-m', 'uv', '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            self.has_uv = True
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.warnings.append(
            "UV package manager not found. "
            "Install with: pip install uv (optional, but 10-100x faster)"
        )
        return False
    
    def check_package_installed(self, package_name: str) -> bool:
        """Check if a Python package is installed."""
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
    
    def check_mph(self) -> bool:
        """Check if mph (COMSOL Python interface) is installed."""
        self.has_mph = self.check_package_installed('mph')
        if not self.has_mph:
            self.errors.append(
                "mph library not found. Required for COMSOL integration.\n"
                "Install with: pip install mph (or 'uv pip install mph' if using UV)"
            )
        return self.has_mph
    
    def check_numpy(self) -> bool:
        """Check if NumPy is installed."""
        self.has_numpy = self.check_package_installed('numpy')
        if not self.has_numpy:
            self.errors.append(
                "numpy library not found. Required for numerical operations.\n"
                "Install with: pip install numpy (or 'uv pip install numpy' if using UV)"
            )
        return self.has_numpy
    
    def check_comsol_availability(self) -> Tuple[bool, Optional[str]]:
        """
        Check if COMSOL is available (optional - only needed for running simulations).
        
        Returns:
            Tuple of (is_available, error_message)
        """
        if not self.has_mph:
            return False, "mph library not installed"
        
        try:
            import mph
            # Try to start COMSOL client (with timeout)
            try:
                client = mph.start(cores=1)
                client.disconnect()
                return True, None
            except Exception as e:
                return False, f"COMSOL connection failed: {str(e)}"
        except Exception as e:
            return False, f"Failed to import mph: {str(e)}"
    
    def check_java_available(self) -> bool:
        """Check if Java is available (required for COMSOL)."""
        if shutil.which('java'):
            try:
                result = subprocess.run(
                    ['java', '-version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        self.warnings.append(
            "Java not found. Required for COMSOL operations.\n"
            "Java is typically installed with COMSOL Multiphysics."
        )
        return False
    
    def check_projects_folder(self) -> bool:
        """Check if comsol_projects folder exists."""
        projects_dir = Path('comsol_projects')
        if not projects_dir.exists():
            self.warnings.append(
                "comsol_projects folder not found. Creating it...\n"
                "Place your .mph files in this folder."
            )
            try:
                projects_dir.mkdir(exist_ok=True)
                return True
            except Exception as e:
                self.errors.append(f"Failed to create comsol_projects folder: {e}")
                return False
        return True
    
    def check_all(self, check_comsol: bool = False) -> bool:
        """
        Run all dependency checks.
        
        Args:
            check_comsol: If True, also check COMSOL availability (slower)
            
        Returns:
            True if all critical dependencies are met
        """
        # Critical checks
        python_ok = self.check_python_version()
        mph_ok = self.check_mph()
        numpy_ok = self.check_numpy()
        
        # Optional/informational checks
        self.check_uv_installed()
        self.check_java_available()
        self.check_projects_folder()
        
        # Check COMSOL if requested
        if check_comsol and mph_ok:
            comsol_ok, comsol_msg = self.check_comsol_availability()
            if not comsol_ok:
                self.warnings.append(
                    f"COMSOL not available: {comsol_msg}\n"
                    "You can still use 'Inspect & Edit' mode without COMSOL."
                )
        
        return python_ok and mph_ok and numpy_ok
    
    def print_results(self):
        """Print check results to console."""
        if self.errors:
            print("\n" + "=" * 60)
            print("❌ ERRORS - Required dependencies missing:")
            print("=" * 60)
            for error in self.errors:
                print(f"\n{error}")
            print("\n" + "=" * 60)
        
        if self.warnings:
            print("\n" + "=" * 60)
            print("⚠️  WARNINGS - Optional features may not work:")
            print("=" * 60)
            for warning in self.warnings:
                print(f"\n{warning}")
            print("\n" + "=" * 60)
        
        if not self.errors and not self.warnings:
            print("\n" + "=" * 60)
            print("✅ All dependencies are installed and configured!")
            print("=" * 60)
    
    def install_missing_dependencies(self, use_uv: bool = None) -> bool:
        """
        Attempt to install missing dependencies.
        
        Args:
            use_uv: If True, use UV; if False, use pip; if None, auto-detect
            
        Returns:
            True if installation succeeded
        """
        missing = []
        if not self.has_mph:
            missing.append('mph')
        if not self.has_numpy:
            missing.append('numpy')
        
        if not missing:
            return True
        
        # Auto-detect UV if not specified
        if use_uv is None:
            use_uv = self.has_uv
        
        print(f"\n{'=' * 60}")
        print(f"Installing missing packages: {', '.join(missing)}")
        print(f"Using: {'UV' if use_uv else 'pip'}")
        print(f"{'=' * 60}\n")
        
        try:
            if use_uv:
                cmd = ['uv', 'pip', 'install'] + missing
            else:
                cmd = [sys.executable, '-m', 'pip', 'install'] + missing
            
            result = subprocess.run(
                cmd,
                check=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("\n✅ Installation successful!")
                return True
            else:
                print("\n❌ Installation failed")
                return False
                
        except subprocess.TimeoutExpired:
            print("\n❌ Installation timed out")
            return False
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Installation failed: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error during installation: {e}")
            return False


def main():
    """Run dependency check as standalone script."""
    print("\n" + "=" * 60)
    print("Console Launcher - Dependency Check")
    print("=" * 60)
    
    checker = DependencyChecker()
    
    # Run all checks
    all_ok = checker.check_all(check_comsol=False)
    
    # Print results
    checker.print_results()
    
    # If there are errors, offer to install
    if checker.errors:
        print("\nWould you like to attempt automatic installation? (y/n): ", end='')
        response = input().strip().lower()
        
        if response in ('y', 'yes'):
            success = checker.install_missing_dependencies()
            if success:
                # Re-check
                checker = DependencyChecker()
                all_ok = checker.check_all(check_comsol=False)
                checker.print_results()
            sys.exit(0 if all_ok else 1)
        else:
            print("\nPlease install the missing dependencies manually.")
            sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
