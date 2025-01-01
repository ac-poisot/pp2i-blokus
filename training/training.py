import os
import sys
import inspect
from matplotlib import pyplot as plt
import json
import numpy as np
from generate_data import generate_data

import tensorflow as tf
from tensorflow.keras import layers, models

print(tf.sysconfig.get_build_info())

print("GPUs available:", len(tf.config.list_physical_devices('GPU')), "\n\n\n\n")

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from random import randint

BOARD_SIZE = 20

def create_model():
    """
    Creates and compiles a Convolutional Neural Network (CNN) model using Keras.
    The model architecture consists of:
    - Three convolutional layers with ReLU activation and max pooling.
    - A flattening layer to convert the 2D matrix to a 1D vector.
    - Two dense (fully connected) layers with ReLU activation.
    - A dropout layer to prevent overfitting.
    - An output dense layer with sigmoid activation for binary classification.
    The model is compiled with the Adam optimizer, mean squared error loss, and mean absolute error as a metric.
    Returns:
        keras.models.Sequential: The compiled CNN model.
    """

    model = models.Sequential()

    model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(BOARD_SIZE, BOARD_SIZE, 5)))

    model.add(layers.MaxPooling2D((2, 2), padding='same'))
    
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))

    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))


    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dropout(0.5))
    
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    print("Model created")

    return model

def load_data(dirname: str):
    """
    Loads data from JSON files and parses them as numpy arrays.
    Args:
        dirname (str): The directory name containing the JSON files.
    Returns:
        tuple: A tuple containing two numpy arrays:
            - games (np.ndarray): The game states loaded from games.json.
            - scores (list[int]): The scores loaded from scores.json.
    """
    games_path = os.path.join("training", "datasets", dirname, "games.json")
    scores_path = os.path.join("training", "datasets", dirname, "scores.json")

    with open(games_path, 'r') as gamefile:
        games = json.load(gamefile)
        games = np.array(games)

    with open(scores_path, 'r') as scorefile:
        scores = json.load(scorefile)

    print(f"Data from {dirname} loaded")

    return games, scores

def load_all_data():
    """
    Loads all data from the "datasets" directory and concatenates them into single numpy arrays.
    Returns:
        tuple: A tuple containing two numpy arrays:
            - all_games (np.ndarray): The concatenated game states.
            - all_scores (list[int]): The concatenated scores.
    """
    all_games = []
    all_scores = []

    for dirname in os.listdir("training/datasets"):
        games, scores = load_data(dirname)
        all_games.append(games)
        all_scores += scores

    all_games = np.concatenate(all_games, axis=0)
    print(len(all_games))

    return all_games, all_scores

def train(model, data):
    """
    Trains the given model using the provided data and saves the training history and validation results.
    Args:
        model: The machine learning model to be trained.
        data: A tuple containing the training data and labels.
    Returns:
        None
    The function performs the following steps:
    1. Generates validation data.
    2. Trains the model for 4 iterations, saving the model and validation results after each iteration.
    3. Plots and saves the training loss for each iteration.
    4. Prints the validation results and the final prediction errors.
    """

    validation = generate_data(10)

    print("Data generated")

    history = []
    validations = []

    for i in range(4):
        history.append(model.fit(np.array(data[0]), np.array(data[1]), epochs=100, batch_size=200))
        predictions = model.predict(np.array(validation[0][:40]))
        validations.append(sum(([(validation[1][j]-predictions[j][0])**2  for j in range(len(predictions))])))

        model.save(f"models/model2_{i}.h5")

    print("Model trained")

    for i in range(4):
        plt.plot(np.concat([history[j].history['loss'] for j in range(i+1)]), label='train')
        plt.savefig(f"training/training_data/loss{i}.png")
        
        print(f"Validation {i}: {validations[i]}")

    predictions = model.predict(np.array(data[0][:40]))
    print(list([float(data[1][i]-predictions[i][0])**2 for i in range(len(predictions))]))

model = create_model()
# model = models.load_model("models/model2.h5")
train(model, load_all_data())
