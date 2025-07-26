import threading
import tkinter as tk
import os
import sys
from pathlib import Path
from subprocess import Popen
from sys import platform

from windows_toasts import Toast, ToastDisplayImage, ToastImage, WindowsToaster
import pystray
from PIL import Image
import config_handler
import spotify_api
import hotkey_handler
from gui import MainWindow, CredentialsDialog, ErrorDialog

VERSION = "1.0.1"
ICON_PATH = "assets/icon/favicon.ico"

def resource_path(rel):
    """
    Transforms a relative path to an absolute path.

    args:
        rel (str): The relative path to the resource.
    returns:
        Path: The absolute path to the resource.
    """
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    return base / rel

class AppController:
    """Main controller for the Spotify Sound Switcher application."""
    def __init__(self):
        self.config_handler = config_handler.ConfigHandler(VERSION)

        # Get Credentials from user if not present
        self.check_credentials()
        self.initialize_spotify()

        self.hotkey_handler = hotkey_handler.HotkeyHandler(self.config_handler)
        self.set_device_switch_hotkey(initial=True)

        self.gui_populate_devices = None
        self.is_tray = False

        self.icon = Image.open(resource_path(ICON_PATH))

        self.main_window: MainWindow

    def check_credentials(self, force=False):
        """
        Check if Spotify credentials are set, prompt for them if not.

        args:
            force (bool): If True, forces the credentials dialog to show
            even if credentials are already set.
        """
        if not self.config_handler.load_config() or force:
            # Temp root window to pass as parent to CredentialsDialog
            temp_root = tk.Tk()
            temp_root.withdraw()

            dialog = CredentialsDialog(temp_root, self.config_handler.save_credentials)
            dialog.wait_window()

            temp_root.destroy()

    def initialize_spotify(self):
        """Initialize the Spotify API with the saved credentials."""
        try:
            self.spotify = spotify_api.SpotifyApi(self.config_handler)
        except Exception as e:
            ErrorDialog(f"Error initializing Spotify API: {e}").wait_window()

    def set_device_switch_hotkey(self, initial=False):
        """Set the hotkey for switching devices.

        args:
            initial (bool): If True, sets the hotkey without removing the existing one.
        """
        self.hotkey_handler.register_hotkey(self.switch_device, initial)

    def switch_device(self):
        """Switch to the next available output device in the selected devices list."""
        if not self.is_current_device_available():
            self.show_toast("Current device is not available. (Try playing something on Spotify)")
            return

        current_device = self.spotify.get_current_device()['id']

        if not self.device_has_index(current_device):
            self.show_toast("Current device is not in the selected devices list.")
            return

        device_ids = self.config_handler.config['selected_devices']
        current_index = device_ids.index(current_device)
        next_index = (current_index + 1) % len(device_ids)
        next_device_id = device_ids[next_index]

        if not self.device_is_available(next_device_id):
            self.show_toast("Next device is not available.")
            return

        self.spotify.transfer_playback(next_device_id)
        if not self.is_tray:
            self.gui_populate_devices(delay_refresh=True)


    def is_current_device_available(self):
        """Check if the current output device is available."""
        current_device = self.spotify.get_current_device()
        if current_device and 'id' in current_device:
            return self.device_is_available(current_device['id'])
        return False

    def device_is_available(self, device_id):
        """
        Check if a device is available.

        args:
            device_id (str): The ID of the device to check.
        returns:
            bool: True if the device is available, False otherwise.
        """
        return device_id in [device['id'] for device in self.spotify.get_available_devices()]

    def device_has_index(self, device_id):
        """
        Check if a device ID is in the selected devices list.

        args:
            device_id (str): The ID of the device to check.
        returns:
            bool: True if the device ID is in the selected devices list, False otherwise.
        """
        return device_id in self.config_handler.config['selected_devices']

    def get_all_devices(self):
        """
        Get all available devices, including unavailable ones.

        returns:
            list: A list of all devices, including unavailable ones.
        """
        devices = self.spotify.get_available_devices()
        unavailable_device_ids = [device for device in self.config_handler.config['selected_devices']
                                  if device not in [device['id'] for device in devices]]
        unavailable_devices = [{"id": device_id, "unavailable": True, "name": device_id, "type": "Unavailable"}
                               for device_id in unavailable_device_ids]
        return devices + unavailable_devices

    def minimize_to_tray(self, main_window):
        """
        Minimize the main window to the system tray. Hiddes the main window and creates
        a system tray icon.

        args:
            main_window (MainWindow): The main window instance to minimize.
        """
        self.is_tray = True
        self.main_window = main_window
        menu = pystray.Menu(
            pystray.MenuItem("Open", self.restore_from_tray, default=True),
            pystray.MenuItem("Exit", self.destroy_app)
        )
        self.tray_icon = pystray.Icon("Spotify Device Switcher", self.icon, menu=menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def restore_from_tray(self):
        """Restore the main window and stop the tray icon."""
        if self.tray_icon:
            self.tray_icon.stop()
        self.main_window.deiconify()
        self.gui_populate_devices()

    def toggle_start_behavior(self):
        """Toggle the start behavior of the application. (Start in tray or not)"""
        self.config_handler.toggle_start_behavior()

    def open_autostart_folder(self):
        """Open the autostart folder in the file explorer."""
        if platform == "win32":
            startup_folder  = os.path.join(os.getenv("APPDATA"),
                        r"Microsoft\Windows\Start Menu\Programs\Startup")
            Popen(f'explorer "{startup_folder}"')
        else:
            ErrorDialog("Autostart folder opening is not supported on this platform.")

    def toggle_close_behavior(self):
        """Toggle the close behavior of the application. (Close into tray or not)"""
        self.config_handler.toggle_close_behavior()
        self.set_close_behavior(self.main_window)

    def set_close_behavior(self, main_window):
        """Set the close behavior of the main window based on the configuration."""
        if self.config_handler.config.get('close_into_tray', False):
            main_window.set_protocol(main_window.minimize_to_tray)
        else:
            main_window.set_protocol(main_window.destroy)

    def show_toast(self, message):
        """Show a toast notification with the given message."""
        if platform == "win32":
            toaster = WindowsToaster("Spotify Device Switcher")
            toast_image = ToastDisplayImage(ToastImage(resource_path(ICON_PATH)))
            msg_toaster = Toast(text_fields=[message], images=[toast_image])
            toaster.show_toast(msg_toaster)
        else:
            pass # TODO: Implement toast notifications for other platforms

    def destroy_app(self):
        """Destroy the application, stopping the tray icon if it exists and closing the main window."""
        if self.is_tray:
            self.tray_icon.stop()

        self.main_window.after(0, self.main_window.destroy)

    def run(self):
        """Run the main application loop."""
        try:
            self.main_window = MainWindow(self, resource_path(ICON_PATH))
            if self.config_handler.config.get('start_in_tray', False):
                self.main_window.minimize_to_tray()
            self.main_window.mainloop()
        except Exception as e:
            dialog = ErrorDialog(f"Error running Spotify Sound Switcher: {e}")
            dialog.wait_window()