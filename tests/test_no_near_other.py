# OBSOLETE: all 3 check functions have been merged into is_legal

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

g1 = Game([1, 2])

assert g1.no_near_other(6, 90, (0, 0), False, 1)
g1.add_piece(6, 90, (0, 0), False)
g1.print_board_see(1)
print('')
g1.add_piece(5, 0, (2, 0), False)
g1.print_board_see(1)
assert not(g1.no_near_other(5, 0, (2, 0), False, 1))