import os

import customtkinter as ctk
from SettingsHelper import SettingsOption, SingleEntry, load_settings, save_settings_to_json, PIN_REGEX
from LaunchHelper import IndicatorFrame
import re
# import usb.core
import cv2
from NetworkInput import network_image_crop, IMAGE_SIZE
from PIL import Image, ImageTk
from AITrackerModel import AITrackerModel

DEBUG = True

class MainScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        #widget creation
        _title_label = ctk.CTkLabel(self, text="Welcome to aiTracker!", font=ctk.CTkFont(size=40))
        _subtitle_label = ctk.CTkLabel(self, text="Click below to get started", font=ctk.CTkFont(size=25))
        _launch_button = ctk.CTkButton(self, text="Launch", corner_radius=10, command=lambda: self._load_launch_screen())
        _about_button = ctk.CTkButton(self, text="Help", corner_radius=10, command=lambda: self.show_screen_callback(AboutScreen))
        _settings_button = ctk.CTkButton(self, text="Settings", corner_radius=10, command=lambda: self.show_screen_callback(SettingsScreen))
        _quit_button = ctk.CTkButton(self, text="Quit", corner_radius=10, command=lambda: root.destroy())

        #widget placement
        _title_label.place(relx=.5, rely=0.3, anchor=ctk.CENTER)
        _subtitle_label.place(relx=.5, rely=0.35, anchor=ctk.CENTER)
        _launch_button.place(relx=.5, rely=0.55, anchor=ctk.CENTER)
        _about_button.place(relx=.5, rely=0.6, anchor=ctk.CENTER)
        _settings_button.place(relx=.5, rely=0.65, anchor=ctk.CENTER)
        _quit_button.place(relx=.5, rely=0.7, anchor=ctk.CENTER)
        
    # checks if the FT232H board is plugged in, and won't continue unless it is
    def _load_launch_screen(self):
        # _usb_devices = usb.core.find(find_all=True)
        _device_found = False

        # for device in _usb_devices:
        #     if device.idVendor == 0x0403 and device.idProduct == 0x6014:
        #         _device_found = True
        #         self.show_screen_callback(LaunchScreen)

        # display warning if not
        if not _device_found:
            warning = ctk.CTkLabel(self, text="Please plug in FT232H breakout board to continue.", font=ctk.CTkFont(size=25))
            warning.place(relx=.5, rely=.45, anchor=ctk.CENTER)
        
        if DEBUG:
            self.show_screen_callback(LaunchScreen)

class AboutScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # widget creation
        _back_button = ctk.CTkButton(self, text="Back", command=lambda: self.show_screen_callback(MainScreen))
        _about_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        
        # loads text from "help.txt" file and puts it into the about_frame
        with open("help.txt", 'r') as file:
            sections = file.read().split('\n')
        
        for i in range(0, len(sections)):
            if i % 2 == 0:
                _header_label = ctk.CTkLabel(_about_frame, text=sections[i], font=ctk.CTkFont(size=25))
                _header_label.grid(row=i, column=0, padx=5, pady=5)
            else:
                _body_label = ctk.CTkLabel(_about_frame, text=sections[i], font=ctk.CTkFont(size=15), wraplength=500)
                _body_label.grid(row=i, column=0, padx=5, pady=15)
        
        # widget placement
        _back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)
        _about_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # settings label and back button
        _title = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=40))
        _title.place(relx=.5, rely=.05, anchor=ctk.CENTER)
        _back_button = ctk.CTkButton(self, text="Back", command=lambda: self._save_settings())
        _back_button.place(relx=.5, rely=.95, anchor=ctk.CENTER)
        
        # frame to hold all settings
        _settings_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        _settings_frame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        # setting options widgets
        self._up = SettingsOption(_settings_frame, name="Up")
        self._down = SettingsOption(_settings_frame, name="Down")
        self._left = SettingsOption(_settings_frame, name="Left")
        self._right = SettingsOption(_settings_frame, name="Right")
        self._up_left = SettingsOption(_settings_frame, name="Up Left")
        self._up_right = SettingsOption(_settings_frame, name="Up Right")
        self._down_left = SettingsOption(_settings_frame, name="Down Left")
        self._down_right = SettingsOption(_settings_frame, name="Down Right")
        self._blink = SettingsOption(_settings_frame, name="Blink")
        self._look_duration = SingleEntry(_settings_frame, name="Look Duration")
        
        self._settings = [
            self._up, self._down, self._left, self._right, self._up_left,
            self._up_right, self._down_left, self._down_right, self._blink
        ]
        
        # setting placements
        self._up.grid(row=0, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._down.grid(row=0, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._left.grid(row=1, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._right.grid(row=1, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._up_left.grid(row=2, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._up_right.grid(row=2, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._down_left.grid(row=3, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._down_right.grid(row=3, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._blink.grid(row=4, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._look_duration.grid(row=4, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        
        # load settings from json
        settings_map = load_settings("settings.json")
        for setting in self._settings:
            setting.set_settings(settings_map[setting.name])
        self._look_duration.set_value(settings_map["Look Duration"])
    
    # saves all the settings and returns back to the main screen
    def _save_settings(self):
        new_settings = dict()
        invalid_pin = False
        
        for setting in self._settings:
            current_settings = setting.get_settings()
            
            # if the setting is active, check if the pin doesn't match
            if current_settings[0] and not re.match(PIN_REGEX, current_settings[1]):
                invalid_pin = True
                break
            new_settings.update({setting.name:current_settings})
        
        new_settings.update(self._look_duration.get_value())
        # display warning message
        if not invalid_pin:
            self.show_screen_callback(MainScreen)
            save_settings_to_json(new_settings, "settings.json")
        else:
            warning = ctk.CTkLabel(self, text="One or more pin values are invalid", font=ctk.CTkFont(size=30))
            warning.place(relx=.5, rely=.85, anchor=ctk.CENTER)

class LaunchScreen(ctk.CTkFrame):
    def __init__(self, root, show_screen_callback):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.show_screen_callback = show_screen_callback
        
        # network and model code
        self._model = AITrackerModel('image_classifier.model', 'H5Demo/final_eye_data.h5')
        
        # value to know whether the screen has been exited
        self._active = True
        
        # leave the screen when "b" is pressed
        root.bind("b", lambda event: self.leave_screen(root))
        self.focus_set()
        
        # indicator squares
        _settings = load_settings("settings.json")
        self._up = IndicatorFrame(self, _settings["Up"])
        self._down = IndicatorFrame(self, _settings["Down"])
        self._left = IndicatorFrame(self, _settings["Left"])
        self._right = IndicatorFrame(self, _settings["Right"])
        self._up_left = IndicatorFrame(self, _settings["Up Left"])
        self._up_right = IndicatorFrame(self, _settings["Up Right"])
        self._down_left = IndicatorFrame(self, _settings["Down Left"])
        self._down_right = IndicatorFrame(self, _settings["Down Right"])
        self._blink = IndicatorFrame(self, _settings["Blink"])
        self._look_duration = _settings["Look Duration"]
        
        # dictionary for the outputs being able to be sent out over hardware
        self._outputs = {'b\'North\'':self._up, 'b\'South\'':self._down, 'b\'West\'':self._left, 'b\'East\'':self._right,
            'b\'North West\'':self._up_left, 'b\'North East\'':self._up_right, 'b\'South West\'':self._down_left,
            'b\'South East\'':self._down_right}
        
        #placing squares
        self._up_left.place(relx=0, rely=0, anchor=ctk.NW)
        self._up.place(relx=0.5, rely=0, anchor=ctk.N)
        self._up_right.place(relx=1, rely=0, anchor=ctk.NE)
        self._left.place(relx=0, rely=0.5, anchor=ctk.W)
        self._blink.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self._right.place(relx=1, rely=0.5, anchor=ctk.E)
        self._down_left.place(relx=0, rely=1, anchor=ctk.SW)
        self._down.place(relx=0.5, rely=1, anchor=ctk.S)
        self._down_right.place(relx=1, rely=1, anchor=ctk.SE)
        
        # camera related code and widgets
        self.cam = cv2.VideoCapture(0)
        self.canvas = ctk.CTkCanvas(self, width=IMAGE_SIZE[0], height=IMAGE_SIZE[1])
        self.canvas.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        
        self._update_camera()
    
    # update camera feed and display cropped image   
    def _update_camera(self):
        ret, frame = self.cam.read()
        if ret:
            # crop the image to our network's expectation
            network_image = network_image_crop(cv2.flip(frame, 1))
            image_display, image_network, correct = network_image[0], network_image[0]/255.0, network_image[1]
            
            # if the image is valid
            if correct:
                # put image on screen if it's properly resized
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(image_display, cv2.COLOR_BGR2RGB)))
                cv2.imwrite('eye_image.jpg', image_display)
                self.canvas.create_image(0, 0, image=self.photo, anchor=ctk.NW)
                
                # network and output logic should go here
                prediction = self._model.predict_direction(cv2.imread('eye_image.jpg'))
                print(prediction)
                IndicatorFrame.send_output(self, self._outputs[prediction])

                if os.path.exists('images/eye_image.jpg'):
                    os.remove('images/eye_image.jpg')



            else:
                # inform the user their eyes aren't being seen
                print("temporary text so the if else block doesn't break")
        self.after(10, self._update_camera)
        
    def leave_screen(self, root):
        self._active = False
        self.cam.release()
        root.unbind('b')
        self.show_screen_callback(MainScreen)