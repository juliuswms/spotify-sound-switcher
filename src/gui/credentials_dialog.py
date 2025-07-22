import customtkinter as ctk

class CredentialsDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Spotify API Credentials")
        self.callback = callback
        self.geometry("400x200")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Client ID:").pack(pady=(10, 0))
        self.client_id_entry = ctk.CTkEntry(self, width=300)
        self.client_id_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Client Secret:").pack(pady=(10, 0))
        self.client_secret_entry = ctk.CTkEntry(self, show="*", width=300)
        self.client_secret_entry.pack(pady=5)

        ctk.CTkButton(self, text="Save", command=self.check_credentials).pack(pady=10)

    def check_credentials(self):
        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()
        if client_id and client_secret:
            self.callback(client_id, client_secret)
            self.destroy()