import customtkinter as ctk
from widgets.NumberEntry import NumberEntry

class NumberSetting(ctk.CTkFrame):
    '''
    A setting option that only takes in a number.
    '''

    def __init__(self, root, name):
        super().__init__(root)
        self._name = name
        
        # widgets
        label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        ms = ctk.CTkLabel(self, text='Milliseconds', font=ctk.CTkFont(size=10))
        self._entry = NumberEntry(self)
        
        # placements
        x_pad,y_pad = 2,2
        label.grid(row=0, column=0, padx=x_pad, pady=y_pad)
        ms.grid(row=1, column=0, padx=x_pad, pady=y_pad)
        self._entry.grid(row=2, column=0, padx=x_pad, pady=y_pad)

    def get_value(self):
        '''
        Get the number in the setting.
        '''
        
        return {self._name:int(self._entry.get_numeric_value())}
        
    def set_value(self, input_value):
        '''
        Set the number in the setting.
        '''
        
        self._entry.set_numeric_value(input_value)