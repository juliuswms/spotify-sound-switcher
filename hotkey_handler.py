import keyboard
import threading

class HotkeyHandler:
    def register_hotkey(config, callback):
        try:
            keyboard.add_hotkey(config['hotkey'], callback)
        except Exception as e:
            print(f"Hotkey error: {e}")

    def start_hotkey_listener():
        def listener():
            keyboard.wait()
        threading.Thread(target=listener, daemon=True).start()