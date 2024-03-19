import customtkinter as ctk
from widgets.NumberEntry import NumberEntry
from widgets.DirectionSetting import DirectionSetting

class BlinkSetting(DirectionSetting):
    '''
    Contains all of the necessary settings and information for modifying how a direction input is handled.
    '''

    def __init__(self, root, name):
        super().__init__(root, name)

        # widget creation
        self._blink_label = ctk.CTkLabel(self, text="Blink Duration (ms)", font=ctk.CTkFont(size=10))
        self._sensitivity_label = ctk.CTkLabel(self, text="Blink Sensitivity", font=ctk.CTkFont(size=10))
        self._blink_duration = NumberEntry(self)
        self._sensitivity_slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=20)

        # place widgets
        x_pad, y_pad = 2,2
        self._blink_label.grid(row=3, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._sensitivity_label.grid(row=3, column=2, columnspan=2, padx=x_pad, pady=y_pad)
        self._blink_duration.grid(row=4, column=0, columnspan=2, padx=x_pad, pady=y_pad)
        self._sensitivity_slider.grid(row=4, column=2, columnspan=2, padx=x_pad, pady=y_pad)
        
    def get_settings(self):
        '''
        Gets the settings for a blink input.
        '''
        return super().get_settings() + (self._blink_duration.get_numeric_value(), round(self._sensitivity_slider.get(), 2))
    
    def set_settings(self, settings):
        '''
        Sets the settings for a blink input.
        '''
        super().set_settings(settings)
        self._blink_duration.set_numeric_value(settings[4])
        self._sensitivity_slider.set(settings[5])