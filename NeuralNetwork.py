import numpy as np
import random
from deap import base, creator, tools, algorithms
import tensorflow as tf
from tensorflow import keras

# Define the neural network structure
input_size = 2
hidden_size = 5
output_size = 1


# Define the neural network creation function
def create_neural_network(weights):
    # Calculate the number of weights for each layer
    num_input_weights = input_size * hidden_size
    num_output_weights = hidden_size * output_size

    # Extract weights for each layer
    input_layer_weights = weights[:num_input_weights].reshape((input_size, hidden_size))
    output_layer_weights = weights[num_input_weights:].reshape((hidden_size, output_size))

    # Create the neural network model
    model = keras.Sequential([
        keras.layers.InputLayer(input_size),
        keras.layers.Dense(hidden_size, activation='sigmoid', use_bias=False, weights=[input_layer_weights]),
        keras.layers.Dense(output_size, activation='sigmoid', use_bias=False, weights=[output_layer_weights])
    ])

    return model


# Define the evaluation function (fitness function)
def evaluate(ind):
    weights = np.array(ind).reshape((input_size * hidden_size + hidden_size * output_size,))
    model = create_neural_network(weights)

    # Generate some example data for XOR problem
    x_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_train = np.array([[0], [1], [1], [0]])

    # Compile and train the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=100, verbose=0)

    # Evaluate the model
    loss = model.evaluate(x_train, y_train, verbose=0)

    # Return the inverse of the loss as the fitness
    return 1 / (loss + 1e-10),


# Create the DEAP framework
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Create the toolbox
toolbox = base.Toolbox()
toolbox.register("individual", tools.initRepeat, creator.Individual, random.random,
                 n=input_size * hidden_size + hidden_size * output_size)
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
best_weights = np.array(best_individual).reshape((input_size * hidden_size + hidden_size * output_size,))
best_model = create_neural_network(best_weights)

# Test the best model
x_test = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
predictions = best_model.predict(x_test)
print("Predictions:")
print(predictions)
