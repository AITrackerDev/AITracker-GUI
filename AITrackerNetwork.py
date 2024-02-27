import cv2 as cv
import h5py
import numpy as np
import matplotlib.pyplot as plt
from keras import datasets, layers, models
from sklearn.model_selection import train_test_split

import h5py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import models, layers

# Load data from H5 file
with h5py.File('H5Demo/final_eye_data.h5', 'r') as h5_file:
    images = h5_file['images'][:]
    labels_str = h5_file['labels'][:]

# Convert string labels to one-hot encoded vectors
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels_str)
labels_one_hot = np.eye(len(np.unique(labels_encoded)))[labels_encoded]

# Split the data into training and testing sets
training_images, testing_images, training_labels, testing_labels = train_test_split(images, labels_one_hot, test_size=0.2, random_state=42)
training_images, testing_images = training_images / 255, testing_images / 255  # scales values so they are between 0-1

# The labels that the neural network can identify given an image
class_names = label_encoder.classes_

# COMMENT UP TO LINE 52 AFTER MODEL IS TRAINED
# Model layers
model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(80,190, 3))) # 80,190 pixels, 3 colors
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(len(class_names), activation='softmax')) # number of classifications

# Define loss function and metric
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels)) # number of epochs

# Retrieve final loss and accuracy values for trained neural network
loss, accuracy = model.evaluate(testing_images, testing_labels)
print(f"Loss: {loss}  Accuracy: {accuracy}")

# save model
model.save('image_classifier.model')

# UNCOMMENT BELOW CODE AFTER MODEL IS TRAINED
# # Loads saved model
# model = models.load_model('image_classifier.model')
#
# # Load and preprocess the image
# img = cv.imread('NetworkDemo/North_image_2.jpg')
# #img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
# img = cv.resize(img, (190, 80))  # Resize the image to match the input size used during training
# img = img / 255.0  # Normalize the pixel values to be between 0 and 1
#
# # Display the image
# plt.imshow(img, cmap=plt.cm.binary)
# plt.show()
#
# # Make predictions
# prediction = model.predict(np.array([img]))
# predicted_class_index = np.argmax(prediction)
# predicted_class = class_names[predicted_class_index]
#
# print(f"Prediction: {predicted_class}")