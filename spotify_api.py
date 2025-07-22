import spotipy
from spotipy.oauth2 import SpotifyOAuth

REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-modify-playback-state user-read-playback-state"
class SpotifyApi:
    def __init__(self, config):
        auth_manager = SpotifyOAuth(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)
        self.get_available_devices()

    def get_available_devices(self):
        return self.client.devices().get('devices', [])

    def transfer_playback(self, device_id):
        self.client.transfer_playback(device_id, force_play=True)

    def get_current_device(self):
        return self.client.current_playback().get('device')