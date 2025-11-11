#!/usr/bin/env python3
"""
Comsol Project Manager - Main Application Entry Point
Modular architecture with separate packages for UI, features, core, and utilities.
"""
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import threading
from pathlib import Path
from typing import Dict, Optional

# Import from local modules
from ui import ToolTip, MainWindowUI, ProjectCardManager
from core import ProjectScanner
from features import QuickRunFeature, LauncherGenerator, AdvancedModeFeature, InspectModeFeature
from utils import DependencyManager


class ComsolProjectManager:
    """
    Main application class - coordinates UI and feature modules.
    Follows separation of concerns with dedicated modules for each responsibility.
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize application.

        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("Comsol Project Manager")
        self.root.geometry("950x650")
        self.root.minsize(900, 600)

        # Setup paths
        self.base_path = Path(__file__).parent
        self.projects_path = self.base_path / "comsol_projects"
        self.projects_path.mkdir(exist_ok=True)

        # Initialize managers
        self.dep_manager = DependencyManager()
        self.project_scanner = ProjectScanner(self.projects_path)

        # Application state
        self.projects = {}
        self.selected_project = None

        # Check dependencies
        self.mph_available = self.dep_manager.check_mph_available()
        self.uv_available = self.dep_manager.check_uv_available()

        # Initialize UI
        self._setup_ui()

        # Load projects
        self.scan_projects()

    def _setup_ui(self):
        """Setup the user interface"""
        # Create UI layout
        self.ui = MainWindowUI(
            self.root,
            self.mph_available,
            self.uv_available,
            self.projects_path
        )

        # Setup callbacks
        callbacks = {
            'quick_run': self._on_quick_run,
            'create_launcher': self._on_create_launcher,
            'advanced_mode': self._on_advanced_mode,
            'inspect_mode': self._on_inspect_mode,
            'show_help': self._show_help,
            'install_uv': self._install_uv,
            'install_mph': self._install_mph,
            'browse_folder': self._browse_folder,
            'refresh_projects': self.scan_projects
        }

        # Build UI and get scrollable frame
        scrollable_frame = self.ui.setup(callbacks)

        # Initialize project card manager
        self.card_manager = ProjectCardManager(
            scrollable_frame,
            self._on_project_selected
        )

    def scan_projects(self):
        """Scan projects directory for .mph files"""
        # Clear existing cards
        self.card_manager.clear()
        self.projects = {}
        self.selected_project = None

        # Scan for projects
        self.projects = self.project_scanner.scan_projects()

        if not self.projects:
            if not self.projects_path.exists():
                self.card_manager.show_empty_state("Projects folder not found")
            else:
                self.card_manager.show_empty_state(
                    "No .mph files found\n\nAdd Comsol models to the projects folder"
                )
            return

        # Create cards
        for project_name, project_info in self.projects.items():
            self.card_manager.create_card(project_name, project_info)

    def _on_project_selected(self, project_name: str):
        """
        Handle project selection.

        Args:
            project_name: Name of selected project
        """
        self.selected_project = project_name
        self.ui.enable_action_buttons()

    def _on_quick_run(self):
        """Handle quick run button click"""
        if not self.selected_project:
            return

        project_info = self.projects[self.selected_project]

        # Create and run quick run feature
        quick_run = QuickRunFeature(self.root, self.base_path)

        def on_complete():
            self.ui.enable_action_buttons()

        # Temporarily disable buttons
        self.ui.disable_action_buttons()

        quick_run.run(project_info, on_complete)

    def _on_create_launcher(self):
        """Handle create launcher button click"""
        if not self.selected_project:
            return

        project_info = self.projects[self.selected_project]
        LauncherGenerator.generate(project_info)

    def _on_advanced_mode(self):
        """Handle advanced mode button click"""
        if not self.selected_project:
            return

        project_info = self.projects[self.selected_project]
        advanced_mode = AdvancedModeFeature(self.root, project_info)
        advanced_mode.show()

    def _on_inspect_mode(self):
        """Handle inspect & edit button click"""
        if not self.selected_project:
            return

        project_info = self.projects[self.selected_project]
        inspect_mode = InspectModeFeature(self.root, project_info)
        inspect_mode.show()

    def _browse_folder(self):
        """Browse for projects folder"""
        folder = filedialog.askdirectory(
            title="Select Projects Folder",
            initialdir=self.projects_path
        )
        if folder:
            self.projects_path = Path(folder)
            self.project_scanner = ProjectScanner(self.projects_path)
            self.scan_projects()

    def _install_uv(self):
        """Install UV package manager"""
        def install():
            try:
                success = self.dep_manager.install_uv_with_pip()
                if success:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Success",
                        "UV installed!\n\nRestart the application."
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Error",
                        "Installation failed"
                    ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Installation failed:\n{str(e)}"
                ))

        threading.Thread(target=install, daemon=True).start()

    def _install_mph(self):
        """Install mph library"""
        def install():
            try:
                if self.uv_available:
                    self.dep_manager.setup_uv_environment(self.base_path)
                else:
                    success = self.dep_manager.install_mph_with_pip()
                    if not success:
                        self.root.after(0, lambda: messagebox.showerror(
                            "Error",
                            "Installation failed"
                        ))
                        return

                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    "mph installed!\n\nRestart the application."
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Installation failed:\n{str(e)}"
                ))

        threading.Thread(target=install, daemon=True).start()

    def _show_help(self):
        """Show help dialog"""
        help_text = """COMSOL PROJECT MANAGER

QUICK START:
1. Add .mph files to 'comsol_projects' folder
2. Click Refresh to scan
3. Click a project card to select it
4. Click Quick Run for instant execution
   OR Advanced for parameter editing
   OR Inspect & Edit to modify without Comsol

FEATURES:
• Quick Run: One-click simulation
• Launcher: Create standalone scripts
• Advanced: Edit parameters before running
• Inspect & Edit: Modify .mph files directly
• UV Support: 10-100x faster setup

REQUIREMENTS:
• Python 3.8+
• mph library (for simulation)
• Comsol Multiphysics (for simulation)
• Java Runtime (bundled with Comsol)

UV (Optional):
Install for faster dependency management:
  pip install uv

INSPECT & EDIT:
This feature works WITHOUT mph or Comsol!
Directly view and modify .mph parameters.
"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Help")
        dialog.geometry("500x500")

        text = scrolledtext.ScrolledText(
            dialog,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        text.insert(1.0, help_text)
        text.config(state=tk.DISABLED)

        tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=8
        ).pack(pady=10)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ComsolProjectManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
