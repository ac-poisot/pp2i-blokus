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
#g2 = Game(2,p_tempo)
#print(g1.is_playing)
#plateau = g1.board
#p = g1.players
#print(plateau)
#print(p)


# TEST ROTATE
afficher(g1.rotate('p20',0,False))
afficher(g1.rotate('p20',90,False))
afficher(g1.rotate('p20',180,False))
afficher(g1.rotate('p20',270,False))
afficher(g1.rotate('p20',0,True))
afficher(g1.rotate('p20',90,True))
afficher(g1.rotate('p20',180,True))
afficher(g1.rotate('p20',270,True))

# TEST ADD_PIECE ET PRINT_BOARD
#g1.print_board_all()
#print('')
#g1.print_board_see()
#print(g1.is_playing)
#g1.add_piece('1',0,(0,0),False)
#g1.add_piece('2',0,(1,1),False)
#g1.add_piece('3',0,(3,2),False)
#g1.add_piece('4',0,(6,6),False)
#g1.add_piece('6',0,(8,10),False)
#print('')
#g1.print_board_see()

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
#print(g1.empty_space('3',0,(0,0),False))
#print(g1.empty_space('3',90,(1,0),True))
##g1.add_piece('3',0,(0,0),False)
#g1.add_piece('3',90,(1,0),True)
#g1.print_board_see()
#print(g1.empty_space('11',270,(2,1)))
#print(g1.empty_space('11',180,(2,2)))
#g1.add_piece('11',180,(2,2))
#g1.print_board_see()