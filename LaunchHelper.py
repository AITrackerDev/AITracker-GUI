'''
All of the necessary functions for the launch screen should be located in here.
'''
import customtkinter as ctk
import random

class IndicatorFrame(ctk.CTkFrame):
    def __init__(self, root, settings):
        super().__init__(root)
        self.active = settings[0]
        self.configure(fg_color="white")
        self.bind("<Button-1>", self.change_color)
    
    def change_color(self, event):
        self.configure(fg_color="#{:06x}".format(random.randint(0, 0xFFFFFF))) 
        
'''
class to make a frame with a color
be able to change the color of that frame
make it so once it's clicked, it changes color

function to start a camera feed

function to end a camera feed

function to take frame from camera and crop it to data collection like ratio
fix the size of the image
enhance it using opencv
'''