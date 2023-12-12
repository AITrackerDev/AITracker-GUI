import h5py
import numpy as np
import random
from deap import base, creator, tools, algorithms
import tensorflow as tf
from tensorflow import keras

import numpy as np
import random
from deap import base, creator, tools, algorithms
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.callbacks import ModelCheckpoint

# Define the neural network structure for image input
global input_shape
global hidden_size
global output_size
global x_train
global y_train

# Load data from HDF5 file
with h5py.File('image_collection2023-12-07_00-59-52.h5', 'r') as hdf_file:
    # Assuming your dataset is stored under the 'images' and 'labels' keys
    x_train = np.array(hdf_file['images'])
    y_train = np.array(hdf_file['labels'])

input_shape = input_shape = x_train.shape[1:]  # Adjust this based on image size and channels
hidden_size = 128
output_size = 8

def create_neural_network(weights):
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=input_shape),
        keras.layers.Flatten(),  # Flatten the 3D tensor to a 1D tensor
        keras.layers.Dense(hidden_size, activation='relu', use_bias=False),
        keras.layers.Dense(output_size, activation='softmax', use_bias=False)
    ])

    # Set the weights of the layers
    model.set_weights(weights)
    return model


def create_convolutional_neural_network(weights):
    model = keras.Sequential([
        keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(output_size, activation='softmax')
    ])

    # Extract shapes of weights for each layer
    conv1_shape = (3, 3, input_shape[-1], 32)  # 3x3 kernel, 'input_shape[-1]' input channels, 32 filters
    dense1_shape = (6272, 128)  # Flattened shape from previous layer to 128 neurons
    dense2_shape = (128, output_size)  # 128 neurons to 'output_size'

    # Split the weights for each layer
    conv1_weights = weights[:np.prod(conv1_shape)]
    dense1_weights = weights[np.prod(conv1_shape): np.prod(conv1_shape) + np.prod(dense1_shape)]
    dense2_weights = weights[np.prod(conv1_shape) + np.prod(dense1_shape):]

    # # Reshape weights for each layer
    # conv1_weights = conv1_weights.reshape(conv1_shape)
    # print(dense1_shape[1])
    # dense1_weights = dense1_weights.reshape(dense1_shape)
    # dense2_weights = dense2_weights.reshape(dense2_shape)

    # Set the weights of each layer
    model.layers[0].set_weights([conv1_weights, np.zeros(32)])
    model.layers[3].set_weights([dense1_weights, np.zeros(128)])
    model.layers[4].set_weights([dense2_weights, np.zeros(output_size)])

    return model

# Define the evaluation function (fitness function)
# def evaluate(ind):
#     weights = np.array(ind).reshape((input_size * hidden_size + hidden_size * output_size,))
#     model = create_neural_network(weights)
#
#     # Generate some example data for XOR problem
#     x_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
#     y_train = np.array([[0], [1], [1], [0]])
#
#     # Compile and train the model
#     model.compile(optimizer='adam', loss='mean_squared_error')
#     model.fit(x_train, y_train, epochs=100, verbose=0)
#
#     # Evaluate the model
#     loss = model.evaluate(x_train, y_train, verbose=0)
#
#     # Return the inverse of the loss as the fitness
#     return 1 / (loss + 1e-10),

def evaluate(ind):
    weights = np.array(ind).reshape((-1,))
    model = create_convolutional_neural_network(weights)

    # Assuming x_train and y_train are training data and labels
    loss, accuracy = model.evaluate(x_train, y_train, verbose=0) # PLACEHOLDER for training data

    #Compile and train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=100, verbose=0) # PLACEHOLDER for training data

    # Print the loss and accuracy during each evaluation
    print(f"Loss: {loss}, Accuracy: {accuracy}")

    # Return the accuracy as the fitness
    return accuracy


# def calculate_total_parameters(input_shape, output_size):
#     model = create_convolutional_neural_network(np.zeros(total_params))
#     return sum(p.numel() for p in model.trainable_variables)
#
#
# total_params = calculate_total_parameters(input_shape, output_size)

# # Create the DEAP framework
# creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMax)
#
# # Create the toolbox
# toolbox = base.Toolbox()
# toolbox.register("individual", tools.initRepeat, creator.Individual, random.random,
#                  n=input_size * hidden_size + hidden_size * output_size)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#
# toolbox.register("evaluate", evaluate)
# toolbox.register("mate", tools.cxTwoPoint)
# toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
# toolbox.register("select", tools.selTournament, tournsize=3)

# Create the DEAP framework
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Create the toolbox
toolbox = base.Toolbox()
toolbox.register("individual", tools.initRepeat, creator.Individual, random.random, n=864)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Set the random seed for reproducibility
random.seed(42)

# Create the initial population
population_size = 10
num_generations = 10
population = toolbox.population(n=population_size)

# Define the ModelCheckpoint callback to save the best model based on validation accuracy
checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)

# Run the genetic algorithm
algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=2 * population_size,
                          cxpb=0.7, mutpb=0.2, ngen=num_generations, stats=None, halloffame=None, verbose=True)

# Get the best individual from the final population
best_individual = tools.selBest(population, k=1)[0]

# After training, load the best model from the saved checkpoint
best_model = keras.models.load_model('best_model.h5')

# best_weights = np.array(best_individual).reshape((input_size * hidden_size + hidden_size * output_size,))
#best_weights = np.concatenate([layer.get_weights()[0].flatten() for layer in best_individual.layers])
#best_model = create_neural_network(best_weights)

# # Test the best model
# x_test = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# predictions = best_model.predict(x_test)
# print("Predictions:")
# print(predictions)
