# game.py, pour le jeu
from pieces import PIECES as pies

class Game:
    def __init__(self,nb_players):
        game_board = [[['N' for i in range(nb_players)] for i in range(22)] for j in range(22)]
        used= [[],[],[],[]]
        game_board[0][0] = ['P'for i in range(nb_players)] # Ca devrait pas être ['P','I','I','I'] ?
        game_board[21][0] = ['P'for i in range(nb_players)]
        game_board[0][21] = ['P'for i in range(nb_players)]
        game_board[21][21] = ['P'for i in range(nb_players)]
        if nb_players >= 2:#Faire pour tout les possibilitées
            game_board[1][1][0] = 'A'
            game_board[20][20][1] = 'A'
        if nb_players >= 3:
            game_board[1][20][2] = 'A'
        if nb_players == 4:
            game_board[20][1][3] = 'A'
        red_pieces = [[(1,1)],[(20,20)],[(1,20)],[(20,1)]] #pour stocker les pieces 'accessibles', utile fin partie
        players = [i for i in range(1,nb_players+1)]
        self.players = players
        self.used = used
        self.board = game_board
        self.red_pieces = red_pieces
        self.is_playing = 1
        self.nb_players = nb_players

    def print_board_all(self,id_players): 
        """affiche le  plateau et les bords virtuels, fonction de debugg, peut-etre utile pour front-end"""
        for i in range(22): #pour chaque ligne
            line = '|'
            for j in range(22):
                line = line + str(self.board[i][j][id_players-1]) + '|'
            print(line)

    def print_board_see(self,joueur): 
        """affiche le  plateau vu par le joueur passe en parametre, fonction de debugg, peut-etre utile pour front-end"""
        for i in range(1,21): #pour chaque ligne
            line = '|'
            for j in range(1,21):
                line = line + str(self.board[i][j][joueur-1]) + '|'
            print(line)

    def add_piece(self,piece : int,rotation : {0,90,180,270},position : tuple[int,int],retourne : bool): #Modifié
        """rajoute une piece sur le plateau sans aucune verification
            la piece vient normalement du dictionnaire global qui n'est pas def ici
            ATTENTION : piece est donc un int !
            position est un tuple (x,y)
            
            a faire : ajout case rouge, suppression case rouge utilisee
        """
        x,y = position
        piece_ajoutable =  self.rotatePieces(piece,rotation,retourne)
        n = len(piece_ajoutable)
        l = len(piece_ajoutable[0])
        for i in range(n):
            for j in range(l):
                if piece_ajoutable[i][j] == 1:#On ajoute la piece
                    if "A" in self.board[i+x][j+y]:#On enlève les pièces rouges
                        if (i+x,j+y) in self.red_pieces[0]:
                            self.red_pieces[0].remove((i+x,j+y))
                        elif(i+x,j+y) in self.red_pieces[1]:
                            self.red_pieces[1].remove((i+x,j+y))
                        elif(i+x,j+y) in self.red_pieces[2]:
                            self.red_pieces[2].remove((i+x,j+y))
                        elif(i+x,j+y) in self.red_pieces[3]:
                            self.red_pieces[3].remove((i+x,j+y))
                    self.board[i+x][j+y] = ['I' for i in range(self.nb_players)]
                    self.board[i+x][j+y][self.is_playing -1] = 'P'
                elif piece_ajoutable[i][j] == 2 and self.board[i+x][j+y][self.is_playing] in ['A','N']:
                    self.red_pieces[self.is_playing-1].append((i+x,j+y))
                    self.board[i+x][j+y][self.is_playing-1] = 'A'

    def empty_space(self,piece,rotation,position,retourne): 
        """
            fonction qui verifie qu'on pose une piece sur une case accessible, donc pas Prise par le joueur ou Inacessible
        """
        x = position[0]
        y = position[1]
        p_act = self.rotatePieces(piece,rotation,retourne)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                # cas sur une piece non vide ou inaccessible
                if p_act[i][j] == 1 and (self.board[x+i][y+j][self.is_playing-1] == 'I' or self.board[x+i][y+j][self.is_playing-1] == 'P'):
                    return False
        return True
    
    def no_near_other(self,piece,rotation,position,retourne):
        """verifie que la piece n'est pas tangente a une piece de la meme couleur"""

        x = position[0]
        y = position[1]
        p_act = self.rotatePieces(piece,rotation,retourne)
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                if p_act[i][j] == 3 and self.board[x+i][y+j][self.is_playing-1] == 'P':
                    return False
        return True

    def on_red(self,piece,rotation,position,retourne):
        """ fonction qui verifie que la piece est bien place sur une case rouge"""
        x = position[0]
        y = position[1]
        p_act = self.rotatePieces(piece,rotation,retourne)
        red_piece = self.red_pieces[self.is_playing-1]
        for i in range(len(p_act)):
            for j in range(len(p_act[0])):
                if p_act[i][j]== 2 and self.board[x+i][y+j][self.is_playing-1] == 'P':
                    #self.red_pieces[self.is_playing - 1].remove((x+i,y+j)) #Permet de garder à jour red_piece
                    return True
        return False

    def is_legal(self,piece,rotation,position,retourne):
        """verifie si un coup est legal en trois etapes:
            - un coin de la piece est dans une case rouge
            - la piece est entierement dans une zone vide
            - la piece ne touche pas le bord d'une piece de la meme couleur
            
            renvoie True ssi on peut poser la piece à cet endroit"""
        # la piece est dans le plateau
        p_act = self.rotatePieces(piece,rotation,retourne)
        if position[0]+len(p_act[0])>21 or position[1]+len(p_act)>21 or position[0]<0 or position[1]<0:
            return False
        #coin sur une case rouge
        corner_on_red = self.on_red(piece,rotation,position,retourne)
        # la piece est entierement sur une case vide
        free = self.empty_space(piece,rotation,position,retourne)
        #la piece n'est pas tangente a une case de la meme couleur
        not_tangent = self.no_near_other(piece,rotation,position,retourne)

        return corner_on_red and free and not_tangent
    
    def possible_moves(self):
        """renvoie la liste des coups possibles pour le joueur actuel"""
        rotation = [0,90,180,270]
        retourne = [True,False]

        res = []

        #recupuere les pieces restantes
        not_used = []
        for i in range(1,22):
            key = 'p'+str(i)
            if not(key in self.used[self.is_playing-1]) :
                not_used.append(key)
        
        # on parcourt la liste des cases accessibles en verifiant pour chaque rotation que la piece est posable, en remarquant les differentes positions possibles
        for p in not_used:
            for c in self.red_pieces[self.is_playing-1]:
                for r in rotation:
                    for b in retourne:
                        # les quatre cas
                        p_act = self.rotatePieces(p,r,b)
                        xmin = c[0]-len(p_act[0])
                        xmax = c[0]
                        ymin = c[1]-len(p_act)
                        ymax = c[1]
                        for x in range(xmin,xmax+1):
                            for y in range(ymin,ymax+1):
                                if self.is_legal(p,r,(x,y),b):
                                    res.append((p,r,(x,y),b))
        
        return res
    
    def delete_player(self):
        """retire un joueur qui ne peut plus jouer"""
        if len(self.possible_moves())==0:
            t = len(self.players)
            i = 0
            while i<t and self.players[i] != self.is_playing:
                i=i+1
            self.players.pop(i)

    def endgame(self):
        """renvoie True ssi la partie est finie"""
        if self.players == []:
            return True
        else:
            return False
        
    def play_game(self):
        while not(self.endgame()):
            self.print_board_see(self.is_playing)
            print('')
            if self.possible_moves() != []:
                print("joueur "+ str(self.is_playing-1)+ " poser une piece:")
                piece = input("poser piece  num? ")
                retourne = bool(input("piece retourne ? (appuyer directement sur Entree si non)"))
                rotation = int(input("inclinaison ? "))
                y = int(input("abscisse ? "))
                x = int(input("ordonnee ? "))
                if self.is_legal(piece,rotation,(x,y),retourne):
                    self.add_piece(piece,rotation,(x,y),retourne)

                else:
                    print("pas possible de poser piece, rip")
                self.print_board_see(self.is_playing-1)
                print('')
                t = len(self.players)
                self.is_playing = self.is_playing + 1
                if self.is_playing > t:
                    self.is_playing = 1
            else:
                self.delete_player()

    def rotatePieces(self,id_piece,rotation,retourne): #check
        """Doit prendre un int, un angle et un bool pour retourner la pièces dans le bond sens"""
        return pies.rotate(pies.get(id_piece),rotation,retourne)

if __name__ == "__init__":
    g1 = Game(2)
    g1.add_piece(1,0,(5,5),False)
    g1.print_board_see(2)
    print(g1.board[6][6])
    print(g1.red_pieces)