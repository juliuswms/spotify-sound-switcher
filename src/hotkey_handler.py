import keyboard
import threading

class HotkeyHandler:
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.current_hotkey = config_handler.config['hotkey']
        self.listening = False  # Flag to control live hotkey listening
        self.rec_hotkey = None  # Stores the recorded hotkey
        self.unfocus_entry = None

    def register_hotkey(self, callback, initial=False):
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
            print(f"Hotkey error: {e}")

    def start_recording_hotkey(self):
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
                print(f"Error recording hotkey: {e}")
        self.listening_thr = threading.Thread(target=record, daemon=True).start()

    def stop_listening(self):
        self.listening = False
        self.unfocus_entry()

    def read_hotkey(self):
        recorded_key = []
        while True:
            event = keyboard.read_event(suppress=True)
            if event.name == "esc" or event.event_type == "up":
                return self.keys_to_string(recorded_key)
            if event not in recorded_key:
                if(keyboard.is_modifier(event.scan_code)): recorded_key.insert(0, event)
                else: recorded_key.append(event)

    def keys_to_string(self, keys):
        hotkey = ''
        for key in keys:
            hotkey += key.name + '+'
        return hotkey[:-1]