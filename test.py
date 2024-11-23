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
#g1.used[0] = ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12','p13','p14','p15','p16','p17','p18','p19','p21']
#print(g1.possible_moves())
#g1.delete_player()
#print(g1.players)


g1.add_piece('p20',0,(0,0),0)
g1.is_playing = g1.is_playing +1
print(g1.possible_moves())
#g1.print_board_see(g1.is_playing-1)
#print(g1.pieces['p20'])
#afficher('p20')
#
#piece = input("poser piece  num? ")
#print(piece)
#print(g1.pieces[piece])
#afficher(piece)
#retourne = bool(input("piece retourne ? "))
#print(retourne)
#rotation = int(input("inclinaison ? "))
#print(rotation)
#y = int(input("abscisse ? "))
#x = int(input("ordonnee ? "))
#print((x,y))
#print(g1.is_legal(piece,rotation,(x,y),retourne))
#print(g1.on_red(piece,rotation,(x,y),retourne))
#print(g1.empty_space(piece,rotation,(x,y),retourne))
#print(g1.no_near_other(piece,rotation,(x,y),retourne))
#print(g1.is_legal('p20',0,(0,0),0))

#g1.print_board_all()
#g1.play_game()
