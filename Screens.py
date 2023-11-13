'''
This file contains all of the code for all of the different screens contained within the application.
Each screen contains it's own set of widgets that are placed on their respective frames.
'''
import customtkinter as ctk

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

class LaunchScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # widget creation
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_screen_callback(MainScreen))
        # widget placement
        back_button.place(relx=.5, rely=0.7, anchor=ctk.CENTER)
        '''
        b key goes back
        camera feed
        9 sections for each input
            each lights up when input is recognized
            overlay on top of the camera feed
        '''
     
class AboutScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # widget creation
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_screen_callback(MainScreen))
        # widget placement
        back_button.place(relx=.5, rely=0.7, anchor=ctk.CENTER)
        '''
        what screen needs:
        frame to load all the objects
        title text
        about text
        back button to main_screen
        '''
   
class SettingsScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # widget creation
        back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_screen_callback(MainScreen))
        # widget placement
        back_button.place(relx=.5, rely=0.7, anchor=ctk.CENTER)
        '''
        what screen needs
        title text
        mode selection text
        radio buttons for the 2 different modes
        pin value text
        4 input fields
        4 text boxes for each direction text
        blink detection box
        input field for blink pin
            depends on whether or not the input field is on or off
        '''