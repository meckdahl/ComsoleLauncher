"""
Project card UI components for displaying .mph files
"""
import tkinter as tk
from typing import Dict, Callable, Optional


class ProjectCardManager:
    """
    Manages project card widgets for displaying .mph files.
    Cards show project name, file size, modification date, and support selection.
    """

    def __init__(self, scrollable_frame, on_select_callback: Callable):
        """
        Initialize project card manager.

        Args:
            scrollable_frame: Parent frame for project cards
            on_select_callback: Function to call when project is selected
        """
        self.scrollable_frame = scrollable_frame
        self.on_select_callback = on_select_callback
        self.project_frames = {}
        self.selected_project = None

    def clear(self):
        """Clear all project cards"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.project_frames = {}
        self.selected_project = None

    def show_empty_state(self, message: str):
        """
        Show empty state when no projects found.

        Args:
            message: Message to display
        """
        empty_frame = tk.Frame(self.scrollable_frame, bg="white")
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=50)

        tk.Label(
            empty_frame,
            text="📂",
            font=("Arial", 48),
            bg="white",
            fg="#bdc3c7"
        ).pack()

        tk.Label(
            empty_frame,
            text=message,
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d"
        ).pack(pady=10)

    def create_card(self, project_name: str, project_info: Dict):
        """
        Create a visual card for a project.

        Args:
            project_name: Unique identifier for project
            project_info: Dictionary with project metadata
        """
        # Card container
        card = tk.Frame(
            self.scrollable_frame,
            bg="white",
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2"
        )
        card.pack(fill=tk.X, padx=10, pady=5)

        # Store reference
        self.project_frames[project_name] = card

        # Bind click events
        card.bind("<Button-1>", lambda e: self.select_project(project_name))

        # Inner padding frame
        inner = tk.Frame(card, bg="white")
        inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # Left side - Icon and name
        self._create_left_side(inner, project_info, project_name)

        # Right side - Metadata
        self._create_right_side(inner, project_info, project_name)

    def _create_left_side(self, parent, project_info: Dict, project_name: str):
        """Create left side of card with icon and name"""
        left_frame = tk.Frame(parent, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Icon
        tk.Label(
            left_frame,
            text="📊",
            font=("Arial", 32),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 15))

        # Project name and details
        info_frame = tk.Frame(left_frame, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            info_frame,
            text=project_info['display_name'],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor=tk.W
        ).pack(anchor=tk.W)

        tk.Label(
            info_frame,
            text=f"{project_info['file_path'].name}",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
            anchor=tk.W
        ).pack(anchor=tk.W, pady=(2, 0))

        # Bind click events to all widgets
        for widget in [left_frame, info_frame]:
            widget.bind("<Button-1>", lambda e: self.select_project(project_name))
            for child in widget.winfo_children():
                child.bind("<Button-1>", lambda e: self.select_project(project_name))

    def _create_right_side(self, parent, project_info: Dict, project_name: str):
        """Create right side of card with metadata"""
        right_frame = tk.Frame(parent, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        metadata_text = (
            f"{project_info['size_str']}  •  {project_info['modified_str']}"
        )
        label = tk.Label(
            right_frame,
            text=metadata_text,
            font=("Arial", 9),
            bg="white",
            fg="#95a5a6"
        )
        label.pack(side=tk.RIGHT)

        # Bind click events
        right_frame.bind("<Button-1>", lambda e: self.select_project(project_name))
        label.bind("<Button-1>", lambda e: self.select_project(project_name))

    def select_project(self, project_name: str):
        """
        Select a project card.

        Args:
            project_name: Name of project to select
        """
        # Deselect previous
        if self.selected_project and self.selected_project in self.project_frames:
            old_card = self.project_frames[self.selected_project]
            old_card.configure(bg="white", borderwidth=1)
            self._set_widget_bg(old_card, "white")

        # Select new
        self.selected_project = project_name
        card = self.project_frames[project_name]
        card.configure(bg="#ebf5fb", borderwidth=2)
        self._set_widget_bg(card, "#ebf5fb")

        # Notify callback
        self.on_select_callback(project_name)

    def _set_widget_bg(self, widget, color: str):
        """
        Recursively set background color of widget and all children.

        Args:
            widget: Widget to update
            color: Background color
        """
        try:
            widget.configure(bg=color)
        except:
            pass
        for child in widget.winfo_children():
            self._set_widget_bg(child, color)

    def get_selected_project(self) -> Optional[str]:
        """
        Get currently selected project.

        Returns:
            Selected project name or None
        """
        return self.selected_project
