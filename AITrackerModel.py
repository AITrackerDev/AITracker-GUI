'''
Load and make predictions on the AITracker neural network model.
'''
import h5py
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import cv2 as cv

class AITrackerModel():
    def __init__(self, network_path: str, data_path: str):
        # load labels for proper predictions
        with h5py.File(data_path, 'r') as h5_file:
            labels_str = h5_file['labels'][:]
            
        # load the model into the program
        self._model = tf.keras.models.load_model(network_path)
        
        # load necessary labels into program
        _label_encoder = LabelEncoder()
        labels_encoded = _label_encoder.fit_transform(labels_str)
        labels_one_hot = np.eye(len(np.unique(labels_encoded)))[labels_encoded]
        self._class_names = _label_encoder.classes_
    
    # make a prediction on a direction through the network
    def predict_direction(self, image):
        img = cv.resize(image, (190, 80))
        prediction = self._model.predict(np.array([img]))
        predicted_class_index = np.argmax(prediction)
        predicted_class = self._class_names[predicted_class_index]
        
        # return string representation of prediction
        return predicted_class.decode('utf-8').strip()
