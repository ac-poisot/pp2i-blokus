from random import randint
from db import new_move

def ai_easy(gameid, game):
    pos = game.possible_moves(game.is_playing)
    piece, rotation, (x, y), flipped = pos[randint(0, len(pos) - 1)]
    game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
    new_move(gameid, game.players[game.is_playing_index], piece, x, y, rotation, flipped)

    game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
    if game.players: game.is_playing = game.players[game.is_playing_index]

def heuristic1(game, player):
    ownscore = len(game.red_pieces[player])
    opposcore = -1
    for i in range(len(game.players)):
        if i != player:
            opposcore = max(opposcore, len(game.red_pieces[i]))
    return ownscore - opposcore

def rec_minmax(game, depth, player, heuristic):
    if depth == 0:
        return heuristic(game, player)
    else:
        best = -1
        for p in game.possible_moves(game.is_playing):
            g = game.copy_game()
            piece, rotation, (x, y), flipped = p
            g.add_piece(piece, rotation, (x, y), flipped, g.is_playing)
            g.is_playing_index = (g.is_playing_index + 1) % (len(g.players))
            best = max(best, rec_minmax(g, depth-1, player, heuristic))
        return best


def min_max(gameid, game, depth, heuristic):
    best = -999999999999
    bestp = None
    for p in game.possible_moves(game.is_playing):
        g = game.copy_game()
        piece, rotation, (x, y), flipped = p
        g.add_piece(piece, rotation, (x, y), flipped, g.is_playing)
        g.is_playing_index = (g.is_playing_index + 1) % (len(g.players))
        score = rec_minmax(g, depth-1, game.is_playing_index, heuristic)
        if best < score:
            best = score
            bestp = p
    piece, rotation, (x, y), flipped = bestp
    game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
    new_move(gameid, game.players[game.is_playing_index], piece, x, y, rotation, flipped)

    game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
    if game.players: game.is_playing = game.players[game.is_playing_index]

def ai2(gameid, game):
    min_max(gameid, game, 1, heuristic1)

def ai3(gameid, game):
    min_max(gameid, game, 2, heuristic1)

ais = [ai_easy, ai2, ai3]