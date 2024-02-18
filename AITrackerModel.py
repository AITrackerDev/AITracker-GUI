'''
Load and make predictions on the AITracker neural network model.
'''
import h5py
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

class AITrackerModel():
    def __init__(self, network_path: str, data_path: str):
        # load labels for proper predictions
        with h5py.File(data_path, 'r') as h5_file:
            labels_str = h5_file['labels'][:]
            
        # load the model into the program
        self._model = tf.keras.models.load_model(network_path)
        
        # load necessary labels into program
        _label_encoder = LabelEncoder()
        self._class_names = _label_encoder.fit_transform(labels_str)
    
    # make a prediction on a direction through the network
    def predict_direction(self, image):
        prediction = self._model.predict(np.array([image]))
        predicted_class_index = np.argmax(prediction)
        predicted_class = self._class_names[predicted_class_index]
        
        return predicted_class