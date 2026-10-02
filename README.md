# Projet PPII — Semestre S5

## Table des matières
1. [Introduction](#introduction)
2. [Membres du groupe](#membres-du-groupe)
3. [Description du projet](#description-du-projet)
4. [Prérequis](#prérequis)
5. [Installation](#installation)
6. [Exécution](#exécution)

---

## Introduction

Bienvenue dans le projet **PPII — Semestre S5**. Ce projet est réalisé dans le cadre du semestre 5 pour l’unité PPII à TELECOM Nancy. Vous trouverez ici toutes les informations nécessaires pour comprendre, installer, et exécuter le projet.


## Membres du groupe

- **Poisot Anne-Cécile** — [anne-cecile.poisot@telecomnancy.eu](mailto:anne-cecile.poisot@telecomnancy.net)
- **Loisil Tom** — [tom.loisil@telecomnancy.eu](mailto:tom.loisil@telecomnancy.eu)
- **Estivals Raphaël** — [raphael.estivals@telecomnancy.eu](mailto:raphael.estivals@telecomnancy.eu)
- **Bui Kévin** — [kevin.bui@telecomnancy.eu](mailto:kevin.bui@telecomnancy.eu)


## Description du projet

- **Sujet** : Blokus en ligne
- **Objectifs** : Réalisation d’un Blokus en version web jouable en local et à distance
- **Technologies utilisées** : Python, Flask, HTML, SASS, JavaScript, SQlite3


## Prérequis

- **Langages :** Python 3.10, JavaScript, HTML, Sass (sous la syntaxe SCSS)
- **Frameworks :** Flask
- **Dépendances :** Voir le fichier `requirements.txt`


## Installation

### Étapes générales :

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/ac-poisot/pp2i-blokus
   cd pp2i-blokus
   ```

2. Créez un environemment Python, lancez-le et installez les dépendances:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Exécution

1. Lancez l’application :

    ```bash
    flask run
    ```

2. Rendez-vous sur la page d’accueil à l'adresse `http://127.0.0.1:5000/` pour initialiser la base de données.

3. Bienvenue sur le site ! Bon jeu !


## Quelques images du jeu

Voici la page d'accueil du jeu, qui vous permet ensuite de vous connecter et/ou découvrir les règles.
![écran d'accueil du jeu](/pp2i-blokus/pictures/blokus_welcome.png)

Vous pouvez créer votre partie. Jouer seul contre des AI, en local ou en ligne avec vos amis !
![écran de création de partie](/pp2i-blokus/pictures/blokus_create_game.png)

Voici une partie en cours.
![example d'une partie en cours](/pp2i-blokus/pictures/blokus_in_game.png)

Voici une partie finie.
![example de fin de partie](/pp2i-blokus/pictures/blokus_endgame.png)

Dans votre profil, vous pouvez retrouver votre historique des parties.
![profil d'un joueur](/pp2i-blokus/pictures/blokus_history.png)