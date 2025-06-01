import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk

class CodingTab(tb.Frame):
    def __init__(self, master, codings=None):
        super().__init__(master)
        self.codings = codings or []
        self.current_codings = []
        self.setup_ui()

    def setup_ui(self):
        # Language selection dropdown (top right)
        lang_frame = tb.Frame(self)
        lang_frame.place(relx=1.0, y=0, anchor="ne")
        ttk.Label(lang_frame, text="Language:", font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 5))
        lang_combo = ttk.Combobox(lang_frame, values=["en", "ar"], width=8, state="readonly")
        lang_combo.set("en")
        lang_combo.pack(side="left")
        lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        self.language_combo = lang_combo

        main_frame = tb.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Left frame for ECU list (green select)
        ecu_frame = tb.LabelFrame(main_frame, text="ECUs", bootstyle="info")
        ecu_frame.pack(side="left", fill="y", padx=2, pady=2)
        self.ecu_listbox = tk.Listbox(
            ecu_frame, width=18, bg="#222", fg="#fff",
            selectbackground="#28a745", selectforeground="#fff", activestyle="none",
            font=("Segoe UI", 12, "bold")
        )
        self.ecu_listbox.pack(fill="both", expand=True, padx=0, pady=2)
        self.ecu_listbox.bind("<<ListboxSelect>>", self.show_codings)
        ecu_list = sorted({c.get("ecu", "") for c in self.codings if c.get("ecu", "")})
        for ecu in ecu_list:
            self.ecu_listbox.insert(tk.END, ecu)

        # Middle frame for codings list (yellow select)
        coding_frame = tb.LabelFrame(main_frame, text="Codings", bootstyle="info")
        coding_frame.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.coding_list = tk.Listbox(
            coding_frame, width=35, bg="#222", fg="#fff",
            selectbackground="#ffc107", selectforeground="#23272b", activestyle="none",
            font=("Segoe UI", 12, "bold")
        )
        self.coding_list.pack(fill="both", expand=True, padx=2, pady=2)
        self.coding_list.bind("<<ListboxSelect>>", self.show_coding_details)

        # Right frame for details
        details_frame = tb.LabelFrame(main_frame, text="Details", bootstyle="info")
        details_frame.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.details_text = tk.Text(details_frame, width=50, bg="#23272b", fg="#fff", font=("Segoe UI", 12))
        self.details_text.pack(fill="both", expand=True, padx=2, pady=2)
        self.details_text.config(state=tk.DISABLED)

    def on_language_change(self, event=None):
        import requests, json, base64
        lang = self.language_combo.get()
        if lang == "ar":
            url = "https://api.github.com/repos/AQbimmerX/Bjson/contents/codings_arabic.json"
        else:
            url = "https://api.github.com/repos/AQbimmerX/Bjson/contents/codings.json"
        try:
            headers = {'Accept': 'application/vnd.github.v3+json'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content = response.json()['content']
                decoded_content = base64.b64decode(content).decode('utf-8')
                self.codings = json.loads(decoded_content)
            else:
                self.codings = []
        except Exception:
            self.codings = []
        # Refresh ECU list and clear coding/details
        self.ecu_listbox.delete(0, tk.END)
        ecu_list = sorted({c.get("ecu", "") for c in self.codings if c.get("ecu", "")})
        for ecu in ecu_list:
            self.ecu_listbox.insert(tk.END, ecu)
        self.coding_list.delete(0, tk.END)
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state=tk.DISABLED)

    def show_codings(self, event=None):
        selection = self.ecu_listbox.curselection()
        if not selection:
            return
        ecu = self.ecu_listbox.get(selection[0])
        self.current_codings = [c for c in self.codings if c.get("ecu") == ecu]
        self.coding_list.delete(0, tk.END)
        for c in self.current_codings:
            cid = c.get("id", "")
            func = c.get("function", "")
            title = c.get("title") or c.get("description", "")[:30]
            display = f"{ecu}"
            if cid:
                display += f" | {cid}"
            if func:
                display += f" | {func}"
            if not func and title:
                display += f" | {title}"
            self.coding_list.insert(tk.END, display)

    def show_coding_details(self, event=None):
        coding_sel = self.coding_list.curselection()
        if not coding_sel or not self.current_codings:
            return
        coding = self.current_codings[coding_sel[0]]
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        ecu = coding.get('ecu', '')
        cid = coding.get('id', '')
        func = coding.get('function', '')
        desc = coding.get('description', '')
        self.details_text.insert(tk.END, f"ECU: {ecu}\n", "ecu")
        if cid:
            self.details_text.insert(tk.END, f"ID: {cid}\n", "cid")
        if func:
            self.details_text.insert(tk.END, f"Function: {func}\n", "func")
        self.details_text.insert(tk.END, f"Description: {desc}\n", "desc")
        self.details_text.insert(tk.END, "\nSteps:\n", "steps")
        steps = coding.get("steps", [])
        for i, step in enumerate(steps, 1):
            self._insert_colored_step(i, step)
        self.apply_details_colors()
        self.details_text.config(state=tk.DISABLED)

    def _insert_colored_step(self, idx, step):
        # Split by '->' and color each part
        tokens = [t.strip() for t in step.split("->")]
        self.details_text.insert(tk.END, f"{idx}. ", "stepnum")
        for i, token in enumerate(tokens):
            tag = None
            # ECU (first token, usually)
            if i == 0:
                tag = "ecu"
            # ID (if numeric or 3068)
            elif token.isdigit() or token == "3068":
                tag = "cid"
            # Function (all uppercase or contains _)
            elif token.isupper() or "_" in token:
                tag = "func"
            # set to OFF, nict_aktiv
            elif token.strip().lower() in ["set to off", "nict_aktiv"]:
                tag = "off"
            # set to ON, set to aktiv
            elif token.strip().lower() in ["set to on", "set to aktiv"]:
                tag = "on"
            # Fallback
            else:
                tag = "step"
            self.details_text.insert(tk.END, token, tag)
            if i < len(tokens) - 1:
                self.details_text.insert(tk.END, " -> ", "arrow")
        self.details_text.insert(tk.END, "\n\n", "step")

        # Highlight specific words inside the step (set to OFF, nict_aktiv, set to ON, set to aktiv)
        for word, tag in [("set to OFF", "off"), ("nict_aktiv", "off"), ("set to ON", "on"), ("set to aktiv", "on")]:
            self._highlight_word_in_line(word, tag)

    def _highlight_word_in_line(self, word, tag):
        idx = self.details_text.search(word, "1.0", tk.END)
        while idx:
            end = f"{idx}+{len(word)}c"
            self.details_text.tag_add(tag, idx, end)
            idx = self.details_text.search(word, end, tk.END)

    def apply_details_colors(self):
        self.details_text.tag_configure("ecu", foreground="#ff3333", font=("Segoe UI", 12, "bold"))  # Red
        self.details_text.tag_configure("cid", foreground="#ffc107", font=("Segoe UI", 12, "bold"))  # Yellow
        self.details_text.tag_configure("func", foreground="#fff", font=("Segoe UI", 12, "bold"))    # White bold
        self.details_text.tag_configure("desc", foreground="#fff", font=("Segoe UI", 12, "bold"))
        self.details_text.tag_configure("steps", foreground="#fff", font=("Segoe UI", 12, "bold"))
        self.details_text.tag_configure("step", foreground="#fff", font=("Segoe UI", 12))
        self.details_text.tag_configure("stepnum", foreground="#fff", font=("Segoe UI", 12, "bold"))
        self.details_text.tag_configure("arrow", foreground="#fff", font=("Segoe UI", 12, "bold"))
        self.details_text.tag_configure("off", foreground="#ff3333", font=("Segoe UI", 12, "bold"))
        self.details_text.tag_configure("on", foreground="#28a745", font=("Segoe UI", 12, "bold"))

        # Also highlight in all text for the 4 keywords
        for word, tag in [("set to OFF", "off"), ("nict_aktiv", "off"), ("set to ON", "on"), ("set to aktiv", "on")]:
            self._highlight_word(word, "#ff3333" if tag == "off" else "#28a745", "bold")

    def _highlight_word(self, word, color, weight="normal"):
        start = "1.0"
        while True:
            idx = self.details_text.search(word, start, tk.END)
            if not idx:
                break
            end = f"{idx}+{len(word)}c"
            self.details_text.tag_add(word, idx, end)
            self.details_text.tag_config(word, foreground=color, font=("Segoe UI", 12, weight))
            start = end
