# SAE Donjon — Jeu d'exploration en Python

Projet réalisé dans le cadre de la **SAE 1.01/1.02** en 1re année de **BUT Informatique** à l'Université Gustave Eiffel (IUT Marne-la-Vallée).

## Description

Jeu d'exploration de donjon en Python avec interface graphique. Le joueur incarne un aventurier qui doit parcourir un labyrinthe de salles, affronter des dragons et trouver la sortie.

### Fonctionnalités

- Génération de donjons avec des salles connectées par des portes
- Rotation des salles (90° horaire) pour créer de nouveaux passages
- Système de combat aventurier vs dragons basé sur les niveaux
- Déplacement des dragons aléatoire avec IA
- Interface graphique avec images (salles, aventurier, dragon)
- Gestion de la victoire (tous les dragons vaincus)

## Technologies

- **Python 3**
- **Tkinter** (via la bibliothèque `fltk` fournie par l'IUT)

## Structure du projet

```
SAE-Donjon/
├── modele.py           # Logique du jeu (salles, déplacements, combats)
├── interface.py        # Interface graphique et boucle de jeu
├── fltk.py             # Bibliothèque graphique (fournie par l'IUT)
└── salles_donjon/      # Images des salles et personnages
    ├── aventurier.png
    ├── dragon.png
    └── salle_XXXX.png  # 16 variantes de salles
```

## Lancement

```bash
python interface.py
```

> Nécessite Python 3.10+ et Tkinter (inclus par défaut avec Python sur la plupart des systèmes).

## Architecture du code

### `modele.py` — Logique métier
- Création et manipulation des salles (tuples de 4 booléens : haut, droite, bas, gauche)
- Gestion du donjon (grille 2D de salles)
- Déplacements et vérification des connexions entre salles
- Système de combat et gestion des niveaux
- Déplacement aléatoire des dragons

### `interface.py` — Affichage graphique
- Dessin du donjon avec images adaptées à la taille de la grille
- Affichage de l'aventurier et des dragons
- Gestion des événements clavier (déplacements, rotation)
- Menus et écrans de fin (victoire/défaite)

## Auteur

**Djibril OUBOUZID** — BUT Informatique, Université Gustave Eiffel
