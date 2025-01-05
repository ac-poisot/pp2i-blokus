from random import randint
from db import new_move

from tensorflow.keras import models
import numpy as np

def ai_easy(gameid, game):
    pos = game.possible_moves[game.is_playing-1]
    piece, rotation, flipped, (x, y) = pos[randint(0, len(pos) - 1)]
    game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
    if(gameid): new_move(gameid, game.players[game.is_playing_index], piece, x, y, rotation, flipped)

def heuristic1(game, player):
    ownscore = game.red_pieces[player]
    opposcore = -1
    for i in range(len(game.players)):
        if i != player:
            opposcore = max(opposcore, game.red_pieces[i])
    return ownscore - opposcore

def rec_minmax(game, depth, player, heuristic):
    if depth == 0:
        return heuristic(game, player)
    elif game.can_play(game.is_playing):
        best = -1
        posList = game.possible_moves[game.is_playing-1].copy()
        initial_red_pieces = game.red_pieces.copy()
        for p in posList:
            piece, rotation, flipped, (x, y) = p
            game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
            currindex = game.is_playing_index
            game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
            if game.players: game.is_playing = game.players[game.is_playing_index]
            while (not game.can_play(game.is_playing)):
                print(game.is_playing)
                # game.delete_player(game.is_playing)
                game.is_playing_index = (game.is_playing_index + 1) % (len(game.players)) # tmp ?
                if game.is_playing_index >= len(game.players):
                    game.is_playing_index = 0
                if game.players: game.is_playing = game.players[game.is_playing_index]

            best = max(best, rec_minmax(game, depth-1, player, heuristic))
            game.is_playing_index = currindex
            game.remove_piece(piece, rotation, (x, y), flipped)
            game.possible_moves[game.is_playing-1] = posList
            game.red_pieces = initial_red_pieces.copy()
        return best
    else:
        return heuristic(game, player)


def min_max(gameid, game, depth, heuristic):
    best = -999999999999
    bestp = None
    g = game.copy_game()
    posList = g.possible_moves[g.is_playing-1].copy()
    initial_red_pieces = g.red_pieces.copy()
    # print(len(posList), g.is_playing, g.is_playing_index)
    for p in posList:
        piece, rotation, flipped, (x, y) = p
        g.add_piece(piece, rotation, (x, y), flipped, g.is_playing)
        
        g.is_playing_index = (g.is_playing_index + 1) % (len(g.players))
        score = rec_minmax(g, depth-1, g.is_playing_index, heuristic)
        g.is_playing_index = (g.is_playing_index + len(g.players) - 1) % (len(g.players))
        g.remove_piece(piece, rotation, (x, y), flipped)
        g.possible_moves[g.is_playing-1] = posList
        g.red_pieces = initial_red_pieces.copy()
        if best < score:
            best = score
            bestp = p
    piece, rotation, flipped, (x, y) = bestp
    game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
    if(gameid): new_move(gameid, game.players[game.is_playing_index], piece, x, y, rotation, flipped)

def ai2(gameid, game):
    min_max(gameid, game, 1, heuristic1)

def ai3(gameid, game):
    min_max(gameid, game, 2, heuristic1)



# Function to convert the current game board to a matrix of integers
def realboard(board):
    """
    Extracts the inner part of a 2D board, excluding the outermost rows and columns.

    board (list of list of any): a 2D list representing the board

    Returns a 2D list representing the inner part of the board
    """
    
    return [board[i][1:-1] for i in range(1, len(board)-1)]


def cnn_ai(modelname):
    model = models.load_model(f"models/{modelname}")

    def cnn_ai_inner(gameid, game):
        # min_max(gameid, game, 1, heuristic)
        g = game.copy_game()
        posList = g.possible_moves[g.is_playing-1].copy()
        possible_datas = []
        c = 0
        for p in posList:
            piece, rotation, flipped, (x, y) = p
            # if(g.is_legal(piece, rotation, (x, y), flipped, g.is_playing)): # TO BE REMOVED WHEN POSSIBLE_MOVES WILL WORK
            c += 1
            g.add_piece(piece, rotation, (x, y), flipped, g.is_playing)
            g.is_playing_index = (g.is_playing_index + 1) % (len(g.players))

            board = np.matrix(realboard(game.board))
            board = np.expand_dims(board, axis=-1)
            player_info = np.zeros((4,))
            player_info[g.is_playing_index] = 1
            expanded_player_info = np.expand_dims(player_info, axis=(0, 1))
            expanded_player_info = np.tile(expanded_player_info, (20, 20, 1))
            input_data = np.concatenate((board, expanded_player_info), axis=-1)
            possible_datas.append(input_data)

            g.is_playing_index = (g.is_playing_index + len(g.players) - 1) % (len(g.players))
            g.remove_piece(piece, rotation, (x, y), flipped)

        possible_datas = np.array(possible_datas)
        possible_datas = possible_datas.reshape((-1, 20, 20, 5))
        scores = model.predict(possible_datas)
        piece, rotation, flipped, (x, y) = posList[np.argmax(scores)]
        game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
        if(gameid): new_move(gameid, game.players[game.is_playing_index], piece, x, y, rotation, flipped)

    return cnn_ai_inner

# cnn_ai0 = cnn_ai("model2_0.h5")
# cnn_ai1 = cnn_ai("model2_1.h5")
# cnn_ai2 = cnn_ai("model2_2.h5")
cnn_ai3 = cnn_ai("model2_3.h5")

# modelList = ["model3_0.h5", "model3_3.h5", "model3_6.h5", "model3_7.h5", "model3_8.h5"]

# ais = [ai_easy] + [cnn_ai(model) for model in modelList]
ais = [ai_easy, ai2, ai3, cnn_ai3]
aiNames = ["easyAI", "mediumAI", "hardAI", "CNN"]