# game.py, pour le jeu
from pieces import *

class Game:
    def __init__(self,nb_players,pieces):
        game_board = [[['N','N','N','N'] for i in range(22)] for j in range(22)]
        used= [[],[],[],[]]
        red_pieces = [[],[],[],[]] #pour stocker les pieces 'accessibles', utile fin partie
        players = [i for i in range(1,nb_players+1)]
        self.players = players
        self.used = used
        self.board = game_board
        self.pieces = pieces
        self.red_pieces = red_pieces
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

   

    def rotate(self,piece,rotation,retourne):
        """retourne la piece et la renvoie"""
        p = self.pieces[piece]
        if rotation==0 and not(retourne):
            G = p  
        if rotation==90 and not(retourne):
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[j][len(p)-1-i] = p[i][j]
        if rotation==180 and not(retourne): # 
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p)-i-1][len(p[0])-j-1] = p[i][j]
        if rotation==270 and not(retourne):
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p[0])-j-1][i] = p[i][j]
        if rotation==0 and retourne: 
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p)-i-1][j] = p[i][j]
        if rotation==90 and retourne:
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[j][i] = p[i][j]
        if rotation==180 and retourne:
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p)-i-1][j] = p[i][j]
        if rotation==270 and retourne:###
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p[0])-j-1][len(p)-i-1] = p[i][j]
        return G


    def add_piece(self,piece,rotation,position,retourne):
        """rajoute une piece sur le plateau sans aucune verification
            la piece vient normalement du dictionnaire global qui n'est pas def ici
            ATTENTION : piece est donc un int !
            position est un tuple (x,y)
            
            a faire : ajout case rouge, suppression case rouge utilisee
        """
        x = position[0]
        y = position[1]
        p_act = self.rotate(piece,rotation,retourne)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                # retirer la case rouge
                if self.board[x+i][y+j][self.is_playing-1] == 'A' and p_act[i][j] == 1:
                    self.red_pieces[self.is_playing-1].remove((x+i,y+j))
                
                #on rajoute la piece et ses composantes
                if p_act[i][j] == 1:
                    self.board[x+i][y+j] = ['I','I','I','I']
                    self.board[x+i][y+j][self.is_playing-1] = 'P'
                    self.used[self.is_playing-1].append(piece)
                elif p_act[i][j] == 2 and not(self.board[x+i][y+j][self.is_playing-1] == 'I' or self.board[x+i][y+j][self.is_playing-1] == 'P'):
                    self.board[x+i][y+j][self.is_playing-1] = 'A'
                    self.red_pieces[self.is_playing-1].append((x+i,y+j))
                elif p_act[i][j] == 3:
                    self.board[x+i][y+j][self.is_playing-1] = 'I'
                
                


    def empty_space(self,piece,rotation,position,retourne):
        """
            fonction qui verifie qu'on pose une piece sur une case accessible, donc pas Prise par le joueur ou Inacessible
        """
        x = position[0]
        y = position[1]
        p = self.pieces[piece]
        p_act = self.rotate(p,rotation,retourne)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                if p_act[i][j] == 1 and not(self.is_playing):
                    pass



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
p_tempo = {'1' : [[2,3,2],[3,1,3],[2,3,2]],
           '2' : [[2,3,2],[3,1,3],[3,1,3],[2,3,2]],
           '3' : [[2,0,2],[0,1,0],[0,1,0],[0,1,0],[2,0,2]],
           '4' : [[2,0,2,0],[0,1,0,2],[0,1,1,0],[2,0,0,2]],
           '5' : [[2,0,2],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[2,0,2]],
           '6' :  [[0,2,0,2],[0,0,1,0],[2,0,1,0],[0,1,1,0],[2,0,0,2]],
           '7' :  [[2,0,2,0],[0,1,0,2],[0,1,1,0],[0,1,0,2],[2,0,2,0]],
           '8' :  [[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2]],
           '9' :  [[2,0,0,2,0],[0,1,1,0,2],[2,0,1,1,0],[0,2,0,0,2]],
           '10' :  [[2,0,2],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[2,0,2]],
           '11' :  [[0,2,0,2],[0,0,1,0],[0,0,1,0],[2,0,1,0],[0,1,1,0],[2,0,0,2]],
           '12' :  [[0,2,0,2],[0,0,1,0],[2,0,1,0],[0,1,1,0],[0,1,0,2],[2,0,2,0]],
           '13' :  [[0,2,0,2],[2,0,1,0],[0,1,1,0],[0,1,1,0],[2,0,0,2]],
           '14' :  [[2,0,0,2],[0,1,1,0],[2,0,1,0],[0,1,1,0],[2,0,0,2]],
           '15' :  [[2,0,2,0],[0,1,0,2],[0,1,1,0],[0,1,0,2],[0,1,0,0],[2,0,2,0]],
           '16' :  [[0,2,0,2,0],[0,0,1,0,0],[2,0,1,0,2],[0,1,1,1,0],[2,0,0,0,2]],
           '17' :  [[2,0,2,0,0],[0,1,0,0,0],[0,1,0,0,2],[0,1,1,1,0],[2,0,0,0,2]],
           '18' :  [[2,0,0,2,0],[0,1,1,0,2],[2,0,1,1,0],[0,2,0,1,0],[0,0,2,0,2]],
           '19' :  [[2,0,2,0,0],[0,1,0,0,2],[0,1,1,1,0],[2,0,0,1,0],[0,0,2,0,2]],
           '20' :  [[2,0,2,0,0],[0,1,0,0,2],[0,1,1,1,0],[2,0,1,0,2],[0,2,0,2,0]],
           '21' :  [[0,2,0,2,0],[2,0,1,0,2],[0,1,1,1,0],[2,0,1,0,2],[0,2,0,2,0]]}


# TEST __INIT__
#print(p_tempo['1'])
g1 = Game(2,p_tempo)
g2 = Game(2,p_tempo)
#print(g1.is_playing)
#plateau = g1.board
#p = g1.players
#print(plateau)
#print(p)

# TEST ADD_PIECE ET PRINT_BOARD
#g1.print_board_all()
#print('')
#g1.print_board_see()
print(g1.is_playing)
g1.add_piece('1',0,(0,0),False)
g1.add_piece('2',0,(1,1),False)
#g1.add_piece('3',0,(3,2),False)
#g1.add_piece('4',0,(6,6),False)
#g1.add_piece('6',0,(8,10),False)
#print('')
g1.print_board_see()

#g2.add_piece('1',270,(0,0),True)
#g2.add_piece('2',270,(1,1),True)
#g2.add_piece('3',270,(3,2),True)
#g2.add_piece('4',270,(6,6),True)
#g2.add_piece('6',270,(8,10),True)
#print('')
#g2.print_board_see()

#print('')
#g1.print_board_all()


# TEST FULL_EMPTY
#print(g1.empty_space('6',90,(0,0),False))
#g1.add_piece('6',90,(0,0),False)
#g1.print_board_see()
#g1.is_playing = g1.is_playing + 1
#print(g1.is_playing)
##print(g1.empty_space('3',0,(0,0),False))
#print(g1.empty_space('3',90,(1,0),True))
##g1.add_piece('3',0,(0,0),False)
#g1.add_piece('3',90,(1,0),True)
#g1.print_board_see()
#print(g1.empty_space('11',270,(2,1)))
#print(g1.empty_space('11',180,(2,2)))
#g1.add_piece('11',180,(2,2))
#g1.print_board_see()