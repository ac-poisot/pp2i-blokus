from piece import Piece
from pieces import pieces
from random import randint

def rotate(piece:int, rotation:{0,90,180,270}, flipped:bool) -> list[list[int]]:
    return pieces[piece-1].rotate(rotation, flipped)

class Game:
    def __init__(self, nb_players:int):
        game_board = [[['N' for _ in range(nb_players)] for _ in range(22)] for _ in range(22)]
        used = [[],[],[],[]]
        game_board[0] = [['I' for _ in range(nb_players)] for _ in range(22)] # Ca devrait pas être ['P','I','I','I'] ? → non, on peut jouer dans tous les coins
        game_board[21] = [['I' for _ in range(nb_players)] for _ in range(22)]

        for i in range(21) :
            game_board[i][0] = ['I' for _ in range(nb_players)]
            game_board[i][21] = ['I' for _ in range(nb_players)]

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

    def print_board(self) -> None:
        for i in range(1,21):
            line = '|'
            for j in range(1,21):
                if self.board[i][j][0] == "P":
                    line = line + "🟩" + '|'
                elif self.board[i][j][1] == "P":
                    line = line + "🟥" + '|'
                elif self.nb_players > 2 and self.board[i][j][2] == "P":
                    line = line + "🟦" + '|'
                elif self.nb_players > 3 and self.board[i][j][3] == "P":
                    line = line + "🟨" + '|'
                else:
                    line = line + "⬛" + '|'

            print(line)

    def print_board_see(self, player:int) -> None: 
        """
        displays the board as seen by a player, debug function
        """
        for i in range(1,21):
            line = '|'
            for j in range(1,21):
                if self.board[i][j][player-1] == "P":
                    line = line + "🟩" + '|'
                elif self.board[i][j][player-1] == "A":
                    line = line + "🟥" + '|'
                elif self.board[i][j][player-1] == "I":
                    line = line + "⬜" + '|'
                else:
                    line = line + "⬛" + '|'

            print(line)

    def add_piece(self, piece:int, rotation:{0,90,180,270}, position:tuple[int,int], flipped:bool) -> None:
        """
        adds a piece onto the board without any verification of legality whatsoever
        CAREFUL: piece is an integer!
        position is a tuple (x,y)
        """
        x,y = position
        piece_ajoutable = rotate(piece,rotation,flipped)
        n = len(piece_ajoutable)
        l = len(piece_ajoutable[0])
        for i in range(n):
            for j in range(l):
                if piece_ajoutable[i][j] == 1: #On ajoute la pièce
                    for k in self.players:
                        if (i+x,j+y) in self.red_pieces[k-1]:
                            self.red_pieces[k-1].remove((i+x,j+y))
                    self.board[i+x][j+y] = ['I' for i in range(self.nb_players)]
                    self.board[i+x][j+y][self.is_playing-1] = 'P'
                elif piece_ajoutable[i][j] == 2 and self.board[i+x][j+y][self.is_playing-1] in ['A','N']:
                    self.red_pieces[self.is_playing-1].append((i+x,j+y))
                    self.board[i+x][j+y][self.is_playing-1] = 'A'
        
        self.used[self.is_playing-1].append(piece)

    def empty_space(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool: 
        """
        returns whether a piece would be placed on availible cells only if placed
        """
        x, y = position
        p_act = rotate(piece, rotation, flipped)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                # cas sur une piece non vide ou inaccessible
                if p_act[i][j] == 1 and (self.board[x+i][y+j][player-1] == 'I' or self.board[x+i][y+j][player-1] == 'P'):
                    return False
                
        return True
    
    def no_near_other(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
        """
        returns whether a piece would be next to another of the same colour if placed
        """

        x, y = position
        p_act = rotate(piece,rotation,flipped)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                if p_act[i][j] == 3 and self.board[x+i][y+j][player-1] == 'P':
                    return False
        return True

    def on_red(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
        """
        returns whether a piece would be tangent to another piece of the same color if placed
        """
        x,y = position
        p_act = rotate(piece,rotation,flipped)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                if p_act[i][j] == 2 and self.board[x+i][y+j][player-1] == 'P':
                    return True
        return False

    def is_legal(self, piece:int, rotation:{0,90,180,270}, position:tuple[int, int], flipped:bool, player:int) -> bool:
        """
        returns the legality of a move in three steps:
            1. A corner of the piece is in a red spot
            2. The piece is located only on availible cells
            3. The piece isn’t directly next to another of the same colour
        """
        # la piece est dans le plateau
        x, y = position
        p_act = rotate(piece,rotation,flipped)
        if x+len(p_act)-1 >= 22 or y+len(p_act[0])-1 >= 22 or x < 0 or y < 0:
            return False
        #coin sur une case rouge
        corner_on_red = self.on_red(piece,rotation,position,flipped,player)
        # la piece est entierement sur une case vide
        free = self.empty_space(piece,rotation,position,flipped,player)
        #la piece n'est pas tangente a une case de la meme couleur
        not_tangent = self.no_near_other(piece,rotation,position,flipped,player)

        return corner_on_red and free and not_tangent
    
    def possible_moves(self, player:int):
        """
        returns the list of all possible moves for a player
        """
        rotation = [0,90,180,270]
        flipped = [True,False]

        res = []

        #recupuere les pieces restantes
        not_used = []
        for i in range(1,22):
            if i not in self.used[player-1]:
                not_used.append(i)
        # on parcourt la liste des cases accessibles en verifiant pour chaque rotation que la piece est posable, en remarquant les differentes positions possibles
        for p in not_used:
            for c in self.red_pieces[player-1]:
                for r in rotation:
                    for b in flipped:
                        # les quatre cas
                        p_act = rotate(p,r,b)
                        xmin = c[0]-len(p_act)
                        xmax = c[0]
                        ymin = c[1]-len(p_act[0])
                        ymax = c[1]
                        for x in range(xmin,xmax+1):
                            for y in range(ymin,ymax+1):
                                if self.is_legal(p,r,(x,y),b, player):
                                    res.append((p,r,(x,y),b))
        
        return res
    
    def delete_player(self, player:int):
        """
        gets rid a player that do not have any availible move
        """
        self.players.remove(player)

    def endgame(self):
        """
        returns whether a game has ended or not
        """
        return not self.players
        
    def play_game(self):
        while not(self.endgame()):
            pos = self.possible_moves(self.is_playing)
            if pos:
                self.print_board()
                # valid = False
                # while not valid:
                #     print("player " + str(self.is_playing) + " make a move:")
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


                print('')
                self.is_playing_index += 1
            else:
                print("Player", self.is_playing, "does not have any availible move!")
                self.delete_player(self.is_playing)
            
            if self.players:
                if self.is_playing_index == len(self.players):
                    self.is_playing_index = 0
                    self.is_playing = self.players[0]
                self.is_playing = self.players[self.is_playing_index]

        print("Game is over!")



if __name__ == "__main__":
    g1 = Game(4)
    g1.play_game()
    # g1.add_piece(3,90,(5,5),False)
    # g1.print_board_see(1)
    # print(g1.board[6][6])
    # print(g1.red_pieces)