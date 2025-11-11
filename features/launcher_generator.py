"""
Launcher script generation feature
"""
import sys
from pathlib import Path
from tkinter import messagebox
from typing import Dict


class LauncherGenerator:
    """Generates standalone launcher scripts for projects"""

    @staticmethod
    def generate(project_info: Dict) -> bool:
        """
        Generate launcher scripts for a project.

        Args:
            project_info: Dictionary with project metadata

        Returns:
            True if successful, False otherwise
        """
        model_path = project_info['file_path']
        project_folder = project_info['folder']

        # Python launcher script
        py_script = f'''#!/usr/bin/env python3
"""Launcher for {project_info['display_name']}"""
import subprocess, sys
from pathlib import Path

model_path = Path(__file__).parent / "{model_path.name}"

try:
    import mph
except ImportError:
    print("ERROR: mph library not found")
    print("Install: pip install mph  or  uv pip install mph")
    sys.exit(1)

try:
    print("Connecting to Comsol...")
    client = mph.start()
    print("Loading model...")
    model = client.load(str(model_path))
    print("Building...")
    model.build()
    print("Solving...")
    model.solve()
    output = model_path.parent / f"{{model_path.stem}}_result.mph"
    model.save(str(output))
    print(f"\\n✓ Success! Results: {{output}}")
except Exception as e:
    print(f"\\nERROR: {{e}}")
    sys.exit(1)
'''

        # Shell script
        sh_script = f'''#!/bin/bash
cd "$(dirname "$0")"
if command -v uv &> /dev/null; then
    [ ! -d ".venv" ] && uv venv
    uv pip install mph numpy
    uv run python run_simulation.py
else
    python3 run_simulation.py
fi
'''

        # Batch script
        bat_script = f'''@echo off
cd /d "%~dp0"
where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    if not exist ".venv" uv venv
    uv pip install mph numpy
    uv run python run_simulation.py
) else (
    python run_simulation.py
)
pause
'''

        try:
            (project_folder / "run_simulation.py").write_text(py_script, encoding='utf-8')
            (project_folder / "run.sh").write_text(sh_script, encoding='utf-8')
            (project_folder / "run.bat").write_text(bat_script, encoding='utf-8')

            if sys.platform != 'win32':
                import stat
                sh_path = project_folder / "run.sh"
                sh_path.chmod(sh_path.stat().st_mode | stat.S_IXUSR)

            messagebox.showinfo(
                "✓ Launcher Created",
                f"Launcher scripts created!\n\n"
                f"Location: {project_folder}\n\n"
                f"Files:\n"
                f"  • run_simulation.py\n"
                f"  • run.sh (Mac/Linux)\n"
                f"  • run.bat (Windows)"
            )
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create launchers:\n{str(e)}")
            return False
