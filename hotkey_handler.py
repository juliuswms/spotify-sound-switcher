import keyboard
import threading

class HotkeyHandler:
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.current_hotkey = config_handler.config['hotkey']
        self.listening = False  # Flag to control live hotkey listening
        self.rec_hotkey = None  # Stores the recorded hotkey

    def register_hotkey(self, hotkey, callback):
        try:
            # Remove old hotkey if it exists
            if self.current_hotkey:
                keyboard.remove_hotkey(self.current_hotkey)

            # Register new hotkey
            keyboard.add_hotkey(hotkey, callback)
            self.current_hotkey = hotkey

            # Save the new hotkey in the config
            self.config_handler.config['hotkey'] = hotkey
            self.config_handler.save_config()
        except Exception as e:
            print(f"Hotkey error: {e}")

    def start_recording_hotkey(self):
        if self.listening:
            return  # Already listening, ignore duplicate calls

        self.listening = True
        # Reset the recorded hotkey
        self.rec_hotkey = None
        
        def record():
            try:
                keyboard.start_recording()
            except Exception as e:
                print(f"Error recording hotkey: {e}")
        
        threading.Thread(target=record, daemon=True).start()

    def stop_recording_hotkey(self):
        keys = keyboard.stop_recording()
        print(keys)
        self.listening = False

    def to_hotkey(keys):
        pass
        # Convert recording queue to hotkey string