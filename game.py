from pieces import *
from random import randint, choice
import time

class Game :
    def __init__(self, players:int):
        game_board = [[0 for _ in range(22)] for _ in  range(22)]
        poss = [[] for _ in  range(players)]
        for j in range(players):
            for p in range(len(pieces)):
                for r in [0,90,180,270] :
                    for b in [True,False]:
                        new_piece = rotate(p,r,b)
                        x_min = 0
                        x_max = len(new_piece[0])-1
                        y_min = 0
                        y_max = len(new_piece)-1
                        if new_piece[y_min][x_min] == 2 : 
                            poss[j].append((p,r,b,(0,0)))
                        if new_piece[y_max][x_min] == 2 : 
                           poss[j].append((p,r,b,(21-y_max,0)))
                        if new_piece[y_min][x_max] == 2 : 
                           poss[j].append((p,r,b,(0,21-x_max)))
                        if new_piece[y_max][x_max] == 2 : 
                           poss[j].append((p,r,b,(21-y_max,21-x_max)))
                        
        
        self.board = game_board
        self.bonus = [False for _ in range(players)]
        self.is_playing = 1
        self.is_playing_index = 0
        self.maxn = players
        self.possible_moves = poss
        self.red_piece = [4 for _ in range(players)]