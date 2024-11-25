import sys
sys.stdout.reconfigure(encoding='utf-8')


class PIECES:
    def __init__(self,id,tableaux):
        self.id = id
        self.form = tableaux
    def rotate(self,rotation,retourne):
        """retourne la piece et la renvoie
            rotation est dans {0,90,180,270} en sens horaire
            retourne est un bool qui vaut True si la piece est retournee (sens horizontal pour piece)"""
        p = self.form
        if rotation==0 and not(retourne):
            G = p  
        if rotation==90 and not(retourne):
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[j][len(p)-1-i] = p[i][j]
        if rotation==180 and not(retourne): # 
            G = [[None for i in range(len(p[0]))] for j in range(len(p))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p)-i-1][len(p[0])-j-1] = p[i][j]
        if rotation==270 and not(retourne):
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p[0])-j-1][i] = p[i][j]
        if rotation==0 and retourne: 
            G = [[None for i in range(len(p[0]))] for j in range(len(p))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p)-i-1][j] = p[i][j]
        if rotation==90 and retourne:
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[j][i] = p[i][j]
        if rotation==180 and retourne:
            G = [[None for i in range(len(p[0]))] for j in range(len(p))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[i][len(p[0])-j-1] = p[i][j]
        if rotation==270 and retourne:###
            G = [[None for i in range(len(p))] for j in range(len(p[0]))]
            for i in range(len(p)):
                for j in range(len(p[0])):
                    G[len(p[0])-j-1][len(p)-i-1] = p[i][j]
        return G

    def afficher(self):
        T = self.form
        if T == []:
            return ""
        l,n = len(T),len(T[1])
        for i in range(l):
            for j in range(n):
                if T[i][j] == 2:
                    print("🟥",end = "")
                elif T[i][j] == 1:
                    print("⬛", end = "")
                elif T[i][j] == 3:
                    print("🟩",end = "")
                else:
                    print("⬜", end = "")
            print("\n")
        print("\n")




p1 = PIECES(1,[[2,3,2],[3,1,3],[2,3,2]])
p2 = PIECES(2,[[2,3,2],[3,1,3],[3,1,3],[2,3,2]])
p3 = PIECES(3,[[2,3,2],[3,1,3],[3,1,3],[3,1,3],[2,3,2]])
p4 = PIECES(4,[[2,3,2,0],[3,1,3,2],[3,1,1,3],[2,3,3,2]])
p5 = PIECES(5,[[2,3,2],[3,1,3],[3,1,3],[3,1,3],[3,1,3],[2,3,2]])
p6 = PIECES(6,[[0,2,3,2],[0,3,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]])
p7 = PIECES(7,[[2,3,2,0],[3,1,3,2],[3,1,1,3],[3,1,3,2],[2,3,2,0]])
p8 = PIECES(8,[[2,3,3,2],[3,1,1,3],[3,1,1,3],[2,3,3,2]])
p9 = PIECES(9,[[2,3,3,2,0],[3,1,1,3,2],[2,3,1,1,3],[0,2,3,3,2]])
p10 = PIECES(10,[[2,3,2],[3,1,3],[3,1,3],[3,1,3],[3,1,3],[3,1,3],[2,3,2]])
p11 = PIECES(11,[[0,2,3,2],[0,3,1,3],[0,3,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]])
p12 = PIECES(12,[[0,2,3,2],[0,3,1,3],[2,3,1,3],[3,1,1,3],[3,1,3,2],[2,3,2,0]])
p13 = PIECES(13,[[0,2,3,2],[2,3,1,3],[3,1,1,3],[3,1,1,3],[2,3,3,2]])
p14 = PIECES(14,[[2,3,3,2],[3,1,1,3],[2,3,1,3],[3,1,1,3],[2,3,3,2]])
p15 = PIECES(15,[[2,3,2,0],[3,1,3,2],[3,1,1,3],[3,1,3,2],[3,1,3,0],[2,3,2,0]])
p16 = PIECES(16,[[0,2,3,2,0],[0,3,1,3,0],[2,3,1,3,2],[3,1,1,1,3],[2,3,3,3,2]])
p17 = PIECES(17,[[2,3,2,0,0],[3,1,3,0,0],[3,1,3,3,2],[3,1,1,1,3],[2,3,3,3,2]])
p18 = PIECES(18,[[2,3,3,2,0],[3,1,1,3,2],[2,3,1,1,3],[0,2,3,1,3],[0,0,2,3,2]])
p19 = PIECES(19,[[2,3,2,0,0],[3,1,3,3,2],[3,1,1,1,3],[2,3,3,1,3],[0,0,2,3,2]])
p20 = PIECES(20,[[2,3,2,0,0],[3,1,3,3,2],[3,1,1,1,3],[2,3,1,3,2],[0,2,3,2,0]])
p21 = PIECES(21,[[0,2,3,2,0],[2,3,1,3,2],[3,1,1,1,3],[2,3,1,3,2],[0,2,3,2,0]])


