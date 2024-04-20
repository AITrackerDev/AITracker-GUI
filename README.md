# AITracker-GUI
## What is this?
AITracker-GUI is an application built upon the AITracker neural network. It provides fine-tuned control in order to customize the application to your specific needs.

## What does it do
Whatever you want it to! This application is more focused on hardware integration, but can be built upon for more software oriented use cases as well.

## Requirements
This application is built in Python 3.11, and should be run using this version.

### MacOS
AITracker-GUI relies upon the library libusb installed via homebrew. If it isn't installed, use this command to install it so the application can find it in the proper location.

`brew install libusb`

## How to run
The following commands will create and activate a virtual environment, and then install of the required packages for the project to run.

`python3.11 -m venv env`

`source env/bin/activate`

`pip3 install -r requirements.txt`

Run this command at the project's directory to run the application:

`python3.11 AITracker-GUI.py`