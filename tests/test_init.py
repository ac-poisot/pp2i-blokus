import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

gs = [Game([1, 2]), Game([1, 2, 3]), Game([2, 4])]

gs[0].print_board_all(1)

for g in gs:
    print(g.players)
    print(g.is_playing)
    print(g.maxn)

