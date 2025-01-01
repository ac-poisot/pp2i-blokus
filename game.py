from pieces import *
from random import randint, choice
import time

initial_possibilities = []
for p in range(len(pieces)):
    for r in [0,90,180,270] :
        for b in [True,False]:
            new_piece = rotate(p,r,b)
            x_min = 0
            x_max = len(new_piece[0])
            y_min = 0
            y_max = len(new_piece)
            if new_piece[y_min][x_min] == 2 : 
                initial_possibilities.append((p,r,b,(0,0)))
            if new_piece[y_max-1][x_min] == 2 : 
                initial_possibilities.append((p,r,b,(0,21-y_max+1)))
            if new_piece[y_min][x_max-1] == 2 : 
                initial_possibilities.append((p,r,b,(21-x_max+1,0)))
            if new_piece[y_max-1][x_max-1] == 2 : 
                initial_possibilities.append((p,r,b,(21-x_max+1,21-y_max+1)))

class Game :
    def __init__(self, players:int):
        """initialise le jeu"""
        game_board = [[0 for _ in range(22)] for _ in  range(22)]
        poss = [[] for _ in  range(players)]
        for j in range(players):
            poss[j] = initial_possibilities.copy()
                        
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
        """
        displays the board as it would be seen on a game page
        """
        for i in range(1, 21):
            line = str()
            for j in range(1, 21):
                if self.board[i][j] == 1:
                    line = line + "🟩 " 
                elif self.board[i][j] == 2:
                    line = line + "🟥 " 
                elif self.maxn > 2 and self.board[i][j]== 3:
                    line = line + "🟦 " 
                elif self.maxn > 3 and self.board[i][j] == 4:
                    line = line + "🟨 "
                else:
                    line = line + "⬛ "

            print(line)
        print("")
    
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
                
        # Check if the piece is at a corner
        if len(self.availible[player-1]) == 21:
            if (x == 0 and y == 0) or (x == 21 - length + 1 and y == 0) or (x == 0 and y == 21 - height + 1) or (x == 21 - length + 1 and y == 21 - height + 1):
                return True

        return valid
    
    def is_red_cell(self, x, y, player):
        """"
        Returns whether a piece of the chosen player can start at this cell or not
        """
        angleContact = False
        if self.board[y][x] != 0: return False

        if y-1 >= 0:
            if self.board[y-1][x] == player: return False
            if x-1 >= 0 and self.board[y-1][x-1] == player: angleContact = True
            if x+1 < len(self.board[y]) and self.board[y-1][x+1] == player: angleContact = True
        # print("here")
        if y+1 < len(self.board):
            if self.board[y+1][x] == player: return False
            if x-1 >= 0 and self.board[y+1][x-1] == player: angleContact = True
            if x+1 < len(self.board[y]) and self.board[y+1][x+1] == player: angleContact = True
        if x-1 >= 0 and self.board[y][x-1] == player: return False
        if x+1 < len(self.board[y]) and self.board[y][x+1] == player: return False
        # print(angleContact)
        return angleContact

    
    def add_piece(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int, int], flipped:bool, playing:int = None) -> None :
        """ add the piece without any verification of legality"""
        if playing is None:
            playing = self.is_playing
        x, y = position
        p_to_add = rotate(piece, rotation, flipped)
        length = len(p_to_add[0])
        height = len(p_to_add)

        # Remove the other corners from the possibilities list
        if(len(self.availible[playing-1]) == 21):
            self.possible_moves[playing-1] = []
            self.red_pieces[playing-1] = 0

        for i in range(length):
            for j in range(height):
                if p_to_add[j][i] == 1 : # add the piece
                    self.board[y+j][x+i] = playing
                elif p_to_add[j][i] == 2 and self.board[y+j][x+i] == 0 : # update red_pieces
                    self.red_pieces[playing-1] = self.red_pieces[playing-1] + 1
                elif p_to_add[j][i] == 2 and self.board[y+j][x+i] == playing : # update red_pieces
                    self.red_pieces[playing-1] = self.red_pieces[playing-1] - 1
        
        # remove current piece from availible
        self.availible[playing-1].remove(piece)

        x_min = x-5
        y_min = y-5
        x_max = x+length
        y_max = y+height

        # remove moves that are now not possible
        for player in self.players :
            to_be_removed = []
            for p in self.possible_moves[player-1]:
                xp, yp = p[3]
                if (p[0]==piece and playing==player) or (xp>=x_min and yp >= y_min and xp<=x_max and yp<=y_max and not self.is_legal(p[0],p[1],p[3],p[2],player)):
                    to_be_removed.append(p)
            self.possible_moves[player-1] = list(filter(lambda elem : not elem in to_be_removed,self.possible_moves[player-1]))

        # add new possibles moves
        t = len(self.availible[playing-1])
        for i in range(x_min,x_max):
            for j in range(y_min,y_max):
                pos = (i,j)
                # if self.is_red_cell(i, j, playing):
                for k in range(t):
                    p = self.availible[playing-1][k]
                    for r in [0,90,180,270]:
                        for b in [True,False] :
                            if self.is_legal(p,r,pos,b,playing):
                                self.possible_moves[playing-1].append((p,r,b,pos))
        
        # bonus if the last piece placed is the monomino
        if len(self.availible[playing-1]) == 0 and piece == 1:
            self.bonus[playing-1] = True

    def remove_piece(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int, int], flipped:bool) -> None :
        """
        Removes a piece from the board and updates the game state accordingly.
        Args:
            piece (int): The identifier of the piece to be removed.
            rotation ({0, 90, 180, 270}): The rotation angle of the piece.
            position (tuple[int, int]): The (x, y) position on the board where the piece is located.
            flipped (bool): Whether the piece is flipped horizontally.
        Returns:
            None
        """
        
        x, y = position
        p_to_add = rotate(piece, rotation, flipped)
        length = len(p_to_add[0])
        height = len(p_to_add)

        

        for i in range(length):
            for j in range(height):
                if p_to_add[j][i] == 1 : # remove the piece
                    self.board[y+j][x+i] = 0
                elif p_to_add[j][i] == 2 and self.board[y+j][x+i] == 0 : # update red_pieces
                    self.red_pieces[self.is_playing_index] = self.red_pieces[self.is_playing_index] - 1
                elif p_to_add[j][i] == 2 and self.board[y+j][x+i] == self.is_playing : # update red_pieces
                    self.red_pieces[self.is_playing_index] = self.red_pieces[self.is_playing_index] + 1
        
        # remove current piece from availible
        self.availible[self.is_playing_index].append(piece) # add the piece back (what about the new index?)

        if(len(self.availible[self.is_playing_index]) == 21):
        #     self.possible_moves[self.is_playing_index] = initial_possibilities.copy()
            self.red_pieces[self.is_playing_index] = 4 ## SHOULD BE THE NUMBER OF CORNERS STILL AVAILABLE

        # x_min = x-5
        # y_min = y-5
        # x_max = x+length
        # y_max = y+height

        # # remove moves that are now not possible
        
        # to_be_removed = []
        # for p in self.possible_moves[self.is_playing_index]:
        #     xp, yp = p[3]
        #     if (p[0]==piece and self.is_playing==self.is_playing) or (xp>=x_min and yp >= y_min and xp<=x_max and yp<=y_max and not self.is_legal(p[0],p[1],p[3],p[2],self.is_playing)):
        #         to_be_removed.append(p)
        # self.possible_moves[self.is_playing_index] = list(filter(lambda elem : not elem in to_be_removed,self.possible_moves[self.is_playing_index]))

        # # add new possibles moves
        # for player in self.players :
        #     for i in range(x_min,x_max):
        #         for j in range(y_min,y_max):
        #             pos = (i,j)
        #             # if self.is_red_cell(i, j, player):
        #             for p in self.availible[player-1] :
        #                 for r in [0,90,180,270]:
        #                     for b in [True,False] :
        #                         if self.is_legal(p,r,(pos[0]-1, pos[1]-1),b,player):
        #                             self.possible_moves[player-1].append((p,r,b,pos))
        
        # bonus if the last piece placed is the monomino
        if len(self.availible[self.is_playing_index]) == 0 and piece == 1:
            self.bonus[self.is_playing_index] = True

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
    
    def can_play(self, player:int) -> bool :
        """ return if a player can play"""
        return player in self.players and len(self.possible_moves[self.players.index(player)]) != 0
    
    def delete_player(self, player:int) -> None :
        """ delete a player from the game"""
        self.players.remove(player)
    
    def play_game(self):
        while self.players:
            pos = self.possible_moves[self.is_playing_index]

            if len(self.possible_moves[self.is_playing_index]) != 0 :
                piece, rotation, flipped, (x,y), = pos[randint(0, len(pos) - 1)]
                self.add_piece(piece,rotation, (x,y), flipped)

                self.is_playing_index = (self.is_playing_index + 1) % len(self.players)
            
            else :
                print(f"Player {self.is_playing} does not have any availible move!")
                self.players.remove(self.is_playing)
                if self.is_playing_index >= len(self.players):
                    self.is_playing_index = 0
            
            if self.players : 
                self.is_playing = self.players[self.is_playing_index]
            
        self.print_board()
        print("Game is over!")
        for player in range(1, self.maxn + 1):
            print(f"Player {player} pieces left: {self.availible[player-1]}")
            print(f"Score: {self.score(player)}")

    def copy_game(self):
        """
        Returns a deep copy of the game.
        Returns:
            Game: A deep copy of the game.
        """
        g = Game(len(self.players))
        g.board = [row.copy() for row in self.board]
        g.availible = [row.copy() for row in self.availible]
        g.bonus = self.bonus.copy()
        g.is_playing = self.is_playing
        g.is_playing_index = self.is_playing_index
        g.maxn = self.maxn
        g.possible_moves = [row.copy() for row in self.possible_moves]
        g.players = self.players.copy()
        g.red_pieces = self.red_pieces.copy()
        return g

def retrieve_game(players:int, moves:list[list[str, int, int, int, int, int, int, bool]]) -> Game:
    """
    recreates a game using database data. “moves” is a list of moves with all required information sorted by when the piece is placed, as given by db.py’s get_game_history function
    """
    g = Game(players)

    player = g.players[-1]
    for move in moves:
        _, _, player, piece, x, y, rotation, flipped = move
        g.add_piece(piece, rotation, (x, y), flipped, player)

    for i in range(players):
        if i < len(g.players) and not g.can_play(g.players[i]):
            g.players.remove(g.players[i])

    g.is_playing_index = g.players.index(player) + 1
    if g.is_playing_index == len(g.players):
        g.is_playing_index = 0

    g.is_playing = g.players[g.is_playing_index] 
    return g



if __name__ == "__main__" : 
    g1 = Game(4)
    start = time.time()
    g1.play_game()
    print(f"Time taken: {time.time() - start}")