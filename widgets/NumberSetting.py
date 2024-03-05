import customtkinter as ctk
from widgets.NumberEntry import NumberEntry

class NumberSetting(ctk.CTkFrame):
    '''
    A setting option that only takes in a number.
    '''

    def __init__(self, root, name):
        super().__init__(root)
        self.name = name
        
        # widgets
        label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        self._entry = NumberEntry(self)
        
        # placements
        label.grid(row=0, column=0, padx=5, pady=5)
        self._entry.grid(row=1, column=0, padx=5, pady=5)

    def get_value(self):
        '''
        Get the number in the setting.
        '''
        
        return {self.name:int(self._entry.get_numeric_value())}
        
    def set_value(self, input_value):
        '''
        Set the number in the setting.
        '''
        
        self._entry.set_numeric_value(input_value)