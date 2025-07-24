import threading
import keyboard
from gui import ErrorDialog

class HotkeyHandler:
    """Handles hotkey registration and management for the application."""
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.current_hotkey = config_handler.config['hotkey']
        self.listening = False  # Flag to control live hotkey listening
        self.rec_hotkey = None  # Stores the recorded hotkey
        self.unfocus_entry = None

    def register_hotkey(self, callback, initial=False):
        """
        Register a hotkey for the application.

        Args:
            callback (callable): The function to call when the hotkey is pressed.
            initial (bool): If True, only registers the hotkey without removing the existing one.
        """
        try:
            # Remove old hotkey if it exists
            if not initial:
                keyboard.remove_hotkey(self.current_hotkey)
            else: self.rec_hotkey = self.current_hotkey

            # Register new hotkey
            keyboard.add_hotkey(self.rec_hotkey, callback)
            self.current_hotkey = self.rec_hotkey

            # Save the new hotkey in the config
            if not initial:
                self.config_handler.save_hotkey(self.current_hotkey)
        except Exception as e:
            ErrorDialog(f"Hotkey error: {e}")

    def start_recording_hotkey(self):
        """
        Start listening for a new hotkey input from the user.
        """
        if self.listening:
            return  # Already listening, ignore duplicate calls

        self.listening = True
        # Reset the recorded hotkey
        self.rec_hotkey = None

        def record():
            try:
                self.rec_hotkey = self.read_hotkey()
                self.stop_listening()
            except Exception as e:
                ErrorDialog(f"Error recording hotkey: {e}")
        threading.Thread(target=record, daemon=True).start()

    def stop_listening(self):
        """Stop listening for hotkey input."""
        self.listening = False
        self.unfocus_entry()

    def read_hotkey(self):
        """
        Read a hotkey input from the user until they press 'esc' or release the key.

        returns:
            str: The recorded hotkey as a string.
        """
        recorded_key = []
        while True:
            event = keyboard.read_event(suppress=True)
            if event.name == "esc" or event.event_type == "up":
                return self.keys_to_string(recorded_key)
            if event not in recorded_key:
                if keyboard.is_modifier(event.scan_code):
                    recorded_key.insert(0, event)
                else:
                    recorded_key.append(event)

    def keys_to_string(self, keys):
        """
        Convert a list of keyboard events to a string representation of the hotkey.

        args:
            keys (list): A list of keyboard events.
        returns:
            str: A string representation of the hotkey.
        """
        hotkey = ''
        for key in keys:
            hotkey += key.name + '+'
        return hotkey[:-1]