from game import Game
import random
import ai

if __name__ == "__main__":
    ais = ai.ais
    victories = [0 for _ in range(len(ais))]
    games = [0 for _ in range(len(ais))]
    ranks = [[] for _ in range(len(ais))]


    for i in range(2):
        print(f"Game {i}")
        nb_players = random.randint(2, 4)
        playing_ais = random.sample(ais, nb_players)
        g = Game([i for i in range(1, nb_players + 1)])
        while g.players:
            if(g.can_play(g.is_playing)):
                playing_ais[g.is_playing_index](None, g)
            else:
                g.delete_player(g.is_playing)
                if g.is_playing_index >= len(g.players):
                    g.is_playing_index = 0
            if g.players:
                g.is_playing = g.players[g.is_playing_index]
        max_score = max([g.score(player) for player in range(1, g.maxn + 1)])
        for i in range(nb_players):
            if max_score == g.score(i + 1):
                victories[ais.index(playing_ais[i])] += 1
            games[ais.index(playing_ais[i])] += 1
            ranks[ais.index(playing_ais[i])].append(sorted([g.score(player) for player in range(1, g.maxn + 1)], reverse=True).index(g.score(i + 1)) + 1)
    for i in range(len(ais)):
        print(f"AI {i} has a winrate of {victories[i] / games[i] if games[i] else "Unknown"}")
        print(f"AI {i} had ranks {ranks[i]}")