import customtkinter as ctk
import usb.core
from IndicatorFrame import DEBUG

class MainScreen(ctk.CTkFrame):
    '''
    The main screen used to access the other screens.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer
        
        #widget creation
        _title_label = ctk.CTkLabel(self, text='Welcome to AITracker!', font=ctk.CTkFont(size=40))
        _subtitle_label = ctk.CTkLabel(self, text='Click below to get started', font=ctk.CTkFont(size=25))
        _launch_button = ctk.CTkButton(self, text='Launch', corner_radius=10, command=lambda: self._load_launch_screen())
        _about_button = ctk.CTkButton(self, text='Help', corner_radius=10, command=lambda: self._screen_changer('AboutScreen'))
        _settings_button = ctk.CTkButton(self, text='Settings', corner_radius=10, command=lambda: self._screen_changer('SettingsScreen'))
        _quit_button = ctk.CTkButton(self, text='Quit', corner_radius=10, command=lambda: root.destroy())

        #widget placement
        _title_label.place(relx=.5, rely=0.3, anchor=ctk.CENTER)
        _subtitle_label.place(relx=.5, rely=0.35, anchor=ctk.CENTER)
        _launch_button.place(relx=.5, rely=0.55, anchor=ctk.CENTER)
        _about_button.place(relx=.5, rely=0.6, anchor=ctk.CENTER)
        _settings_button.place(relx=.5, rely=0.65, anchor=ctk.CENTER)
        _quit_button.place(relx=.5, rely=0.7, anchor=ctk.CENTER)

    def _load_launch_screen(self):
        '''
        Loads the launch screen of the application and checks if the breakout board is plugged in.
        '''

        if not DEBUG:
            _usb_devices = usb.core.find(find_all=True)
            _device_found = False
            for device in _usb_devices:
                if device.idVendor == 0x0403 and device.idProduct == 0x6014:
                    _device_found = True
                    self._screen_changer('LaunchScreen')
            # display warning if the board isn't found
            if not _device_found:
                warning = ctk.CTkLabel(self, text='Please plug in FT232H breakout board to continue.', font=ctk.CTkFont(size=25))
                warning.place(relx=.5, rely=.45, anchor=ctk.CENTER)
        else:
            self._screen_changer('LaunchScreen')