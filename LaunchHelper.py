'''
All of the necessary functions for the launch screen should be located in here.
'''
import customtkinter as ctk

DEBUG = True

class IndicatorFrame(ctk.CTkFrame):
    def __init__(self, root, settings):
        super().__init__(root)
        
        # loads in modules once reaching this screen
        if not DEBUG:
            self._load_modules()
        
        # set the properties of the frame
        self._active = settings[0]
        if self._active and not DEBUG:
            try:
                self._pin = digitalio.DigitalInOut(getattr(board, settings[1]))
                self._pin.direction = digitalio.Direction.OUTPUT
            except Exception as e:
                error = ctk.CTkLabel(self, text=f"Error: {e}. Please restart application", font=ctk.CTkFont(size=15), wraplength=200, text_color='black')
                error.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        self._constant = settings[2]
        self._out_duration = settings[3]
        
        # don't show the frame if the setting isn't active
        self.configure(fg_color="white" if self._active else "transparent")
    
    @property
    def active(self) -> bool:
        return self._active
    
    @property
    def constant(self) -> bool:
        return self._constant
    
    # change the color of the frame depending on what the settings are
    def send_output(self):
        if self.active:
            if self._constant:
                if self.cget("fg_color") == "white":
                    self.configure(fg_color="green")
                    if not DEBUG: self._pin.value = True
                else:
                    self.configure(fg_color="white")
                    if not DEBUG: self._pin.value = False
            else:
                if not DEBUG: self._pin.value = True
                self.configure(fg_color="green")
                self.after(self._out_duration, lambda: self._reset_pin())
            
    def _reset_pin(self):
        self.configure(fg_color="white")
        if not DEBUG: self._pin.value = False
    
    def _load_modules(self):
        global board, digitalio
        import board
        import digitalio
        
'''
function to start a camera feed

function to end a camera feed

function to take frame from camera and crop it to data collection like ratio
fix the size of the image
enhance it using opencv
'''