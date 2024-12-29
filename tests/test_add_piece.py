import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game import Game
from pieces import rotate

pieces2 = [
[[2,3,2],[3,1,3],[3,1,3],[2,3,2]],
[[0,2,3,2],[0,3,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]]]


g = Game(2)
poss = [[] for _ in  range(2)]
for j in range(2):
    for p in [2,6]:
        for r in [0,90,180,270] :
            for b in [True,False]:
                new_piece = rotate(p,r,b)
                x_min = 0
                x_max = len(new_piece[0])-1
                y_min = 0
                y_max = len(new_piece)-1
                if new_piece[y_min][x_min] == 2 : 
                    poss[j].append((p,r,b,(0,0)))
                if new_piece[y_max][x_min] == 2 : 
                   poss[j].append((p,r,b,(21-y_max,0)))
                if new_piece[y_min][x_max] == 2 : 
                   poss[j].append((p,r,b,(0,21-x_max)))
                if new_piece[y_max][x_max] == 2 : 
                   poss[j].append((p,r,b,(21-y_max,21-x_max)))
g.availible = [[2,6] for j in range(2)]
g.bonus = [False for _ in range(2)]
g.possible_moves = poss
g.red_pieces = [4 for _ in range(2)]

def test_add_on_board():
    g = Game(2)
    g.availible = [[2,6] for j in range(2)]
    g.bonus = [False for _ in range(2)]
    g.possible_moves = poss.copy()
    g.red_pieces = [4 for _ in range(2)]
    g.add_piece(6,90,(0,0),False) # faire attention a rester dans {1,2,4,6}
    g.print_board() # attention si on veut voir le tableau à le mettre hors de la fonction (rappel donc plante car availible a change)

def test_remove_availible():
    g = Game(2)
    g.availible = [[2,6] for j in range(2)]
    g.bonus = [False for _ in range(2)]
    g.possible_moves = poss.copy()
    g.red_pieces = [4 for _ in range(2)]
    g.add_piece(6,90,(0,0),False)
    assert g.availible[0] == [2]

def test_possible_moves():
    g = Game(2)
    g.availible = [[2,6] for j in range(2)]
    g.bonus = [False for _ in range(2)]
    g.possible_moves = poss.copy()
    print(g.possible_moves[1])
    g.red_pieces = [4 for _ in range(2)]
    g.add_piece(6,90,(0,0),False)
    assert g.possible_moves[0] == [(2, 0, True, (18, 0)), (2, 0, True, (0, 19)), (2, 0, True, (18, 19)), (2, 0, False, (18, 0)), (2, 0, False, (0, 19)), (2, 0, False, (18, 19)), (2, 90, True, (19, 0)), (2, 90, True, (0, 18)), (2, 90, True, (19, 18)), (2, 90, False, (19, 0)), (2, 90, False, (0, 18)), (2, 90, False, (19, 18)), (2, 180, True, (18, 0)), (2, 180, True, (0, 19)), (2, 180, True, (18, 19)), (2, 180, False, (18, 0)), (2, 180, False, (0, 19)), (2, 180, False, (18, 19)), (2, 270, True, (19, 0)), (2, 270, True, (0, 18)), (2, 270, True, (19, 18)), (2, 270, False, (19, 0)), (2, 270, False, (0, 18)), (2, 270, False, (19, 18)), (2, 90, True, (3, 0)), (2, 90, False, (3, 0)), (2, 270, True, (3, 0)), (2, 270, False, (3, 0)), (2, 0, True, (3, 2)), (2, 0, False, (3, 2)), (2, 90, True, (3, 2)), (2, 90, False, (3, 2)), (2, 180, True, (3, 2)), (2, 180, False, (3, 2)), (2, 270, True, (3, 2)), (2, 270, False, (3, 2))]
    assert g.possible_moves[1] == [(2, 0, True, (18, 0)), (2, 0, True, (0, 19)), (2, 0, True, (18, 19)), (2, 0, False, (18, 0)), (2, 0, False, (0, 19)), (2, 0, False, (18, 19)), (2, 90, True, (19, 0)), (2, 90, True, (0, 18)), (2, 90, True, (19, 18)), (2, 90, False, (19, 0)), (2, 90, False, (0, 18)), (2, 90, False, (19, 18)), (2, 180, True, (18, 0)), (2, 180, True, (0, 19)), (2, 180, True, (18, 19)), (2, 180, False, (18, 0)), (2, 180, False, (0, 19)), (2, 180, False, (18, 19)), (2, 270, True, (19, 0)), (2, 270, True, (0, 18)), (2, 270, True, (19, 18)), (2, 270, False, (19, 0)), (2, 270, False, (0, 18)), (2, 270, False, (19, 18)), (6, 0, True, (17, 0)), (6, 0, True, (17, 18)), (6, 0, False, (17, 0)), (6, 0, False, (0, 18)), (6, 0, False, (17, 18)), (6, 90, True, (18, 0)), (6, 90, True, (0, 17)), (6, 90, True, (18, 17)), (6, 90, False, (18, 0)), (6, 90, False, (18, 17)), (6, 180, True, (0, 18)), (6, 180, True, (17, 18)), (6, 180, False, (17, 0)), (6, 180, False, (0, 18)), (6, 270, True, (18, 0)), (6, 270, True, (0, 17)), (6, 270, False, (0, 17)), (6, 270, False, (18, 17))]
