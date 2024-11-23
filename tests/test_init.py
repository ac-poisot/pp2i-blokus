from game import *

# importation des pieces et def du dictionnaire
p_tempo = {}

for i in range(1, 22):
    #print(i)
    var_name = f"p{i}"
    value = globals().get(var_name)
    p_tempo[var_name] = value
    #afficher(value)

# TEST __INIT__
#print(p_tempo['1'])
g1 = Game(2,p_tempo)
#print(g1.pieces)
g2 = Game(2,p_tempo)
g3 = Game(3,p_tempo)
#print(g1.is_playing)
#plateau = g1.board
#p = g1.players
#print(plateau)
#print(p)