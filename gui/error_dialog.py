import customtkinter as ctk

class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, message):
        super().__init__()
        self.title("Error")
        self.geometry("300x100")
        self.resizable(False, False)

        ctk.CTkLabel(self, text=message).pack(pady=10)
        ctk.CTkButton(self, text="OK", command=self.destroy).pack(pady=10)