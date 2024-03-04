'''
All of the necessary functions and classes for the settings screen should be located in here.
'''
import customtkinter as ctk
import json
import re

PIN_REGEX = "^C[0-7]$|^D[4-7]$"

'''
A class that holds 2 entry widgets, switch, label, and checkbox for a specific setting.
'''
class SettingsOption(ctk.CTkFrame):
    def __init__(self, root, name):
        super().__init__(root)
        
        #setting info
        self._name = name
        self._label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        
        # active switch
        self._switch_var = ctk.BooleanVar(value=True)
        self._switch = ctk.CTkSwitch(self, variable=self._switch_var, onvalue=True, offvalue=False, text="Active")
        
        # pin entry
        self._pin_var = ctk.StringVar(value="")
        self._pin_input = ctk.CTkEntry(self, textvariable=self._pin_var)
        self._pin_input.bind("<KeyRelease>", self._validate_pin)
        
        # output duration entry
        self._duration_input = NumberEntry(self)
        
        # constant input widgets
        self._check_var = ctk.BooleanVar(value=False)
        self._check = ctk.CTkCheckBox(self, variable=self._check_var, onvalue=True, offvalue=False, text="Constant")
        
        #setting placements
        x_pad,y_pad = 5,5
        self._label.grid(row=0, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._check.grid(row=0, column=2, padx=x_pad, pady=y_pad)
        self._switch.grid(row=0, column=3, padx=x_pad, pady=y_pad)
        self._pin_input.grid(row=1, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._duration_input.grid(row=1, column=2, columnspan=2, padx=x_pad, pady=y_pad)
    
    @property
    def name(self) -> str:
        return self._name
        
    # checks if the pin matches the regex 
    def _validate_pin(self, *args):
        if re.match(PIN_REGEX, self._pin_var.get().strip()):
            self._pin_input.configure(text_color="green")
        else:
            self._pin_input.configure(text_color="red")
    
    # returns a dictionary mapping for the setting name, and all of the values  
    def get_settings(self):
        return (self._switch_var.get(), self._pin_var.get(), self._check_var.get(), self._duration_input.get_numeric_value())
    
    # sets the settings
    def set_settings(self, settings):
        self._switch_var.set(settings[0])
        self._pin_var.set(settings[1])
        self._check_var.set(settings[2])
        self._duration_input.set_numeric_value(settings[3])
        
        # if the pin was saved incorrectly, set the text color to indicate
        if re.match(PIN_REGEX, settings[1]):
            self._pin_input.configure(text_color="green")
        else:
            self._pin_input.configure(text_color="red")

'''
A setting option that only takes in a number.
'''
class SingleEntry(ctk.CTkFrame):
    def __init__(self, root, name):
        super().__init__(root)
        self.name = name
        
        # widgets
        label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        self._entry = NumberEntry(self)
        
        # placements
        label.grid(row=0, column=0, padx=5, pady=5)
        self._entry.grid(row=1, column=0, padx=5, pady=5)
    
    # validates that only a number can be an pin_input to the field
    def get_value(self):
        return {self.name:int(self._entry.get_numeric_value())}
        
    def set_value(self, input_value):
        self._entry.set_numeric_value(input_value)

'''
An entry widget that only allows integers to be put into it.
'''  
class NumberEntry(ctk.CTkEntry):
    def __init__(self, root):
        super().__init__(root)
        self._input_var = ctk.StringVar(value="")
        
        # ensures only a number can be put into the text field
        self.configure(validate="key", validatecommand=(self.register(self._validate_input), '%S', '%P'), textvariable=self._input_var)

    # ensures only a number can be put into the text field
    def _validate_input(self, char, entry_value):
        return char.isdigit() or char == ""
    
    # get number as an int
    def get_numeric_value(self):
        return int(self._input_var.get())

    # set the value
    def set_numeric_value(self, value):
        self._input_var.set(str(value))

def load_settings(json_path):
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

def save_settings_to_json(settings_dict, json_path):
    try:
        with open(json_path, 'w') as json_file:
            json.dump(settings_dict, json_file, indent=2)
    except Exception as e:
        print(f"Error saving data to '{json_path}': {e}")