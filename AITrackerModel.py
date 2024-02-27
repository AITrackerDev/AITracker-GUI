'''
Load and make predictions on the AITracker neural network model, as well as process images to fit the network's needs.
'''
import h5py
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import cv2
import dlib
import os
import math # math.dist to calculate distance between 2 points

class AITrackerModel():
    def __init__(self):
        # load labels for proper predictions
        with h5py.File(os.path.join('H5Demo', 'final_eye_data.h5'), 'r') as h5_file:
            labels_str = h5_file['labels'][:]
            
        # imaging process constants
        self._eyes_detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(os.path.join('assets', 'shape_predictor_68_face_landmarks.dat'))
        self._image_size = (190, 80)
            
        # load the model into the program
        self._model = tf.keras.models.load_model(os.path.join('image_classifier.model'))
        
        # load necessary labels into program
        _label_encoder = LabelEncoder()
        labels_encoded = _label_encoder.fit_transform(labels_str)
        labels_one_hot = np.eye(len(np.unique(labels_encoded)))[labels_encoded]
        self._class_names = _label_encoder.classes_
    
    @property
    def image_size(self):
        return self._image_size
    
    # make a prediction on a direction through the network
    def predict_direction(self, image):
        prediction = self._model.predict(np.array([image]), verbose=0)
        predicted_class = self._class_names[np.argmax(prediction)]
        
        # return string representation of prediction
        return predicted_class.decode('utf-8').strip()

    # takes the image, crops the eyes, puts it into the template, resizes to our network's image input size      
    def process_image(self, image):
        # grayscale image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # if a face is detected
        faces = self._eyes_detector(gray)
        if len(faces) > 0:
            landmarks = self._predictor(gray, faces[0])
            pad = 5
            
            left_eye = (
                #left width, top height
                landmarks.part(36).x - pad, landmarks.part(37).y - pad,
                #right width, bottom height
                landmarks.part(39).x + pad, landmarks.part(41).y + pad
            )
            
            right_eye = (
                #left width, top height
                landmarks.part(42).x - pad, landmarks.part(43).y - pad,
                #right width, bottom height
                landmarks.part(45).x + pad, landmarks.part(47).y + pad
            )
            
            # get separate images for each eye
            # [start_y:end_y, start_x:end_x]
            left_eye_region = gray[left_eye[1]:left_eye[3], left_eye[0]:left_eye[2]]
            right_eye_region = gray[right_eye[1]:right_eye[3], right_eye[0]:right_eye[2]]
            
            # put eyes into template similar to our training data
            template = self._eye_template(left_eye_region, right_eye_region)
            
            # return resized image and true indicating it can be used for input in our network
            return (cv2.resize(template, self._image_size), True)
        
        # if no faces are found return original image and false
        return (image, False)

    # makes the template with the regions specified by cropping the eyes
    def _eye_template(self, left_eye, right_eye):
        # composite image height and width
        height = max(left_eye.shape[0], right_eye.shape[0])
        width = left_eye.shape[1] + right_eye.shape[1]

        # create a blank image to put data into
        composite_image = np.zeros((height, width), dtype=np.uint8)

        # put left and right eyes in the image side by side
        composite_image[:left_eye.shape[0], :left_eye.shape[1]] = left_eye
        composite_image[:right_eye.shape[0], left_eye.shape[1]:] = right_eye

        # return the composite image
        return composite_image
    
    # calculate the distance between the top and bottom of each eye and return it as a tuple
    def eye_distance(self, image):
        # grayscale image for better detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # if a face is detected
        faces = self._eyes_detector(gray)
        if len(faces) > 0:
            landmarks = self._predictor(gray, faces[0])
            pad = 5
            
            left_eye = (
                #left width, top height
                landmarks.part(36).x - pad, landmarks.part(37).y - pad,
                #right width, bottom height
                landmarks.part(39).x + pad, landmarks.part(41).y + pad
            )
            
            right_eye = (
                #left width, top height
                landmarks.part(42).x - pad, landmarks.part(43).y - pad,
                #right width, bottom height
                landmarks.part(45).x + pad, landmarks.part(47).y + pad
            )
        print("eye distance calculation goes here")