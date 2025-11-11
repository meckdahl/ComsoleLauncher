"""
Main window UI setup for Comsol Project Manager
"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Callable, Dict

from .tooltip import ToolTip


class MainWindowUI:
    """
    Handles creation and layout of the main application window.
    Provides a modern visual design with status indicators, project grid, and action buttons.
    """

    def __init__(
        self,
        root,
        mph_available: bool,
        uv_available: bool,
        projects_path: Path
    ):
        """
        Initialize main window UI.

        Args:
            root: tkinter root window
            mph_available: Whether mph library is available
            uv_available: Whether UV is available
            projects_path: Path to projects directory
        """
        self.root = root
        self.mph_available = mph_available
        self.uv_available = uv_available
        self.projects_path = projects_path

        # Widgets that need to be accessed later
        self.canvas = None
        self.scrollable_frame = None
        self.quick_run_button = None
        self.launcher_button = None
        self.advanced_button = None
        self.inspect_button = None

    def setup(self, callbacks: Dict[str, Callable]) -> tk.Frame:
        """
        Setup the complete UI layout.

        Args:
            callbacks: Dictionary mapping button names to callback functions

        Returns:
            Frame containing the scrollable project area
        """
        self._create_title_section()
        self._create_status_section(callbacks)
        self._create_path_controls(callbacks)
        self._create_projects_grid()
        self._create_action_buttons(callbacks)

        return self.scrollable_frame

    def _create_title_section(self):
        """Create title bar at top"""
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="Comsol Project Manager",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=(10, 5))

        tk.Label(
            title_frame,
            text="Manage and run Comsol Multiphysics simulations via Python",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack()

    def _create_status_section(self, callbacks: Dict):
        """Create status indicators with install buttons"""
        status_frame = tk.Frame(self.root, bg="#ecf0f1", height=35)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)

        status_inner = tk.Frame(status_frame, bg="#ecf0f1")
        status_inner.pack(pady=5)

        # mph status
        mph_status = "✓ mph library" if self.mph_available else "✗ mph library"
        mph_color = "#27ae60" if self.mph_available else "#e74c3c"
        tk.Label(
            status_inner,
            text=mph_status,
            fg=mph_color,
            bg="#ecf0f1",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=10)

        # UV status
        uv_status = "✓ UV" if self.uv_available else "✗ UV"
        uv_color = "#27ae60" if self.uv_available else "#f39c12"
        tk.Label(
            status_inner,
            text=uv_status,
            fg=uv_color,
            bg="#ecf0f1",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=10)

        # Install buttons if needed
        if not self.uv_available and 'install_uv' in callbacks:
            tk.Button(
                status_inner,
                text="Install UV",
                command=callbacks['install_uv'],
                bg="#3498db",
                fg="white",
                relief=tk.FLAT,
                padx=10,
                font=("Arial", 8)
            ).pack(side=tk.LEFT, padx=5)

        if not self.mph_available and 'install_mph' in callbacks:
            tk.Button(
                status_inner,
                text="Install mph",
                command=callbacks['install_mph'],
                bg="#3498db",
                fg="white",
                relief=tk.FLAT,
                padx=10,
                font=("Arial", 8)
            ).pack(side=tk.LEFT, padx=5)

    def _create_path_controls(self, callbacks: Dict):
        """Create path display and controls"""
        path_frame = tk.Frame(self.root, bg="white", height=40)
        path_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(
            path_frame,
            text="📁 Projects:",
            bg="white",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=(10, 5))

        tk.Label(
            path_frame,
            text=str(self.projects_path),
            bg="white",
            fg="#3498db",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)

        if 'browse_folder' in callbacks:
            tk.Button(
                path_frame,
                text="Browse",
                command=callbacks['browse_folder'],
                bg="#95a5a6",
                fg="white",
                relief=tk.FLAT,
                padx=15,
                font=("Arial", 9)
            ).pack(side=tk.RIGHT, padx=5)

        if 'refresh_projects' in callbacks:
            tk.Button(
                path_frame,
                text="↻ Refresh",
                command=callbacks['refresh_projects'],
                bg="#3498db",
                fg="white",
                relief=tk.FLAT,
                padx=15,
                font=("Arial", 9, "bold")
            ).pack(side=tk.RIGHT)

    def _create_projects_grid(self):
        """Create scrollable project cards area"""
        projects_outer = tk.Frame(self.root, bg="white")
        projects_outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(
            projects_outer,
            text="Available Projects",
            bg="white",
            font=("Arial", 11, "bold"),
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(5, 10))

        # Scrollable canvas for project cards
        self.canvas = tk.Canvas(
            projects_outer,
            bg="white",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            projects_outer,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        )

    def _create_action_buttons(self, callbacks: Dict):
        """Create bottom action button bar"""
        button_frame = tk.Frame(self.root, bg="#ecf0f1", height=70)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)

        # Center the buttons
        button_inner = tk.Frame(button_frame, bg="#ecf0f1")
        button_inner.pack(expand=True)

        # Quick Run button
        self.quick_run_button = tk.Button(
            button_inner,
            text="▶  Quick Run",
            command=callbacks.get('quick_run'),
            state=tk.DISABLED,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2"
        )
        self.quick_run_button.pack(side=tk.LEFT, padx=5)

        # Create Launcher button
        self.launcher_button = tk.Button(
            button_inner,
            text="📄 Create Launcher",
            command=callbacks.get('create_launcher'),
            state=tk.DISABLED,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.launcher_button.pack(side=tk.LEFT, padx=5)

        # Advanced button
        self.advanced_button = tk.Button(
            button_inner,
            text="⚙️ Advanced",
            command=callbacks.get('advanced_mode'),
            state=tk.DISABLED,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.advanced_button.pack(side=tk.LEFT, padx=5)

        # Inspect & Edit button
        self.inspect_button = tk.Button(
            button_inner,
            text="🔍 Inspect & Edit",
            command=callbacks.get('inspect_mode'),
            state=tk.DISABLED,
            bg="#e67e22",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.inspect_button.pack(side=tk.LEFT, padx=5)

        # Help button
        help_button = tk.Button(
            button_inner,
            text="❓ Help",
            command=callbacks.get('show_help'),
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2"
        )
        help_button.pack(side=tk.LEFT, padx=15)

        # Add tooltips
        ToolTip(self.quick_run_button, "Run simulation with default settings")
        ToolTip(self.launcher_button, "Generate standalone launch scripts")
        ToolTip(self.advanced_button, "Connect to Comsol and edit parameters")
        ToolTip(self.inspect_button, "View and edit .mph file directly (no Comsol needed)")
        ToolTip(help_button, "Show help and documentation")

    def enable_action_buttons(self):
        """Enable all action buttons (called when project is selected)"""
        self.quick_run_button.config(state=tk.NORMAL)
        self.launcher_button.config(state=tk.NORMAL)
        self.advanced_button.config(state=tk.NORMAL)
        self.inspect_button.config(state=tk.NORMAL)

    def disable_action_buttons(self):
        """Disable all action buttons"""
        self.quick_run_button.config(state=tk.DISABLED)
        self.launcher_button.config(state=tk.DISABLED)
        self.advanced_button.config(state=tk.DISABLED)
        self.inspect_button.config(state=tk.DISABLED)
