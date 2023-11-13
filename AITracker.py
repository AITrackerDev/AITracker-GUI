'''
This file contains all of the necessary code to start the application and run through all of the necessary startup requirements.
'''

import customtkinter as ctk
import platform
from Screens import MainScreen, LaunchScreen, AboutScreen, SettingsScreen

class AITracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("aiTracker")
        self.current_screen = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        if platform.system() == "Windows":
            self.state("zoomed")
            pad = 3
            self.geometry("{0}x{1}+0+0".format(
            self.winfo_screenwidth()-pad, app.winfo_screenheight()-pad))
        elif platform.system() == "Darwin":
            self.wm_attributes("-fullscreen", True)
        self.show_screen(MainScreen)
        
    def show_screen(self, screen_class):
        # Destroy current screen if exists
        if self.current_screen:
            self.current_screen.destroy()

        # Create and display the requested screen
        self.current_screen = screen_class(self, self.show_screen)
        self.current_screen.pack()
