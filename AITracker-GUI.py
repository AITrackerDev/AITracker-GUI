import os
import subprocess as sp
import platform
import ctypes
import customtkinter as ctk
from screens.MainScreen import MainScreen
from screens.LaunchScreen import LaunchScreen
from screens.AboutScreen import AboutScreen
from screens.SettingsScreen import SettingsScreen, load_settings_from_json

class AITrackerGUI(ctk.CTk):
    '''
    Create a new app window, set the attributes, and load the main screen.
    '''
    
    def __init__(self):
        super().__init__()

        # window setup
        self.title('AITracker')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.geometry('1080x720')
        self.attributes('-topmost', 1)
        self.update()
        self.attributes('-topmost', 0)
        self.wm_attributes('-fullscreen', True)
        self._current_screen = None
        
        # screen references to load them when requested
        self._screens = {
            'MainScreen':MainScreen,
            'LaunchScreen':LaunchScreen,
            'AboutScreen':AboutScreen,
            'SettingsScreen':SettingsScreen
        }
        
        # load main screen
        self.show_screen('MainScreen')

    def show_screen(self, screen_name):
        '''
        Loads in and displays a new screen as requested.
        '''  
        # load settings in case they change from screen changes
        settings = load_settings_from_json('settings.json')
        
        # if the current screen exists
        if self._current_screen:
            self._current_screen.destroy()
        
        # load new screen
        screen_class = self._screens[screen_name]
        
        # if the new screen needs info from the settings
        if screen_name == 'MainScreen' or screen_name == 'LaunchScreen':
            self._current_screen = screen_class(self, self.show_screen, settings)
        else:
            self._current_screen = screen_class(self, self.show_screen)
        self._current_screen.pack()

if __name__ == '__main__':
    # adafruit environment variable
    os.environ['BLINKA_FT232H'] = '1'

    # platform specific fixes
    if platform.system() == 'Windows':
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    elif platform.system() == 'Darwin':
        # find the version of libusb that's installed and set it as an environment variable
        version_path = sp.run('readlink -f $(brew --prefix libusb)', shell=True, capture_output=True).stdout.strip().decode('utf-8')
        os.environ['DYLD_LIBRARY_PATH'] = os.path.join(version_path, 'lib')

    app = AITrackerGUI()
    app.mainloop()
