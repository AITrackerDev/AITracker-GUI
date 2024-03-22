import customtkinter as ctk
from widgets.IndicatorSquare import IndicatorSquare
from screens.SettingsScreen import load_settings_from_json

settings = load_settings_from_json('settings.json')
demo = True

# Create the main window
root = ctk.CTk()

# Set the window size to full screen
root.attributes('-fullscreen', True)

# Function to exit fullscreen mode and close the window
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)
    root.destroy()
    
up = IndicatorSquare(root, settings['Up'], demo)
down = IndicatorSquare(root, settings['Down'], demo)
left = IndicatorSquare(root, settings['Left'], demo)
right = IndicatorSquare(root, settings['Right'], demo)
up_left = IndicatorSquare(root, settings['Up Left'], demo)
up_right = IndicatorSquare(root, settings['Up Right'], demo)
down_left = IndicatorSquare(root, settings['Down Left'], demo)
down_right = IndicatorSquare(root, settings['Down Right'], demo)
blink = IndicatorSquare(root, settings['Blink'], demo)

up_left.place(relx=0, rely=0, anchor=ctk.NW)
up.place(relx=0.5, rely=0, anchor=ctk.N)
up_right.place(relx=1, rely=0, anchor=ctk.NE)
left.place(relx=0, rely=0.5, anchor=ctk.W)
blink.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
right.place(relx=1, rely=0.5, anchor=ctk.E)
down_left.place(relx=0, rely=1, anchor=ctk.SW)
down.place(relx=0.5, rely=1, anchor=ctk.S)
down_right.place(relx=1, rely=1, anchor=ctk.SE)

# Bind the escape key to exit fullscreen mode
root.bind('<Escape>', exit_fullscreen)

# Run the Tkinter event loop
root.mainloop()
