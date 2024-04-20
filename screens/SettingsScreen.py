import customtkinter as ctk
import re
import json
import os
from widgets import DirectionSetting
from widgets import MiscSettings
from widgets.IndicatorSquare import PIN_REGEX
from widgets import BlinkSetting

class SettingsScreen(ctk.CTkFrame):
    '''
    The screen used to give the user an easy way to modify settings.
    '''
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer

        # settings label and back button
        _title = ctk.CTkLabel(self, text='Settings', font=ctk.CTkFont(size=40))
        _title.place(relx=.5, rely=.05, anchor=ctk.CENTER)
        _back_button = ctk.CTkButton(self, text='Back', command=lambda: self._save_settings())
        _back_button.place(relx=.5, rely=.95, anchor=ctk.CENTER)

        # frame to hold all settings
        _settings_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)
        _settings_frame.place(relx=.5, rely=.5, anchor=ctk.CENTER)

        # setting options widgets
        self._north = DirectionSetting(_settings_frame, name='North')
        self._south = DirectionSetting(_settings_frame, name='South')
        self._west = DirectionSetting(_settings_frame, name='West')
        self._east = DirectionSetting(_settings_frame, name='East')
        self._north_west = DirectionSetting(_settings_frame, name='North West')
        self._north_east = DirectionSetting(_settings_frame, name='North East')
        self._south_west = DirectionSetting(_settings_frame, name='South West')
        self._south_east = DirectionSetting(_settings_frame, name='South East')
        self._blink = BlinkSetting(_settings_frame, name='Blink')
        self._misc_settings = MiscSettings(_settings_frame, name='Look Duration')

        self._settings = [
            self._north, self._south, self._west, self._east, self._north_west,
            self._north_east, self._south_west, self._south_east, self._blink
        ]

        # setting placements
        self._north.grid(row=0, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._south.grid(row=0, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._west.grid(row=1, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._east.grid(row=1, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._north_west.grid(row=2, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._north_east.grid(row=2, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._south_west.grid(row=3, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._south_east.grid(row=3, column=1, padx=5, pady=5, sticky=ctk.NSEW)
        self._blink.grid(row=4, column=0, padx=5, pady=5, sticky=ctk.NSEW)
        self._misc_settings.grid(row=4, column=1, padx=5, pady=5, sticky=ctk.NSEW)

        # load settings from json
        settings_map = load_settings_from_json('settings.json')
        for setting in self._settings:
            setting.set_settings(settings_map[setting.name])
        self._misc_settings.set_value(settings_map['Look Duration'], settings_map['Demo Mode'])
    
    def _save_settings(self):
        '''
        Save the settings to a JSON file and return to the main screen.
        '''
        new_settings = dict()
        invalid_pin = False

        for setting in self._settings:
            current_settings = setting.get_settings()

            # check if the pin doesn't match
            if not re.match(PIN_REGEX, current_settings[1]):
                invalid_pin = True
                break
            new_settings.update({setting.name:current_settings})

        new_settings.update(self._misc_settings.get_value())
        
        # save settings
        if not invalid_pin:
            try:
                with open(os.path.join('settings.json'), 'w') as json_file:
                    json.dump(new_settings, json_file, indent=2)
            except Exception as e:
                print(f"Error saving data to 'settings.json': {e}")
            self._screen_changer('MainScreen')
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