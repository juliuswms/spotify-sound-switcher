import config_handler
import spotify_api
from gui import MainWindow, CredentialsDialog, ErrorDialog
import hotkey_handler
import pystray
import threading
from PIL import Image

class AppController:
    def __init__(self):
        self.config_handler = config_handler.ConfigHandler()

        # Get Credentials from user if not present
        self.check_credentials()
        self.initialize_spotify()

        self.hotkey_handler = hotkey_handler.HotkeyHandler(self.config_handler)
        self.set_device_switch_hotkey(initial=True)
        
    def check_credentials(self, force=False):
        if(not self.config_handler.load_config() or force):
            dialog = CredentialsDialog(self.config_handler.save_credentials)
            dialog.wait_window()

    def initialize_spotify(self):
        try:
            self.spotify = spotify_api.SpotifyApi(self.config_handler.config)
        except Exception as e:
            ErrorDialog(f"Error initializing Spotify API: {e}")

    def set_device_switch_hotkey(self, initial=False):
        self.hotkey_handler.register_hotkey(self.switch_device, initial)

    def switch_device(self):
        # If the current device is in the selected devices list, switch to the next device in the list
        if self.device_is_available(self.spotify.get_current_device()['id']) and self.device_has_index(self.spotify.get_current_device()['id']):
            # Get the index of the current device in the selected devices list
            current_index = self.config_handler.config['selected_devices'].index(self.spotify.get_current_device()['id'])
            # Get the next index in the list, looping back to the start if necessary
            next_index = (current_index + 1) % len(self.config_handler.config['selected_devices'])
            # Transfer playback to the next device if it is available
            if self.device_is_available(self.config_handler.config['selected_devices'][next_index]):
                self.spotify.transfer_playback(self.config_handler.config['selected_devices'][next_index])

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
        self.main_window = main_window
        image = Image.new("RGB", (64, 64), "white") # PLACEHOLDER
        menu = pystray.Menu(
            pystray.MenuItem("Open", self.restore_from_tray),
            pystray.MenuItem("Exit", self.destroy_app)
        )
        self.tray_icon = pystray.Icon("Spotify Device Switcher", image, menu=menu) # TODO: Add icon
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def restore_from_tray(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.main_window.deiconify()

    def destroy_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.main_window.after(0, self.main_window.destroy)

    def run(self):
        main_window = MainWindow(self)
        main_window.mainloop()