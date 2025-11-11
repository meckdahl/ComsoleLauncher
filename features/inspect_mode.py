"""
Inspect & Edit mode - View and modify .mph files without Comsol
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from pathlib import Path
from typing import Dict

from ui.tooltip import ToolTip
from utils.mph_parser import MphParser
from utils.mph_saver import MphSaver


class InspectModeFeature:
    """
    Handles the Inspect & Edit feature for viewing and modifying .mph files.
    Works without requiring mph library or Comsol installation.
    """

    def __init__(self, root, project_info: Dict):
        """
        Initialize inspect mode.

        Args:
            root: Parent tkinter window
            project_info: Dictionary with project metadata
        """
        self.root = root
        self.project_info = project_info
        self.mph_path = project_info['file_path']
        self.param_tree = None
        self.modified_params = set()

    def show(self):
        """Display the inspect & edit window"""
        # Create inspect window
        inspect_window = tk.Toplevel(self.root)
        inspect_window.title(f"Inspect & Edit - {self.project_info['display_name']}")
        inspect_window.geometry("900x700")

        # Title bar
        self._create_title_bar(inspect_window)

        # Notebook for tabs
        notebook = ttk.Notebook(inspect_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        file_tree, param_tree, info_text = self._create_tabs(notebook)
        self.param_tree = param_tree

        # Bottom buttons
        self._create_bottom_buttons(inspect_window)

        # Load data
        self._load_content(file_tree, param_tree, info_text)

    def _create_title_bar(self, window):
        """Create colored title bar"""
        title_bar = tk.Frame(window, bg="#d35400", height=60)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text=f"🔍  {self.project_info['display_name']}.mph",
            font=("Arial", 14, "bold"),
            bg="#d35400",
            fg="white"
        ).pack(pady=15)

    def _create_tabs(self, notebook):
        """Create the three tabs and return their widgets"""
        # Tab 1: File Structure
        contents_frame = ttk.Frame(notebook)
        notebook.add(contents_frame, text="📁 File Structure")
        file_tree = self._create_file_structure_tab(contents_frame)

        # Tab 2: Parameters
        params_frame = ttk.Frame(notebook)
        notebook.add(params_frame, text="⚙️ Parameters")
        param_tree = self._create_parameters_tab(params_frame)

        # Tab 3: Model Info
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="ℹ️ Model Info")
        info_text = self._create_model_info_tab(info_frame)

        return file_tree, param_tree, info_text

    def _create_file_structure_tab(self, parent):
        """Create file structure tab with color-coded tree"""
        header_frame = tk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            header_frame,
            text="Internal file structure:",
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT)

        # Color legend
        self._create_color_legend(parent)

        # File tree
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        file_tree = ttk.Treeview(tree_frame, columns=('size', 'type'), show='tree headings')
        file_tree.heading('#0', text='File Name')
        file_tree.heading('size', text='Size')
        file_tree.heading('type', text='Type')
        file_tree.column('#0', width=400)
        file_tree.column('size', width=100)
        file_tree.column('type', width=150)

        # Configure color tags
        file_tree.tag_configure('xml', foreground='#2980b9')
        file_tree.tag_configure('json', foreground='#16a085')
        file_tree.tag_configure('binary', foreground='#8e44ad')
        file_tree.tag_configure('image', foreground='#27ae60')
        file_tree.tag_configure('text', foreground='#7f8c8d')
        file_tree.tag_configure('archive', foreground='#e67e22')

        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=file_tree.yview)
        file_tree.configure(yscrollcommand=tree_scroll.set)

        file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        return file_tree

    def _create_color_legend(self, parent):
        """Create color legend for file types"""
        legend_frame = tk.Frame(parent, bg="#f8f9fa", bd=1, relief=tk.SOLID)
        legend_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        legend_inner = tk.Frame(legend_frame, bg="#f8f9fa")
        legend_inner.pack(pady=5)

        tk.Label(
            legend_inner,
            text="Legend:",
            font=("Arial", 8, "bold"),
            bg="#f8f9fa",
            fg="#34495e"
        ).pack(side=tk.LEFT, padx=5)

        colors = [
            ("#2980b9", "Config"),
            ("#16a085", "Metadata"),
            ("#8e44ad", "Simulation"),
            ("#27ae60", "Image"),
            ("#7f8c8d", "Text"),
            ("#e67e22", "Checkpoint")
        ]

        for color, label in colors:
            tk.Label(
                legend_inner,
                text="●",
                fg=color,
                bg="#f8f9fa",
                font=("Arial", 10)
            ).pack(side=tk.LEFT, padx=(8, 0))
            tk.Label(
                legend_inner,
                text=label,
                font=("Arial", 8),
                bg="#f8f9fa",
                fg="#34495e"
            ).pack(side=tk.LEFT, padx=(0, 5))

    def _create_parameters_tab(self, parent):
        """Create parameters tab with editable tree"""
        tk.Label(
            parent,
            text="Model Parameters (editable):",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, padx=10, pady=5)

        # Parameters tree
        param_tree_frame = tk.Frame(parent)
        param_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        param_tree = ttk.Treeview(
            param_tree_frame,
            columns=('name', 'value', 'description'),
            show='headings',
            height=20
        )
        param_tree.heading('name', text='Parameter')
        param_tree.heading('value', text='Value')
        param_tree.heading('description', text='Description')
        param_tree.column('name', width=150)
        param_tree.column('value', width=150)
        param_tree.column('description', width=400)

        # Configure tag for modified parameters
        param_tree.tag_configure('modified', background='#fff9e6', foreground='#e67e22')

        param_scroll = ttk.Scrollbar(param_tree_frame, orient=tk.VERTICAL, command=param_tree.yview)
        param_tree.configure(yscrollcommand=param_scroll.set)

        param_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        param_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click to edit
        param_tree.bind('<Double-1>', lambda e: self._edit_parameter())

        # Help text
        help_frame = tk.Frame(parent, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        help_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            help_frame,
            text="💡 Double-click any parameter to edit  •  Modified parameters are highlighted in orange",
            font=("Arial", 9),
            fg="#34495e",
            bg="#ecf0f1",
            anchor=tk.W
        ).pack(padx=10, pady=8)

        return param_tree

    def _create_model_info_tab(self, parent):
        """Create model info tab with statistics"""
        info_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Courier", 9))
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        return info_text

    def _create_bottom_buttons(self, window):
        """Create bottom action buttons"""
        btn_frame = tk.Frame(window, bg="#ecf0f1", height=60)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        btn_frame.pack_propagate(False)

        btn_inner = tk.Frame(btn_frame, bg="#ecf0f1")
        btn_inner.pack(expand=True)

        save_btn = tk.Button(
            btn_inner,
            text="💾 Save Changes",
            command=self._save_changes,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        export_btn = tk.Button(
            btn_inner,
            text="📂 Export Files",
            command=self._export_files,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, padx=5)

        close_btn = tk.Button(
            btn_inner,
            text="Close",
            command=window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        close_btn.pack(side=tk.LEFT, padx=5)

        # Add tooltips
        ToolTip(save_btn, "Write modified parameters to new .mph file")
        ToolTip(export_btn, "Extract all files to a folder for inspection")
        ToolTip(close_btn, "Close inspector (changes not saved)")

    def _load_content(self, file_tree, param_tree, info_text):
        """Load all content into the tabs"""
        # Load file list
        files = MphParser.load_file_list(self.mph_path)
        for file_info in files:
            file_tree.insert(
                '',
                'end',
                text=file_info['filename'],
                values=(file_info['size'], file_info['type']),
                tags=(file_info['tag'],)
            )

        # Load parameters
        parameters = MphParser.load_parameters_from_mph(self.mph_path)
        for name, value, desc in parameters:
            param_tree.insert('', 'end', values=(name, value, desc), tags=(name,))

        # Load model info
        model_info = MphParser.load_model_info(self.mph_path)
        if model_info:
            info_text.insert(tk.END, "=== FILE INFORMATION ===\n\n")
            info_text.insert(tk.END, f"File: {self.mph_path.name}\n")
            info_text.insert(tk.END, f"Size: {self.mph_path.stat().st_size / 1024 / 1024:.2f} MB\n")
            info_text.insert(tk.END, f"Comsol Version: {model_info['version']}\n")
            info_text.insert(tk.END, f"Internal files: {model_info['file_count']}\n\n")
            info_text.insert(tk.END, f"Title: {model_info['title']}\n")
            info_text.insert(tk.END, f"Description: {model_info['description']}\n")
            info_text.insert(tk.END, "\n=== STORAGE BREAKDOWN ===\n\n")
            info_text.insert(tk.END, f"Total data size: {model_info['total_size_mb']:.2f} MB\n")
            info_text.insert(tk.END, f"Configuration (XML/JSON): {model_info['text_size_mb']:.2f} MB ({model_info['text_percent']:.1f}%)\n")
            info_text.insert(tk.END, f"Simulation data (binary): {model_info['binary_size_mb']:.2f} MB ({model_info['binary_percent']:.1f}%)\n")
            info_text.config(state=tk.DISABLED)

    def _edit_parameter(self):
        """Open parameter edit dialog"""
        from .inspect_mode_editor import ParameterEditor
        ParameterEditor(self.root, self.param_tree, self.mph_path).show()

    def _save_changes(self):
        """Save modified parameters to new .mph file"""
        # Collect all parameters
        params = {}
        modified_count = 0
        for item in self.param_tree.get_children():
            values = self.param_tree.item(item, 'values')
            tags = self.param_tree.item(item, 'tags')
            if len(values) >= 2:
                params[values[0]] = values[1]
                if 'modified' in tags:
                    modified_count += 1

        if modified_count == 0:
            messagebox.showinfo("No Changes", "No parameters have been modified.")
            return

        # Show progress
        progress = self._show_progress_dialog(modified_count)

        # Save
        success, message, new_mph, backup = MphSaver.save_modified_mph(self.mph_path, params)

        progress.destroy()

        if success:
            messagebox.showinfo(
                "✓ Success",
                f"Changes saved successfully!\n\n"
                f"New file: {new_mph.name}\n"
                f"Backup: {backup.name}\n\n"
                f"Modified parameters: {modified_count}\n"
                f"Total parameters: {len(params)}"
            )
        else:
            messagebox.showerror("Error", f"Failed to save changes:\n\n{message}")

    def _show_progress_dialog(self, modified_count):
        """Show progress dialog during save"""
        progress = tk.Toplevel(self.root)
        progress.title("Saving Changes")
        progress.geometry("350x120")
        progress.resizable(False, False)
        progress.transient(self.root)
        progress.configure(bg="white")

        tk.Label(
            progress,
            text="💾 Saving parameter changes...",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            progress,
            text=f"Processing {modified_count} modified parameter(s)",
            font=("Arial", 9),
            fg="#7f8c8d",
            bg="white"
        ).pack(pady=5)

        progress_bar = ttk.Progressbar(progress, mode='indeterminate', length=280)
        progress_bar.pack(pady=10)
        progress_bar.start(10)

        self.root.update()
        return progress

    def _export_files(self):
        """Export .mph contents to folder"""
        extract_dir = filedialog.askdirectory(
            title="Select destination folder",
            initialdir=self.mph_path.parent
        )

        if not extract_dir:
            return

        success, message, file_count = MphSaver.extract_mph(self.mph_path, Path(extract_dir))

        if success:
            messagebox.showinfo(
                "Export Complete",
                f"Successfully exported to:\n{message}\n\n"
                f"Files exported: {file_count}"
            )
        else:
            messagebox.showerror("Error", f"Export failed:\n{message}")
