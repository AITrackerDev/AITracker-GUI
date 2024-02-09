'''
This file contains all of the necessary code to start the application and run through all of the necessary startup requirements.
'''

import os
import platform

# sets environment variables before loading board module to prevent errors
os.environ["BLINKA_FT232H"] = "1"
if platform.system() == "Darwin":
    os.environ["DYLD_LIBRARY_PATH"] = "/usr/local/Cellar/libusb/1.0.26/lib"
elif platform.system() == "Windows":
    print("idk i'm on a mac")

import ctypes
import cv2
import tkinter as tk
from tkinter import Canvas, PhotoImage
import customtkinter as ctk
from Screens import MainScreen

class AITracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_screen = None

        # window setup
        self.title("aiTracker")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.geometry("1080x720")  # Original size
        self.attributes('-topmost', 1)
        self.update()
        self.attributes('-topmost', 0)
        self.wm_attributes("-fullscreen", True)
        self.show_screen(MainScreen)

        # open the webcam
        self.cap = None

        # create a button to open the webcam feed in a separate window
        self.open_camera_button = ctk.CTkButton(self, text="Open Camera", command=self.open_camera_window)
        self.open_camera_button.pack(side=tk.TOP)

    def open_camera_window(self):
        # Create a new Toplevel window for the camera feed
        self.cap = cv2.VideoCapture(0)
        camera_window = ctk.CTkToplevel(self)
        camera_window.title("Camera Feed")

        # Create a canvas to display the webcam feed in the new window
        camera_canvas = Canvas(camera_window, width=640, height=480)  # Adjust dimensions based on your webcam resolution
        camera_canvas.pack()

        # Start updating the frame in the new window
        self.update_frame(camera_canvas)

    def update_frame(self, canvas):
        ret, frame = self.cap.read()

        if ret:
            # flip image
            frame = cv2.flip(frame, 1)
            # Convert BGR image to RGB
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # If the image is grayscale, convert it to RGB
            if len(gray.shape) == 2:
                gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

            # Resize the image to fit the canvas dimensions
            h, w, _ = gray.shape
            ratio_w = canvas.winfo_width() / w
            ratio_h = canvas.winfo_height() / h
            ratio = min(ratio_w, ratio_h)

            new_w = int(w * ratio)
            new_h = int(h * ratio)

            # Ensure that new dimensions are valid
            if new_w > 0 and new_h > 0:
                resized_image = cv2.resize(gray, (new_w, new_h))

                # Convert the resized image to a PhotoImage object
                photo = PhotoImage(data=cv2.imencode('.ppm', resized_image)[1].tobytes())

                # Update the canvas with the new image
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                canvas.image = photo

            # Repeat the update after a delay (in milliseconds)
            canvas.after(10, lambda: self.update_frame(canvas))
        else:
            # If there's an issue reading the frame, stop updating
            self.cap.release()

    def show_screen(self, screen_class):
        # Destroy current screen if exists
        if self.current_screen:
            self.current_screen.destroy()

        # Create and display the requested screen
        self.current_screen = screen_class(self, self.show_screen)
        self.current_screen.pack()

    def __del__(self):
        # Release the camera when the AITracker object is deleted
        self.cap.release()

if __name__ == "__main__":
    # fixes the GUI being bugged in windows
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    app = AITracker()
    app.mainloop()