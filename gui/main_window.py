import customtkinter as ctk
from gui.components import HotkeyEntry, DeviceFrame
from functools import partial

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("Spotify Device Switcher")
        self.geometry("400x420")
        # TODO: Add functionality to MACOS and Linux
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.resizable(False, False)
        self.tray_icon = None
        self.controller = controller
        self.grid_columnconfigure((0, 1), weight=1)

        # Hotkey configuration
        ctk.CTkLabel(self, text="Hotkey:").pack(padx=5)
        self.hotkey_entry = HotkeyEntry(self, controller.hotkey_handler)
        self.hotkey_entry.pack(pady=10)

        ctk.CTkButton(self, text="Set Hotkey", command=self.controller.set_device_switch_hotkey).pack(pady=5)

        # Device list
        self.device_frame = DeviceFrame(self, controller)
        self.device_frame.pack(pady=10, fill="both")

        ctk.CTkButton(self, text="Refresh Devices", command=self.device_frame.populate_devices).pack(pady=5, anchor="w")
        open_autostart_folder_BTN = ctk.CTkButton(self, text="Open Autostart Folder", command=controller.open_autostart_folder)
        open_autostart_folder_BTN.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="w")

        start_in_tray = ctk.BooleanVar(value=self.controller.config_handler.config.get('start_in_tray', False))
        ctk.CTkCheckBox(self, text="Start in tray", variable=start_in_tray, command=controller.toggle_start_behavior).pack(pady=5, anchor="w")

    def minimize_to_tray(self):
        self.withdraw()
        self.controller.minimize_to_tray(self)