pieces = [[[2,3,2],[3,1,3],[2,3,2]],
[[2,3,2],[3,1,3],[3,1,3],[2,3,2]],
[[2,3,2],[3,1,3],[3,1,3],[3,1,3],[2,3,2]],
[[2,3,2,0],[3,1,3,2],[3,1,1,3],[2,3,3,2]],
[[2,3,2],[3,1,3],[3,1,3],[3,1,3],[3,1,3],[2,3,2]],
[[0,2,3,2],[0,3,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]],
[[2,3,2,0],[3,1,3,2],[3,1,1,3],[3,1,3,2],[2,3,2,0]],
[[2,3,3,2],[3,1,1,3],[3,1,1,3],[2,3,3,2]],
[[2,3,3,2,0],[3,1,1,3,2],[2,3,1,1,3],[0,2,3,3,2]],
[[2,3,2],[3,1,3],[3,1,3],[3,1,3],[3,1,3],[3,1,3],[2,3,2]],
[[0,2,3,2],[0,3,1,3],[0,3,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]],
[[0,2,3,2],[0,3,1,3],[2,3,1,3],[3,1,1,3],[3,1,3,2],[2,3,2,0]],
[[0,2,3,2],[2,3,1,3],[3,1,1,3],[3,1,1,3],[2,3,3,2]],
[[2,3,3,2],[3,1,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]],
[[2,3,2,0],[3,1,3,2],[3,1,1,3],[3,1,3,2],[3,1,3,0],[2,3,2,0]],
[[0,2,3,2,0],[0,3,1,3,0],[2,3,1,3,2],[3,1,1,1,3],[2,3,3,3,2]],
[[2,3,2,0,0],[3,1,3,0,0],[3,1,3,3,2],[3,1,1,1,3],[2,3,3,3,2]],
[[2,3,3,2,0],[3,1,1,3,2],[2,3,1,1,3],[0,2,3,1,3],[0,0,2,3,2]],
[[2,3,2,0,0],[3,1,3,3,2],[3,1,1,1,3],[2,3,3,1,3],[0,0,2,3,2]],
[[2,3,2,0,0],[3,1,3,3,2],[3,1,1,1,3],[2,3,1,3,2],[0,2,3,2,0]],
[[0,2,3,2,0],[2,3,1,3,2],[3,1,1,1,3],[2,3,1,3,2],[0,2,3,2,0]]]

def rotate(piece:int, rotation:{0, 90, 180, 270}, flipped:bool) -> list[list[int]]:
    """
    returns the shape of the rotated piece
    rotation must be in {0, 90, 180, 270} and represents clockwise inclination 
    flipped is a boolean which corresponds to whether the piece should be flipped horizontally or not
    """
    p = pieces[piece - 1]
    if rotation == 0 and not(flipped):
        G = p
    elif rotation == 90 and not(flipped):
        G = [[None for i in range(len(p))] for j in range(len(p[0]))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[j][len(p)-1-i] = p[i][j]
    elif rotation == 180 and not(flipped):
        G = [[None for i in range(len(p[0]))] for j in range(len(p))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[len(p)-i-1][len(p[0])-j-1] = p[i][j]
    elif rotation == 270 and not(flipped):
        G = [[None for i in range(len(p))] for j in range(len(p[0]))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[len(p[0])-j-1][i] = p[i][j]
    elif rotation == 0 and flipped: 
        G = [[None for i in range(len(p[0]))] for j in range(len(p))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[i][len(p[0])-j-1] = p[i][j]
    elif rotation == 90 and flipped:
        G = [[None for i in range(len(p))] for j in range(len(p[0]))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[j][i] = p[i][j]
    elif rotation == 180 and flipped:
        G = [[None for i in range(len(p[0]))] for j in range(len(p))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[len(p)-i-1][j] = p[i][j]
    elif rotation == 270 and flipped:
        G = [[None for i in range(len(p))] for j in range(len(p[0]))]
        for i in range(len(p)):
            for j in range(len(p[0])):
                G[len(p[0])-j-1][len(p)-i-1] = p[i][j]
    return G

def display(piece:int, rotation:{0, 90, 180, 270} = 0, flipped:bool = False):
        T = rotate(piece, rotation, flipped)
        if not T:
            return ""
        l, n = len(T), len(T[1])
        for i in range(l):
            for j in range(n):
                if T[i][j] == 2:
                    print("🟥", end = "")
                elif T[i][j] == 1:
                    print("⬛", end = "")
                elif T[i][j] == 3:
                    print("🟩", end = "")
                else:
                    print("⬜", end = "")
            print()
        print("\n")

def possible_rotations(piece:int) -> list[list[list[int]]]:
    T = pieces[piece - 1]
    res = [[0, False]]
    tested = [T]
    for rot in [0, 90, 180, 270]:
        for flipped in [True, False]:
            p = rotate(piece, rot, flipped)
            if p not in tested:
                tested.append(p)
                res.append([rot, flipped])

    return res

pieces_rotations = [possible_rotations(i) for i in range(len(pieces))]
