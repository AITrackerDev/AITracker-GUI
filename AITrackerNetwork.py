import h5py
import os
import numpy as np
# from wandb import magic
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras import models, layers, callbacks

EPOCHS = 30
MODEL_FILE = 'image_classifier5.keras'
PATIENCE = int(EPOCHS * .2)

# Load data from H5 file
with h5py.File(os.path.join('H5Demo', 'numpy_eye_data.h5'), 'r') as h5_file:
    images = h5_file['images'][:]
    labels_str = h5_file['labels'][:]

# Convert string labels to one-hot encoded vectors
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels_str)
labels_one_hot = np.eye(len(np.unique(labels_encoded)))[labels_encoded]

# Split the data into training and testing sets
training_images, testing_images, training_labels, testing_labels = train_test_split(
    images, labels_one_hot, test_size=0.2, random_state=42)
training_images, testing_images = training_images / 255, testing_images / 255  # Scales values to be between 0-1

# The labels that the neural network can identify given an image
class_names = label_encoder.classes_

# Model layers
model = models.Sequential()

# Convolutional layers
model.add(layers.Reshape((80, 190, 1), input_shape=(80, 190)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

# Flatten layer
model.add(layers.Flatten())

# Dense layers
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(len(class_names), activation='softmax'))  # Number of classifications

# Define loss function and metric
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# call backs to stop training when val_loss is low enough and val_accuracy is high
es = callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=PATIENCE)
mc = callbacks.ModelCheckpoint(MODEL_FILE, monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)

# Training the model
model.fit(training_images, training_labels, epochs=EPOCHS, validation_data=(testing_images, testing_labels), callbacks=[es, mc])

# Retrieve final loss and accuracy values for the trained neural network
loss, accuracy = model.evaluate(testing_images, testing_labels)
print(f"Loss: {loss}  Accuracy: {accuracy}")

# Save the trained model
model.save('image_classifier5.model')

# NEW MODEL
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout
#
# model = Sequential()
#
# # Input layer
# model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(80, 190, 3)))
# model.add(BatchNormalization())
# model.add(MaxPooling2D(2, 2))
#
# # Second convolutional layer
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(BatchNormalization())
# model.add(MaxPooling2D(2, 2))
#
# # Third convolutional layer
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(BatchNormalization())
# model.add(MaxPooling2D(2, 2))
#
# # Flatten layer
# model.add(Flatten())
#
# # Dense layers
# model.add(Dense(128, activation='relu'))
# model.add(Dropout(0.5))  # Add dropout for regularization
# model.add(Dense(len(class_names), activation='softmax'))
#
# # Compile the model
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
# # Display the summary of the model
# model.summary()
#
# # Training the model
# model.fit(training_images, training_labels, epochs=20, validation_data=(testing_images, testing_labels))
#
# # Evaluate and save the model
# loss, accuracy = model.evaluate(testing_images, testing_labels)
# print(f"Loss: {loss}  Accuracy: {accuracy}")
#
# # Save the model
# model.save('image_classifier2.model')


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
