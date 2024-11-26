import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import PIECES as pies


g1 = Game(2,p_tempo)

# TEST EMPTY_SPACE
print(g1.empty_space('p6',90,(0,0),False))
g1.add_piece('p6',90,(0,0),False)
g1.print_board_see(1)
g1.is_playing = g1.is_playing + 1
print(g1.is_playing)
print(g1.empty_space('p3',0,(0,0),False))
print(g1.empty_space('p3',90,(1,0),True))
#g1.add_piece('p3',0,(0,0),False)
#g1.add_piece('p3',90,(1,0),True)
#g1.print_board_see(1)
print(g1.empty_space('p11',270,(2,1),True))
print(g1.empty_space('p11',180,(2,2),True))
g1.add_piece('p11',180,(2,2),True)
g1.print_board_see(2)