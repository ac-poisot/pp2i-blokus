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
g2 = Game(2,p_tempo)
g3 = Game(3,p_tempo)



g1.print_board_see(1)
g1.add_piece('p1',0,(0,0),False)
g1.add_piece('p2',0,(1,1),False)
g1.add_piece('p3',0,(3,2),False)
g1.add_piece('p4',0,(6,6),False)
g1.add_piece('p6',0,(8,10),False)
print('')
g1.print_board_see(1)
g2.add_piece('p1',270,(0,0),True)
g2.add_piece('p2',270,(1,1),True)
g2.add_piece('p3',270,(3,2),True)
g2.add_piece('p4',270,(6,6),True)
g2.add_piece('p13',270,(8,10),True)
print('')
g2.print_board_see(1)
print('')
g2.print_board_see(2)
print('')
g3.add_piece('p20',0,(0,0),False)
g3.add_piece('p20',90,(0,5),False)
g3.add_piece('p20',180,(0,10),False)
g3.add_piece('p20',270,(0,15),False)
g3.add_piece('p20',0,(7,0),True)
g3.add_piece('p20',90,(7,5),True)
g3.add_piece('p20',180,(7,10),True)
g3.add_piece('p20',270,(7,15),True)

g3.print_board_see(2)
print('')
g3.print_board_see(1)