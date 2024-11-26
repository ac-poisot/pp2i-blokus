import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import PIECES as pies


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
g1.print_board_all()