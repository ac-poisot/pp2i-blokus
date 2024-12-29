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
                        
        self.availible = [[i for i in range(1,22)] for j in range(players)]
        self.board = game_board
        self.bonus = [False for _ in range(players)]
        self.is_playing = 1
        self.is_playing_index = 0
        self.maxn = players
        self.possible_moves = poss
        self.players = [i+1 for i in range(players)]
        self.red_pieces = [4 for _ in range(players)]
    
    def print_board(self):
        """ display the board, debug function"""
        for i in range(22):
            print(self.board[i])
    
    def is_legal(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int,int], flipped:bool, player:int) -> bool :
        """ 
        returns the legality of a move :
            - the piece is availible
            - a corner of a piece is in a corner of an other one of the same color
            - the piece is located only on free cells
            - the piece isn't directly next to another of the same color"""
        
        # check avaibility
        if piece not in self.availible[player-1] :
            return False
        
        x, y = position
        p_to_add = rotate(piece, rotation, flipped)
        length = len(p_to_add[0])
        height = len(p_to_add)

        # check on board
        if x < 0 or y < 0 or x + length > 22 or y + height > 22 :
            return False
        
        valid = False
        for i in range(length):
            for j in range(height):
                if p_to_add[j][i] == 1 and self.board[y+j][x+i] != 0 : # check no on another piece
                    return False
                if p_to_add[j][i] == 2 and self.board[y+j][x+i] == player : # check corner
                    valid = True
                if p_to_add[j][i] == 3 and self.board[y+j][x+i] == player : # chech no near another piece of same color
                    return False
        
        return valid
    
    def add_piece(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int, int], flipped:bool) -> None :
        """ add the piece without any verification of legality"""
        x, y = position
        p_to_add = rotate(piece, rotation, flipped)
        length = len(p_to_add[0])
        height = len(p_to_add)

        for i in range(length):
            for j in range(height):
                if p_to_add[j][i] == 1 : # add the piece
                    self.board[y+j][x+i] = self.is_playing
                elif p_to_add[j][i] == 2 and self.board[y+j][x+i] == 0 : # update red_pieces
                    self.red_pieces[self.is_playing_index] = self.red_pieces[self.is_playing] + 1
                elif p_to_add[j][i] == 2 and self.board[y+j][x+i] == self.is_playing : # update red_pieces
                    self.red_pieces[self.is_playing_index] = self.red_pieces[self.is_playing] - 1
        
        # remove current piece from availible
        self.availible[self.is_playing_index].remove(piece)

        x_min = x-5
        y_min = y-5
        x_max = x+length
        y_max = y+height

        # remove moves that are now not possible
        for player in self.players :
            to_be_removed = []
            for p in self.possible_moves[player-1]:
                xp, yp = p[3]
                if (p[0]==piece and self.is_playing==player) or (xp>=x_min and yp >= y_min and xp<=x_max and yp<=y_max and not self.is_legal(p[0],p[1],p[3],p[2],player)):
                    to_be_removed.append(p)
            self.possible_moves[player-1] = list(filter(lambda elem : not elem in to_be_removed,self.possible_moves[player-1]))

        # add new possibles moves
        for i in range(x_min,x_max):
            for j in range(y_min,y_max):
                pos = (i,j)
                for p in self.availible[self.is_playing_index] :
                    for r in [0,90,180,270]:
                        for b in [True,False] :
                            if self.is_legal(p,r,pos,b,self.is_playing):
                                self.possible_moves[self.is_playing_index].append((p,r,b,pos))
        
        # bonus if the last piece placed is the monomino
        if len(self.availible[player-1]) == 0 and piece == 1:
            self.bonus[player-1] = True

    def score(self,player:int) -> int :
        """ return the score of a player"""

        total = 0
        for piece in self.availible[player-1]:
            shape = pieces[piece-1]
            height = len(shape)
            length = len(shape[0])
            for i in range(length):
                for j in range(height):
                    if shape[j][i] == 1:
                        total = total - 1
        
        if len(self.availible[player-1]) == 0 :
            total = total + 20
        
        if self.bonus[player-1]:
            total = total + 5
        
        return total





if __name__ == "__main__" : 
    g1 = Game(4)
    g1.print_board()