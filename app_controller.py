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
        
    def check_credentials(self, force=False):
        if(not self.config_handler.load_config() or force):
            dialog = CredentialsDialog(self.config_handler.save_credentials)
            dialog.wait_window()

    def initialize_spotify(self):
        try:
            self.spotify = spotify_api.SpotifyApi(self.config_handler.config)
        except Exception as e:
            ErrorDialog(f"Error initializing Spotify API: {e}")

    def set_hotkey(self, hotkey):
        pass

    def run(self):
        main_window = MainWindow(self)
        main_window.mainloop()