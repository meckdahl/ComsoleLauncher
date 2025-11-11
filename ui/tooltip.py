"""
ToolTip widget for displaying hover help text
"""
import tkinter as tk


class ToolTip:
    """
    Simple tooltip widget for showing help text on hover.

    Usage:
        button = tk.Button(root, text="Click me")
        ToolTip(button, "This is a helpful tooltip")
    """

    def __init__(self, widget, text):
        """
        Initialize tooltip for a widget.

        Args:
            widget: The tkinter widget to attach tooltip to
            text: The tooltip text to display
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        """Show the tooltip near the widget"""
        # Position tooltip below and to the right of widget
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip,
            text=self.text,
            justify=tk.LEFT,
            background="#34495e",
            foreground="white",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 9),
            padx=8,
            pady=5
        )
        label.pack()

    def hide(self, event=None):
        """Hide the tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
