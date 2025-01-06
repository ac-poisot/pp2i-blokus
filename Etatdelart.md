# État de l'art

## Introduction:

Les Algorithmes que nous souhaitons étudier ici essayent de répondre à une question simple : " Dans un jeu donné, dans une situation donnée, quelle action me permet de gagner ? "
Ces algorithmes sont donc inclus dans le domaine de la Théorie des Jeux.

## Heuristique:

Un problème se pose toutefois. Dans un jeu donné, dans une situation donnée, comment savoir si nous sommes proches de gagner ?

On pourrait calculer tous les prochains coups, mais cela peut se révéler long et fastidieux. Nous allons donc nous tourner vers des heuristiques. Il est possible de voir une heuristique comme une approximation de la probabilité de gagner. Cela peut dépendre de beaucoup facteurs, parfois difficiles à trouver, et toutes les heuristiques ne sont pas bonnes.

Par exemple pour le jeu des Dames, il existe plusieurs manières de calculer l'heuristique : se baser sur le nombre de pion ou sur l'emplacement de ceux-ci par exemple. Ces manières peuvent être mélangées entre elles naturellement.

Pour le Blokus, nous avons trouvé plusieurs facteurs, et réfléchi à leurs implémentations:
- le nombre de carrés posées
- le nombre de cases où l'on peut poser des pièces
 

## Algorithmes

Nos recherches nous ont fait trouver un grand nombre d'algorithmes tous différents, mais pour la plupart très proches, nous parlerons ici de :
- Aléatoire
- MinMax
- élagage alpha beta
- Nega Scout
- Arborescence de Monte-Carlo
- CNN (réseaux neuronaux convolutifs)

On notera cependant l'existence d'autre programme tel que SSS*,MTD,...

### Aléatoire
Le programme va choisir aléatoirement un coup à chaque fois parmi les coups possibles. Il ne se base sur aucune heuristique.

### Min-Max
Min-Max est initialement prévu pour un jeu à somme nulle entre deux joueurs, c'esr-à-dire qu'il y a toujours un seul gagnant.
L'algorithme Min-Max construit un arbre de jeu, un arbre dont les noeuds sont les différentes configuration du jeu et les arêtes sont les mouvements pour passer d'une configuration à la suivante.
Cependant, celui-ci demande de calculer l'ensemble des coups possibles, et cela peut devenir trop long. On choisit alors de borner la profondeur d'exploration de l'arbre et on utilise une heuristique pour calculer les scores des feuilles du sous-arbre exploré.
On utilise l'arbre en partant des feuilles et on choisit alternativement de minimiser ou de maximiser le score du joueur dont c'est le tour de jouer, c'est-à-dire que les deux joueurs vont chercher à jouer leur meilleur coup.

Dans le cas du Blokus, le nombre de joueurs varie entre deux et quatre, et chaque joueur veut maximiser son score. On adopte une variante pour le bon nombre de joueurs.

### Min-Max élagage $\alpha$ $\beta$

L'algorithme Min-Max avec élagage $\alpha$ $\beta$ se base sur Min-Max. L'élagage $\alpha$ consiste à retirer des branches ayant une valeur trop petite par rapport à un minimum établi, $\alpha$, qui évolue au cours du parcours.
L'élagage $\beta$ consiste à faire la même chose pour l'autre joueur, donc avec un maximum.
Cela permet de ne pas explorer certaines branches de l'arbre quand on sait que la valeur de cette branche est hors des bornes $\alpha$ et $\beta$.


### Nega Scout
Le Nega Scout est une fusion de l'élagage Alpha-Beta et un algorithme Scout, reconnu mathématiquement supérieur à l'élagage. Il va supposer qu'un type de coup est automatiquement supérieur à d'autres.
Dans le cas du blockus, il considérera que poser une pièce de taille 5 est souvent meilleur que n'importe laquelle de taille inférieur, il étudiera donc les branches qui en descendent.

### Arborescence de Monte-Carlo

L'Arborescence de Monte-Carlo agit différemment, elle joue en effet avec une part d'aléatoire. Elle prend la situation de base, qu'elle enregistre avec les valeurs **0**/**0** soit **parties_gagnées**/**parties_jouées** , crée plusieurs nouvelles parties enfants auxquelles elle donne les valeurs 0/0, puis joue aléatoirement à partir de chaque partie crée. Enfin, si une partie est gagnée, elle met le nœud enfant à 1/1 et incrémente celui du nœud mère de 0/+1, si la partie est perdue, alors, on a 0/1 et +1/+1.
Elle répète cela pour chaque nœud, en rajoutant 0/+1 où +1/+1 si perdu où gagner et en inversant une génération sur deux. À la génération N, elle s'arrête et regarde le nœud génération 1 qui a le meilleur ratio. 

### Réseaux neuronaux convolutifs

Les Réseaux neuronaux sont des modèles qui reposent en partie sur notre compréhension du cerveau humain. Le côté convolutif va faire en sorte qu'en utilisant des filtres, on va trouver des "concepts". Quand on cherche des chiffres en alphanumérique par exemple, ça va représenter les barres, les angles, etc.














