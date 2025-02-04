import customtkinter as ctk
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
        ctk.CTkLabel(self, text="Hotkey:").pack()
        self.test = ctk.CTkEntry(self).pack()
        self.hotkey_entry = ctk.CTkEntry(self)
        self.hotkey_entry.bind("<FocusOut>", self.log)
        self.hotkey_entry.pack(pady=5)
        ctk.CTkButton(self, text="Set Hotkey", command=self.controller.set_hotkey).pack()

        # Device list
        self.device_frame = ctk.CTkScrollableFrame(self)
        self.device_frame.pack(pady=10, fill="both")
        self.populate_devices()
        
        ctk.CTkButton(self, text="Refresh Devices", command=self.populate_devices).pack(pady=5, anchor="w")
    
    def log(self, event=None):
        print("Focus out event")

    def populate_devices(self):
        # Clear existing widgets before repopulating
        for widget in self.device_frame.winfo_children():
            widget.destroy()

        self.device_vars = {}  # Dictionary to track checkboxes

        # Get available devices
        devices = self.controller.spotify.get_available_devices()

        for device in devices:
            device_id = device['id']
            device_name = f"{device['name']} ({device['type']})"

            # Create a BooleanVar to track selection state
            var = ctk.BooleanVar(value=device_id in self.controller.config_handler.config['selected_devices'])
            self.device_vars[device_id] = var

            frame = ctk.CTkFrame(self.device_frame)
            frame.pack(fill="x", pady=2)

            checkbox = ctk.CTkCheckBox(frame, variable=var, text="", command=partial(self.toggle_device_selection, device_id))
            checkbox.pack(side="left")

            ctk.CTkLabel(frame, text=device_name).pack(side="left", padx=5)

    def toggle_device_selection(self, device_id):
        selected = self.device_vars[device_id].get()
        self.controller.config_handler.toggle_device(device_id, selected)

class CredentialsDialog(ctk.CTkToplevel):
    def __init__(self, callback):
        super().__init__()
        self.title("Spotify API Credentials")
        self.callback = callback
        self.geometry("400x200")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Client ID:").pack(pady=(10, 0))
        self.client_id_entry = ctk.CTkEntry(self, width=300)
        self.client_id_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Client Secret:").pack(pady=(10, 0))
        self.client_secret_entry = ctk.CTkEntry(self, show="*", width=300)
        self.client_secret_entry.pack(pady=5)

        ctk.CTkButton(self, text="Save", command=self.check_credentials).pack(pady=10)

    def check_credentials(self):
        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()
        if client_id and client_secret:
            self.callback(client_id, client_secret)
            self.destroy()

class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, message):
        super().__init__()
        self.title("Error")
        self.geometry("300x100")
        self.resizable(False, False)

        ctk.CTkLabel(self, text=message).pack(pady=10)
        ctk.CTkButton(self, text="OK", command=self.destroy).pack(pady=10)