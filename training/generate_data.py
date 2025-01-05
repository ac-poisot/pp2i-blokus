import os
import sys
import inspect
import json

import numpy as np

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import ai
from game import Game
from random import randint


# The ais that will be randomly picked to play to generate the data
ais = [ai.ai_easy, ai.ai_easy, ai.ai2, ai.ai2, ai.cnn_ai0, ai.cnn_ai1, ai.cnn_ai2, ai.cnn_ai3]

# Function to convert the current game board to a matrix of integers
# Function to convert the current game board to a matrix of integers
def realboard(board):
    """
    Extracts the inner part of a 2D board, excluding the outermost rows and columns.
    Args:
        board (list of list of any): A 2D list representing the board.
    Returns:
        list of list of any: A 2D list representing the inner part of the board.
    """
    
    return [board[i][1:-1] for i in range(1, len(board)-1)]

def maxScore(l):
    """
    Returns the maximum score in the input list.
    Args:
        l (list of int): A list of scores.
    Returns:
        int: The maximum score in the input list.
    """
    return sorted(l, reverse=True)[0]

BOARD_SIZE = 20

class NumpyEncoder(json.JSONEncoder):
    """
    A JSON encoder that can handle numpy arrays.
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def generate_data(n: int):
    """
    Generates game data and scores for a specified number of games.
    This function simulates 3n games with a varying number of players (from 2 to 4).
    Each game is played until no players can play anymore. The game state and scores
    are recorded and saved into JSON files.
    Args:
        n (int): The number of games of each number of players to generate.
    Returns:
        Nothing
    The function saves the generated game data and scores into JSON files
    in a newly created directory under "training/datasets".
    """
    
    games=[]
    scores=[]
    for _ in range(n):
        for nbplayers in range(2, 5): # 2->4 (inclus)

            # Simulate a game with the specified number of players
            g = Game(nbplayers+1)
            while g.players:
                if(g.can_play(g.is_playing)):
                    ais[randint(0, len(ais)-1)](None, g)
                else:
                    g.delete_player(g.is_playing)
                    if g.is_playing_index >= len(g.players):
                        g.is_playing_index = 0
                if g.players:
                    g.is_playing = g.players[g.is_playing_index]
            
            # Mostly formating it to be used in the neural network
            board = np.matrix(realboard(g.board))
            board = np.expand_dims(board, axis=-1)
            scoreboard=[g.score(player) for player in range(1, g.maxn + 1)]
            max = maxScore(scoreboard)
            
            for i in range(nbplayers):
                player_info = np.zeros((4,))
                player_info[i] = 1
                expanded_player_info = np.expand_dims(player_info, axis=(0, 1))
                expanded_player_info = np.tile(expanded_player_info, (BOARD_SIZE, BOARD_SIZE, 1))
                games.append(np.concatenate([board, expanded_player_info], axis=-1))
                scores.append(1 if max == scoreboard[i] else 0)


    # Save the generated data and scores into JSON files
    os.chdir("training/datasets2")
    i = 0
    while os.path.exists(f"dataset{i}"):
        i += 1
    os.makedirs(f"dataset{i}")
    os.chdir(f"dataset{i}")
    with open("games.json", 'w') as f:
        json.dump(games, f, cls=NumpyEncoder)
    with open("scores.json", 'w') as f:
        json.dump(scores, f)
    os.chdir("../../../")
    print(f"Dataset {i} généré")

    return games, scores


if __name__ == "__main__":
    for i in range(200): # The number of datasets to generate
        generate_data(100) # The number of games of each number of players to simulate for each dataset