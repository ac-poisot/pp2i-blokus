import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game

def test_begining():
    g = Game(2)
    assert g.score(1) == -89

def test_end():
    g = Game(2)
    g.available[1] = []
    g.bonus[1] = True
    g.available[0] = []
    assert g.score(2) == 25
    assert g.score(1) == 20

def test_mid():
    g = Game(2)
    g.available[0] = [1,2,3,5,9]
    assert g.score(1) == -14