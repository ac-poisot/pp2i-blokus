import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pieces import *

to_test = 12 #piece qui n'a pas de symetrique et qui possede une hauteur differente de sa largeur

def test_possible_rotation():
    rots = possible_rotations(to_test)
    assert sorted(rots) == sorted([[0,False],[0,True],[90,False],[90,True],[180,False],[180,True],[270,False],[270,True]])
        
def test_rotation():
    assert rotate(to_test,0,True) == [[2,3,2,0],
                                         [3,1,3,0],
                                         [3,1,3,2],
                                         [3,1,1,3],
                                         [2,3,1,3],
                                         [0,2,3,2]]
    assert rotate(to_test,90,True) == [[0,0,2,3,3,2],
                                      [2,3,3,1,1,3],
                                      [3,1,1,1,3,2],
                                      [2,3,3,3,2,0]]
    assert rotate(to_test,180,True) == [[2,3,2,0],
                                        [3,1,3,2],
                                        [3,1,1,3],
                                        [2,3,1,3],
                                        [0,3,1,3],
                                        [0,2,3,2]]
    assert rotate(to_test,270,True) == [[0,2,3,3,3,2],
                                        [2,3,1,1,1,3],
                                        [3,1,1,3,3,2],
                                        [2,3,3,2,0,0]]
    assert rotate(to_test,0,False) == [[0,2,3,2],
                                        [0,3,1,3],
                                        [2,3,1,3],
                                        [3,1,1,3],
                                        [3,1,3,2],
                                        [2,3,2,0]]
    assert rotate(to_test,90,False) == [[2,3,3,2,0,0],
                                        [3,1,1,3,3,2],
                                        [2,3,1,1,1,3],
                                        [0,2,3,3,3,2]]
    assert rotate(to_test,180,False) == [[0,2,3,2],
                                         [2,3,1,3],
                                         [3,1,1,3],
                                         [3,1,3,2],
                                         [3,1,3,0],
                                         [2,3,2,0]]
    assert rotate(to_test,270,False) == [[2,3,3,3,2,0],
                                         [3,1,1,1,3,2],
                                         [2,3,3,1,1,3],
                                         [0,0,2,3,3,2]]