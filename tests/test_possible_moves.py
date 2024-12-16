import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

g1 = Game([1, 2])

g1.availible[0] = [20]
g1.red_pieces[0] = [(10,10)]
g1.board[10][10][0] = 'P'
print(g1.possible_moves(1))