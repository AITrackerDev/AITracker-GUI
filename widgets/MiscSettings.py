import customtkinter as ctk
from widgets.NumberEntry import NumberEntry

class MiscSettings(ctk.CTkFrame):
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
        
        # demo mode
        demo = ctk.CTkLabel(self, text='Demo Mode', font=ctk.CTkFont(size=20))
        description = ctk.CTkLabel(self, text='Runs application without sending USB outputs', font=ctk.CTkFont(size=10))
        
        self._check_var = ctk.BooleanVar(value=False)
        self._check = ctk.CTkCheckBox(self, variable=self._check_var, onvalue=True, offvalue=False, text='Requires Restart')
        
        # placements
        x_pad,y_pad = 2,2
        label.grid(row=0, column=0, padx=x_pad, pady=y_pad)
        ms.grid(row=1, column=0, padx=x_pad, pady=y_pad)
        self._entry.grid(row=2, column=0, padx=x_pad, pady=y_pad)
        demo.grid(row=0, column=2, padx=x_pad, pady=y_pad)
        description.grid(row=1, column=2, padx=x_pad, pady=y_pad)
        self._check.grid(row=2, column=2, padx=x_pad, pady=y_pad)
        

    def get_value(self):
        '''
        Get the number in the setting.
        '''
        return {self._name:int(self._entry.get_numeric_value()), 'Demo Mode':self._check_var.get()}
        
    def set_value(self, input_value, demo_value):
        '''
        Set the number in the setting.
        '''
        self._entry.set_numeric_value(input_value)
        self._check_var.set(demo_value)