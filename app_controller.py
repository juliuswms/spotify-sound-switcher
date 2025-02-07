import config_handler
import spotify_api
from gui import MainWindow, CredentialsDialog, ErrorDialog
import hotkey_handler

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
        if self.spotify.get_current_device()['id'] in self.config_handler.config['selected_devices']:
            current_index = self.config_handler.config['selected_devices'].index(self.spotify.get_current_device()['id'])
            next_index = (current_index + 1) % len(self.config_handler.config['selected_devices'])
            self.spotify.transfer_playback(self.config_handler.config['selected_devices'][next_index])
        else:
            self.spotify.transfer_playback(self.config_handler.config['selected_devices'][0])

    def run(self):
        main_window = MainWindow(self)
        main_window.mainloop()