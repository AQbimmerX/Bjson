# ملف جديد: project_tabs/image_change_tab.py
import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
from tkinter import messagebox
import os

class ImageChangeRetrofitTab(tb.Frame):
    # Define CodeBlock as inner class
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

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.image_refs = []
        self.setup_ui()

    def setup_ui(self):
        canvas = tk.Canvas(self, bg="#f8f9fa")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tb.Frame(canvas)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title banner with WhatsApp and AQ icons
        banner = tb.Label(scroll_frame, 
                         text="NBT Image Change Retrofit Guide", 
                         font=("Helvetica", 18, "bold"), 
                         bootstyle="inverse-primary", 
                         padding=10)
        banner.pack(fill="x", pady=(0, 10))

        # WhatsApp and AQ icons row
        icon_row = tb.Frame(scroll_frame)
        icon_row.pack(fill="x", pady=(0, 10))
        # WhatsApp icon
        try:
            wa_img = Image.open("image/whats.png").resize((32, 32))
            wa_imgtk = ImageTk.PhotoImage(wa_img)
            wa_btn = tk.Label(icon_row, image=wa_imgtk, cursor="hand2")
            wa_btn.image = wa_imgtk
            wa_btn.pack(side="left", padx=(10, 5))
            wa_btn.bind("<Button-1>", lambda e: webbrowser.open("https://wa.link/dwgks8"))
        except Exception:
            wa_btn = tb.Button(icon_row, text="WhatsApp", command=lambda: webbrowser.open("https://wa.link/dwgks8"))
            wa_btn.pack(side="left", padx=(10, 5))
        # AQ icon
        try:
            aq_img = Image.open("image/app.ico").resize((32, 32))
            aq_imgtk = ImageTk.PhotoImage(aq_img)
            aq_btn = tk.Label(icon_row, image=aq_imgtk, cursor="hand2")
            aq_btn.image = aq_imgtk
            aq_btn.pack(side="left", padx=(5, 5))
            aq_btn.bind("<Button-1>", lambda e: messagebox.showinfo(
                "To activate NBT SSH",
                "To activate NBT SSH:\n\nUse AQ///Tool or Featureinstaller code.\n\nSend WhatsApp message for assistance"
            ))
        except Exception:
            tb.Button(icon_row, text="AQ", command=lambda: messagebox.showinfo(
                "To activate NBT SSH",
                "To activate NBT SSH:\n\nUse AQ///Tool or Featureinstaller code."
            )).pack(side="left", padx=(5, 5))

        # Quick summary
        tb.Label(scroll_frame, 
                text="This guide shows how to change your vehicle image and add M Key display on NBT systems",
                font=("Helvetica", 12),
                bootstyle="secondary").pack(fill="x", pady=(0, 20))

        # Requirements section
        req_frame = tb.LabelFrame(scroll_frame, text="Requirements", bootstyle="info")
        req_frame.pack(fill="x", padx=10, pady=10)
        req_items = [
            "• Feature Installer Windows 64bit v1.0.14.7",
            "• Free activation code: 8NPSW-CLECW (or purchase new one if expired)",
            "• WinSCP for file transfer",
            "• PuTTY for SSH access",
            "• Properly sized PNG images (378x243 pixels, 32bit)"
        ]
        for item in req_items:
            tb.Label(req_frame, text=item, anchor="w").pack(fill="x", padx=5, pady=2)

        # Step 1 - SSH Access
        self.add_step(scroll_frame, "STEP 1: Enable SSH Access",
            "1. Open Feature Installer with the provided code",
            "2. Enable SSH functionality",
            "3. Close the installer using ISTA or FlashXcode tools",
            ("image/feature_installer.jpg", "Feature Installer interface"),
            "Alternative code purchase: https://www.flashxcode.com/product/feature-installer-code/"
        )

        # Step 2 - Connect to Head Unit (with IP, user, pass, and copy)
        self.add_step(scroll_frame, "STEP 2: Connect to Head Unit",
            "1. Launch WinSCP",
            "2. Use these connection details:",
            None, None,
            [
                "Host: 169.254.199.119",
                "Username: root",
                "Password: ts&SK412 (for NBT1/NBT2EVO)",
                "CIC old: cic0803",
                "CIC new: Hm83stN"
            ],
            ("image/winscp_login.jpg", "WinSCP connection settings"),
            lambda parent: self._add_ip_user_pass(parent)
        )

        # Step 3 - Special Case for NBT2-EVO
        self.add_step(scroll_frame, "STEP 3: Special Handling for NBT2-EVO",
            "For NBT2-EVO that doesn't support SCP directly:",
            "1. Download the attached SCP.BIN file",
            "2. Unzip and copy to FAT32 formatted USB",
            "3. Connect USB to vehicle",
            "4. Use PuTTY to connect (same credentials as WinSCP)",
            "5. Run these commands:",
            [
                "mount -uw qnx6 /net/hu-omap/fs/sda0",
                "mount -uw qnx6 /net/mnt/umass00100t12"
            ],
            "If you get errors during unmount, don't panic. Check USB contents with:",
            [
                "ls -l /fs/usb0",
                "cp /fs/usb0/scp.bin .",
                "chmod +x scp.bin"
            ],
            "Reboot the system (hold Volume + Eject buttons together)"
        )

        # Step 4 - Image Replacement
        self.add_step(scroll_frame, "STEP 4: Replace Vehicle Images",
            "Navigate to these directories to replace images:",
            "For M Key display:",
            "/net/hu-omap/fs/sda0/opt/hmi/ID5/data/ro/bmw/id61/assetDB/Domains/content_preview/PTA_Preview_Guest",
            "/net/hu-omap/fs/sda0/opt/hmi/ID5/data/ro/bmw/id61/assetDB/Domains/content_preview/cp_fahreprofil_aktivieren",
            "For vehicle images (ID6):",
            "id6_hero_xxx.png",
            "id6hero_fxx.png",
            "Vehicle image paths:",
            "hu-omap://opt/hmi/ID5/data/ro/bmw/id61/assetDB/Domains/Main/Heroes",
            ("image/m_key_sample.png", "Example M Key image")
        )

        # Vehicle Model Paths
        model_frame = tb.LabelFrame(scroll_frame, text="Vehicle Model Paths", bootstyle="info")
        model_frame.pack(fill="x", padx=10, pady=10)
        models = [
            "hero_myvehicle_F06", "hero_myvehicle_F12", "hero_myvehicle_F13",
            "hero_myvehicle_F15", "hero_myvehicle_F16", "hero_myvehicle_F20",
            "hero_myvehicle_F21", "hero_myvehicle_F22", "hero_myvehicle_F23",
            "hero_myvehicle_F30", "hero_myvehicle_F31", "hero_myvehicle_F32",
            "hero_myvehicle_F33", "hero_myvehicle_F34", "hero_myvehicle_F36",
            "hero_myvehicle_F39", "hero_myvehicle_F40", "hero_myvehicle_F44",
            "hero_myvehicle_F45", "hero_myvehicle_F46", "hero_myvehicle_F48",
            "hero_myvehicle_F52", "hero_myvehicle_G01", "hero_myvehicle_G02",
            "hero_myvehicle_G11", "hero_myvehicle_G20", "hero_myvehicle_G21",
            "hero_myvehicle_G29", "hero_myvehicle_G30", "hero_myvehicle_G31",
            "hero_myvehicle_G32"
        ]
        model_canvas = tk.Canvas(model_frame, height=150)
        model_scroll = ttk.Scrollbar(model_frame, orient="vertical", command=model_canvas.yview)
        model_inner = tb.Frame(model_canvas)
        model_canvas.configure(yscrollcommand=model_scroll.set)
        model_canvas.pack(side="left", fill="both", expand=True)
        model_scroll.pack(side="right", fill="y")
        model_canvas.create_window((0, 0), window=model_inner, anchor="nw")
        model_inner.bind("<Configure>", lambda e: model_canvas.configure(scrollregion=model_canvas.bbox("all")))
        cols = 4
        for i, model in enumerate(models):
            row = i // cols
            col = i % cols
            tb.Label(model_inner, text=model).grid(row=row, column=col, sticky="w", padx=5, pady=2)

        # Attachments section
        attach_frame = tb.LabelFrame(scroll_frame, text="Attachments", bootstyle="info")
        attach_frame.pack(fill="x", padx=10, pady=10)
        try:
            img = Image.open("image/m_key_sample.png").resize((200, 150))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(attach_frame, image=img_tk)
            img_label.image = img_tk
            self.image_refs.append(img_tk)
            img_label.pack(side="left", padx=10)
        except Exception:
            tk.Label(attach_frame, text="[m_key_sample.png]").pack(side="left", padx=10)
        tb.Label(attach_frame, text="Attached Files:").pack(side="left", padx=10)
        btn_frame = tb.Frame(attach_frame)
        btn_frame.pack(side="left", padx=10)
        tb.Button(btn_frame, 
                 text="Download SCP.BIN", 
                 bootstyle="success",
                 command=lambda: self.download_file("scp.bin")).pack(pady=5)
        tb.Button(btn_frame, 
                 text="Sample M Key Images", 
                 bootstyle="primary",
                 command=lambda: self.download_file("m_key_images.zip")).pack(pady=5)

        # Disclaimer
        tb.Label(scroll_frame, 
                text="Disclaimer: This modification is performed at your own risk. We are not affiliated with BMW AG.",
                font=("Helvetica", 9, "italic"),
                bootstyle="danger",
                wraplength=900).pack(fill="x", pady=20)

    def _add_ip_user_pass(self, parent):
        # Add IP, user, pass with copy buttons
        frame = tb.Frame(parent)
        frame.pack(anchor="w", pady=2, padx=10)
        # IP
        tb.Label(frame, text="IP:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=(0,2), sticky="w")
        ip_block = self.CodeBlock(frame, "169.254.199.119", width=16)  # Use self.CodeBlock
        ip_block.grid(row=0, column=1, padx=(0,10), sticky="w")
        # User
        tb.Label(frame, text="User:", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=(0,2), sticky="w")
        user_block = self.CodeBlock(frame, "root", width=8)  # Use self.CodeBlock
        user_block.grid(row=0, column=3, padx=(0,10), sticky="w")
        # Password
        tb.Label(frame, text="Password:", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=(0,2), sticky="w")
        pass_block = self.CodeBlock(frame, "ts&SK412", width=10)  # Use self.CodeBlock
        pass_block.grid(row=0, column=5, padx=(0,10), sticky="w")

    def add_step(self, parent, title, *args):
        step = tb.Frame(parent)
        step.pack(fill="x", pady=10)
        tb.Label(step, text=title, font=("Helvetica", 13, "bold"), bootstyle="primary").pack(anchor="w")
        for arg in args:
            if callable(arg):
                arg(step)
            elif isinstance(arg, str):
                tb.Label(step, text=arg, wraplength=900, justify="left").pack(anchor="w", pady=2)
            elif isinstance(arg, list):
                code_text = "\n".join(arg)
                code_block = self.CodeBlock(step, code_text)  # Use self.CodeBlock
                code_block.pack(fill="x", padx=10, pady=5)
            elif isinstance(arg, tuple) and len(arg) == 2:
                img_path, caption = arg
                try:
                    img = Image.open(img_path).resize((400, 220))
                    img_tk = ImageTk.PhotoImage(img)
                    lbl = tk.Label(step, image=img_tk)
                    lbl.image = img_tk
                    self.image_refs.append(img_tk)
                    lbl.pack(anchor="w", pady=5)
                except Exception:
                    tk.Label(step, text=f"[{img_path}]").pack(anchor="w", pady=5)
                if caption:
                    tb.Label(step, text=caption, font=("Helvetica", 9, "italic"), bootstyle="secondary").pack(anchor="w")

    def launch_exe(self, exe_name):
        exe_path = os.path.abspath(exe_name)
        if os.path.exists(exe_path):
            try:
                os.startfile(exe_path)
            except Exception:
                messagebox.showinfo("Open", f"Cannot launch {exe_name} directly. Please open it manually:\n{exe_path}")
        else:
            messagebox.showerror("Not found", f"{exe_name} not found in the program folder.")

    def download_file(self, filename):
        if os.path.exists(filename):
            webbrowser.open(filename)
        else:
            messagebox.showerror("Error", f"File not found: {filename}")

    def download_esys(self):
        webbrowser.open("https://mega.nz/file/pZkHnBIY#jiROUGOMJofaU7PGl6R5rVjIoUTYiDGjQQ_Su6kw1E8")

    def download_psdz(self):
        webbrowser.open("https://mega.nz/folder/NjJ3ESqK#DuWNCqX9H75nPoa9Wngyrw/folder/E6xAxbRS")

    def show_emergency_recovery(self):
        recovery_win = tb.Toplevel(self)
        recovery_win.title("Emergency Recovery")
        recovery_win.geometry("600x400")
        
        tb.Label(recovery_win, 
                text="Emergency Recovery Procedures", 
                font=("Helvetica", 14, "bold"), 
                bootstyle="danger").pack(fill="x", pady=10)
        
        tb.Label(recovery_win, 
                text="If your head unit is bricked during flashing:", 
                font=("Helvetica", 10)).pack(anchor="w", padx=10, pady=5)
        
        steps = [
            "1. Disconnect battery for 10 minutes",
            "2. Reconnect power supply",
            "3. Boot into recovery mode (hold MENU + BACK buttons)",
            "4. Connect with E-Sys and attempt recovery flash",
            "5. If unsuccessful, you may need to replace the head unit"
        ]
        
        for step in steps:
            tb.Label(recovery_win, text=step, anchor="w").pack(fill="x", padx=20, pady=2)
        
        tb.Button(recovery_win, 
                 text="Download Recovery Tools", 
                 bootstyle="danger", 
                 command=lambda: webbrowser.open("https://example.com/recovery")).pack(pady=20)
