# Documentation

## Table des matières
1. [Les pièces](#les-pièces)
2. [Le jeu](#le-jeu)
3. [Web](#web)
4. [I.A.](#ia)
---

## Les pièces

### Stockage
Les pièces sont stockées dans des matrices plus grandes qu’elles :

Exemple (pièce nº 11) :
| 0 | 2 | 3 | 2 |
| --- | --- | --- | --- |
| **0** | **3** | **1** | **3** |
|**0** | **3** | **1**  | **3** |
|**2** | **3** | **1** | **3** |
|**3** | **1** | **1** | **3** |
|**2** | **3** | **3** | **2** |

Notons que
- **0** désigne une zone qui ne concerne pas la pièce,
- **1** est le corps de la pièce,
- **2** est la zone qui doit être en contact avec une autre pièce (les coins), et
- **3** désigne les zones où il ne doit pas y avoir d’autres pièces de la même couleur.


### Orientation et retournement

Les pièces sont par défaut représentées sans orientation. On utilisera ensuite le sens horaire et des rotations de 0 (pas de rotation), 90, 180 et 270 degrés pour les faire tourner. Pour les retournements, on tourne d’abord la pièce puis on la retourne verticalement.

 ⬜⬜⬛ → ⬜⬛⬜  
 ⬛⬛⬛ → ⬛⬛⬛  
 ⬜⬛⬜ → ⬜⬜⬛
 
## Le jeu

On commence par créer la liste des coups possibles au début de la partie.

On définit une classe ``Game``. Elle prend en paramètre un nombre de joueurs sous forme d’entier.

Cette classe contiendra ensuite les attributs suivants :
  - ``available: list[list[int]]`` : pour chaque joueur, la liste des pièces qu’il peut poser.
  - ``board: list[list[int]]`` : le plateau du jeu, avec 22 cases : on tient compte des bords pour éviter des problèmes lors des tests. Il est initialement rempli avec des ``0`` et contiendra ``i`` si le joueur ``i`` a posé une pièce sur cette case.
  - ``bonus: list[bool]`` : pour chaque joueur, vaut ``True`` si celui-ci a le droit à un bonus de 5 points (dans le cas où toutes les pièces sont posées et la dernière pièce posée est le monomino, pièce nº 1)
  - ``is_playing: int`` : le joueur qui est en train de jouer
  - ``is_playing_index: int`` : l’indice du joueur qui est en train de jouer, pour faciliter l’accès aux tableaux (éviter -1 à chaque fois)
  - ``maxn: int`` : le nombre de joueurs initialement présents dans la partie
  - ``possible_moves: list[list[tuple[int, int, int, tuple[int, int]]]]`` : la liste des coups possibles pour chaque joueur, un coup étant représenté par le tuple (pièce, rotation, retourné, position)
  - ``players: list[int]`` : les numéros des joueurs encore en jeu
  - ``red_pieces: list[int]`` : pour chaque joueur, l’ensemble des cases rouges qu’il possède

On définit ensuite les méthodes suivantes :
  - ``init: int -> None``
  - ``print_board: void -> void``
  - ``is_legal: int, int, tuple[int, int], bool, int -> bool``
  - ``is_red_cell: int, int, int -> bool``
  - ``add_piece: int, int, tuple[int, int], bool -> None``
  - ``remove_piece: int, int, tuple[int, int], bool -> None``
  - ``score: int -> int``
  - ``can_pay: int -> bool``
  - ``delete_player: int -> None``
  - ``play_game: None -> None``
  - ``copy_game: None -> Game``
  - ``retrieve_game: int, list[list[str, int, int, int, int, int, int, bool]] -> Game``


### Les méthodes de la classe Game
  * ``init`` : initialise le jeu avec les attributs cités plus haut. On fait le calcul des mouvements possibles avant.
  * ``print_board`` : affiche le plateau de jeu.
  * ``is_legal`` : vérifie qu’un coup est légal pour le joueur passé en paramètre. Pour cela, la pièce doit être disponible et ne doit pas sortir du plateau. Les autres conditions permettent de vérifier que 1) la pièce est bien posée sur des cases libres, 2) vérifier que la pièce est bien posée sur un coin (``valid`` est un booléen de controle → vrai si un coin a été vu), 3) vérifier que la pièce n’est pas tangente à celle d’une même couleur. Dans le cas où la pièce est posée dans un coin (au début), il n’y a pas encore de pièces, ``valid`` est forcément à ``False``, donc on rajoute ce cas manuellement.
  * ``add_piece`` : ajoute la pièce sans vérification de la légalité du mouvement. Pour cela, on commence par vérifier si on est dans un coin (début de la partie donc toutes les pièces sont disponibles) pour retirer les autres coins comme cases disponibles au joueur. On met ensuite la pièce sur le plateau, puis on retire la pièce des pièces disponibles. Afin d’éviter le calcul des coups possibles à chaque tour (200 en moyenne), on calcule les coups possibles à chaque fois qu’on pose une pièce. Cela nécessite de retirer les coups qui ne sont plus disponibles de tous les joueurs puis de rajouter les mouvements du joueur qui joue. Il y a également le bonus si la dernère pièce posée est le monomino et que toutes les autres pièces ont été placées.
  * ``remove_piece`` : retire une pièce du plateau. On commence par retirer la pièce du plateau (remettre des ``0``), puis on la rajoute aux pièces disponibles. On retire ensuite les mouvements qui ne sont plus possibles et on rajoute les nouveaux.
  * ``score`` : renvoie le score du joueur, défini par les règles du jeu.
  * ``can_play`` : renvoie ``True`` si et seulement si le joueur passé en paramètre peut jouer, donc s’il lui reste des mouvements possibles.
  * ``delete_player`` : retire un joueur de la partie.
  * ``play_game`` : joue une partie en mode aléatoire.
  * ``copy_game`` : renvoie une copie de la partie en cours.
  * ``retrieve_game`` : recrée un jeu à l’aide de la base de données, en se basant sur les informations de ``db.py``.


## Web

La partie Web du projet est centrée autour d’un unique fichier, ``app.py``.
Celui-ci fait appel à des templates situés dans le fichier éponyme et organisés en deux catégories, les *pages* et les *widgets*, les *widgets* pouvant être utilisés dans plusieurs pages.
De même, le CSS, stocké dans ``static/css`` s’organise également en deux sous-dossiers *pages* et *widgets*. On trouve, dans ceux-ci, les fichiers ``.scss`` et les fichiers ``.css`` correspondants. Les fichiers ``.css`` sont issus de la compilation des fichiers ``.scss`` dans lesquels nous écrivons nos instructions de style. Les fichiers ``.css`` sont tout de même fournis pour que le code soit du « prêt à lancer » dès que les librairies sont installées.
Nous disposons également d’un ``_variable.scss`` dans le dossier de style des *widgets*. Celui-ci permet d’introduire des règles appliquées dans tous les fichiers de style dans lesquels ``_variable.scss`` est importé.
Nous avons également, dans ``static``, un dossier d’images ``/images``, un dossier contenant les traductions en différentes langues sous forme de fichiers JSON dans ``/lang`` et des fichiers de script JavaScript, importés par les pages HTML.

## I.A.
Le cœur de l’I.A. se trouve dans le fichier ``ai.py``.
Il contient ainsi les fonctions qui nous permettent d’introduire l’algorithme de minmax ainsi que de construire des I.A. utilisant les modèles entraînés situés dans ``/models``.
Ceux-ci sont des réseaux neuronaux convolutifs. Leur script d’entraînement se trouve dans ``training/training.py``. Il repose sur des *datasets* créés dans ``/training`` par ``training/generate_data.py``. Celui-ci fait jouer les I.A. existantes dans des parties qui servent ensuite de données d’entraînement.
L’entraînement peut-être suivi avec les graphes de perte dans ``training/training_data``.
Nous avons également écrit un script pour essayer de classer les I.A. selon leurs performances dans ``rate_ais.py``.