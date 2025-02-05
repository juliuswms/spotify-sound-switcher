import customtkinter as ctk

class HotkeyEntry(ctk.CTkEntry):
    def __init__(self, parent, hotkey_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, textvariable=ctk.StringVar(value="das"))
        self.parent = parent
        self.hotkey_handler = hotkey_handler
        
        # Event bindings to handle clicks and unfocus
        self.bind("<FocusIn>", self.start_listening)

        # Cursor enter and leave events
        self.bind("<Enter>", self.on_cursor_enter)
        self.bind("<Leave>", self.on_cursor_leave)
        self.master.bind("<Button-1>", self.on_click)
        self.curser_inside = False

        # Stop listening on escape
        self.bind("<Escape>", self.stop_listening)

        self.bind("<Key>", self.set_text)

    def on_cursor_enter(self, event):
        self.curser_inside = True

    def on_cursor_leave(self, event):
        self.curser_inside = False
        self.configure(textvariable=ctk.StringVar(value="daasdasds"))

    def on_click(self, event):
        if not self.curser_inside:
            self.stop_listening()

    def start_listening(self, event):
        self.hotkey_handler.start_recording_hotkey()


    def stop_listening(self, event=None):
        self.hotkey_handler.stop_recording_hotkey()
        self.parent.focus_set()

    def set_text(self, event):
        self.configure(textvariable=ctk.StringVar(value=self.hotkey_handler.rec_hotkey))