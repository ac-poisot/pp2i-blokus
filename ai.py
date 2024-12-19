from random import randint
from db import new_move

def ai_easy(gameid, game):
    pos = game.possible_moves(game.is_playing)
    piece, rotation, (x, y), flipped = pos[randint(0, len(pos) - 1)]
    game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)
    new_move(gameid, game.players[game.is_playing_index], piece, x, y, rotation, flipped)

    game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
    if game.players: game.is_playing = game.players[game.is_playing_index]


ais = [ai_easy, ai_easy]