"""
Dependency management utilities (UV, pip, mph library)
"""
import subprocess
import sys
from pathlib import Path


class DependencyManager:
    """
    Manages Python dependencies using UV or pip.
    """

    @staticmethod
    def check_mph_available() -> bool:
        """
        Check if mph library is installed and importable.

        Returns:
            True if mph is available, False otherwise
        """
        try:
            import mph
            return True
        except ImportError:
            return False

    @staticmethod
    def check_uv_available() -> bool:
        """
        Check if UV package manager is installed.

        Returns:
            True if UV is available, False otherwise
        """
        try:
            result = subprocess.run(
                ["uv", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    def setup_uv_environment(base_path: Path) -> None:
        """
        Setup UV environment with required packages.

        Args:
            base_path: Base directory for virtual environment

        Raises:
            subprocess.CalledProcessError: If setup fails
        """
        venv_path = base_path / ".venv"

        if not venv_path.exists():
            subprocess.run(
                ["uv", "venv"],
                cwd=base_path,
                check=True
            )

        subprocess.run(
            ["uv", "pip", "install", "mph", "numpy"],
            cwd=base_path,
            check=True
        )

    @staticmethod
    def install_mph_with_pip() -> bool:
        """
        Install mph library using pip.

        Returns:
            True if installation succeeded, False otherwise
        """
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "mph", "numpy"],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def install_uv_with_pip() -> bool:
        """
        Install UV using pip.

        Returns:
            True if installation succeeded, False otherwise
        """
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "uv"],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
