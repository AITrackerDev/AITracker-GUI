import customtkinter as ctk
from SettingsHelper import SettingsOption, NumberEntry, load_settings, save_settings_to_json
from LaunchHelper import IndicatorFrame
import re

class MainScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        #widget creation
        title_label = ctk.CTkLabel(self, text="Welcome to aiTracker!", font=ctk.CTkFont(size=40))
        subtitle_label = ctk.CTkLabel(self, text="Click below to get started", font=ctk.CTkFont(size=25))
        launch_button = ctk.CTkButton(self, text="Launch", corner_radius=10, command=lambda: self.show_screen_callback(LaunchScreen))
        about_button = ctk.CTkButton(self, text="Help", corner_radius=10, command=lambda: self.show_screen_callback(AboutScreen))
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
        about_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        
        # loads text from "help.txt" file and puts it into the about_frame
        with open("help.txt", 'r') as file:
            sections = file.read().split('\n')
        
        for i in range(0, len(sections)):
            if i % 2 == 0:
                header_label = ctk.CTkLabel(about_frame, text=sections[i], font=ctk.CTkFont(size=25))
                header_label.grid(row=i, column=0, padx=5, pady=5)
            else:
                body_label = ctk.CTkLabel(about_frame, text=sections[i], font=ctk.CTkFont(size=15), wraplength=500)
                body_label.grid(row=i, column=0, padx=5, pady=15)
        
        # widget placement
        back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)
        about_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # settings label and back button
        title = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=40))
        title.place(relx=.5, rely=.05, anchor=ctk.CENTER)
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.save_settings())
        back_button.place(relx=.5, rely=.95, anchor=ctk.CENTER)
        
        # frame to hold all settings
        settings_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        settings_frame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        # setting options widgets
        self.up = SettingsOption(settings_frame, name="Up")
        self.down = SettingsOption(settings_frame, name="Down")
        self.left = SettingsOption(settings_frame, name="Left")
        self.right = SettingsOption(settings_frame, name="Right")
        self.up_left = SettingsOption(settings_frame, name="Up Left")
        self.up_right = SettingsOption(settings_frame, name="Up Right")
        self.down_left = SettingsOption(settings_frame, name="Down Left")
        self.down_right = SettingsOption(settings_frame, name="Down Right")
        self.blink = SettingsOption(settings_frame, name="Blink")
        self.look_duration = NumberEntry(settings_frame, name="Look Duration")
        
        self.settings = [
            self.up, self.down, self.left, self.right, self.up_left,
            self.up_right, self.down_left, self.down_right, self.blink
        ]
        
        # setting placements
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
        
        # load settings from json
        settings_map = load_settings("settings.json")
        for setting in self.settings:
            setting.set_settings(settings_map[setting.name])
        self.look_duration.set_value(settings_map["Look Duration"])
    
    # saves all of the settings and returns back to the main screen
    def save_settings(self):
        new_settings = dict()
        invalid_pin = False
        
        for setting in self.settings:
            current_settings = setting.get_settings()
            
            # if the setting is active, check if the pin doesn't match
            if current_settings[0] and not re.match("^C[1-9]$|^D[0-7]$", current_settings[1]):
                invalid_pin = True
                break
            new_settings.update({setting.name:current_settings})
        
        new_settings.update(self.look_duration.get_value())
        # display warning message
        if not invalid_pin:
            self.show_screen_callback(MainScreen)
            save_settings_to_json(new_settings, "settings.json")
        else:
            warning = ctk.CTkLabel(self, text="1 or more pin values are invalid", font=ctk.CTkFont(size=30))
            warning.place(relx=.5, rely=.85, anchor=ctk.CENTER)

class LaunchScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # leave the screen when "b" is pressed
        root.bind("b", lambda event: self.leave_screen())
        self.focus_set()
        
        # indicator squares
        settings = load_settings("settings.json")
        self.up = IndicatorFrame(self, settings["Up"])
        self.down = IndicatorFrame(self, settings["Down"])
        self.left = IndicatorFrame(self, settings["Left"])
        self.right = IndicatorFrame(self, settings["Right"])
        self.up_left = IndicatorFrame(self, settings["Up Left"])
        self.up_right = IndicatorFrame(self, settings["Up Right"])
        self.down_left = IndicatorFrame(self, settings["Down Left"])
        self.down_right = IndicatorFrame(self, settings["Down Right"])
        self.blink = IndicatorFrame(self, settings["Blink"])
        
        #placing squares
        self.up_left.place(relx=0, rely=0, anchor=ctk.NW)
        self.up.place(relx=0.5, rely=0, anchor=ctk.N)
        self.up_right.place(relx=1, rely=0, anchor=ctk.NE)
        self.left.place(relx=0, rely=0.5, anchor=ctk.W)
        self.blink.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.right.place(relx=1, rely=0.5, anchor=ctk.E)
        self.down_left.place(relx=0, rely=1, anchor=ctk.SW)
        self.down.place(relx=0.5, rely=1, anchor=ctk.S)
        self.down_right.place(relx=1, rely=1, anchor=ctk.SE)
        
    def leave_screen(self):
        self.show_screen_callback(MainScreen)