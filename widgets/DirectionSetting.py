import customtkinter as ctk
import re
from widgets.NumberEntry import NumberEntry
from widgets.IndicatorSquare import PIN_REGEX

class DirectionSetting(ctk.CTkFrame):
    '''
    Contains all of the necessary settings and information for modifying how a direction input is handled.
    '''

    def __init__(self, root, name):
        super().__init__(root)
        
        #setting info
        self._name = name
        self._label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        
        # active switch
        self._switch_var = ctk.BooleanVar(value=True)
        self._switch = ctk.CTkSwitch(self, variable=self._switch_var, onvalue=True, offvalue=False, text="Active")
        
        # pin entry
        self._pin = ctk.CTkLabel(self, text='FT232H Pin Value', font=ctk.CTkFont(size=10))
        self._pin_var = ctk.StringVar(value="")
        self._pin_input = ctk.CTkEntry(self, textvariable=self._pin_var)
        self._pin_input.bind("<KeyRelease>", self._validate_pin)
        
        # output duration entry
        self._duration = ctk.CTkLabel(self, text='Output Duration (ms)', font=ctk.CTkFont(size=10))
        self._duration_input = NumberEntry(self)
        
        # constant input widgets
        self._check_var = ctk.BooleanVar(value=False)
        self._check = ctk.CTkCheckBox(self, variable=self._check_var, onvalue=True, offvalue=False, text="Constant")
        
        #setting placements
        x_pad,y_pad = 2,2
        self._label.grid(row=0, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._check.grid(row=0, column=2, padx=x_pad, pady=y_pad)
        self._switch.grid(row=0, column=3, padx=x_pad, pady=y_pad)
        self._pin.grid(row=1, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._duration.grid(row=1, column=2, columnspan=2, padx=x_pad, pady=y_pad)
        self._pin_input.grid(row=2, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._duration_input.grid(row=2, column=2, columnspan=2, padx=x_pad, pady=y_pad)
    
    @property
    def name(self) -> str:
        '''
        Name of the setting.
        '''
        
        return self._name
        
    def _validate_pin(self, *args):
        '''
        Checks if the text input matches the regex.
        '''
        
        if re.match(PIN_REGEX, self._pin_var.get().strip()):
            self._pin_input.configure(text_color="green")
        else:
            self._pin_input.configure(text_color="red")
    
    def get_settings(self):
        '''
        Returns a dictionary mapping for the setting name, and all of the values.
        '''
        
        return (self._switch_var.get(), self._pin_var.get(), self._check_var.get(), self._duration_input.get_numeric_value())
    
    def set_settings(self, settings):
        '''
        Sets the settings.
        '''
        
        self._switch_var.set(settings[0])
        self._pin_var.set(settings[1])
        self._check_var.set(settings[2])
        self._duration_input.set_numeric_value(settings[3])
        
        # if the pin was saved incorrectly, set the text color to indicate
        if re.match(PIN_REGEX, settings[1]):
            self._pin_input.configure(text_color="green")
        else:
            self._pin_input.configure(text_color="red")