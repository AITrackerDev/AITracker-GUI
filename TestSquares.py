import tkinter as tk
import os
import platform
import ctypes
import subprocess as sp
import usb.core

class ArrowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arrow Key Input")
        self.label = tk.Label(root, text="Press arrow keys")
        self.label.pack()
        self.up_pin = digitalio.DigitalInOut(board.C0)
        self.up_pin.direction = digitalio.Direction.OUTPUT

        self.down_pin = digitalio.DigitalInOut(board.C1)
        self.down_pin.direction = digitalio.Direction.OUTPUT

        self.left_pin = digitalio.DigitalInOut(board.C2)
        self.left_pin.direction = digitalio.Direction.OUTPUT

        self.right_pin = digitalio.DigitalInOut(board.C3)
        self.right_pin.direction = digitalio.Direction.OUTPUT

        # Binding arrow key events
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)

        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.bind("<Key>", self.on_key)

        # Track pressed keys
        self.pressed_keys = set()

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)
        self.update_display()

    def on_key_release(self, event):
        self.pressed_keys.discard(event.keysym)
        self.up_pin.value = False

        self.down_pin.value = False

        self.left_pin.value = False

        self.right_pin.value = False
        self.update_display()

    def on_key(self, event):
        if event.keysym == "q":
            self.root.quit()

    def update_display(self):
        if "Up" in self.pressed_keys and "Left" in self.pressed_keys:
            direction = "North West"
            self.up_pin.value = True
            self.left_pin.value = True
        elif "Up" in self.pressed_keys and "Right" in self.pressed_keys:
            direction = "North East"
            self.up_pin.value = True
            self.right_pin.value = True
        elif "Down" in self.pressed_keys and "Left" in self.pressed_keys:
            direction = "South West"
            self.down_pin.value = True
            self.left_pin.value = True
        elif "Down" in self.pressed_keys and "Right" in self.pressed_keys:
            direction = "South East"
            self.down_pin.value = True
            self.right_pin.value = True
        elif "Up" in self.pressed_keys:
            direction = "North"
            self.up_pin.value = True
        elif "Down" in self.pressed_keys:
            direction = "South"
            self.down_pin.value = True
        elif "Left" in self.pressed_keys:
            direction = "West"
            self.left_pin.value = True
        elif "Right" in self.pressed_keys:
            direction = "East"
            self.right_pin.value = True
        else:
            direction = "Press arrow keys"
        self.label.config(text=direction)

def main():
    root = tk.Tk()
    root.geometry('720x480')
    app = ArrowApp(root)
    root.mainloop()

if __name__ == "__main__":
    # adafruit environment variable
    os.environ['BLINKA_FT232H'] = '1'

    # platform specific fixes
    if platform.system() == 'Windows':
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    elif platform.system() == 'Darwin':
        # find the version of libusb that's installed and set it as an environment variable
        version_path = sp.run('readlink -f $(brew --prefix libusb)', shell=True, capture_output=True).stdout.strip().decode('utf-8')
        os.environ['DYLD_LIBRARY_PATH'] = os.path.join(version_path, 'lib')
    
    import board
    import digitalio
    
    _usb_devices = usb.core.find(find_all=True)
    _device_found = False
    for device in _usb_devices:
        # FT323H specific values
        if device.idVendor == 0x0403 and device.idProduct == 0x6014:
            _device_found = True
            main()
    # display warning if the board isn't found
    if not _device_found:
        print('board not found')