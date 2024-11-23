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

g1.print_board_see(1)
print('')
assert g1.on_red('p6',90,(0,0),False)
g1.add_piece('p6',90,(0,0),False)
g1.print_board_see(1)
print('')
assert g1.on_red('p5',0,(2,0),False)