import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import PIECES as pies


g1 = Game(2)

g1.print_board_see(1)
print('')
assert g1.on_red(6,90,(0,0),False)
g1.add_piece(6,90,(0,0),False)
g1.print_board_see(1)
print('')
assert g1.on_red(5,0,(2,0),False)