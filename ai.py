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
    elif game.can_play(game.is_playing):
        best = -1
        posList = game.possible_moves(game.is_playing).copy()
        for p in posList:
            piece, rotation, (x, y), flipped = p
            game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
            game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
            while (not game.can_play(game.is_playing)):
                game.delete_player(game.is_playing)
                if game.is_playing_index >= len(game.players):
                    game.is_playing_index = 0

            best = max(best, rec_minmax(game, depth-1, player, heuristic))
            game.remove_piece(piece, rotation, (x, y), flipped, game.is_playing)
        return best
    else:
        return heuristic(game, player)


def min_max(gameid, game, depth, heuristic):
    best = -999999999999
    bestp = None
    g = game.copy_game()
    posList = g.possible_moves(g.is_playing).copy()
    for p in posList:
        piece, rotation, (x, y), flipped = p
        g.add_piece(piece, rotation, (x, y), flipped, g.is_playing)
        g.is_playing_index = (g.is_playing_index + 1) % (len(g.players))
        score = rec_minmax(g, depth-1, g.is_playing_index, heuristic)
        g.is_playing_index = (g.is_playing_index + len(g.players) - 1) % (len(g.players))
        g.remove_piece(piece, rotation, (x, y), flipped, g.is_playing)
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

ais = [ai_easy, ai3, ai3]