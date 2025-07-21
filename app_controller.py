import config_handler
import spotify_api
import hotkey_handler
import pystray
import threading
import tkinter as tk
import os
from subprocess import Popen
from gui import MainWindow, CredentialsDialog, ErrorDialog
from PIL import Image
from sys import platform

VERSION = "1.0.0"

class AppController:
    def __init__(self):
        self.config_handler = config_handler.ConfigHandler(VERSION)

        # Get Credentials from user if not present
        self.check_credentials()
        self.initialize_spotify()

        self.hotkey_handler = hotkey_handler.HotkeyHandler(self.config_handler)
        self.set_device_switch_hotkey(initial=True)

        self.gui_populate_devices = None
        self.is_tray = False

    def check_credentials(self, force=False):
        if not self.config_handler.load_config() or force:
            # Temp root window to pass as parent to CredentialsDialog
            temp_root = tk.Tk()
            temp_root.withdraw()

            dialog = CredentialsDialog(temp_root, self.config_handler.save_credentials)
            dialog.wait_window()

            temp_root.destroy()

    def initialize_spotify(self):
        try:
            self.spotify = spotify_api.SpotifyApi(self.config_handler.config)
        except Exception as e:
            ErrorDialog(f"Error initializing Spotify API: {e}")

    def set_device_switch_hotkey(self, initial=False):
        self.hotkey_handler.register_hotkey(self.switch_device, initial)

    def switch_device(self):
        # TODO: Refactor needed
        # If the current device is in the selected devices list, switch to the next device in the list
        if self.is_current_device_available() and self.device_has_index(self.spotify.get_current_device()['id']):
            # Get the index of the current device in the selected devices list
            current_index = self.config_handler.config['selected_devices'].index(self.spotify.get_current_device()['id'])
            # Get the next index in the list, looping back to the start if necessary
            next_index = (current_index + 1) % len(self.config_handler.config['selected_devices'])
            # Transfer playback to the next device if it is available
            if self.device_is_available(self.config_handler.config['selected_devices'][next_index]):
                self.spotify.transfer_playback(self.config_handler.config['selected_devices'][next_index])
                if not self.is_tray:
                    self.gui_populate_devices(delay_refresh=True)

    def is_current_device_available(self):
        current_device = self.spotify.get_current_device()
        if current_device and 'id' in current_device:
            return self.device_is_available(current_device['id'])
        return False

    def device_is_available(self, device_id):
        return device_id in [device['id'] for device in self.spotify.get_available_devices()]

    def device_has_index(self, device_id):
        return device_id in self.config_handler.config['selected_devices']

    def get_all_devices(self):
        devices = self.spotify.get_available_devices()
        unavailable_device_ids = [device for device in self.config_handler.config['selected_devices'] if device not in [device['id'] for device in devices]]
        unavailable_devices = [{"id": device_id, "unavailable": True, "name": device_id, "type": "Unavailable"} for device_id in unavailable_device_ids]
        return devices + unavailable_devices

    def minimize_to_tray(self, main_window):
        self.is_tray = True
        self.main_window = main_window
        image = Image.new("RGB", (64, 64), "white") # PLACEHOLDER
        menu = pystray.Menu(
            pystray.MenuItem("Open", self.restore_from_tray, default=True),
            pystray.MenuItem("Exit", self.destroy_app)
        )
        self.tray_icon = pystray.Icon("Spotify Device Switcher", image, menu=menu) # TODO: Add icon
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def restore_from_tray(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.main_window.deiconify()
        self.gui_populate_devices()

    def toggle_start_behavior(self):
        self.config_handler.toggle_start_behavior()

    def open_autostart_folder(self):
        if platform == "win32":
            startup_folder  = os.path.join(os.getenv("APPDATA"),
                        r"Microsoft\Windows\Start Menu\Programs\Startup")
            Popen(f'explorer "{startup_folder}"')
        else:
            ErrorDialog("Autostart folder opening is not supported on this platform.")

    def toggle_close_behavior(self):
        self.config_handler.toggle_close_behavior()

    def destroy_app(self):
        if self.is_tray:
            self.tray_icon.stop()

        self.main_window.after(0, self.main_window.destroy)

    def run(self):
        main_window = MainWindow(self)
        if self.config_handler.config.get('start_in_tray', False):
            main_window.minimize_to_tray()
        main_window.mainloop()