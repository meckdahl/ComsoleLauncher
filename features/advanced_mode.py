"""
Advanced Mode feature - Connect to Comsol, edit parameters, run simulations
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from pathlib import Path
from typing import Dict, Optional


class AdvancedModeFeature:
    """
    Handles advanced mode functionality.
    Connects directly to Comsol server for interactive parameter editing and simulation.
    """

    def __init__(self, root, project_info: Dict):
        """
        Initialize advanced mode.

        Args:
            root: Parent tkinter window
            project_info: Dictionary with project metadata
        """
        self.root = root
        self.project_info = project_info
        self.mph_client = None
        self.current_model = None
        self.params_tree = None
        self.window = None

    def show(self):
        """Display the advanced mode window"""
        self.window = tk.Toplevel(self.root)
        self.window.title(f"Advanced Mode - {self.project_info['display_name']}")
        self.window.geometry("750x550")

        self._create_title_bar()
        self._create_parameters_tree()
        self._create_bottom_buttons()

    def _create_title_bar(self):
        """Create colored title bar"""
        title_bar = tk.Frame(self.window, bg="#34495e", height=60)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text=f"⚙️  {self.project_info['display_name']}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(pady=15)

    def _create_parameters_tree(self):
        """Create parameters tree view"""
        params_frame = tk.Frame(self.window)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(
            params_frame,
            text="Model Parameters (Double-click to edit)",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))

        params_columns = ('parameter', 'value', 'status')
        self.params_tree = ttk.Treeview(
            params_frame,
            columns=params_columns,
            show='headings',
            height=15
        )

        self.params_tree.heading('parameter', text='Parameter')
        self.params_tree.heading('value', text='Value')
        self.params_tree.heading('status', text='Status')

        self.params_tree.column('parameter', width=250)
        self.params_tree.column('value', width=200)
        self.params_tree.column('status', width=150)

        params_scroll = ttk.Scrollbar(
            params_frame,
            orient=tk.VERTICAL,
            command=self.params_tree.yview
        )
        self.params_tree.configure(yscrollcommand=params_scroll.set)

        self.params_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        params_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click to edit
        self.params_tree.bind('<Double-1>', lambda e: self._edit_parameter())

    def _create_bottom_buttons(self):
        """Create bottom action buttons"""
        btn_frame = tk.Frame(self.window, bg="#ecf0f1", height=60)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        btn_frame.pack_propagate(False)

        btn_inner = tk.Frame(btn_frame, bg="#ecf0f1")
        btn_inner.pack(expand=True)

        # Connect button
        self.connect_btn = tk.Button(
            btn_inner,
            text="🔌 Connect",
            command=self._connect_to_comsol,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.connect_btn.pack(side=tk.LEFT, padx=3)

        # Load Parameters button
        self.load_btn = tk.Button(
            btn_inner,
            text="📋 Load Parameters",
            command=self._load_parameters,
            state=tk.DISABLED,
            bg="#16a085",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.load_btn.pack(side=tk.LEFT, padx=3)

        # Run button
        self.run_btn = tk.Button(
            btn_inner,
            text="▶ Run",
            command=self._run_simulation,
            state=tk.DISABLED,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.run_btn.pack(side=tk.LEFT, padx=3)

        # Export button
        self.export_btn = tk.Button(
            btn_inner,
            text="💾 Export",
            command=self._export_results,
            state=tk.DISABLED,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.export_btn.pack(side=tk.LEFT, padx=3)

        # Close button
        tk.Button(
            btn_inner,
            text="Close",
            command=self.window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

    def _connect_to_comsol(self):
        """Connect to Comsol server"""
        def connect_thread():
            try:
                import mph
                self.mph_client = mph.start()
                self.root.after(0, lambda: self.load_btn.config(state=tk.NORMAL))
                self.root.after(0, lambda: messagebox.showinfo(
                    "Connected",
                    "Connected to Comsol server"
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Connection failed:\n{str(e)}"
                ))

        threading.Thread(target=connect_thread, daemon=True).start()

    def _load_parameters(self):
        """Load model and parameters from Comsol"""
        if not self.mph_client:
            messagebox.showwarning("Not Connected", "Connect to Comsol first")
            return

        def load_thread():
            try:
                # Load model
                self.current_model = self.mph_client.load(
                    str(self.project_info['file_path'])
                )

                # Get parameters
                params = self.current_model.parameters()

                # Update UI
                self.root.after(0, lambda: self._display_parameters(params))
                self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Load failed:\n{str(e)}"
                ))

        threading.Thread(target=load_thread, daemon=True).start()

    def _display_parameters(self, params: Dict[str, str]):
        """
        Display parameters in the tree view.

        Args:
            params: Dictionary of parameter names to values
        """
        # Clear existing items
        for item in self.params_tree.get_children():
            self.params_tree.delete(item)

        # Add parameters
        for param_name, param_value in params.items():
            self.params_tree.insert('', 'end', values=(param_name, param_value, ""))

    def _edit_parameter(self):
        """Open dialog to edit selected parameter"""
        if not self.current_model:
            return

        selection = self.params_tree.selection()
        if not selection:
            return

        item = selection[0]
        param_name = self.params_tree.item(item, 'values')[0]
        current_value = self.params_tree.item(item, 'values')[1]

        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit: {param_name}")
        dialog.geometry("350x130")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text=param_name,
            font=("Arial", 10, "bold")
        ).pack(pady=10)

        tk.Label(
            dialog,
            text="Value (with units, e.g., '10[mm]'):"
        ).pack()

        entry = tk.Entry(dialog, width=30)
        entry.insert(0, current_value)
        entry.pack(pady=5)
        entry.focus()

        def save():
            new_value = entry.get().strip()
            if new_value:
                try:
                    self.current_model.parameter(param_name, new_value)
                    self.params_tree.item(
                        item,
                        values=(param_name, new_value, "✓ Updated")
                    )
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        tk.Button(
            dialog,
            text="Save",
            command=save,
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=20, pady=10)

        tk.Button(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.RIGHT, padx=20, pady=10)

        entry.bind('<Return>', lambda e: save())

    def _run_simulation(self):
        """Run simulation with current parameters"""
        if not self.current_model:
            return

        def run_thread():
            try:
                self.current_model.build()
                self.current_model.solve()
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    "Simulation complete!"
                ))
                self.root.after(0, lambda: self.export_btn.config(state=tk.NORMAL))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    str(e)
                ))

        threading.Thread(target=run_thread, daemon=True).start()

    def _export_results(self):
        """Export simulation results to file"""
        if not self.current_model:
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Model",
            defaultextension=".mph",
            filetypes=[("Comsol Model", "*.mph")]
        )

        if save_path:
            try:
                self.current_model.save(save_path)
                messagebox.showinfo(
                    "Saved",
                    f"Model saved to:\n{save_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", str(e))
