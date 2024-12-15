import sys
sys.stdout.reconfigure(encoding='utf-8')

class Piece:
    def __init__(self, id:int, shape:list[list[int]]):
        self.id = id
        self.shape = shape

    def rotate(self, rotation:{0, 90, 180, 270}, flipped:bool) -> list[list[int]]:
        """
        returns the shape of the rotated piece
        rotation must be in {0, 90, 180, 270} and represents clockwise inclination 
        flipped is a boolean which corresponds to whether the piece should be flipped horizontally or not
        """
        p = self.shape
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
                    G[len(p[0])-j-1][len(p)-i-1] = p[i][j]
        elif rotation == 180 and flipped:
            G = [[None for i in range(len(p[0]))] for j in range(len(p))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p)-i-1][j] = p[i][j]
        elif rotation == 270 and flipped:
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[j][i] = p[i][j]
        return G

    def afficher(self, rotation:{0, 90, 180, 270} = 0, flipped:bool = False):
        T = self.rotate(rotation, flipped)
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