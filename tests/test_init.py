import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game


def test_maxn():
    g1 = Game(2)
    assert g1.maxn == 2

def test_possible_moves():
    g1 = Game(2)
    # le calcul correspond au nombre de coups possibles au tout début du jeu
    # voir test_init_test pour de un test plus complet
    assert len(g1.possible_moves[0]) == 4 * (8 * 7 + 6 * 5 + 4 * 7 + 2)