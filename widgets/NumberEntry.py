import customtkinter as ctk

class NumberEntry(ctk.CTkEntry):
    '''
    An entry widget that only allows integers to be put into it.
    '''  
    def __init__(self, root):
        super().__init__(root)
        self._input_var = ctk.StringVar(value="")
        
        # ensures only a number can be put into the text field
        self.configure(validate="key", validatecommand=(self.register(self._validate_input), '%S', '%P'), textvariable=self._input_var)

    def _validate_input(self, char, entry_value):
        '''
        Ensures only a number can be put into the text field.
        '''
        
        return char.isdigit() or char == ""
    
    def get_numeric_value(self):
        '''
        Get number as an int.
        '''
        
        return int(self._input_var.get())

    def set_numeric_value(self, value):
        '''
        Set the value.
        '''
        
        self._input_var.set(str(value))