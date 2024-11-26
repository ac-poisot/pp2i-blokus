import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import PIECES as pies

g1 = Game(2)
print(0)
pies.afficher(pies.get(13),0,False)
print(90)
pies.afficher(pies.get(13),90,False)
print(180)
pies.afficher(pies.get(13),180,False)
print(270)
pies.afficher(pies.get(13),270,False)
print(0)
pies.afficher(pies.get(13),0,True)
print(90)
pies.afficher(pies.get(13),90,True)
print(180)
pies.afficher(pies.get(13),180,True)
print(270)
pies.afficher(pies.get(13),270,True)