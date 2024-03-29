import os
import customtkinter as ctk
import cv2
import time
from PIL import Image, ImageTk
from widgets.IndicatorSquare import IndicatorSquare
from AITrackerModel import AITrackerModel

CAR_DEMO = False

class LaunchScreen(ctk.CTkFrame):
    '''
    The screen that the user interacts with using their eyes.
    '''
    
    def __init__(self, root, screen_changer, settings):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer

        # network and model code
        self._model = AITrackerModel(0)

        # leave the screen when 'b' is pressed
        root.bind('b', lambda event: self.leave_screen(root))
        self.focus_set()
        
        # demo mode setting
        demo = settings['Demo Mode']

        # indicator squares
        self._up = IndicatorSquare(self, settings['Up'], demo)
        self._down = IndicatorSquare(self, settings['Down'], demo)
        self._left = IndicatorSquare(self, settings['Left'], demo)
        self._right = IndicatorSquare(self, settings['Right'], demo)
        self._up_left = IndicatorSquare(self, settings['Up Left'], demo)
        self._up_right = IndicatorSquare(self, settings['Up Right'], demo)
        self._down_left = IndicatorSquare(self, settings['Down Left'], demo)
        self._down_right = IndicatorSquare(self, settings['Down Right'], demo)
        self._blink = IndicatorSquare(self, settings['Blink'], demo)
        
        # settings variables
        self._input_duration = settings['Look Duration'] / 1000
        self._blink_duration = settings['Blink'][4] / 1000
        self._blink_sensitivity = settings['Blink'][5]

        # dictionary for the outputs being able to be sent out over hardware
        self._outputs = {
            'North':self._up,
            'South':self._down,
            'West':self._left,
            'East':self._right,
            'North West':self._up_left,
            'North East':self._up_right,
            'South West':self._down_left,
            'South East':self._down_right,
            'Blink':self._blink
        }

        #placing squares
        self._up_left.place(relx=0, rely=0, anchor=ctk.NW)
        self._up.place(relx=0.5, rely=0, anchor=ctk.N)
        self._up_right.place(relx=1, rely=0, anchor=ctk.NE)
        self._left.place(relx=0, rely=0.5, anchor=ctk.W)
        self._blink.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self._right.place(relx=1, rely=0.5, anchor=ctk.E)
        self._down_left.place(relx=0, rely=1, anchor=ctk.SW)
        self._down.place(relx=0.5, rely=1, anchor=ctk.S)
        self._down_right.place(relx=1, rely=1, anchor=ctk.SE)

        # look duration variables
        self._current_direction = 'Center'
        self._look_time = time.time()
        
        # blink detection variables
        self._blink_time = time.time()

        # camera related code and widgets
        self._cam = cv2.VideoCapture(0)
        self._canvas = ctk.CTkCanvas(self, width=self._model.image_size[0], height=self._model.image_size[1])
        self._canvas.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        self._warning_text = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=40))
        self._warning_text.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
        self._update_camera()
    
    def _update_camera(self):
        '''
        Updates the camera feed and performs the necessary prediction/blink detection. Also displays the cropped
        eye image the neural network sees.
        '''
        
        ret, frame = self._cam.read()
        if ret:
            # crop the image to our network's expectation
            cropped_image, correct = self._model.process_image(cv2.flip(frame, 1))

            # if the image is valid
            if correct:
                # put image on screen if it's properly resized
                self._photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)))
                self._canvas.create_image(0, 0, image=self._photo, anchor=ctk.NW)
                self._warning_text.configure(text="")

                # make prediction
                prediction = self._model.predict_direction(cropped_image)
                self._look_duration(prediction)
                self._blink_detection()
            else:
                # inform the user their eyes aren't being seen
                self._warning_text.configure(text="Eyes aren't visible!")
        self.after(1, self._update_camera)

    def _look_duration(self, prediction: str):
        '''
        Check if the user has been looking in a certain direction for a certain amount of time.
        
        Parameters:
        -----------
            prediction(str): The current prediction of the neural network.
        '''
        
        # if the directions are not the same, the user has looked somewhere else
        if self._current_direction != prediction:
            self._current_direction = prediction
            self._look_time = time.time()

        # the direction is consistent, meaning that the user is looking in only 1 direction
        else:
            # check if the start time + input duration is bigger then current time
            if self._look_time + self._input_duration <= time.time():
                # send the output since it passed both blocks
                if CAR_DEMO:
                    self._send_multiple_outputs_CAR(prediction)
                else:
                    if prediction != 'Center':
                        self._outputs[prediction].send_output()
                self._current_direction = 'Center'
                self._blink_time = time.time()
                
    def _send_multiple_outputs_CAR(self, prediction):
        if prediction != 'Center':
            if prediction == 'North West':
                self._outputs['North'].send_output()
                self._outputs['West'].send_output()
            elif prediction == 'North East':
                self._outputs['North'].send_output()
                self._outputs['East'].send_output()
            elif prediction == 'South West':
                self._outputs['South'].send_output()
                self._outputs['West'].send_output()
            elif prediction == 'South East':
                self._outputs['South'].send_output()
                self._outputs['East'].send_output()
            else:
                self._outputs[prediction].send_output()

    def _send_blink_CAR(self):
        self._outputs['North'].send_output()
        self._outputs['East'].send_output()
        self._outputs['South'].send_output()
        self._outputs['West'].send_output()

    def _blink_detection(self):
        '''
        Check if the user has blinked for a certain amount of time.
        '''
        
        # calculate distance between the top and bottom of each eye
        left_EAR, right_EAR = self._model.EAR
        
        # in case the eyes can't be seen, skip
        if left_EAR != -1 and right_EAR != -1:
            # if the eyes are open past a certain point, the user isn't trying to blink
            if round(left_EAR, 2) > self._blink_sensitivity and round(right_EAR, 2) > self._blink_sensitivity:
                self._blink_time = time.time()
            
            # the distance between the eyes is small enough to represent a blink
            else:
                # check if the start time + input duration is bigger then current time
                if self._blink_time + self._blink_duration <= time.time():
                    # send the output since it passed both blocks
                    if CAR_DEMO:
                        self._send_blink_CAR()
                    else:
                        self._outputs['Blink'].send_output()
                    self._blink_time = time.time()

    def leave_screen(self, root):
        '''
        Performs certain actions to 'clean up' the screen and leave without issues.
        '''
        self._cam.release()
        root.unbind('b')
        self._screen_changer('MainScreen')