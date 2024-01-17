import customtkinter as ctk
from SettingsHelper import SettingsOption, EntrySetting, load_settings, save_settings_to_json

ABOUT_STRING = "aiTracker is a simple application used to provide new forms of input to hardware with just your eyes! Simply look in the direction "

class MainScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        #widget creation
        title_label = ctk.CTkLabel(self, text="Welcome to aiTracker!", font=ctk.CTkFont(size=40))
        subtitle_label = ctk.CTkLabel(self, text="Click below to get started", font=ctk.CTkFont(size=25))
        launch_button = ctk.CTkButton(self, text="Launch", corner_radius=10, command=lambda: self.show_screen_callback(LaunchScreen))
        about_button = ctk.CTkButton(self, text="About", corner_radius=10, command=lambda: self.show_screen_callback(AboutScreen))
        settings_button = ctk.CTkButton(self, text="Settings", corner_radius=10, command=lambda: self.show_screen_callback(SettingsScreen))
        quit_button = ctk.CTkButton(self, text="Quit", corner_radius=10, command=lambda: root.destroy())

        #widget placement
        title_label.place(relx=.5, rely=0.3, anchor=ctk.CENTER)
        subtitle_label.place(relx=.5, rely=0.35, anchor=ctk.CENTER)
        launch_button.place(relx=.5, rely=0.55, anchor=ctk.CENTER)
        about_button.place(relx=.5, rely=0.6, anchor=ctk.CENTER)
        settings_button.place(relx=.5, rely=0.65, anchor=ctk.CENTER)
        quit_button.place(relx=.5, rely=0.7, anchor=ctk.CENTER)

class AboutScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # widget creation
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_screen_callback(MainScreen))
        title = ctk.CTkLabel(self, text="About", font=ctk.CTkFont(size=40))
        about = ctk.CTkLabel(self, text=ABOUT_STRING, font=ctk.CTkFont(size=25))
        # widget placement
        back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)
        title.place(relx=.5, rely=0.05, anchor=ctk.CENTER)
        about.place(relx=.5, rely=0.35, anchor=ctk.CENTER)

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # settings label and back button
        title = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=40))
        title.place(relx=.5, rely=.05, anchor=ctk.CENTER)
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.save_settings())
        back_button.place(relx=.5, rely=.95, anchor=ctk.CENTER)
        
        # frame to hold all setting options
        settings_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        settings_frame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        # settings options
        self.up = SettingsOption(settings_frame, name="Up")
        self.down = SettingsOption(settings_frame, name="Down")
        self.left = SettingsOption(settings_frame, name="Left")
        self.right = SettingsOption(settings_frame, name="Right")
        self.up_left = SettingsOption(settings_frame, name="Up Left")
        self.up_right = SettingsOption(settings_frame, name="Up Right")
        self.down_left = SettingsOption(settings_frame, name="Down Left")
        self.down_right = SettingsOption(settings_frame, name="Down Right")
        self.blink = SettingsOption(settings_frame, name="Blink")
        self.look_duration = EntrySetting(settings_frame, name="Look Duration")
        
        # settings placements
        self.up.grid(row=0, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self.down.grid(row=0, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self.left.grid(row=1, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self.right.grid(row=1, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self.up_left.grid(row=2, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self.up_right.grid(row=2, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self.down_left.grid(row=3, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self.down_right.grid(row=3, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self.blink.grid(row=4, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self.look_duration.grid(row=4, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        
        # load settings
        settings_map = load_settings("settings.json")
        self.up.set_settings(settings_map["Up"])
        self.down.set_settings(settings_map["Down"])
        self.left.set_settings(settings_map["Left"])
        self.right.set_settings(settings_map["Right"])
        self.up_left.set_settings(settings_map["Up Left"])
        self.up_right.set_settings(settings_map["Up Right"])
        self.down_left.set_settings(settings_map["Down Left"])
        self.down_right.set_settings(settings_map["Down Right"])
        self.blink.set_settings(settings_map["Blink"])
        self.look_duration.set_value(settings_map["Look Duration"])
    
    # saves all of the settings and returns back to the main screen
    def save_settings(self):
        settings = dict()
        settings.update(self.up.get_settings())
        settings.update(self.down.get_settings())
        settings.update(self.left.get_settings())
        settings.update(self.right.get_settings())
        settings.update(self.up_left.get_settings())
        settings.update(self.up_right.get_settings())
        settings.update(self.down_left.get_settings())
        settings.update(self.down_right.get_settings())
        settings.update(self.blink.get_settings())
        settings.update(self.look_duration.get_value())
        save_settings_to_json(settings, "settings.json")
        self.show_screen_callback(MainScreen)

class LaunchScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # widget creation
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_screen_callback(MainScreen))
        # widget placement
        back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)
        '''
        b key goes back
        camera feed
        9 sections for each input
            each lights up when input is recognized
            overlay on top of the camera feed
        '''