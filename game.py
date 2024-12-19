from pieces import *
from random import randint, choice
import time

# def rotate(piece:int, rotation:{0, 90, 180, 270}, flipped:bool) -> list[list[int]]:
#     return pieces[piece - 1].rotate(rotation, flipped)

class Game:
    def __init__(self, players:list[int]):
        n = max(players)
        game_board = [[['N' for _ in range(n)] for _ in range(22)] for _ in range(22)]        
        # Board edges
        game_board[0] = [['I' for _ in range(n)] for _ in range(22)]
        game_board[21] = [['I' for _ in range(n)] for _ in range(22)]

        for i in range(21) :
            game_board[i][0] = ['I' for _ in range(n)]
            game_board[i][21] = ['I' for _ in range(n)]

        # Mark every corner as an availible spot
        game_board[0][0] = ['P' for _ in range(n)]
        game_board[1][1] = ['A' for _ in range(n)]

        game_board[21][0] = ['P' for _ in range(n)]
        game_board[20][1] = ['A' for _ in range(n)]

        game_board[0][21] = ['P' for _ in range(n)]
        game_board[1][20] = ['A' for _ in range(n)]

        game_board[21][21] = ['P' for _ in range(n)]
        game_board[20][20] = ['A' for _ in range(n)]

        red_pieces = [[(1, 1), (20, 20), (1, 20), (20, 1)] for _ in range(n)]
        availible = [[i for i in range(1, 22)] for _ in range(n)]
        bonus = [False for i in range(n)]

        self.players = players
        self.availible = availible
        self.bonus = bonus
        self.board = game_board
        self.red_pieces = red_pieces
        self.is_playing = players[0]
        self.is_playing_index = 0
        self.maxn = n

    def print_board_all(self, player:int) -> None: 
        """
        displays the board as seen by a player along with the virtual edges, debug function
        """
        for i in range(22):
            line = '|'
            for j in range(22):
                line = line + str(self.board[i][j][player - 1]) + '|'
            print(line)

    def print_board_see(self, player:int) -> None: 
        """
        displays the board as seen by a player, debug function
        """
        for i in range(1, 21):
            line = '|'
            for j in range(1, 21):
                if self.board[i][j][player - 1] == 'P':
                    line = line + "🟩|"
                elif self.board[i][j][player - 1] == 'A':
                    line = line + "🟥|"
                elif self.board[i][j][player - 1] == 'I':
                    line = line + "⬜|"
                else:
                    line = line + "⬛|"

            print(line, "\n")

    def print_board(self) -> None:
        """
        displays the board as it would be seen on a game page
        """
        for i in range(1, 21):
            line = str()
            for j in range(1, 21):
                if self.board[i][j][0] == 'P':
                    line = line + "🟩 " 
                elif self.board[i][j][1] == 'P':
                    line = line + "🟥 " 
                elif self.maxn > 2 and self.board[i][j][2] == 'P':
                    line = line + "🟦 " 
                elif self.maxn > 3 and self.board[i][j][3] == 'P':
                    line = line + "🟨 "
                else:
                    line = line + "⬛ "

            print(line)
        print("")


    def add_piece(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int, int], flipped:bool, player:int) -> None:
        """
        adds a piece onto the board without any verification of legality whatsoever
        CAREFUL: piece is an integer!
        position is a tuple (x, y)
        """
        x, y = position
        to_add = rotate(piece, rotation, flipped)
        n = len(to_add)
        l = len(to_add[0])
        for i in range(n):
            for j in range(l):
                if to_add[i][j] == 1: # Adding the piece
                    for k in self.players:
                        if (i+x, j+y) in self.red_pieces[k - 1]:
                            self.red_pieces[k - 1].remove((i+x, j+y))
                    self.board[i+x][j+y] = ['I' for _ in range(self.maxn)]
                    self.board[i+x][j+y][player - 1] = 'P'
                    
                elif to_add[i][j] == 2 and self.board[i+x][j+y][player - 1] in ['A', 'N']:
                    self.red_pieces[player - 1].append((i+x, j+y))
                    self.board[i+x][j+y][player - 1] = 'A'
    
        # Make it so that a player cannot play in another corner
        if len(self.availible[player - 1]) == 21:
            corners = (1, 1, 0, 0), (1, 20, 0, 21), (20, 1, 21, 0), (20, 20, 21, 21)
            for corner in corners:
                if self.board[corner[0]][corner[1]][player - 1] == 'A':
                    self.red_pieces[player - 1].remove((corner[0], corner[1]))
                    self.board[corner[0]][corner[1]][player - 1] = 'N'
                    self.board[corner[2]][corner[3]][player - 1] = 'I'

        # Bonus if the last piece placed is the monomino
        if len(self.availible[player - 1]) == 1 and piece == 1:
            self.bonus[player - 1] = True
        self.availible[player - 1].remove(piece)


    def is_legal(self, piece:int, rotation:{0, 90, 180, 270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
        """
        returns the legality of a move in three steps:
            1. A corner of the piece is in a red spot
            2. The piece is located only on availible cells
            3. The piece isn’t directly next to another of the same colour
        """
        
        # Check if the piece is availible to the player
        if piece not in self.availible[player - 1]:
            return False
        
        # Check if piece is within board bounds
        x, y = position
        cur_p = rotate(piece, rotation, flipped)
        if x + len(cur_p) - 1 >= 22 or y + len(cur_p[0]) - 1 >= 22 or x < 0 or y < 0:
            return False

        valid = False
        for i in range(len(cur_p)):
            for j in range(len(cur_p[0])):
                if cur_p[i][j] == 2 and self.board[x + i][y + j][player - 1] == 'P':
                    valid = True

                elif cur_p[i][j] == 1 and (self.board[x + i][y + j][player - 1] == 'I' or self.board[x+i][y+j][player - 1] == 'P'):
                    return False

                elif cur_p[i][j] == 3 and self.board[x + i][y + j][player - 1] == 'P':
                    return False
        
        return valid
                    
    def score(self, player:int) -> int:
        """
        returns the score of a player, i.e. the amount of squares of each unused piece
        """
        total = 0
        for piece in self.availible[player - 1]:
            shape = pieces[piece - 1]
            for line in shape:
                for cell in line:
                    if cell == 1:
                        total -= 1

        if not self.availible[player - 1]:
            total += 20
        if self.bonus[player - 1]:
            total += 5
        
        return total

    def possible_moves(self, player:int):
        """
        returns the list of all possible moves for a player
        """

        res = list()

        # we go through every availible cell, and check if every rotation of every piece can be placed there
        for p in self.availible[player - 1]:
            for c in self.red_pieces[player - 1]:
                for [r, f] in pieces_rotations[p-1]:
                    cur_p = rotate(p, r, f)

                    xmin = c[0] - len(cur_p)
                    xmax = c[0]
                    ymin = c[1] - len(cur_p[0])
                    ymax = c[1]
                    for x in range(xmin, xmax + 1):
                        for y in range(ymin, ymax + 1):
                            if self.is_legal(p, r, (x, y), f, player):
                                res.append((p, r, (x, y), f))
        
        return res

    def can_play(self, player:int) -> bool:
        """
        returns whether a player as an availible move or not
        """
        # we go through every availible cell, and check if every rotation of every piece can be placed there
        for p in self.availible[player - 1]:
            for c in self.red_pieces[player - 1]:
                for [r, f] in pieces_rotations[p-1]:
                        cur_p = rotate(p, r, f)
                    
                        xmin = c[0] - len(cur_p)
                        xmax = c[0]
                        ymin = c[1] - len(cur_p[0])
                        ymax = c[1]
                        for x in range(xmin, xmax + 1):
                            for y in range(ymin, ymax + 1):
                                if self.is_legal(p, r, (x, y), f, player):
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
            self.print_board()

            if self.can_play(self.is_playing):
                # valid = False
                # while not valid:
                #     print(f"player {self.is_playing} make a move:")
                #     piece = int(input("piece to place: "))
                #     flipped = bool(input("flipped? (press Enter if no)"))
                #     rotation = int(input("rotation: "))
                #     y = int(input("horizontal coordinate? "))
                #     x = int(input("vertical coordinate? "))
                #     valid = self.is_legal(piece, rotation, (x, y), flipped, self.is_playing)
                #     if not valid:
                #         print("piece cannot be placed here! R.I.P.")
                piece, rotation, (x, y), flipped = pos[randint(0, len(pos) - 1)]
                self.add_piece(piece, rotation, (x, y), flipped, self.is_playing)

                self.is_playing_index = (self.is_playing_index + 1) % (len(self.players))
            else:
                print(f"Player {self.is_playing} does not have any availible move!")
                self.delete_player(self.is_playing)
                if self.is_playing_index >= len(self.players):
                    self.is_playing_index = 0
            
            if self.players:
                self.is_playing = self.players[self.is_playing_index]
        
        self.print_board()
        print("Game is over!")
        for player in range(1, self.maxn + 1):
            print(f"Player {player} pieces left: {self.availible[player-1]}")
            print(f"Score: {self.score(player)}")


def retrieve_game(players:list[int], moves:list[list[str, int, int, int, int, int, int, bool]]) -> Game:
    """
    recreates a game using database data. “moves” is a list of moves with all required information sorted by when the piece is placed, as given by db.py’s get_game_history function
    """
    g = Game(players)

    player = g.players[-1]
    for move in moves:
        _, _, player, piece, x, y, rotation, flipped = move
        g.add_piece(piece, rotation, (x, y), flipped, player)

    for p in players:
        if not g.can_play(p):
            g.players.remove(p)

    g.is_playing_index = g.players.index(player) + 1
    if g.is_playing_index == len(g.players):
        g.is_playing_index = 0

    g.is_playing = g.players[g.is_playing_index] 
    return g

if __name__ == "__main__":
    g1 = Game([1, 2, 4])
    start = time.time()
    g1.play_game()
    print(f"Time taken: {time.time() - start}")
