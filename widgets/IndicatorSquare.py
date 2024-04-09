import customtkinter as ctk

PIN_REGEX = "^C[0-7]$|^D[4-7]$"

class IndicatorSquare(ctk.CTkFrame):
    '''
    Indicator frame widget that sends outputs through the FT232H board.
    '''
    
    def __init__(self, root, settings, demo):
        super().__init__(root, width=100, height=100)
        
        self._demo = demo
        
        # loads in modules once reaching the launch screen
        if not self._demo:
            self._load_modules()
        
        # set the properties of the frame
        self._active = settings[0]
        if self._active and not self._demo:
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
    
    def send_output(self):
        '''
        Send outputs over USB and change the color of the frame.
        '''
        if self._active:
            if self._constant:
                if self.cget("fg_color") == "white":
                    self.configure(fg_color="green")
                    if not self._demo: self._pin.value = True
                else:
                    self.configure(fg_color="white")
                    if not self._demo: self._pin.value = False
            else:
                if not self._demo: self._pin.value = True
                self.configure(fg_color="green")
                self.after(self._out_duration, lambda: self._reset_pin())
                     
    def _reset_pin(self):
        '''
        Reset the pin to false and change the color to white.
        '''
        self.configure(fg_color="white")
        if not self._demo: self._pin.value = False
    
    def _load_modules(self):
        '''
        Loads the breakout board modules dynamically to prevent the app from freaking out.
        '''
        global board, digitalio
        import board
        import digitalio