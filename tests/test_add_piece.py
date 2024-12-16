import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

g1 = Game([1, 2])
g2 = Game([1, 2])
g3 = Game([1, 2, 3])

g1.print_board_see(1)
print('')
g1.add_piece(1, 0, (0, 0), False, 1)
g1.add_piece(2, 0, (1, 1), False, 2)
g1.add_piece(3, 0, (3, 2), False, 1)
g1.add_piece(4, 0, (6, 6), False, 2)
g1.add_piece(6, 0, (8, 10), False, 1)
g1.print_board_see(1)
print('')

g2.add_piece(1, 270, (0, 0), True, 1)
g2.add_piece(2, 270, (1, 1), True, 2)
g2.add_piece(3, 270, (3, 2), True, 1)
g2.add_piece(4, 270, (6, 6), True, 2)
g2.add_piece(13, 270, (8, 10), True, 1)

g2.print_board_see(1)
print('')
g2.print_board_see(2)
print('')

g3.add_piece(20, 0, (0, 0), False, 1)
g3.add_piece(20, 90, (0, 5), False, 2)
g3.add_piece(20, 180, (0, 10), False, 3)
g3.add_piece(19, 270, (0, 15), False, 1)
g3.add_piece(19, 0, (7, 0), True, 2)
g3.add_piece(15, 90, (7, 5), True, 3)
g3.add_piece(13, 180, (7, 10), True, 1)
g3.add_piece(11, 270, (7, 15), True, 2)
g3.print_board_see(2)
print('')
g3.print_board_see(1)
