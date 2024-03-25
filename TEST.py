import threading
import time

# Define a method that will be executed by the thread
def time_consuming_task():
    print("Starting time-consuming task...")
    time.sleep(5)  # Simulate a time-consuming task (e.g., I/O operation, network call)
    print("Time-consuming task completed.")

# Start a separate thread for the time-consuming task
thread = threading.Thread(target=time_consuming_task)
thread.start()

# The main thread can continue to execute other tasks without waiting for the time-consuming task to finish
print("Main thread continues to execute...")

# Wait for the time-consuming task thread to finish
thread.join()

print("Main thread: All tasks completed.")