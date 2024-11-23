from game import *

# importation des pieces et def du dictionnaire
p_tempo = {}

for i in range(1, 22):
    #print(i)
    var_name = f"p{i}"
    value = globals().get(var_name)
    p_tempo[var_name] = value
    #afficher(value)

g1 = Game(2,p_tempo)

# TEST EMPTY_SPACE
print(g1.empty_space('p6',90,(0,0),False))
g1.add_piece('p6',90,(0,0),False)
g1.print_board_see(1)
g1.is_playing = g1.is_playing + 1
print(g1.is_playing)
print(g1.empty_space('p3',0,(0,0),False))
print(g1.empty_space('p3',90,(1,0),True))
#g1.add_piece('p3',0,(0,0),False)
#g1.add_piece('p3',90,(1,0),True)
#g1.print_board_see(1)
print(g1.empty_space('p11',270,(2,1),True))
print(g1.empty_space('p11',180,(2,2),True))
g1.add_piece('p11',180,(2,2),True)
g1.print_board_see(2)