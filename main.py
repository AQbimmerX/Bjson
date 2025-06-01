import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import json
import base64
import os
import threading
from datetime import datetime

# Import all tabs
from project_tabs.coding_tab import CodingTab
from project_tabs.hdd_guide_tab import HDDGuideTab
from project_tabs.wellcome_headlight_tab import WellcomeHeadlightTab
from project_tabs.image_change_tab import ImageChangeRetrofitTab
from project_tabs.flash_guide_tab import FlashGuideTab

# GitHub settings
GITHUB_TOKEN = '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'
REPO_OWNER = 'AQbimmerX'
REPO_NAME = 'Bjson'
FILE_PATH = 'codings.json'
GITHUB_API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'

# Add Arabic codings file path
ARABIC_FILE_PATH = 'codings_arabic.json'
ARABIC_GITHUB_API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{ARABIC_FILE_PATH}'

# Load data from GitHub
def load_codings_from_github(arabic=False):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = ARABIC_GITHUB_API_URL if arabic else GITHUB_API_URL
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()['content']
        decoded_content = base64.b64decode(content).decode('utf-8')
        return json.loads(decoded_content)
    else:
        print(f"Failed to load file from GitHub. Status code: {response.status_code}")
        return []

# Load data on startup
try:
    codings = load_codings_from_github()
except Exception as e:
    print(f"Error loading codings: {e}")
    codings = []

ecu_list = sorted({c.get("ecu", "") for c in codings if c.get("ecu", "")})

class MainApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("BMW Coding Dark Tools")
        self.geometry("1400x850")
        self.minsize(1200, 700)
        # Set background image using a Label with a PIL image for JPEG support
        try:
            from PIL import Image, ImageTk
            bg_path = os.path.join("images", "backgruond.jpg")
            if os.path.exists(bg_path):
                pil_img = Image.open(bg_path)
                pil_img = pil_img.resize((1400, 850), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(pil_img)
                self.bg_label = tk.Label(self, image=self.bg_image)
                self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            else:
                self.configure(bg="#23272b")
        except Exception:
            self.configure(bg="#23272b")
        self.language = tk.StringVar(value="en")

        # --- Move language selection here so it's always on top ---
        self.lang_frame = ttk.Frame(self)
        self.lang_frame.pack(side="top", anchor="ne", padx=10, pady=10)
        ttk.Label(self.lang_frame, text="Language:", font=("Helvetica", 10, "bold")).pack(side="left", padx=(0,5))
        lang_combo = ttk.Combobox(self.lang_frame, textvariable=self.language, values=["en", "ar"], width=8, state="readonly")
        lang_combo.pack(side="left")
        lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        # ----------------------------------------------------------

        self.setup_ui()

    def setup_ui(self):
        style = tb.Style()
        style.theme_use("superhero")
        style.configure('TNotebook.Tab', font=('Helvetica', 12, 'bold'), padding=[20, 10])
        style.configure('TNotebook', background="#23272b", borderwidth=0)
        style.map("TNotebook.Tab",
            background=[("selected", "#28a745"), ("active", "#ffc107"), ("!selected", "#343a40")],
            foreground=[("selected", "#fff"), ("active", "#23272b"), ("!selected", "#fff")]
        )

        # Raise notebook above background label
        notebook = tb.Notebook(self, bootstyle="darkly")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        notebook.lift()

        # Store notebook and coding tab for language switching
        self.notebook = notebook
        self.coding_tab = CodingTab(notebook, codings=codings)
        notebook.add(self.coding_tab, text="BMW Codings")
        notebook.add(HDDGuideTab(notebook), text="NBT EVO HDD Guide")
        notebook.add(ImageChangeRetrofitTab(notebook), text="Image Retrofit")
        #notebook.add(FlashGuideTab(notebook), text="Flash Guide")
        # --- Scrollable Welcome Headlight Tab ---
        from ttkbootstrap.scrolled import ScrolledFrame
        wellcome_scroll = ScrolledFrame(notebook, autohide=True)
        wellcome_tab = WellcomeHeadlightTab(wellcome_scroll)
        wellcome_tab.pack(fill="both", expand=True)
        notebook.add(wellcome_scroll.container, text="Welcome Headlight")
        # ----------------------------------------

        # Suppress warnings about incomplete hex pairs from WellcomeHeadlightTab
        import warnings
        warnings.filterwarnings("ignore", message="Incomplete hex pair found at index*")

        # Force WellcomeHeadlightTab to reload JSON on every tab switch
        def reload_welcome_tab(event):
            tab_id = notebook.select()
            tab_widget = notebook.nametowidget(tab_id)
            if isinstance(tab_widget, WellcomeHeadlightTab):
                # Auto scroll to top when switching to the tab
                try:
                    wellcome_scroll.yview_moveto(0)
                except Exception:
                    pass
                tab_widget.load_version_data(tab_widget.selected_version.get() if hasattr(tab_widget, "selected_version") else None)
        notebook.bind("<<NotebookTabChanged>>", reload_welcome_tab)

        # Set tab minimum width for better appearance
        for i in range(notebook.index("end")):
            notebook.tab(i, padding=[30, 10])

    def on_language_change(self, event=None):
        # Reload codings from selected language and update CodingTab
        lang = self.language.get()
        arabic = lang == "ar"
        try:
            new_codings = load_codings_from_github(arabic=arabic)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load codings: {e}")
            return
        # Replace CodingTab with new data
        idx = self.notebook.index(self.coding_tab)
        self.notebook.forget(idx)
        self.coding_tab = CodingTab(self.notebook, codings=new_codings)
        self.notebook.insert(idx, self.coding_tab, text="BMW Codings")
        self.notebook.select(idx)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
