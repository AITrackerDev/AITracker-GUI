'''
This file contains all of the necessary code to start the application and run through all of the necessary startup requirements.
'''

import customtkinter as ctk
import platform
from Screens import MainScreen
import ctypes

class AITracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("aiTracker")
        self.current_screen = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.geometry("1080x720")
        self.attributes('-topmost', 1)
        self.update()
        self.attributes('-topmost', 0)
        self.wm_attributes("-fullscreen", True)
        self.show_screen(MainScreen)
        
    def show_screen(self, screen_class):
        # destroy current screen if exists
        if self.current_screen:
            self.current_screen.destroy()

        # create and display the requested screen
        self.current_screen = screen_class(self, self.show_screen)
        self.current_screen.pack()

if __name__ == '__main__':
    # fixes the GUI being bugged in windows
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # starts app
    app = AITracker()
    app.mainloop()