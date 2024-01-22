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
        self.configure(fg_color="white" if self._active else "transparent")
        
        # testing code
        if self._active:
            self.bind("<Button-1>", lambda event: self.change_color("green" if self.cget("fg_color") == "white" else "white", event))
    
    @property
    def active(self) -> bool:
        return self._active
    
    @property
    def pin(self) -> str:
        return self._pin
    
    @property
    def constant(self) -> bool:
        return self._constant
    
    def change_color(self, color, event):
        self.configure(fg_color=color)
        
'''
function to start a camera feed

function to end a camera feed

function to take frame from camera and crop it to data collection like ratio
fix the size of the image
enhance it using opencv
'''