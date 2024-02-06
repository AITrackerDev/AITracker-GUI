import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from keras import datasets, layers, models

# load dataset
(training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
training_images, testing_images = training_images / 255, testing_images / 255  # scales values so they are between 0-1

# The labels that the neural network can identify given an image
class_names = ['Plane', 'Car', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

# shows first 16 images in working dataset
for i in range(16):
    plt.subplot(4, 4, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(training_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[training_labels[i][0]])

plt.show()

# Only use first 20000 images in dataset to speed up training process
training_images = training_images[:20000]
training_labels = training_labels[:20000]
testing_images = testing_images[:4000]
testing_labels = testing_labels[:4000]

# COMMENT UP TO LINE 50 AFTER MODEL IS TRAINED
# # Model layers
# model = models.Sequential()
# model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3))) # 32,32 pixels, 3 colors
# model.add(layers.MaxPooling2D(2, 2))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D(2, 2))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(10, activation='softmax')) # number of classifications
#
# # Define loss function and metric
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))
#
# # Retrieve final loss and accuracy values for trained neural network
# loss, accuracy = model.evaluate(testing_images, testing_labels)
# print(f"Loss: {loss}  Accuracy: {accuracy}")
#
# # save model
# model.save('image_classifier.model')

# UNCOMMENT BELOW CODE AFTER MODEL IS TRAINED
# Loads saved model
model = models.load_model('image_classifier.model')

# Predicting images given images
img = cv.imread('horse.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

plt.imshow(img, cmap=plt.cm.binary)

prediction = model.predict(np.array([img]) / 255)
index = np.argmax(prediction)
print(f"Prediction: {class_names[index]}")
