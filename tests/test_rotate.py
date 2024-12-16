import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pieces import afficher

to_test = 19

for flipped in [True, False]:
    for rot in [0, 90, 180, 270]:
        print(rot, flipped)
        afficher(to_test, rot, flipped)
