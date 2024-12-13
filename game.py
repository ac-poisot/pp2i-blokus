from piece import Piece
from pieces import pieces
from random import randint

def rotate(piece:int, rotation:{0,90,180,270}, flipped:bool) -> list[list[int]]:
    return pieces[piece-1].rotate(rotation, flipped)

class Game:
    def __init__(self, nb_players:int):
        game_board = [[['N' for _ in range(nb_players)] for _ in range(22)] for _ in range(22)]        
        # Board edges
        game_board[0] = [['I' for _ in range(nb_players)] for _ in range(22)]
        game_board[21] = [['I' for _ in range(nb_players)] for _ in range(22)]

        for i in range(21) :
            game_board[i][0] = ['I' for _ in range(nb_players)]
            game_board[i][21] = ['I' for _ in range(nb_players)]

        # Mark every corner as an availible spot
        game_board[0][0] = ['P' for _ in range(nb_players)]
        game_board[1][1] = ['A' for _ in range(nb_players)]

        game_board[21][0] = ['P' for _ in range(nb_players)]
        game_board[20][1] = ['A' for _ in range(nb_players)]

        game_board[0][21] = ['P' for _ in range(nb_players)]
        game_board[1][20] = ['A' for _ in range(nb_players)]

        game_board[21][21] = ['P' for _ in range(nb_players)]
        game_board[20][20] = ['A' for _ in range(nb_players)]

        red_pieces = [[(1,1),(20,20),(1,20),(20,1)] for _ in range(nb_players)]
        players = [i for i in range(1,nb_players+1)]
        used = [[] for _ in range(nb_players)]


        self.players = players
        self.used = used
        self.board = game_board
        self.red_pieces = red_pieces
        self.is_playing = 1
        self.is_playing_index = 0
        self.nb_players = nb_players

    def print_board_all(self, player:int) -> None: 
        """
        displays the board as seen by a player along with the virtual edges, debug function
        """
        for i in range(22):
            line = '|'
            for j in range(22):
                line = line + str(self.board[i][j][player-1]) + '|'
            print(line)

    def print_board_see(self, player:int) -> None: 
        """
        displays the board as seen by a player, debug function
        """
        for i in range(1,21):
            line = '|'
            for j in range(1,21):
                if self.board[i][j][player-1] == 'P':
                    line = line + "🟩|"
                elif self.board[i][j][player-1] == 'A':
                    line = line + "🟥|"
                elif self.board[i][j][player-1] == 'I':
                    line = line + "⬜|"
                else:
                    line = line + "⬛|"

            print(line, "\n")

    def print_board(self) -> None:
        """
        displays the board as it would be seen on a game page
        """
        for i in range(1,21):
            line = str()
            for j in range(1,21):
                if self.board[i][j][0] == 'P':
                    line = line + "🟩 " 
                elif self.board[i][j][1] == 'P':
                    line = line + "🟥 " 
                elif self.nb_players > 2 and self.board[i][j][2] == 'P':
                    line = line + "🟦 " 
                elif self.nb_players > 3 and self.board[i][j][3] == 'P':
                    line = line + "🟨 "
                else:
                    line = line + "⬛ "

            print(line)
        print("")


    def add_piece(self, piece:int, rotation:{0,90,180,270}, position:tuple[int,int], flipped:bool) -> None:
        """
        adds a piece onto the board without any verification of legality whatsoever
        CAREFUL: piece is an integer!
        position is a tuple (x,y)
        """
        x, y = position
        to_add = rotate(piece, rotation, flipped)
        n = len(to_add)
        l = len(to_add[0])
        for i in range(n):
            for j in range(l):
                if to_add[i][j] == 1: # Adding the piece
                    for k in self.players:
                        if (i+x,j+y) in self.red_pieces[k-1]:
                            self.red_pieces[k-1].remove((i+x, j+y))
                    self.board[i+x][j+y] = ['I' for i in range(self.nb_players)]
                    self.board[i+x][j+y][self.is_playing-1] = 'P'
                    
                elif to_add[i][j] == 2 and self.board[i+x][j+y][self.is_playing-1] in ['A','N']:
                    self.red_pieces[self.is_playing-1].append((i+x, j+y))
                    self.board[i+x][j+y][self.is_playing-1] = 'A'
        
        self.used[self.is_playing - 1].append(piece)

    # def empty_space(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool: 
    #     """
    #     returns whether a piece would be placed on availible cells only if placed
    #     """
    #     x, y = position
    #     cur_p = rotate(piece, rotation, flipped)
    #     for i in range(len(cur_p)):
    #         for j in range(len(cur_p[0])):
    #             # Illegal if the cell is either in an invalid or taken state
    #             if cur_p[i][j] == 1 and (self.board[x+i][y+j][player-1] == 'I' or self.board[x+i][y+j][player-1] == 'P'):
    #                 return False
                
    #     return True
    
    # def no_near_other(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
    #     """
    #     returns whether a piece would be next to another of the same colour if placed
    #     """

    #     x, y = position
    #     cur_p = rotate(piece,rotation,flipped)
    #     for i in range(len(cur_p)):
    #         for j in range(len(cur_p[0])):
    #             if cur_p[i][j] == 3 and self.board[x+i][y+j][player-1] == 'P':
    #                 return False
    #     return True

    # def on_red(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
    #     """
    #     returns whether a piece would be tangent to another piece of the same color if placed
    #     """
    #     x,y = position
    #     cur_p = rotate(piece,rotation,flipped)
    #     for i in range(len(cur_p)):
    #         for j in range(len(cur_p[0])):
    #             if cur_p[i][j] == 2 and self.board[x+i][y+j][player-1] == 'P':
    #                 return True
    #     return False

    def is_legal(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
        """
        returns the legality of a move in three steps:
            1. A corner of the piece is in a red spot
            2. The piece is located only on availible cells
            3. The piece isn’t directly next to another of the same colour
        """
        # Check if piece is within board bounds
        x, y = position
        cur_p = rotate(piece,rotation,flipped)
        if x+len(cur_p)-1 >= 22 or y+len(cur_p[0])-1 >= 22 or x < 0 or y < 0:
            return False

        valid = False
        for i in range(len(cur_p)):
            for j in range(len(cur_p[0])):
                if cur_p[i][j] == 2 and self.board[x+i][y+j][player-1] == 'P':
                    valid = True

                if cur_p[i][j] == 1 and (self.board[x+i][y+j][player-1] == 'I' or self.board[x+i][y+j][player-1] == 'P'):
                    return False

                elif cur_p[i][j] == 3 and self.board[x+i][y+j][player-1] == 'P':
                    return False
        
        return valid
                    
    def score(self, player:int) -> int:
        """
        returns the score of a player, i.e. the amount of squares of each unused piece
        """
        not_used = [i for i in range(1,22) if i not in self.used[player-1]]
        total = 0
        for piece in not_used:
            shape = pieces[piece-1].shape
            for line in shape:
                for cell in line:
                    if cell == 1:
                        total += 1
        return total

    def possible_moves(self, player:int):
        """
        returns the list of all possible moves for a player
        """
        rotation = [0,90,180,270]
        flipped = [True,False]

        res = list()

        # retrieves availible pieces
        not_used = [i for i in range(1,22) if i not in self.used[player-1]]

        # we go through every availible cell, and check if every rotation of every piece can be placed there
        for p in not_used:
            for c in self.red_pieces[player-1]:
                for r in rotation:
                    for b in flipped:
                        
                        cur_p = rotate(p,r,b)
                        # Avoid checking duplicate cases
                        if cur_p == pieces[p-1].shape and (flipped or rotation > 0):
                            xmin = c[0]-len(cur_p)
                            xmax = c[0]
                            ymin = c[1]-len(cur_p[0])
                            ymax = c[1]
                            for x in range(xmin,xmax+1):
                                for y in range(ymin,ymax+1):
                                    if self.is_legal(p,r,(x,y),b, player):
                                        res.append((p,r,(x,y),b))
        
        return res

    def can_play(self, player:int) -> bool:
        """
        returns whether a player as an availible move or not
        """
        rotation = [0,90,180,270]
        flipped = [True,False]

        # retrieves availible pieces
        not_used = [i for i in range(1,22) if i not in self.used[player-1]]

        # we go through every availible cell, and check if every rotation of every piece can be placed there
        for p in not_used:
            for c in self.red_pieces[player-1]:
                for r in rotation:
                    for b in flipped:
                        
                        cur_p = rotate(p,r,b)
                        # Avoid checking duplicate cases
                        if cur_p == pieces[p-1].shape and (flipped or rotation > 0):
                            xmin = c[0]-len(cur_p)
                            xmax = c[0]
                            ymin = c[1]-len(cur_p[0])
                            ymax = c[1]
                            for x in range(xmin,xmax+1):
                                for y in range(ymin,ymax+1):
                                    if self.is_legal(p,r,(x,y),b, player):
                                        return True
        
        return False


    def delete_player(self, player:int):
        """
        gets rid a player that do not have any availible move
        """
        self.players.remove(player)
        
    def play_game(self):
        while self.players:
            pos = self.possible_moves(self.is_playing)
            if self.can_play(self.is_playing):
                self.print_board()
                # valid = False
                # while not valid:
                #     print(f"player {self.is_playing} make a move:")
                #     piece = int(input("piece to place: "))
                #     flipped = bool(input("flipped? (press Enter if no)"))
                #     rotation = int(input("rotation: "))
                #     y = int(input("horizontal coordinate? "))
                #     x = int(input("vertical coordinate? "))
                #     valid = self.is_legal(piece, rotation, (x,y), flipped, self.is_playing)
                #     if not valid:
                #         print("piece cannot be placed here! R.I.P.")
                piece, rotation, (x,y), flipped = pos[randint(0, len(pos)-1)]
                self.add_piece(piece, rotation, (x,y), flipped)

                self.is_playing_index = (self.is_playing_index + 1) % (len(self.players))
            else:
                print(f"Player {self.is_playing} does not have any availible move!")
                self.delete_player(self.is_playing)
                if self.is_playing_index >= len(self.players):
                    self.is_playing_index = 0
            
            if self.players:
                self.is_playing = self.players[self.is_playing_index]

        print("Game is over!")
        for player in range(1, self.nb_players+1):
            print(f"Player {player} pieces left: {[i for i in range(1,22) if i not in self.used[player-1]]}")
            print(f"Score: {self.score(player)}")


def retrieve_game(nb_players:int, moves:list[list[str, int, int, int, int, int, int, bool]]) -> Game:
    """
    recreates a game using database data. “moves” is a list of moves with all required information sorted by when the piece is placed, as given by db.py’s get_game_history function
    """
    g = Game(nb_players)

    for move in moves:
        _, _, player, piece, x, y, rotation, flipped = move
        if g.possible_moves(g.is_playing):
            g.add_piece(piece, rotation, (x,y), flipped)
            g.is_playing_index = (g.is_playing_index + 1) % (len(g.players))

        else:
            g.delete_player(g.is_playing)
            if g.is_playing_index >= len(g.players):
                    g.is_playing_index = 0
            
        if g.players:
            g.is_playing = g.players[g.is_playing_index]
    
    return g

if __name__ == "__main__":
    g1 = Game(4)
    g1.play_game()