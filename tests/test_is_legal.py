import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

g1 = Game([1, 2])

assert g1.is_legal(1, 90, (19, 19), False, 1)
g1.add_piece(6, 90, (0, 0), False, 1)
g1.print_board_see(1)
print('')
assert(g1.can_play(1))
assert (g1.is_legal(18, 180, (1, 3), True, 1))
assert not(g1.is_legal(5, 0, (2, 0), False, 1))
assert not(g1.is_legal(6, 0, (2, 0), False, 1))
assert not(g1.is_legal(2, 0, (0, 22), False, 1))