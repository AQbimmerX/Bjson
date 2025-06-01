# ملف جديد: project_tabs/hdd_guide_tab.py
import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser
import os

class HDDGuideTab(tb.Frame):
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
        self.image_refs = []  # Keep references to images
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

        banner = tb.Label(scroll_frame, text="NBT EVO HDD CHANGING TUTORIAL", font=("Helvetica", 18, "bold"), bootstyle="inverse-primary", padding=10)
        banner.pack(fill="x", pady=(0, 10))

        icon_row = tb.Frame(scroll_frame)
        icon_row.pack(fill="x", pady=(0, 10))
        try:
            wa_img = Image.open("images/whats.png").resize((32, 32))
            wa_imgtk = ImageTk.PhotoImage(wa_img)
            wa_btn = tk.Label(icon_row, image=wa_imgtk, cursor="hand2")
            wa_btn.image = wa_imgtk
            wa_btn.pack(side="left", padx=(10, 5))
            def open_whatsapp(event):
                webbrowser.open("https://wa.link/dwgks8")
            wa_btn.bind("<Button-1>", open_whatsapp)
        except Exception:
            wa_btn = tb.Button(icon_row, text="WhatsApp", command=lambda: webbrowser.open("https://wa.link/dwgks8"))
            wa_btn.pack(side="left", padx=(10, 5))
        try:
            aq_img = Image.open("images/app.ico").resize((32, 32))
            aq_imgtk = ImageTk.PhotoImage(aq_img)
            aq_btn = tk.Label(icon_row, image=aq_imgtk, cursor="hand2")
            aq_btn.image = aq_imgtk
            aq_btn.pack(side="left", padx=(5, 5))
            def show_ssh_info(event):
                messagebox.showinfo(
                    "To activate NBT SSH",
                    "To activate NBT SSH:\n\n"
                    "Use AQ///Tool or Featureinstaller code.\n\n"
                    "send whatsapp message\n\n"
                )
            aq_btn.bind("<Button-1>", show_ssh_info)
        except Exception:
            aq_btn = tb.Button(icon_row, text="AQ", command=lambda: messagebox.showinfo(
                "To activate NBT SSH",
                "To activate NBT SSH:\n\nUse AQ///Tool or Featureinstaller code.\n\nAQ icon = images/app.ico"
            ))
            aq_btn.pack(side="left", padx=(5, 5))

        tb.Label(scroll_frame, text="Note: This tutorial is shown how to do it on NBT EVO ID4/5/6 units, BUT process is very similar for NBT units as well. If you have common sense, you will succeed with it on NBT too.", bootstyle="warning", wraplength=900, padding=10).pack(fill="x", pady=5)

        tb.Label(scroll_frame, text="HOW DO YOU KNOW IF YOU NEED TO CHANGE YOUR HDD?", font=("Helvetica", 14, "bold"), bootstyle="primary").pack(anchor="w", pady=(20, 0))
        tb.Label(scroll_frame, text="Usually when NBT or EVO HDD fails, head unit starts rebooting, you hear the clicking sound from the unit, maps being stuck on loading screen, you can't use bluetooth audio, USB Flash drives are not recognized when inserted.\nNot necessary all of the mentioned symptoms will occur when HDD fails, it might be one symptom, or might be few of them.", wraplength=900, justify="left").pack(anchor="w", pady=5)

        tb.Label(scroll_frame, text="HDD CHANGING IS DONE IN SEVEN STEPS:", font=("Helvetica", 14, "bold"), bootstyle="primary").pack(anchor="w", pady=(20, 0))
        steps = [
            "Remove your faulty HDD from the Head Unit",
            "Install new HDD in Head Unit",
            "Enable SSH access",
            "Initialize new HDD",
            "Flash Head Unit",
            "Install map data",
            "Install gracenote"
        ]
        steps_frame = tb.Frame(scroll_frame)
        steps_frame.pack(anchor="w", fill="x", padx=20, pady=5)
        for i, s in enumerate(steps, 1):
            tb.Label(steps_frame, text=f"{i}. {s}", font=("Helvetica", 12), anchor="w").pack(anchor="w", pady=1)

        video_frame = tb.Frame(scroll_frame)
        video_frame.pack(fill="x", pady=10)
        try:
            img = Image.open("images/hdd1.jpg").resize((400, 220))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(video_frame, image=img_tk)
            lbl.image = img_tk
            self.image_refs.append(img_tk)
            lbl.pack(side="left", padx=10)
        except Exception:
            tk.Label(video_frame, text="[hdd1.jpg]").pack(side="left", padx=10)

        # --- Embed YouTube video in the right space using tkhtmlview if available ---
        try:
            from tkhtmlview import HTMLLabel
            yt_html = """
            <iframe width="400" height="220" src="https://www.youtube.com/embed/MHpItaBhS-w?start=1"
            frameborder="0" allowfullscreen></iframe>
            """
            yt_label = HTMLLabel(video_frame, html=yt_html)
            yt_label.pack(side="right", padx=10, fill="both", expand=False)
        except Exception:
            # Fallback: open YouTube externally
            tb.Button(
                video_frame,
                text="Watch Video on YouTube",
                bootstyle="info",
                command=lambda: webbrowser.open("https://www.youtube.com/watch?v=MHpItaBhS-w&t=1s")
            ).pack(side="right", padx=10)
        # --------------------------------------------------------------------------

        # Download file button (downloads the attached file when clicked)
        def download_attached_file():
            import requests
            file_url = "https://github.com/AQbimmerX/Bjson/raw/main/images/hdd.mp4"
            local_filename = os.path.join("images", "hdd.mp4")
            try:
                os.makedirs("images", exist_ok=True)
                r = requests.get(file_url, stream=True)
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                messagebox.showinfo("Download Complete", f"File downloaded as {local_filename}")
            except Exception as e:
                messagebox.showerror("Download Failed", f"Error: {e}")

        tb.Button(
            video_frame,
            text="Download Video File",
            bootstyle="success",
            command=download_attached_file
        ).pack(side="right", padx=10)
        # -------------------------------------------------------

        self.add_step(scroll_frame, "STEP 1 (Removing faulty HDD)",
            "Unscrew four bolts from the top cover. (MARKED RED IN PICTURE BELOW).",
            ("images/hdd1.jpg", "Red circles show the four bolts to remove"),
            "Remove top cover and loosen the centre bolt (MARKED RED IN PICTURE BELOW) then remove DVD-Rom from head unit by lifting it up.",
            ("images/hdd2.jpg", "Center bolt location for DVD-ROM removal"),
        )
        self.add_step(scroll_frame, "STEP 2 (Installing new HDD)",
            "Just assemble everything back, but do not rush to screw all the bolts back, assemble everything and power the unit in car or on bench, just to see if it is not rebooting, common issue when units are rebooting when installed new HDD.",
            ("images/hdd33.jpg", "New HDD installation"),
            "What to do if unit is rebooting?\nRemove HDD, power unit without it and only then install HDD, unit will stop rebooting and you will be able to do the further work."
        )
        self.add_step(scroll_frame, "STEP 3 (Enabling SSH access)",
            "This part is on you, there are several ways to activate SSH access, HU TOOL, Feature Installer, and others.\nI prefer Feature Installer, as it is the easiest way, just get the activation code from one of thousands resellers.",
            ("images/hdd3.jpg", "Different methods to enable SSH access")
        )
        self.add_step(scroll_frame, "STEP 4 (Initialize new HDD)",
            "After enabling SSH access to your head unit, now you are able to initialize your new HDD with PuTTY.\nOpen PuTTY, enter the EVO IP address 169.254.199.119 and port 22",
            ("images/step4_putty.png", "PuTTY configuration screen"),
            lambda parent: tb.Button(parent, text="Launch PuTTY", bootstyle="info", command=lambda: self.launch_exe("putty.exe")).pack(anchor="w", padx=10, pady=5),
            "PuTTY Configuration\nLog in with these credentials:\nUser: root\nPassword: ts&SK412\n\nWhen logged in, enter these commands:",
            None, None,
            [
                "create_hdd.sh -c partition",
                "create_hdd.sh -c format",
                "create_hdd.sh -c mount",
                "OnOfIDSICommander appreset"
            ],
            "Head unit will reboot, close PuTTY and open it again, login with the same credentials like before, and enter the last command that is mentioned below.\nIf your head unit is restarting after reboot – refer to the STEP2 and do the same as you did earlier.",
            None, None,
            ["create_hdd.sh -c directories"],
            "Reboot is needed as often without reboot it will just not create the directories.\nYour HDD is now initialized! You can continue on the next steps."
        )
        self.add_step(scroll_frame, "STEP 5 (Flashing your unit)",
            "This tutorial is how to change HDD, if you are doing it by your self you should know how to flash your head unit, so i will not cover this part.\nYou can flash your unit in full (BTLD, SWFL, CAFD, IBAD), or if your psdzdata is matching your head units actual software level, you can flash only IBADs.",
            ("images/step5_flash.jpg", "Flashing options for NBT EVO")
        )
        step6 = tb.Frame(scroll_frame)
        step6.pack(fill="x", pady=10)
        tb.Label(step6, text="STEP 6 (Installing map data)", font=("Helvetica", 13, "bold"), bootstyle="primary").pack(anchor="w")
        tb.Label(step6, text="Same as with flashing, will not cover this step in details, as if you are doing this procedure, you should know how to do it.\nLong story short:\nDownload map data, copy to USB flash drive, in FSC directory insert your map update FSC, insert USB in car, update.", wraplength=900, justify="left").pack(anchor="w", pady=5)
        try:
            img = Image.open("images/step6_maps.jpg").resize((400, 220))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(step6, image=img_tk)
            lbl.image = img_tk
            lbl.pack(anchor="w", pady=5)
            self.image_refs.append(img_tk)
        except Exception:
            tk.Label(step6, text="[images/step6_maps.jpg]").pack(anchor="w", pady=5)
        tb.Label(step6, text="Map data installation process", font=("Helvetica", 9, "italic"), bootstyle="secondary").pack(anchor="w")
        tb.Button(step6, text="Run FeatureInstaller.exe", bootstyle="info", command=lambda: self.launch_exe("FeatureInstaller.exe")).pack(pady=10)

        tb.Label(scroll_frame, text="Some facts:", font=("Helvetica", 13, "bold"), bootstyle="primary").pack(anchor="w", pady=(20, 0))
        facts = [
            "Switching from HDD to SSD will not improve your head unit performance in any way!",
            "Not all HDDs are working with NBT and EVO units, it's up to you to find working ones, there are lots of information on forums, do the research.",
            "After you install HDD in your unit and power it up, HDD is immediately being locked, yes, it is possible to unlock, but that's a different procedure."
        ]
        for fact in facts:
            tb.Label(scroll_frame, text="• " + fact, wraplength=900, justify="left").pack(anchor="w", padx=20)

        tb.Button(scroll_frame, text="Launch AQEVO Tool", bootstyle="primary", command=lambda: self.launch_exe("evoAQtool.v1.exe")).pack(pady=20)

    def add_step(self, parent, title, *args):
        step = tb.Frame(parent)
        step.pack(fill="x", pady=10)
        tb.Label(step, text=title, font=("Helvetica", 13, "bold"), bootstyle="primary").pack(anchor="w")
        for arg in args:
            if callable(arg):
                arg(step)
            elif isinstance(arg, str):
                tb.Label(step, text=arg, wraplength=900, justify="left", font=("Helvetica", 13)).pack(anchor="w", pady=2)
            elif isinstance(arg, list):
                code_text = "\n".join(arg)
                code_block = self.CodeBlock(step, code_text)
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
            messagebox.showerror("CANT RAUN", f"{exe_name} connect developer to get app.")