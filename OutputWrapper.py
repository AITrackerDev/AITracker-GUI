import os
import platform
# sets environment variables before loading board module to prevent errors
os.environ["BLINKA_FT232H"] = "1"
if platform.system() == "Darwin":
    os.environ["DYLD_LIBRARY_PATH"] = "/usr/local/Cellar/libusb/1.0.26/lib"
elif platform.system() == "Windows":
    print("idk i'm on a mac")
import board