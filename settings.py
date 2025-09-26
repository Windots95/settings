import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import threading
import time
import getpass
import ctypes
from datetime import datetime

class SettingsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows Settings Simulator")
        self.geometry("1000x600")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        self.tutorial_done = False

        self.create_top_bar()
        self.create_bottom_recommended()
        self.create_main_frame()
        self.create_hamburger_menu()
        self.show_home_screen()

        # Define searchable items mapping
        self.search_mapping = {
            "user": self.open_accounts,
            "account": self.open_accounts,
            "bluetooth": lambda: self.open_category("Bluetooth & Devices"),
            "devices": lambda: self.open_category("Bluetooth & Devices"),
            "system": lambda: self.open_category("System"),
            "taskbar": lambda: self.open_system_feature("Display"),
            "display": lambda: self.open_system_feature("Display"),
            "windows update": lambda: self.open_category("Windows Update"),
            "update": lambda: self.open_category("Windows Update"),
            "personalize": lambda: self.open_system_feature("Display")
        }

    # -------------------- Top Bar --------------------
    def create_top_bar(self):
        self.top_bar = tk.Frame(self, bg="#0078D7", height=50)
        self.top_bar.pack(side="top", fill="x")

        self.settings_label = tk.Label(self.top_bar, text="Settings", fg="white", bg="#0078D7", font=("Segoe UI", 16))
        self.settings_label.place(x=10, y=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.top_bar, textvariable=self.search_var, width=30)
        self.search_entry.place(x=150, y=12)
        self.search_entry.bind("<FocusIn>", self.show_search_bar)
        self.search_entry.bind("<FocusOut>", self.hide_search_bar)
        self.search_button = tk.Button(self.top_bar, text="🔍", command=self.search_settings)
        self.search_button.place(x=400, y=10)

        self.wifi_button = tk.Button(self.top_bar, text="📶", bg="#0078D7", fg="white", borderwidth=0)
        self.wifi_button.place(x=900, y=10)

        self.up_arrow_button = tk.Button(self.top_bar, text="⬆", bg="#0078D7", fg="white", borderwidth=0, command=self.open_about_settings)
        self.up_arrow_button.place(x=940, y=10)

        self.hamburger_button = tk.Button(self.top_bar, text="☰", bg="#0078D7", fg="white", borderwidth=0, command=self.toggle_hamburger)
        self.hamburger_button.place(x=460, y=10)

    def show_search_bar(self, event):
        self.search_entry.place(x=150, y=12)
        self.search_button.place(x=400, y=10)

    def hide_search_bar(self, event):
        self.search_entry.place_forget()
        self.search_button.place_forget()

    # -------------------- Bottom Recommended --------------------
    def create_bottom_recommended(self):
        self.bottom_frame = tk.Frame(self, bg="#e0e0e0", height=80)
        self.bottom_frame.pack(side="bottom", fill="x")

        recommended = ["Lock Screen", "Sounds", "Mouse", "Pointer", "Touch", "Bluetooth", "Personalize"]
        for i, item in enumerate(recommended):
            btn = tk.Button(self.bottom_frame, text=item, command=lambda it=item: self.open_recommended(it))
            btn.grid(row=0, column=i, padx=10, pady=10)

    # -------------------- Main Frame --------------------
    def create_main_frame(self):
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="top", fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # -------------------- Hamburger Menu --------------------
    def create_hamburger_menu(self):
        self.menu_frame = tk.Frame(self, bg="#e6e6e6", width=250, height=600)
        self.menu_frame.place(x=-250, y=50)
        self.menu_visible = False

        self.account_label = tk.Label(self.menu_frame, text="User Account", bg="#cccccc", width=30)
        self.account_label.pack(pady=10)

        self.close_menu_button = tk.Button(self.menu_frame, text="⬅ Close Menu", command=self.toggle_hamburger)
        self.close_menu_button.pack(pady=5)

        menu_items = ["System", "Bluetooth & Devices", "Network & Internet", "Personalized Apps",
                      "Accounts", "Time & Language", "Gaming", "Activities", "Privacy & Security", "Windows Update"]
        self.menu_buttons = []
        for item in menu_items:
            btn = tk.Button(self.menu_frame, text=item, width=25, command=lambda i=item: self.open_category(i))
            btn.pack(pady=2)
            self.menu_buttons.append(btn)

    def toggle_hamburger(self):
        def slide():
            x = self.menu_frame.winfo_x()
            if not self.menu_visible:
                for i in range(x, 0, 10):
                    self.menu_frame.place(x=i, y=50)
                    self.update()
            else:
                for i in range(x, -250, -10):
                    self.menu_frame.place(x=i, y=50)
                    self.update()
            self.menu_visible = not self.menu_visible
        threading.Thread(target=slide).start()

    # -------------------- Home Screen --------------------
    def show_home_screen(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Home", font=("Segoe UI", 24)).pack(pady=20)
        tk.Label(self.main_frame, text="Welcome to Settings Simulator", font=("Segoe UI", 14)).pack(pady=10)

    # -------------------- Category Screens --------------------
    def open_category(self, category):
        self.clear_main_frame()
        tk.Label(self.main_frame, text=category, font=("Segoe UI", 20)).pack(pady=10)

        if category == "System":
            buttons = ["Display", "Sound", "Notifications", "Power & Battery", "Storage", "Nearby Sharing", "Activation"]
            for b in buttons:
                btn = tk.Button(self.main_frame, text=b, width=20, command=lambda n=b: self.open_system_feature(n))
                btn.pack(pady=5)

        elif category == "Windows Update":
            tk.Label(self.main_frame, text="Windows Update", font=("Segoe UI", 16)).pack(pady=10)
            self.update_status_label = tk.Label(self.main_frame, text="You're up to date ✅")
            self.update_status_label.pack(pady=5)
            tk.Button(self.main_frame, text="Check for Updates", command=self.check_updates).pack(pady=5)

        elif category == "Bluetooth & Devices":
            tk.Label(self.main_frame, text="Paired Bluetooth Devices", font=("Segoe UI", 14)).pack(pady=10)
            tk.Label(self.main_frame, text="Device 1\nDevice 2\nDevice 3").pack(pady=5)

        elif category == "Accounts":
            self.open_accounts()

        elif category == "Network & Internet":
            self.open_wifi()

        elif category == "Time & Language":
            tk.Label(self.main_frame, text=f"Current Time: {datetime.now().strftime('%H:%M:%S')}", font=("Segoe UI", 14)).pack(pady=5)
            tk.Label(self.main_frame, text=f"Current Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Segoe UI", 14)).pack(pady=5)
            tk.Label(self.main_frame, text=f"Time Zone: {time.tzname[0]}", font=("Segoe UI", 14)).pack(pady=5)

        elif category == "Gaming":
            tk.Label(self.main_frame, text="Gaming Bar: Enabled", font=("Segoe UI", 14)).pack(pady=5)
            tk.Label(self.main_frame, text="Game Mode: Enabled", font=("Segoe UI", 14)).pack(pady=5)
            tk.Label(self.main_frame, text="Captions: Enabled", font=("Segoe UI", 14)).pack(pady=5)

        else:
            tk.Label(self.main_frame, text=f"{category} options coming soon...").pack(pady=10)

    def open_system_feature(self, feature):
        self.clear_main_frame()
        tk.Label(self.main_frame, text=feature, font=("Segoe UI", 16)).pack(pady=10)
        if feature == "Display":
            tk.Button(self.main_frame, text="Change Background Color", command=self.change_background_color).pack(pady=5)
            tk.Button(self.main_frame, text="Back", command=lambda: self.open_category("System")).pack(pady=20)
        else:
            tk.Label(self.main_frame, text=f"{feature} options coming soon").pack(pady=10)
            tk.Button(self.main_frame, text="Back", command=lambda: self.open_category("System")).pack(pady=20)

    # -------------------- Search --------------------
    def search_settings(self):
        query = self.search_var.get().lower()
        found = False
        for key in self.search_mapping:
            if key in query:
                found = True
                def animate_open():
                    for _ in range(3):
                        self.main_frame.config(bg="#cce7ff")
                        self.update()
                        time.sleep(0.1)
                        self.main_frame.config(bg="white")
                        self.update()
                        time.sleep(0.1)
                    self.search_mapping[key]()
                threading.Thread(target=animate_open).start()
                break
        if not found:
            messagebox.showinfo("Search", f"No results found for '{query}'")

    # -------------------- Accounts --------------------
    def open_accounts(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text=f"Account: {getpass.getuser()}", font=("Segoe UI", 14)).pack(pady=10)
        tk.Label(self.main_frame, text="Rewards: Coming Soon").pack(pady=5)
        tk.Label(self.main_frame, text="OneDrive: Coming Soon").pack(pady=5)

    # -------------------- Wi-Fi --------------------
    def open_wifi(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Available Wi-Fi Networks", font=("Segoe UI", 16)).pack(pady=10)
        networks = ["HomeWiFi", "OfficeNetwork", "GuestNetwork", "MobileHotspot"]
        for n in networks:
            tk.Label(self.main_frame, text=n).pack()

    # -------------------- Change Desktop Color --------------------
    def change_background_color(self):
        color_code = colorchooser.askcolor(title="Choose background color")[1]
        if color_code:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, color_code, 3)
            messagebox.showinfo("Background", f"Background color changed to {color_code}")

    # -------------------- Windows Update --------------------
    def check_updates(self):
        def update_process():
            try:
                self.update_status_label.config(text="Checking for updates...")
            except AttributeError:
                self.update_status_label = tk.Label(self.main_frame, text="Checking for updates...")
                self.update_status_label.pack(pady=5)
            self.update()
            time.sleep(5)
            self.update_status_label.config(text="You're up to date ✅")
        threading.Thread(target=update_process).start()

    # -------------------- Bottom Recommended --------------------
    def open_recommended(self, item):
        messagebox.showinfo(item, f"{item} settings opened (simulated)")

    # -------------------- About Settings & Tutorial --------------------
    def open_about_settings(self):
        about_window = tk.Toplevel(self)
        about_window.title("About Settings")
        about_window.geometry("400x300")
        tk.Label(about_window, text="About Settings", font=("Segoe UI", 16)).pack(pady=10)
        tk.Button(about_window, text="Full Tutorial", command=lambda: self.start_tutorial(about_window)).pack(pady=20)
        tk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=20)

    def start_tutorial(self, window):
        if self.tutorial_done:
            messagebox.showinfo("Tutorial", "Tutorial already completed!")
            return

        tutorial_steps = [
            ("Clicking Hamburger Menu", self.toggle_hamburger),
            ("This is your Apps section", lambda: self.open_category("Bluetooth & Devices")),
            ("This is System Update", lambda: self.open_category("Windows Update")),
            ("These are System Update Features", lambda: self.open_system_feature("Display")),
        ]
        step_index = 0

        box = tk.Toplevel(self)
        box.geometry("400x150")
        box.title("Tutorial")
        msg = tk.Label(box, text=tutorial_steps[step_index][0], wraplength=350, font=("Segoe UI", 12))
        msg.pack(pady=20)
        btn_next = tk.Button(box, text="Next", command=lambda: next_step())
        btn_next.pack(pady=10)

        def next_step():
            nonlocal step_index
            if step_index < len(tutorial_steps):
                tutorial_steps[step_index][1]()  # Execute the step
                step_index += 1
                if step_index < len(tutorial_steps):
                    msg.config(text=tutorial_steps[step_index][0])
                else:
                    msg.config(text="Tutorial Completed! Have Fun!")
                    btn_next.config(text="Close", command=lambda: box.destroy())
                    self.tutorial_done = True

if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()
