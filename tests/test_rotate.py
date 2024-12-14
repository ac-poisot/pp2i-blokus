import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from piece import Piece as pies
from pieces import pieces

g1 = Game(2)
print(0)
pies.afficher(pieces[14],0,False)
print(90)
pies.afficher(pieces[14],90,False)
print(180)
pies.afficher(pieces[14],180,False)
print(270)
pies.afficher(pieces[14],270,False)
print(0)
pies.afficher(pieces[14],0,True)
print(90)
pies.afficher(pieces[14],90,True)
print(180)
pies.afficher(pieces[14],180,True)
print(270)
pies.afficher(pieces[14],270,True)