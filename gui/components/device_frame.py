import customtkinter as ctk
from functools import partial
import time

class DeviceFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.controller.gui_populate_devices = self.populate_devices
        self.populate_devices()

    def populate_devices(self, delay_refresh=False):
        if delay_refresh:
            #threading.Event().wait(1)
            time.sleep(1)
        # Clear existing widgets before repopulating
        for widget in self.winfo_children():
            widget.destroy()

        self.device_vars = {}  # Dictionary to track checkboxes

        # Get available devices
        devices = self.controller.get_all_devices()

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

            device_label = ctk.CTkLabel(frame, text=device_name)
            device_label.pack(side="left", padx=5)

            if device.get("is_active") is not None and device["is_active"]:
                device_label.configure(text_color="lime green")
                checkbox.configure(fg_color="lime green")

            if device.get("unavailable") is not None and device["unavailable"]:
                checkbox.configure(state=ctk.DISABLED)
                device_label.configure(text_color="gray")
                checkbox.configure(fg_color="gray")

    def toggle_device_selection(self, device_id):
        selected = self.device_vars[device_id].get()
        self.controller.config_handler.toggle_device(device_id, selected)