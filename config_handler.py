import os
import json
from platformdirs import user_config_dir

class ConfigHandler:
    def __init__(self, version):
        self.path = user_config_dir(appname="SpotifySoundSwitcher", version=version) # Why is app name doubled? (.../Local/SoundSwitcher/SpotifySoundSwitcher)
        self.config_file = os.path.join(self.path, "config.json")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
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
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)