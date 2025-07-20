import os
import json

CONFIG_FILE = "config.json"

class ConfigHandler:
    def __init__(self):
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config = json.load(f)
                    return True
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading config: {e}")
        self.config = {
            "hotkey": "ctrl+alt+s",
            "selected_devices": [],
            "client_id": "",
            "client_secret": "",
            "start_in_tray": False
        }
        return False
    
    def save_credentials(self, client_id, client_secret):
        self.config['client_id'] = client_id
        self.config['client_secret'] = client_secret
        self.write_config()

    def save_hotkey(self, hotkey):
        self.config['hotkey'] = hotkey
        self.write_config()

    def toggle_device(self, device_id, var):
        if var:
            if device_id not in self.config['selected_devices']:
                self.config['selected_devices'].append(device_id)
        else:
            if device_id in self.config['selected_devices']:
                self.config['selected_devices'].remove(device_id)
        self.write_config()

    def toggle_start_behavior(self):
        self.config['start_in_tray'] = not self.config.get('start_in_tray', False)
        self.write_config()

    def write_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f)