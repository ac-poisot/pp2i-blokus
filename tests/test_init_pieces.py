import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pieces import *


def init_moves(p:int) -> list[tuple[int, int, bool, tuple[int, int]]]:
    moves = []
    for r in [0, 90, 180, 270]:
            for b in [True, False]:
                new_piece = rotate(p, r, b)
                x_min = 0
                x_max = len(new_piece[0])
                y_min = 0
                y_max = len(new_piece)
                if new_piece[y_min][x_min] == 2: 
                    moves.append((p, r, b, (0, 0)))
                if new_piece[y_max-1][x_min] == 2: 
                    moves.append((p, r, b, (0, 21 - y_max + 1)))
                if new_piece[y_min][x_max-1] == 2: 
                    moves.append((p, r, b, (21 - x_max + 1, 0)))
                if new_piece[y_max-1][x_max-1] == 2: 
                    moves.append((p, r, b, (21 - x_max + 1, 21 - y_max + 1)))
    return moves

def test_p21():
    assert init_moves(21) == []

def test_p1():
    assert init_moves(1) == [(1,0,True,(0,0)),(1,0,True,(0,19)),(1,0,True,(19,0)),(1,0,True,(19,19)),(1,0,False,(0,0)),(1,0,False,(0,19)),(1,0,False,(19,0)),(1,0,False,(19,19)),
                              (1,90,True,(0,0)),(1,90,True,(0,19)),(1,90,True,(19,0)),(1,90,True,(19,19)),(1,90,False,(0,0)),(1,90,False,(0,19)),(1,90,False,(19,0)),(1,90,False,(19,19)),
                              (1,180,True,(0,0)),(1,180,True,(0,19)),(1,180,True,(19,0)),(1,180,True,(19,19)),(1,180,False,(0,0)),(1,180,False,(0,19)),(1,180,False,(19,0)),(1,180,False,(19,19)),
                              (1,270,True,(0,0)),(1,270,True,(0,19)),(1,270,True,(19,0)),(1,270,True,(19,19)),(1,270,False,(0,0)),(1,270,False,(0,19)),(1,270,False,(19,0)),(1,270,False,(19,19))]
     
def test_p6():
    assert init_moves(6) == [(6,0,True,(0,0)),(6,0,True,(0,17)),(6,0,True,(18,17)),(6,0,False,(0,17)),(6,0,False,(18,0)),(6,0,False,(18,17)),
                            (6,90,True,(0,18)),(6,90,True,(17,0)),(6,90,True,(17,18)),(6,90,False,(0,0)),(6,90,False,(0,18)),(6,90,False,(17,18)),
                            (6,180,True,(0,0)),(6,180,True,(18,0)),(6,180,True,(18,17)),(6,180,False,(0,0)),(6,180,False,(0,17)),(6,180,False,(18,0)),
                            (6,270,True,(0,0)),(6,270,True,(0,18)),(6,270,True,(17,0)),(6,270,False,(0,0)),(6,270,False,(17,0)),(6,270,False,(17,18))]