import customtkinter as ctk
import re
import json
from widgets.DirectionSetting import DirectionSetting
from widgets.NumberSetting import NumberSetting
from widgets.IndicatorSquare import PIN_REGEX

class SettingsScreen(ctk.CTkFrame):
    '''
    The screen used to give the user an easy way to modify settings.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self.screen_changer = screen_changer

        # settings label and back button
        _title = ctk.CTkLabel(self, text='Settings', font=ctk.CTkFont(size=40))
        _title.place(relx=.5, rely=.05, anchor=ctk.CENTER)
        _back_button = ctk.CTkButton(self, text='Back', command=lambda: self._save_settings())
        _back_button.place(relx=.5, rely=.95, anchor=ctk.CENTER)

        # frame to hold all settings
        _settings_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        _settings_frame.place(relx=.5, rely=.5, anchor=ctk.CENTER)

        # setting options widgets
        self._up = DirectionSetting(_settings_frame, name='Up')
        self._down = DirectionSetting(_settings_frame, name='Down')
        self._left = DirectionSetting(_settings_frame, name='Left')
        self._right = DirectionSetting(_settings_frame, name='Right')
        self._up_left = DirectionSetting(_settings_frame, name='Up Left')
        self._up_right = DirectionSetting(_settings_frame, name='Up Right')
        self._down_left = DirectionSetting(_settings_frame, name='Down Left')
        self._down_right = DirectionSetting(_settings_frame, name='Down Right')
        self._blink = DirectionSetting(_settings_frame, name='Blink')
        self._look_duration = NumberSetting(_settings_frame, name='Input Duration')

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
        settings_map = load_settings_from_json('settings.json')
        for setting in self._settings:
            setting.set_settings(settings_map[setting.name])
        self._look_duration.set_value(settings_map['Input Duration'])
    
    def _save_settings(self):
        '''
        Save the settings to a JSON file and return to the main screen.
        '''
        
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
        
        # save settings
        if not invalid_pin:
            self.screen_changer('MainScreen')
            try:
                with open('settings.json', 'w') as json_file:
                    json.dump(new_settings, json_file, indent=2)
            except Exception as e:
                print(f"Error saving data to 'settings.json': {e}")
        # display warning message
        else:
            warning = ctk.CTkLabel(self, text='One or more pin values are invalid', font=ctk.CTkFont(size=30))
            warning.place(relx=.5, rely=.85, anchor=ctk.CENTER)

def load_settings_from_json(json_path):
    '''
    Loads in the settings from a specified path to a JSON file.
    '''
    
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        # convert arrays to tuples
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = tuple(value)

        return data
    except FileNotFoundError:
        print(f"File '{json_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{json_path}'.")
        return {}