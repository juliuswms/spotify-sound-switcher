import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from gui import ErrorDialog

REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-modify-playback-state user-read-playback-state"
class SpotifyApi:
    """A class to interact with the Spotify API using Spotipy."""
    def __init__(self, config_handler):
        config = config_handler.config
        cache_path = config_handler.path
        cache_path = os.path.join(cache_path, ".cache-spotify")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        auth_manager = SpotifyOAuth(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_handler=CacheFileHandler(cache_path=cache_path),
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)
        self.get_available_devices()

    def get_available_devices(self):
        """Get all available devices from the Spotify API."""
        try:
            return self.client.devices().get('devices', [])
        except (requests.ConnectionError, requests.Timeout) as e:
            error_dialog = ErrorDialog(f"Error getting available Devices {e}")
            error_dialog.wait_window()
            return []

    def transfer_playback(self, device_id):
        """Transfer playback to a specific device using the ID."""
        try:
            self.client.transfer_playback(device_id, force_play=True)
        except (spotipy.SpotifyException) as e:
            error_dialog = ErrorDialog(f"Error transferring playback: {e}")
            error_dialog.wait_window()

    def get_current_device(self):
        """Get the current playback device."""
        try:
            return self.client.current_playback().get('device', {})
        except (requests.ConnectionError, requests.Timeout) as e:
            error_dialog = ErrorDialog(f"Error getting current device: {e}")
            error_dialog.wait_window()
            return {}
        except AttributeError as e:
            error_dialog = ErrorDialog(f"Error getting current device: {e}")
            error_dialog.wait_window()
            return {}