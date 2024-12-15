import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from piece import Piece
from pieces import pieces2

to_test = 19

for flipped in [True, False]:
    for rot in [0, 90, 180, 270]:
        print(rot, flipped)
        Piece.afficher(pieces2[to_test], rot, flipped)
