import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import PIECES as pies


g1 = Game(2,p_tempo)

assert g1.no_near_other('p6',90,(0,0),False)
g1.add_piece('p6',90,(0,0),False)
g1.print_board_see(1)
print('')
g1.add_piece('p5',0,(2,0),False)
g1.print_board_see(1)
assert g1.no_near_other('p5',0,(2,0),False)