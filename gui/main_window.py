import customtkinter as ctk
from gui.components import HotkeyEntry, DeviceFrame

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("Spotify Device Switcher")
        self.geometry("400x420")
        # TODO: Add functionality to MACOS and Linux
        #self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.resizable(False, False)
        self.tray_icon = None
        self.controller = controller
        self.grid_columnconfigure((0, 1), weight=1)

        # Hotkey configuration
        ctk.CTkLabel(self, text="Hotkey:").grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.hotkey_entry = HotkeyEntry(self, controller.hotkey_handler)
        self.hotkey_entry.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="w")

        ctk.CTkButton(self, text="Set Hotkey", command=self.controller.set_device_switch_hotkey).grid(row=1, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        # Device list
        self.device_frame = DeviceFrame(self, controller)
        self.device_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")

        refresh_button =ctk.CTkButton(self, text="Refresh Devices", command=self.device_frame.populate_devices)
        refresh_button.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")
        open_autostart_folder_BTN = ctk.CTkButton(self, text="Open Autostart Folder", command=controller.open_autostart_folder)
        open_autostart_folder_BTN.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="w")

        start_in_tray = ctk.BooleanVar(value=self.controller.config_handler.config.get('start_in_tray', False))
        ctk.CTkCheckBox(self, text="Start in tray", variable=start_in_tray, command=controller.toggle_start_behavior).grid(row=4, column=0, padx=20, pady=(0, 20), sticky="w")

        close_into_tray = ctk.BooleanVar(value=self.controller.config_handler.config.get('close_into_tray', False))
        ctk.CTkCheckBox(self, text="Close into tray", variable=close_into_tray, command=controller.toggle_close_behavior).grid(row=4, column=1, padx=20, pady=(0, 20), sticky="w")

    def minimize_to_tray(self):
        self.withdraw()
        self.controller.minimize_to_tray(self)

    def destroy(self):
        return super().destroy()

    def set_protocol(self, function):
        self.protocol("WM_DELETE_WINDOW", function)
