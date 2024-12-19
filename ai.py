from random import randint

def ai_easy(game):
    pos = game.possible_moves(game.is_playing)
    piece, rotation, (x, y), flipped = pos[randint(0, len(pos) - 1)]
    game.add_piece(piece, rotation, (x, y), flipped, game.is_playing)

    game.is_playing_index = (game.is_playing_index + 1) % (len(game.players))
    if game.players: game.is_playing = game.players[game.is_playing_index]
    while (not game.can_play(game.is_playing)) and len(game.players) != 0:
        game.delete_player(game.is_playing)
        if game.is_playing_index >= len(game.players):
            game.is_playing_index = 0
        if len(game.players) != 0:
            game.is_playing = game.players[game.is_playing_index]


ais = [ai_easy, ai_easy]