import os
import json
from platformdirs import user_config_dir

class ConfigHandler:
    """Handles reading and writing configuration."""
    def __init__(self, version):
        self.path = user_config_dir(appname="SpotifySoundSwitcher", version=version) # Why is app name doubled? (.../Local/SoundSwitcher/SpotifySoundSwitcher)
        self.config_file = os.path.join(self.path, "config.json")
        self.load_config()

    def load_config(self):
        """
        Load the configuration from the config file. If not found or invalid, create a default config.

        returns:
            bool: True if the config was loaded successfully, False if it was not found or invalid.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    return True
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading config: {e}")
        self.config = {
            "hotkey": "ctrl+alt+s",
            "selected_devices": [],
            "client_id": "",
            "client_secret": "",
            "start_in_tray": False,
            "close_into_tray": False
        }
        return False

    def save_credentials(self, client_id, client_secret):
        """
        Save Spotify API credentials to the config file.

        args:
            client_id (str): The Spotify API client ID.
            client_secret (str): The Spotify API client secret.
        """
        self.config['client_id'] = client_id
        self.config['client_secret'] = client_secret
        self.write_config()

    def save_hotkey(self, hotkey):
        """
        Save the hotkey to the config file.

        args:
            hotkey (str): The hotkey to save.
        """
        self.config['hotkey'] = hotkey
        self.write_config()

    def set_device_state(self, device_id, should_select):
        """
        Set the selection state of a device in the config.

        args:
            device_id (str): The ID of the device to toggle.
            should_select (bool): True to select the device, False to deselect it.
        """
        if should_select:
            if device_id not in self.config['selected_devices']:
                self.config['selected_devices'].append(device_id)
        else:
            if device_id in self.config['selected_devices']:
                self.config['selected_devices'].remove(device_id)
        self.write_config()

    def toggle_start_behavior(self):
        """Toggle the start behavior of the application (start in tray or not)."""
        self.config['start_in_tray'] = not self.config.get('start_in_tray', False)
        self.write_config()

    def toggle_close_behavior(self):
        """Toggle the close behavior of the application (close into tray or not)."""
        self.config['close_into_tray'] = not self.config.get('close_into_tray', False)
        self.write_config()

    def write_config(self):
        """
        Write the current configuration to the config file.
        If the directory does not exist, it will be created.
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f)