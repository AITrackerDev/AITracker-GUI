import cv2
import multiprocessing
from multiprocessing import Queue
import tkinter as tk
from PIL import Image, ImageTk
import time

def capture_frames(frame_queue):
    cap = cv2.VideoCapture(0)  # Open webcam (adjust the index if you have multiple webcams)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put(frame)  # Put the frame into the queue

    cap.release()

def display_frames(frame_queue, root):
    canvas = tk.Canvas(root)
    canvas.pack()

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()  # Get frame from the queue
            # Convert frame to ImageTk format
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            root.update()  # Update the Tkinter window
            # Keep updating the window with the latest frame
        else:
            time.sleep(0.01)  # Sleep briefly if queue is empty

def main():
    frame_queue = Queue()  # Queue for passing frames between processes
    root = tk.Tk()

    # Start capture process
    capture_process = multiprocessing.Process(target=capture_frames, args=(frame_queue,))
    capture_process.start()

    # Start display process
    display_process = multiprocessing.Process(target=display_frames, args=(frame_queue, root))
    display_process.start()

    # Wait for processes to finish
    capture_process.join()
    display_process.join()

    root.mainloop()

if __name__ == "__main__":
    main()
