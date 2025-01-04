import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pieces import *

to_test = 2

rots = possible_rotations(to_test)
for a in rots:
    print(a)

for flipped in [True, False]:
    for rot in [0, 90, 180, 270]:
        print(rot, flipped)
        display(to_test, rot, flipped)
