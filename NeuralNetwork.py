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

# Define the neural network structure for image input
global input_shape
global hidden_size
global output_size

input_shape = (64, 64, 1)  # Adjust this based on image size and channels
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
    # Adjust the input shape based on your image dimensions and channels

    model = keras.Sequential([
        keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
        keras.layers.MaxPooling2D(pool_size=(2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(units=128, activation='relu'),
        keras.layers.Dense(units=output_size, activation='softmax')
    ])

    # Set the weights of the layers
    model.set_weights(weights)
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

    # Assuming x_train and y_train are your training data and labels
    loss, accuracy = model.evaluate(x_train, y_train, verbose=0) # PLACEHOLDER for training data

    #Compile and train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=100, verbose=0) # PLACEHOLDER for training data

    # Print the loss and accuracy during each evaluation
    print(f"Loss: {loss}, Accuracy: {accuracy}")

    # Return the accuracy as the fitness
    return accuracy


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
toolbox.register("individual", tools.initRepeat, creator.Individual, random.random, n=total_params)
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

# Run the genetic algorithm
algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=2 * population_size,
                          cxpb=0.7, mutpb=0.2, ngen=num_generations, stats=None, halloffame=None, verbose=True)

# Get the best individual from the final population
best_individual = tools.selBest(population, k=1)[0]
# best_weights = np.array(best_individual).reshape((input_size * hidden_size + hidden_size * output_size,))
best_weights = np.concatenate([layer.get_weights()[0].flatten() for layer in best_individual.layers])
best_model = create_neural_network(best_weights)

# # Test the best model
# x_test = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# predictions = best_model.predict(x_test)
# print("Predictions:")
# print(predictions)
