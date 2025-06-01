# ملف جديد: project_tabs/flash_guide_tab.py
import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser
import os

class FlashGuideTab(tb.Frame):
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

            # Copy button
            copy_btn = tb.Button(self, text="Copy", bootstyle="secondary", command=self.copy_to_clipboard)
            copy_btn.pack(side="right", padx=5)

        def copy_to_clipboard(self):
            self.master.clipboard_clear()
            self.master.clipboard_append(self.code_text)

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.setup_ui()

    def back_to_retrofits(self):
        # Dummy method to avoid AttributeError
        pass

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

        # مربع وصول سريع مثل hdd retrofit
        quick_access = tb.Frame(scroll_frame, bootstyle="info", padding=10)
        quick_access.pack(fill="x", pady=(10, 20))
        try:
            img = Image.open("image/bmw_flash.jpg")
            img.thumbnail((120, 120))
            img_tk = ImageTk.PhotoImage(img)
            img_lbl = tk.Label(quick_access, image=img_tk)
            img_lbl.image = img_tk
            img_lbl.pack(side="left", padx=10)
        except Exception:
            tk.Label(quick_access, text="[bmw_flash.jpg]", width=15).pack(side="left", padx=10)
        tb.Label(quick_access, text="NBT EVO FLASH\ncarplay full screen", font=("Helvetica", 12, "bold")).pack(side="left", padx=10)
        tb.Button(quick_access, text="Back to Retrofits", bootstyle="secondary", command=self.back_to_retrofits).pack(side="right", padx=10)

        # Header
        tb.Label(scroll_frame, 
                text="NBT EVO Flashing Tutorial with E-Sys + ICOM/ENET", 
                font=("Helvetica", 18, "bold"), 
                bootstyle="inverse-primary", 
                padding=10).pack(fill="x", pady=(0, 10))
        tb.Label(scroll_frame, 
                text="Complete DIY guide for flashing NBT EVO head units", 
                font=("Helvetica", 12), 
                bootstyle="secondary").pack(fill="x", pady=(0, 20))

        # Warning
        tb.Label(scroll_frame, 
                text="Warning: This procedure involves risks. Make sure you have proper battery charger connected (at least 50A) and backup all data before proceeding.", 
                bootstyle="warning", 
                wraplength=900, 
                padding=10).pack(fill="x", pady=5)

        # Buttons
        btn_frame = tb.Frame(scroll_frame)
        btn_frame.pack(fill="x", pady=10)
        tb.Button(btn_frame, 
                 text="Launch AQ///Cheat Tool", 
                 bootstyle="primary", 
                 command=lambda: self.launch_exe("/apps/AQCheatTool.exe")).pack(side="left", padx=5)
        tb.Button(btn_frame, 
                 text="Download E-Sys 3.30.1", 
                 bootstyle="success", 
                 command=self.download_esys).pack(side="left", padx=5)
        tb.Button(btn_frame, 
                 text="PSdZData Full", 
                 bootstyle="info", 
                 command=self.download_psdz).pack(side="left", padx=5)

        # Introduction
        tb.Label(scroll_frame, 
                text="Introduction", 
                font=("Helvetica", 14, "bold"), 
                bootstyle="primary").pack(anchor="w", pady=(20, 0))
        tb.Label(scroll_frame, 
                text="This tutorial will guide you through the process of flashing your NBT EVO head unit to enable features like Apple CarPlay full screen. The process can be done with either ICOM or ENET interface.", 
                wraplength=900, 
                justify="left").pack(anchor="w", pady=5)

        # Tabbed interface for ICOM/ENET
        self.setup_tab_interface(scroll_frame)

        # Step-by-Step Guide
        tb.Label(scroll_frame, 
                text="Step-by-Step Flashing Guide", 
                font=("Helvetica", 14, "bold"), 
                bootstyle="primary").pack(anchor="w", pady=(20, 0))

        self.add_step(scroll_frame, "Step 1: Prepare Your Equipment",
            "• 50A battery charger connected to OBD port\n"
            "• E-Sys 3.30.1 with PSdZData Full\n"
            "• ICOM or ENET interface\n"
            "• AQ///Cheat Tool (optional but recommended)",
            "images/setup.jpg", "Proper setup with battery charger"
        )

        self.add_step(scroll_frame, "Step 2: Connect to Vehicle",
            "1. Launch E-Sys\n"
            "2. Click 'Open Connection'\n"
            "3. Select your connection type (ICOM or ENET)\n"
            "4. For ICOM: Use `tcp://169.254.92.38:50160`\n"
            "5. For ENET: Use `tcp://169.254.99.82:6801`\n"
            "6. Click 'Connect'",
            "images/esys_connect.jpg", "E-Sys connection settings"
        )

        self.add_step(scroll_frame, "Step 3: Read V ehicle Data",
            "1. Read FA (Vehicle Order) and save it\n"
            "2. Right-click on FA folder and select 'Activate FA'\n"
            "3. Click 'Read SVT' (Skip BDC_BODY for F85)\n"
            "4. Save SVT as `SVT_ist`\n"
            "5. Select same I-Step (Shipment) under Target/KIS/SVT\n"
            "6. Select latest I-Step (Target)\n"
            "7. Choose 'Complete Flash' on right side\n"
            "8. Click 'Calculate'\n"
            "9. Save as `SVT_soll`\n"
            "10. Click 'Calculate' under TAL list\n"
            "11. Click OK (you may get a warning)\n"
            "12. Save calculation as `SVT_tal`"
        )

        self.add_step(scroll_frame, "Step 4: Process TAL",
            "1. Click 'Expert Mode' on left side\n"
            "2. Click 'Tal...' (3 dots) and open `SVT_tal`\n"
            "3. TAL will show all ECUs needing update\n"
            "4. Click 'SVT...' (3 dots) and open `SVT_soll`\n"
            "5. Click 'FA...' (3 dots) and read FA\n"
            "6. Click 'Read VIN' outside FA\n"
            "7. Select all necessary updates or individual modules\n"
            "8. For NBT EVO, select `HU_NBT_63` with `bFlash`, `swDeploy`, `cdDeploy`, and `ibaDeploy`\n"
            "9. Click 'Check software availability'",
            None, None,
            "Important: Make sure you have all required software files available before proceeding.",
            "warning"
        )

        self.add_step(scroll_frame, "Step 5: Start Flashing",
            "1. Click 'Start' to begin flashing process\n"
            "2. Monitor progress in ECU Parameters Log\n"
            "3. Do not interrupt the process\n"
            "4. Wait for confirmation message",
            "images/flashing.jpg", "Flashing progress in E-Sys"
        )

        self.add_step(scroll_frame, "Step 6: Post-Flash Configuration",
            "After successful flash, enable Apple CarPlay full screen:",
            None, None,
            "HMI_ID_VERSION => id6_light\n"
            "APPLE_ENHANCEMENTS => aktiv\n"
            "HMI/CARPLAY_FULLSCREEN => aktiv",
            None, None,
            "Success! Your NBT EVO should now be updated to the latest version with full screen Apple CarPlay capability.",
            "success"
        )

        # Troubleshooting
        tb.Label(scroll_frame, 
                text="Troubleshooting", 
                font=("Helvetica", 14, "bold"), 
                bootstyle="primary").pack(anchor="w", pady=(20, 0))

        # Create a table for troubleshooting
        table_frame = tb.Frame(scroll_frame)
        table_frame.pack(fill="x", pady=10)

        # Table headers
        tb.Label(table_frame, text="Error", font=("Helvetica", 10, "bold"), 
                bootstyle="inverse-secondary", width=40).grid(row=0, column=0, sticky="w")
        tb.Label(table_frame, text="Solution", font=("Helvetica", 10, "bold"), 
                bootstyle="inverse-secondary", width=60).grid(row=0, column=1, sticky="w")

        # Table rows
        issues = [
            ("VCM not activating [C197]", "Check battery voltage and connection"),
            ("TAL validation failed [C205]", "Recalculate TAL and verify FA"),
            ("Asynchronous programming [C049]", "Check all ECUs in TAL and retry"),
            ("DVD drive not ready", "Remove any discs before flashing")
        ]

        for i, (error, solution) in enumerate(issues, 1):
            tb.Label(table_frame, text=error, width=40, wraplength=400).grid(row=i, column=0, sticky="w")
            tb.Label(table_frame, text=solution, width=60, wraplength=600).grid(row=i, column=1, sticky="w")

        # Danger Zone
        danger_frame = tb.Frame(scroll_frame, bootstyle="danger")
        danger_frame.pack(fill="x", pady=20)
        tb.Label(danger_frame, 
                text="DANGER ZONE", 
                font=("Helvetica", 14, "bold"), 
                bootstyle="inverse-danger").pack(fill="x", pady=(5, 10))
        tb.Label(danger_frame, 
                text="Improper flashing can brick your head unit. Always:", 
                font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10)
        
        precautions = [
            "• Use proper power supply (50A minimum)",
            "• Verify all files before flashing",
            "• Don't interrupt the process",
            "• Have backup recovery plan"
        ]
        
        for prec in precautions:
            tb.Label(danger_frame, text=prec, anchor="w").pack(fill="x", padx=20, pady=2)

        # Bottom buttons
        btn_frame_bottom = tb.Frame(scroll_frame)
        btn_frame_bottom.pack(fill="x", pady=20)
        tb.Button(btn_frame_bottom, 
                 text="Launch AQEVO Tool", 
                 bootstyle="primary", 
                 command=lambda: self.launch_exe("AQCheatTool.exe")).pack(side="left", padx=5)
        tb.Button(btn_frame_bottom, 
                 text="Emergency Recovery", 
                 bootstyle="danger", 
                 command=self.show_emergency_recovery).pack(side="left", padx=5)

    def setup_tab_interface(self, parent):
        # Create notebook for tabs
        tab_control = tb.Notebook(parent)
        tab_control.pack(fill="x", pady=10)

        # ICOM Tab
        icom_tab = tb.Frame(tab_control)
        tab_control.add(icom_tab, text="ICOM Method")

        # ENET Tab
        enet_tab = tb.Frame(tab_control)
        tab_control.add(enet_tab, text="ENET Method")

        # Add content to ICOM tab
        tb.Label(icom_tab, 
                text="ICOM Configuration", 
                font=("Helvetica", 12, "bold"), 
                bootstyle="primary").pack(anchor="w", pady=(5, 0))
        tb.Label(icom_tab, 
                text="For ICOM interface, use these settings:", 
                wraplength=900).pack(anchor="w", pady=5)
        
        code_text_icom = (
            "ConnectionMode = STATIC_IP\n"
            "ip = 192.168.68.85\n"
            "Netmask = 255.255.255.0\n"
            "Gateway = 192.168.68.99"
        )
        code_block_icom = self.CodeBlock(icom_tab, code_text_icom)
        code_block_icom.pack(fill="x", padx=5, pady=5)

        tb.Label(icom_tab, 
                text="DHCP Server Configuration", 
                font=("Helvetica", 15, "bold"), 
                bootstyle="primary").pack(anchor="w", pady=(10, 0))
        tb.Label(icom_tab, 
                text="", 
                wraplength=900).pack(anchor="w", pady=5)
        tb.Label(icom_tab, 
                text="Example DHCPSRV.INI configuration:", 
                wraplength=900).pack(anchor="w", pady=5)
        
        code_text_dhcp = (
            "[GLOBALS]\n"
            "IPPOOL_1=192.168.68.1-254\n"
            "IPBIND_1=192.168.68.99\n"
            "AssociateBindsToPools=1\n"
            "LEASETIME=86400\n"
            "NODETYPE=8\n"
            "SUBNET_MASK=255.255.255.0\n"
            "ROUTER=192.168.68.1"
        )
        code_block_dhcp = self.CodeBlock(icom_tab, code_text_dhcp)
        code_block_dhcp.pack(fill="x", padx=5, pady=5)

        # Add content to ENET tab
        tb.Label(enet_tab, 
                text="ENET Configuration", 
                font=("Helvetica", 12, "bold"), 
                bootstyle="primary").pack(anchor="w", pady=(5, 0))
        tb.Label(enet_tab, 
                text="For ENET interface, follow these steps:", 
                wraplength=900).pack(anchor="w", pady=5)
        
        steps = [
            "1. Go to Network Connections",
            "2. Open Properties of your Ethernet adapter",
            "3. Select Internet Protocol Version 4 (TCP/IPv4)",
            "4. Configure with these settings:",
            "   IP address: 169.254.92.38",
            "   Subnet mask: 255.255.255.0",
            "5. Run ZGW_SEARCH from E:/EDIABAS/Hardware/ENET"
        ]
        
        for step in steps:
            tb.Label(enet_tab, text=step, anchor="w").pack(fill="x", padx=10, pady=2)

    def add_step(self, parent, title, *args):
        step = tb.Frame(parent)
        step.pack(fill="x", pady=10)
        tb.Label(step, text=title, font=("Helvetica", 13, "bold"), bootstyle="primary").pack(anchor="w")
        for arg in args:
            if callable(arg):
                # إذا كان العنصر دالة (زر أو عنصر ديناميكي)، نفذها مع تمرير الإطار الحالي
                arg(step)
            elif isinstance(arg, str):
                # Special handling for user/pass and ip/port in step 4
                if "STEP 4" in title.upper() and "User: root" in arg and "Password:" in arg:
                    creds_frame = tb.Frame(step)
                    creds_frame.pack(anchor="w", pady=2, padx=10)
                    # IP & Port (short bars, above user/pass)
                    ip_label = tb.Label(creds_frame, text="IP:", font=("Helvetica", 10, "bold"))
                    ip_label.grid(row=0, column=0, padx=(0,2), sticky="w")
                    try:
                        ip_block = self.CodeBlock(creds_frame, "169.254.199.119", width=16)
                        ip_block.grid(row=0, column=1, padx=(0,10), sticky="w")
                    except Exception as e:
                        tb.Label(creds_frame, text="169.254.199.119").grid(row=0, column=1, padx=(0,10), sticky="w")
                    port_label = tb.Label(creds_frame, text="Port:", font=("Helvetica", 10, "bold"))
                    port_label.grid(row=0, column=2, padx=(0,2), sticky="w")
                    try:
                        port_block = self.CodeBlock(creds_frame, "22", width=5)
                        port_block.grid(row=0, column=3, padx=(0,10), sticky="w")
                    except Exception as e:
                        tb.Label(creds_frame, text="22").grid(row=0, column=3, padx=(0,10), sticky="w")
                    # User & Password (short bars)
                    user_label = tb.Label(creds_frame, text="User:", font=("Helvetica", 10, "bold"))
                    user_label.grid(row=1, column=0, padx=(0,2), sticky="w")
                    try:
                        user_block = self.CodeBlock(creds_frame, "root", width=8)
                        user_block.grid(row=1, column=1, padx=(0,10), sticky="w")
                    except Exception as e:
                        tb.Label(creds_frame, text="root").grid(row=1, column=1, padx=(0,10), sticky="w")
                    pass_label = tb.Label(creds_frame, text="Password:", font=("Helvetica", 10, "bold"))
                    pass_label.grid(row=1, column=2, padx=(0,2), sticky="w")
                    try:
                        pass_block = self.CodeBlock(creds_frame, "ts&SK412", width=10)
                        pass_block.grid(row=1, column=3, padx=(0,10), sticky="w")
                    except Exception as e:
                        tb.Label(creds_frame, text="ts&SK412").grid(row=1, column=3, padx=(0,10), sticky="w")
                else:
                    # Make explanation text larger
                    tb.Label(step, text=arg, wraplength=900, justify="left", font=("Helvetica", 13)).pack(anchor="w", pady=2)
            elif isinstance(arg, list):
                # Show command list as code block with copy icon if in step 4 (by title)
                if "STEP 4" in title.upper():
                    code_text = "\n".join(arg)
                    code_block = self.CodeBlock(step, code_text)
                    code_block.pack(fill="x", padx=10, pady=5)
                else:
                    for cmd in arg:
                        tb.Label(step, text=cmd, font=("Consolas", 10), bootstyle="secondary").pack(anchor="w", padx=20)
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

