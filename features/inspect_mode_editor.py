"""
Parameter editor dialog for Inspect Mode
"""
import tkinter as tk
from tkinter import messagebox
from pathlib import Path


class ParameterEditor:
    """
    Dialog for editing a single parameter with validation.
    """

    def __init__(self, root, param_tree, mph_path: Path):
        """
        Initialize parameter editor.

        Args:
            root: Parent tkinter window
            param_tree: Treeview widget containing parameters
            mph_path: Path to .mph file
        """
        self.root = root
        self.param_tree = param_tree
        self.mph_path = mph_path

    def show(self):
        """Show parameter edit dialog"""
        selection = self.param_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.param_tree.item(item, 'values')
        param_name = values[0]
        current_value = values[1]
        description = values[2]

        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Parameter")
        dialog.geometry("500x280")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="white")

        # Header
        self._create_header(dialog, param_name)

        # Content
        content, entry, feedback_label = self._create_content(
            dialog, description, current_value
        )

        # Buttons
        self._create_buttons(
            dialog, entry, param_name, current_value, description, item
        )

        # Setup validation
        self._setup_validation(entry, feedback_label, current_value)

    def _create_header(self, dialog, param_name):
        """Create colored header"""
        header = tk.Frame(dialog, bg="#e67e22", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=param_name,
            font=("Arial", 13, "bold"),
            bg="#e67e22",
            fg="white"
        ).pack(pady=18)

    def _create_content(self, dialog, description, current_value):
        """Create content area with entry field"""
        content = tk.Frame(dialog, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Description
        tk.Label(
            content,
            text=description,
            font=("Arial", 9),
            fg="#7f8c8d",
            bg="white",
            wraplength=450
        ).pack(pady=(0, 10))

        # Label
        tk.Label(
            content,
            text="New Value:",
            font=("Arial", 9, "bold"),
            bg="white",
            anchor=tk.W
        ).pack(fill=tk.X)

        # Entry with border
        entry_frame = tk.Frame(content, bg="#3498db", bd=0)
        entry_frame.pack(fill=tk.X, pady=5)

        entry = tk.Entry(
            entry_frame,
            width=40,
            font=("Arial", 11),
            bd=2,
            relief=tk.SOLID
        )
        entry.pack(padx=2, pady=2)
        entry.insert(0, current_value)
        entry.focus()
        entry.select_range(0, tk.END)

        # Help text
        help_frame = tk.Frame(content, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        help_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(
            help_frame,
            text="💡 Examples:  10[W]  •  5.5[mm]  •  300[K]  •  0.8 (unitless)",
            font=("Arial", 8),
            fg="#34495e",
            bg="#ecf0f1",
            anchor=tk.W
        ).pack(padx=8, pady=5)

        # Feedback label
        feedback_label = tk.Label(
            content,
            text="",
            font=("Arial", 8),
            bg="white",
            fg="#e74c3c"
        )
        feedback_label.pack()

        return content, entry, feedback_label

    def _create_buttons(self, dialog, entry, param_name, current_value, description, item):
        """Create action buttons"""
        btn_frame = tk.Frame(dialog, bg="#f8f9fa")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        btn_inner = tk.Frame(btn_frame, bg="#f8f9fa")
        btn_inner.pack(pady=12)

        def save():
            new_value = entry.get().strip()
            if new_value:
                self.param_tree.item(item, values=(param_name, new_value, description))
                # Mark as modified
                self.param_tree.item(item, tags=('modified',))
                dialog.destroy()

        tk.Button(
            btn_inner,
            text="✓ Apply Change",
            command=save,
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=8,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_inner,
            text="Cancel",
            command=dialog.destroy,
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=8,
            font=("Arial", 9),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        entry.bind('<Return>', lambda e: save())
        entry.bind('<Escape>', lambda e: dialog.destroy())

    def _setup_validation(self, entry, feedback_label, current_value):
        """Setup real-time validation"""
        def validate_input(*args):
            value = entry.get().strip()
            if not value:
                feedback_label.config(text="⚠ Value cannot be empty", fg="#e74c3c")
                return False
            elif value == current_value:
                feedback_label.config(text="ℹ No change", fg="#95a5a6")
                return True
            else:
                feedback_label.config(text="✓ Valid", fg="#27ae60")
                return True

        entry_var = tk.StringVar()
        entry_var.trace('w', validate_input)
        entry.config(textvariable=entry_var)
        entry_var.set(current_value)
