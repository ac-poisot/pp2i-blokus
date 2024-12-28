import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game_refact import Game


def test_maxn():
    g1 = Game(2)
    assert g1.maxn == 2

def test_possible_moves():
    g1 = Game(2)
    # la calcul correspond au nombre de possibilites des positions.
    assert len(g1.possible_moves[0]) == 4*(8*7+6*5+4*7+2)