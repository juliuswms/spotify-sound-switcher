import customtkinter as ctk
from gui.components import HotkeyEntry, DeviceFrame
from functools import partial

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("Spotify Device Switcher")
        self.geometry("400x400")
        #self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.resizable(False, False)
        self.tray_icon = None
        self.controller = controller

        # Hotkey configuration
        ctk.CTkLabel(self, text="Hotkey:").pack(padx=5)
        self.hotkey_entry = HotkeyEntry(self, controller.hotkey_handler)
        self.hotkey_entry.pack(pady=10)

        ctk.CTkButton(self, text="Set Hotkey", command=self.controller.set_device_switch_hotkey).pack(pady=5)

        # Device list
        self.device_frame = DeviceFrame(self, controller)
        self.device_frame.pack(pady=10, fill="both")
        
        ctk.CTkButton(self, text="Refresh Devices", command=self.device_frame.populate_devices).pack(pady=5, anchor="w")