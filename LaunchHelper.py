'''
All of the necessary functions for the launch screen should be located in here.
'''
import customtkinter as ctk
import random

class IndicatorFrame(ctk.CTkFrame):
    def __init__(self, root, settings, look_duration_time):
        super().__init__(root)
        
        # set the properties of the frame
        self.active = settings[0]
        self.constant = settings[2]
        self.duration = look_duration_time
        self.configure(fg_color="white" if self.active else "transparent")
        
        # testing code
        if self.active:
            self.bind("<Button-1>", self.change_color)
    
    def change_color(self, event):
        if self.constant:
            if self.cget("fg_color") == "white":
                self.configure(fg_color="green")
            else:
                self.configure(fg_color="white")
        else:
            self.configure(fg_color="green")
            self.after(self.duration, lambda: self.configure(fg_color="white")) 
        
'''
function to start a camera feed

function to end a camera feed

function to take frame from camera and crop it to data collection like ratio
fix the size of the image
enhance it using opencv
'''