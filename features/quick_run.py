"""
Quick Run feature - Simple one-click simulation execution
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from typing import Dict

from utils.dependency_manager import DependencyManager


class QuickRunFeature:
    """
    Handles quick run functionality - load, build, solve, save.
    """

    def __init__(self, root, base_path: Path):
        """
        Initialize quick run feature.

        Args:
            root: Parent tkinter window
            base_path: Base directory for the application
        """
        self.root = root
        self.base_path = base_path
        self.dep_manager = DependencyManager()

    def run(self, project_info: Dict, on_complete_callback=None):
        """
        Execute quick run for a project.

        Args:
            project_info: Dictionary with project metadata
            on_complete_callback: Function to call when complete
        """
        if not self.dep_manager.check_mph_available():
            messagebox.showerror(
                "mph Not Available",
                "The mph library is required.\n\n"
                "Install with: pip install mph\n"
                "or use UV: uv pip install mph"
            )
            return

        model_path = project_info['file_path']
        progress = self._show_progress_window(project_info['display_name'])

        def run_thread():
            try:
                # Setup UV environment if available
                if self.dep_manager.check_uv_available():
                    self._update_progress(progress, "Setting up UV environment...")
                    self.dep_manager.setup_uv_environment(self.base_path)

                # Import mph
                import mph

                # Connect to Comsol
                self._update_progress(progress, "Connecting to Comsol server...")
                client = mph.start()

                # Load model
                self._update_progress(progress, f"Loading {model_path.name}...")
                model = client.load(str(model_path))

                # Build model
                self._update_progress(progress, "Building model...")
                model.build()

                # Solve model
                self._update_progress(progress, "Solving model (please wait)...")
                model.solve()

                # Export results
                output_path = model_path.parent / f"{model_path.stem}_result.mph"
                self._update_progress(progress, "Saving results...")
                model.save(str(output_path))

                # Success
                self.root.after(0, lambda: progress.destroy())
                self.root.after(0, lambda: messagebox.showinfo(
                    "✓ Success",
                    f"Simulation completed!\n\nResults saved to:\n{output_path.name}"
                ))

            except Exception as e:
                self.root.after(0, lambda: progress.destroy())
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Simulation failed:\n\n{str(e)}"
                ))
            finally:
                if on_complete_callback:
                    self.root.after(0, on_complete_callback)

        thread = threading.Thread(target=run_thread, daemon=True)
        thread.start()

    def _show_progress_window(self, project_name):
        """Show progress window"""
        progress = tk.Toplevel(self.root)
        progress.title("Running Simulation")
        progress.geometry("400x150")
        progress.resizable(False, False)
        progress.transient(self.root)

        tk.Label(
            progress,
            text=f"Running: {project_name}",
            font=("Arial", 11, "bold")
        ).pack(pady=(20, 10))

        progress.status_label = tk.Label(
            progress,
            text="Initializing...",
            font=("Arial", 10)
        )
        progress.status_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress, mode='indeterminate', length=300)
        progress_bar.pack(pady=20)
        progress_bar.start(10)

        return progress

    def _update_progress(self, window, message):
        """Update progress window message"""
        if window and window.winfo_exists():
            self.root.after(0, lambda: window.status_label.config(text=message))
