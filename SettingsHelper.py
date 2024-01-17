'''
All of the necessary functions for the settings screen should be located in here.
'''
import customtkinter as ctk

class SettingsOption(ctk.CTkFrame):
    def __init__(self, root, name):
        super().__init__(root)
        
        #setting widgets
        self.name = name
        self.label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        self.switch_var = ctk.BooleanVar(value=True)
        self.switch = ctk.CTkSwitch(self, variable=self.switch_var, onvalue=True, offvalue=False, text="Active")
        
        self.input_var = ctk.StringVar(value="")
        self.input = ctk.CTkEntry(self, textvariable=self.input_var, placeholder_text="Pin Value")
        
        self.check_var = ctk.BooleanVar(value=False)
        self.check = ctk.CTkCheckBox(self, variable=self.check_var, onvalue=True, offvalue=False, text="Constant Input")
        
        #setting placements
        self.label.grid(row=0, column=0, padx=5, pady=5)
        self.switch.grid(row=0, column=1, padx=5, pady=5)
        self.input.grid(row=1, column=0, padx=5, pady=5)
        self.check.grid(row=1, column=1, padx=5, pady=5)
    
    # returns a dictionary mapping for the setting name, and all of the values  
    def get_settings(self):
        return {self.name: (self.switch_var.get(), self.input_var.get(), self.check_var.get())}
    
    def set_settings(self, switch_value, input_value, check_value):
        self.switch_var.set(switch_value)
        self.input_var.set(input_value)
        self.check_var.set(check_value)

class EntrySetting(ctk.CTkFrame):
    def __init__(self, root, name):
        super().__init__(root)
        validate_cmd = root.register(self.validate_input)
        self.name = name
        
        # widgets
        label = ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=20))
        self.entry_var = ctk.StringVar(value="0")
        entry = ctk.CTkEntry(self, textvariable=self.entry_var, validate="key", validatecommand=(validate_cmd, "%P"))
        
        # placements
        label.grid(row=0, column=0, padx=5, pady=5)
        entry.grid(row=1, column=0, padx=5, pady=5)
    
    # validates that only a number can be an input to the field
    def validate_input(self, new_value):
        try:
            if new_value == "":
                return True
            
            float(new_value)
            return True
        except ValueError:
            return False
    
    def get_value(self):
        return {self.name:int(self.entry_var.get())}
        
    def set_value(self, input_value):
        self.entry_var.set(str(input_value))