import customtkinter as ctk

class ErrorDialog(ctk.CTkToplevel):
    """A dialog window to display an error message."""
    def __init__(self, message):
        super().__init__()
        self.title("Error")
        self.geometry("400x100")
        self.resizable(True, True)

        ctk.CTkLabel(self, text=message).pack(pady=10)
        ctk.CTkButton(self, text="OK", command=self.destroy).pack(pady=10)