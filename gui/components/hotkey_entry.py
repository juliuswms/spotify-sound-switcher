import customtkinter as ctk

class HotkeyEntry(ctk.CTkEntry):
    def __init__(self, parent, hotkey_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, textvariable=ctk.StringVar(value=hotkey_handler.current_hotkey))
        hotkey_handler.unfocus_entry = self.stop_listening
        self.hotkey_handler = hotkey_handler
        
        # Event bindings to handle clicks and unfocus
        self.bind("<FocusIn>", self.start_listening)

    def start_listening(self, event):
        self.configure(textvariable=ctk.StringVar(value="Recording..."))
        self.hotkey_handler.start_recording_hotkey()

    def stop_listening(self, event=None):
        self.configure(textvariable=ctk.StringVar(value=self.hotkey_handler.rec_hotkey))
        self.master.focus_set()