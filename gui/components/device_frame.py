import customtkinter as ctk
from functools import partial

class DeviceFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.populate_devices()

    def populate_devices(self):
        # Clear existing widgets before repopulating
        for widget in self.winfo_children():
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

            frame = ctk.CTkFrame(self)
            frame.pack(fill="x", pady=2)

            checkbox = ctk.CTkCheckBox(frame, variable=var, text="", command=partial(self.toggle_device_selection, device_id))
            checkbox.pack(side="left")

            ctk.CTkLabel(frame, text=device_name).pack(side="left", padx=5)
    
    def toggle_device_selection(self, device_id):
        selected = self.device_vars[device_id].get()
        self.controller.config_handler.toggle_device(device_id, selected)