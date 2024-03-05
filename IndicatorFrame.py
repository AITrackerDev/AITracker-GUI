'''
Indicator frame widget that sends outputs through the FT232H board.
'''
import customtkinter as ctk

DEBUG = True

class IndicatorFrame(ctk.CTkFrame):
    def __init__(self, root, settings):
        super().__init__(root, width=150, height=150)
        
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
    
    # send outputs over USB and change the color of the frame
    def send_output(self):
        if self._active:
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
                
    # reset the pin to false and change the color to white     
    def _reset_pin(self):
        self.configure(fg_color="white")
        if not DEBUG: self._pin.value = False
    
    # loads the modules dynamically to prevent the app from freaking out
    def _load_modules(self):
        global board, digitalio
        import board
        import digitalio