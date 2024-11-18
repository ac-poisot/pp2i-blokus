# game.py, pour le jeu
from pieces import *

class Game:
    def __init__(self,nb_players,pieces):
        game_board = [[0 for i in range(22)] for j in range(22)]
        used= {'id_piece' : [], 'position': []}
        players = [i for i in range(1,nb_players+1)]
        self.players = players
        self.used = used
        self.board = game_board
        self.pieces = pieces
        self.is_playing = 1

    def print_board_all(self):
        """affiche le  plateau et les bords virtuels, fonction de debugg, peut-etre utile pour front-end"""
        for i in range(22): #pour chaque ligne
            line = '|'
            for j in range(22):
                line = line + str(self.board[i][j]) + '|'
            print(line)

    def print_board_see(self):
        """affiche le  plateau vu par les joueurs, fonction de debugg, peut-etre utile pour front-end"""
        for i in range(1,21): #pour chaque ligne
            line = '|'
            for j in range(1,21):
                line = line + str(self.board[i][j]) + '|'
            print(line)

    def add_piece(self,piece,rotation,position):
        """rajoute une piece sur le plateau sans aucune verification
            la piece vient normalement du dictionnaire global qui n'est pas def ici
            ATTENTION : piece est donc un int !
            position est un tuple (x,y)

            Peut-etre a faire : modification des pieces utilisees, ajout case rouge, suppression case rouge utilisee
        """
        x = position[0]
        y = position[1]
        if rotation==0:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1:
                        self.board[i+y][x+j] = self.is_playing
        if rotation==90:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1:
                        self.board[y+j][x+len(p)-i-1] = self.is_playing

        if rotation==180:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1:
                        self.board[y+len(p)-i-1][x+len(p[0])-j-1] = self.is_playing

        if rotation==270:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1:
                        self.board[y+len(p[0])-j-1][x+i] = self.is_playing
        

    def empty_space(self,piece,rotation,position):
        x = position[0]
        y = position[1]
        if rotation==0:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1 and self.board[i+y][x+j]!=0:
                        return False
            return True
        
        if rotation==90:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1 and self.board[y+j][x+len(p)-i-1] !=0:
                        return False
            return True

        if rotation==180:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1 and self.board[y+len(p)-i-1][x+len(p[0])-j-1] !=0:
                        return False
            return True

        if rotation==270:
            p = self.pieces[piece]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    if p[i][j]==1 and self.board[y+len(p[0])-j-1][x+i] !=0:
                        return False
            return True
        
    #def legal_add_piece(self,piece,rotation,position):
    #    """verifie si un coup est legal en trois etapes:
    #        - un coin de la piece est dans une case rouge
    #        - la piece est entierement dans une zone vide
    #        - la piece ne touche pas le bord d'une piece de la meme couleur
    #        
    #        renvoie True ssi on peut poser la piece à cet endroit"""
    #    #coin sur une case rouge
    #    # a faire car modif possible de la structure des pieces

    #    # la piece est entierement sur une case vide

    #    # la piece n'est pas tangente a une case de la meme couleur

        




####### TESTS (oui ca va finir dans un fichier test tkt) ######

# def temporaire d'un dictionnaire
p_tempo = {}

for i in range(1,21):
    p_tempo[f"{i}"] = globals().get(f"p{i}")
# TEST __INIT__
#print(p_tempo['1'])
g1 = Game(2,p_tempo)
#print(g1.is_playing)
#plateau = g1.board
#p = g1.players
#print(plateau)
#print(p)

# TEST ADD_PIECE ET PRINT_BOARD
#g1.print_board_all()
#print('')
#g1.print_board_see()
#g1.add_piece('1',0,(0,0))
#g1.add_piece('2',0,(1,1))
#g1.add_piece('3',0,(3,2))
#g1.add_piece('4',0,(6,6))
#g1.add_piece('6',0,(8,8))
#print('')
#g1.print_board_see()

#print('')
#g1.print_board_all()
print(p_tempo["18"])
# TEST FULL_EMPTY
"""
g1.add_piece('6',90,(0,0))
g1.print_board_see()
g1.is_playing = g1.is_playing + 1
print(g1.is_playing)
print(g1.empty_space('3',0,(0,0)))
print(g1.empty_space('3',0,(19,17)))
g1.add_piece('3',0,(19,17))
g1.print_board_see()
print(g1.empty_space('11',270,(2,1)))
print(g1.empty_space('11',180,(2,2)))
g1.add_piece('11',180,(2,2))
g1.print_board_see()"""