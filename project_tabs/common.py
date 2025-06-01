import ttkbootstrap as tb
import tkinter as tk

class CodeBlock(tb.Frame):
    def __init__(self, master, code_text, width=50, **kwargs):
        super().__init__(master, **kwargs)
        self.code_text = code_text
        self.width = width
        self.setup_ui()

    def setup_ui(self):
        self.config(borderwidth=1, relief="solid", padding=5)
        self.text_widget = tb.Text(self, wrap="none", width=self.width, height=5, font=("Consolas", 10))
        self.text_widget.insert("1.0", self.code_text)
        self.text_widget.config(state="disabled")
        self.text_widget.pack(fill="both", expand=True)
        copy_btn = tb.Button(self, text="Copy", bootstyle="secondary", command=self.copy_to_clipboard)
        copy_btn.pack(side="right", padx=5)

    def copy_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.code_text)
