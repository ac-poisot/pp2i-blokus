import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import PIECES as pies


g1 = Game(2,p_tempo)

g1.print_board_see(1)
print('')
assert g1.on_red('p6',90,(0,0),False)
g1.add_piece('p6',90,(0,0),False)
g1.print_board_see(1)
print('')
assert g1.on_red('p5',0,(2,0),False)