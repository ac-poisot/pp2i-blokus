Ce document a pour but de faire l'état des algorithmes actuellement utilisés dans le milieu de jeu, de faire l' " état de l'art". 

## Introduction:

Les Algorithmes que nous souhaitons étudier ici essayent de répondre à une question simple : " Dans un jeu donné, dans une situation donnée, quelle action me permet de gagner ? "
Ces algorithmes sont donc inclus dans le domaine de la Théorie des Jeux.

## Heuristique:

Un problème se pose toutefois. Dans un jeu donné, dans une situation donnée, comment savoir si nous sommes proches de gagner ?
Il suffit de calculer tous les prochains coups, et de voir si on trouve une série de coups gagnante, comme au Morpion, c'est assez simple. Enfin, ça l'est pour le morpion seulement, mais rapidement pour des jeux comme les échecs où à chaque coup une centaine de coups est possible, cela devient rapidement compliqué. Alors pour notre jeu, où l'on peut faire au maximum 21 coups, mais que chaque pièce a jusqu'à 8 positions différentes, et jusqu'à une vingtaine d'emplacements différents, cela devient trop compliqué. Nous devons donc définir une heuristique, une manière de savoir notre "distance" à la victoire, et là aussi, nous viens une quantité d'Heuristique toute différentes. Pour le jeu des Dames, pourtant, il existe plusieurs manières ou facteurs de calculer l'heuristique, se baser sur le nombre de pion, où sur l'emplacement de ceux-ci par exemple. Ces manières peuvent être mélangées entre elles naturellement.
Pour le Blokus, nous avons trouvé plusieurs facteurs, et réfléchis à leurs implémentations:
- le nombre de carrés posé
- le nombre de cases où l'on peut poser des pièces
Nous pourrions aussi rajouter les cases où l'adversaire aurait pu jouer que l'on a enlevé, mais c'est simplement rajouter l'opposée de l'heuristique de l'adversaire. 
 

## Algorithme

Nos recherches nous on fait trouvées un grand nombre d'Algorithme tout différent, mais pour la plupart très proches, nous parlerons ici de :
- Aléatoire
- MinMax
- élagage alpha beta
- Nega Scout
- Arborescence de Monte-Carlo
- CNN (réseaux neuronaux convolutifs)

On notera cependant l'existence d'autre programme tel que SSS*,MTD,...

### Aléatoire
Le programme va simplement choisir aléatoirement un coup à chaque fois.

### Min-Max
Le plus simple de tous est sans conteste le Min-Max. Celui-ci consiste à calculer tous les coups possibles sur X coups d'affilée, et de calculer le coup qui est le plus sûr pour gagner la partie. 
Cependant, celui-ci demande de calculer l'ensemble des possibilités, et cela peut devenir trop long.

### Min-Max élagage $\alpha$ $\beta$

Le Min-Max, élagage $\alpha$ $\beta$ fonctionne de la même manière que le Min-Max, mais on rajoute une heuristique, et si jamais notre coup possible semble trop négatif pour nous, il ne calcule pas les branches ayant ce coup comme racine.

Il semble être facile à implenté dès que l'on choisit notre heuristique

### Nega Scout
Le Nega Scout est une fusion de l'élagage Alpha-Beta et un algorithme Scout, mathématiquement supérieur à l'élagage. Il va supposer qu'un type de coup est automatiquement supérieur à d'autres, ici par exemple, il considérera que poser une pièce de taille 5 est souvent meilleur que n'importe laquelle de taille inférieur, il étudiera donc les branches qui en descendent.

### Arborescence de Monte-Carlo

L'Arborescence de Monte-Carlo agit différemment, elle joue en effet avec une part d'aléatoire. Elle prend la situation de base, qu'elle enregistre avec les valeurs **0**/**0** soit **parties_gagnées**/**parties_jouées** , crée plusieurs nouvelle partie enfants auquel elle donne les valeurs 0/0, puis joue aléatoirement à partir de chaque partie crée. Enfin, si une partie est gagnée, elle met le nœud enfant à 1/1 et incrémente celui du nœud mère de 0/+1, si la partie est perdue, alors, on a 0/1 et +1/+1.
Elle répète cela pour chaque nœud, en rajoutant 0/+1 où +1/+1 si perdu où gagner et en inversant une génération sur deux. À la génération N, elle s'arrête et regarde le nœud génération 1 qui a le meilleur ratio. 

### Réseaux neuronaux convolutifs

Les Réseaux neuronaux sont des modèles qui reposent en partie sur notre compréhension du cerveau humain. Le côté convolutif va faire en sorte qu'en utilisant des filtres, on va trouver des "concepts". Quand on cherche des chiffres en alphanumérique par exemple, ça va représenter les barres, les angles, etc.














