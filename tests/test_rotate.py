from game import *

# importation des pieces et def du dictionnaire
p_tempo = {}

for i in range(1, 22):
    #print(i)
    var_name = f"p{i}"
    value = globals().get(var_name)
    p_tempo[var_name] = value
    #afficher(value)

g1 = Game(2,p_tempo)


print(0)
afficher(g1.rotate('p13',0,False))
print(90)
afficher(g1.rotate('p13',90,False))
print(180)
afficher(g1.rotate('p13',180,False))
print(270)
afficher(g1.rotate('p13',270,False))
print(0)
afficher(g1.rotate('p13',0,True))
print(90)
afficher(g1.rotate('p13',90,True))
print(180)
afficher(g1.rotate('p13',180,True))
print(270)
afficher(g1.rotate('p13',270,True))