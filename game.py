from pieces import *
from random import randint, choice
import time

class Game :
    def __init__(self, players:int):
        """initialise le jeu"""
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
                        
        self.availible = [ [i for i in range(1,22)] for j in range(players)]
        self.board = game_board
        self.bonus = [False for _ in range(players)]
        self.is_playing = 1
        self.is_playing_index = 0
        self.maxn = players
        self.possible_moves = poss
        self.red_pieces = [4 for _ in range(players)]
    
    def print_board(self):
        """ display the board, debug function"""
        for i in range(22):
            print(self.board[i])
    
    def is_legal(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int,int], flipped:bool) -> bool :
        """ 
        returns the legality of a move :
            - the piece is availible
            - a corner of a piece is in a corner of an other one of the same color
            - the piece is located only on free cells
            - the piece isn't directly next to another of the same color"""
        
        if piece not in self.availible[self.is_playing_index] :
            return False
        
        x, y = position
        p_to_add = rotate(piece, rotation, flipped)
        length = len(p_to_add[0])
        height = len(p_to_add)
        if x < 0 or y < 0 or x + length > 22 or y + height > 22 :
            return False
        
        valid = False
        for i in range(length):
            for j in range(height):
                if p_to_add[j][i] == 1 and self.board[y+j][x+i] != 0 :
                    return False
                if p_to_add[j][i] == 2 and self.board[y+j][x+i] == self.is_playing :
                    valid = True
                if p_to_add[j][i] == 3 and self.board[y+j][x+i] == self.is_playing :
                    return False
        
        return valid


if __name__ == "__main__" : 
    g1 = Game(4)
    g1.print_board()