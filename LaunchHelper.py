'''
All of the necessary functions for the launch screen should be located in here.
'''
import customtkinter as ctk
import random

class IndicatorFrame(ctk.CTkFrame):
    def __init__(self, root, settings):
        super().__init__(root)
        
        # set the properties of the frame
        self._active = settings[0]
        self._pin = settings[1]
        self._constant = settings[2]
        self._out_duration = settings[3]
        
        # don't show the frame if the setting isn't active
        self.configure(fg_color="white" if self._active else "transparent")
        
        # testing code
        if self._active:
            self.bind("<Button-1>", self.change_color)
    
    @property
    def active(self) -> bool:
        return self._active
    
    @property
    def pin(self) -> str:
        return self._pin
    
    @property
    def constant(self) -> bool:
        return self._constant
    
    # change the color of the frame depending on what the settings are
    def change_color(self, event):
        if self._constant and self._active:
            if self.cget("fg_color") == "white":
                self.configure(fg_color="green")
            else:
                self.configure(fg_color="white")
        elif self._active:
            self.configure(fg_color="green")
            self.after(self._out_duration, lambda: self.configure(fg_color="white"))
        
'''
function to start a camera feed

function to end a camera feed

function to take frame from camera and crop it to data collection like ratio
fix the size of the image
enhance it using opencv
'''