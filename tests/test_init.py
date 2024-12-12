import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

# TEST __INIT__
#print['1'])
g1 = Game(2)
#print(g1.pieces)
g2 = Game(2)
g3 = Game(3)
#print(g1.is_playing)
#plateau = g1.board
#p = g1.players
#print(plateau)
#print(p)
g1.print_board_all()