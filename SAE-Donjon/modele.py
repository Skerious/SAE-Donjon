def cree_salle(haut, droite, bas, gauche):
    """
    Crée une salle avec les sorties spécifiées.
    """
    return (haut, droite, bas, gauche)


def pivote_salle(salle):
    """
    Fait pivoter une salle de 90° dans le sens horaire.
    """
    haut, droite, bas, gauche = salle
    # Gauche → Haut, Haut → Droite, Droite → Bas, Bas → Gauche
    return (gauche, haut, droite, bas)


def cree_donjon(nb_lignes, nb_colonnes):
    """
    Crée un donjon vide (toutes les salles ont 4 sorties).
    """
    donjon = []
    for i in range(nb_lignes):
        ligne = []
        for j in range(nb_colonnes):
            # Créer une salle avec 4 sorties (salle "croix")
            salle = cree_salle(True, True, True, True)
            ligne.append(salle)
        donjon.append(ligne)
    return donjon


def cree_aventurier(ligne, colonne, niveau=1):
    """
    Crée un aventurier à la position donnée.
    """
    position = (ligne, colonne)
    return [position, niveau]


def cree_dragon(ligne, colonne, niveau):
    """
    Crée un dragon à la position et niveau donnés.
    """
    position = (ligne, colonne)
    return [position, niveau]


def salles_connectees(donjon, ligne1, col1, ligne2, col2):
    """
    Vérifie si deux salles adjacentes sont connectées.
    """
    # Récupérer les deux salles
    salle1 = donjon[ligne1][col1]
    salle2 = donjon[ligne2][col2]
    
    haut1, droite1, bas1, gauche1 = salle1
    haut2, droite2, bas2, gauche2 = salle2
    
    # Vérifier selon la direction
    # Cas 1 : salle1 est AU-DESSUS de salle2 (on va vers le BAS)
    if ligne1 == ligne2 - 1 and col1 == col2:
        return bas1 and haut2
    
    # Cas 2 : salle1 est EN-DESSOUS de salle2 (on va vers le HAUT)
    if ligne1 == ligne2 + 1 and col1 == col2:
        return haut1 and bas2
    
    # Cas 3 : salle1 est à GAUCHE de salle2 (on va vers la DROITE)
    if ligne1 == ligne2 and col1 == col2 - 1:
        return droite1 and gauche2
    
    # Cas 4 : salle1 est à DROITE de salle2 (on va vers la GAUCHE)
    if ligne1 == ligne2 and col1 == col2 + 1:
        return gauche1 and droite2
    
    # Les salles ne sont pas adjacentes
    return False


def trouve_dragon(dragons, ligne, colonne):
    """
    Cherche si un dragon se trouve à la position donnée.
    """
    # Parcourir tous les dragons
    for dragon in dragons:
        ligne_dragon, colonne_dragon = dragon[0]
        
        # Si le dragon est à cette position
        if ligne_dragon == ligne and colonne_dragon == colonne:
            return dragon
    
    # Aucun dragon trouvé à cette position
    return None


def deplace_aventurier(aventurier, nouvelle_ligne, nouvelle_colonne):
    """
    Déplace l'aventurier vers une nouvelle position.
    """
    aventurier[0] = (nouvelle_ligne, nouvelle_colonne)

def combat(aventurier, dragon, dragons):
    """
    Gère le combat entre l'aventurier et un dragon.
    """
    niveau_aventurier = aventurier[1]
    niveau_dragon = dragon[1]
    
    # L'aventurier est assez fort ?
    if niveau_aventurier >= niveau_dragon:
        # Victoire ! L'aventurier gagne un niveau
        aventurier[1] = aventurier[1] + 1
        
        # On retire le dragon de la liste
        dragons.remove(dragon)
        
        return True  # Aventurier gagne
    else:
        # Défaite ! L'aventurier meurt
        return False  # Partie perdue
    
def pivote_salle_donjon(donjon, ligne, colonne):
    """
    Pivote la salle du donjon à la position donnée.
    """
    salle_actuelle = donjon[ligne][colonne]
    salle_pivotee = pivote_salle(salle_actuelle)
    donjon[ligne][colonne] = salle_pivotee

def tous_dragons_morts(dragons):
    """
    Vérifie si tous les dragons ont été tués.
    """
    return len(dragons) == 0

def cree_donjon_facile():
    """
    Crée un donjon facile 4x4 
    """
    donjon = cree_donjon(4, 4)
    
    # Créer un vrai labyrinthe avec des impasses
    donjon[0][0] = cree_salle(False, True, False, False)   # Départ - seulement droite
    donjon[0][1] = cree_salle(False, False, True, True)    # Couloir qui descend
    donjon[0][2] = cree_salle(False, True, False, False)   # Impasse à droite
    donjon[0][3] = cree_salle(False, False, False, True)   # Impasse
    
    donjon[1][0] = cree_salle(False, True, False, False)   # Mur
    donjon[1][1] = cree_salle(True, True, False, False)    # Carrefour
    donjon[1][2] = cree_salle(False, False, True, True)    # Descente
    donjon[1][3] = cree_salle(False, False, True, False)   # Descente
    
    donjon[2][0] = cree_salle(False, False, True, False)   # Impasse
    donjon[2][1] = cree_salle(False, True, False, True)    # Couloir horizontal
    donjon[2][2] = cree_salle(True, True, False, True)     # Carrefour
    donjon[2][3] = cree_salle(True, False, True, True)     # T
    
    donjon[3][0] = cree_salle(False, True, False, False)   # Salle
    donjon[3][1] = cree_salle(False, True, False, True)    # Couloir
    donjon[3][2] = cree_salle(False, True, False, True)    # Couloir vers dragon
    donjon[3][3] = cree_salle(True, False, False, True)    # Salle du dragon
    
    # Créer l'aventurier en haut à gauche
    aventurier = cree_aventurier(0, 0)
    
    # 1 dragon niveau 1 dans le coin
    dragons = []
    dragons.append(cree_dragon(3, 3, 1))
    
    return (donjon, aventurier, dragons)


def cree_donjon_moyen():
    """
    Crée un donjon moyen 5x5 
    """
    donjon = cree_donjon(5, 5)
    
    # Spirale complexe avec plusieurs chemins
    donjon[0][0] = cree_salle(False, True, False, False)   # Départ
    donjon[0][1] = cree_salle(False, True, False, True)    # Couloir
    donjon[0][2] = cree_salle(False, True, False, True)    # Couloir
    donjon[0][3] = cree_salle(False, True, False, True)    # Couloir
    donjon[0][4] = cree_salle(False, False, True, True)    # Coin
    
    donjon[1][0] = cree_salle(False, False, True, False)   # Impasse
    donjon[1][1] = cree_salle(False, True, False, False)   # Mur
    donjon[1][2] = cree_salle(False, False, True, False)   # Mur
    donjon[1][3] = cree_salle(False, True, False, False)   # Mur
    donjon[1][4] = cree_salle(True, False, True, False)    # Descente
    
    donjon[2][0] = cree_salle(True, True, False, False)    # Coin
    donjon[2][1] = cree_salle(False, True, False, True)    # Couloir
    donjon[2][2] = cree_salle(True, False, True, True)     # T (dragon ici!)
    donjon[2][3] = cree_salle(False, False, False, True)   # Impasse
    donjon[2][4] = cree_salle(True, False, True, False)    # Descente
    
    donjon[3][0] = cree_salle(False, True, True, False)    # L
    donjon[3][1] = cree_salle(False, False, False, True)   # Impasse
    donjon[3][2] = cree_salle(True, True, False, False)    # L
    donjon[3][3] = cree_salle(False, True, False, True)    # Couloir
    donjon[3][4] = cree_salle(True, False, False, True)    # L (dragon ici!)
    
    donjon[4][0] = cree_salle(True, True, False, False)    # L
    donjon[4][1] = cree_salle(False, True, False, True)    # Couloir
    donjon[4][2] = cree_salle(False, True, False, True)    # Couloir
    donjon[4][3] = cree_salle(False, True, False, True)    # Couloir
    donjon[4][4] = cree_salle(False, False, False, True)   # Arrivée
    
    # Aventurier en haut à gauche
    aventurier = cree_aventurier(0, 0)
    
    # 2 dragons stratégiquement placés
    dragons = []
    dragons.append(cree_dragon(2, 2, 1))  # Dragon niveau 1 au centre
    dragons.append(cree_dragon(3, 4, 2))  # Dragon niveau 2 vers la fin
    
    return (donjon, aventurier, dragons)


def cree_donjon_difficile():
    """
    Crée un donjon difficile 6x6 
    """
    donjon = cree_donjon(6, 6)
    
    # Labyrinthe très complexe avec multiples chemins et impasses
    # Ligne 0
    donjon[0][0] = cree_salle(True, False, False, False)    # Départ
    donjon[0][1] = cree_salle(False, False, True, False)   # Mur
    donjon[0][2] = cree_salle(False, True, False, False)   # Mur
    donjon[0][3] = cree_salle(False, True, True, True)     # T
    donjon[0][4] = cree_salle(False, False, True, True)    # L
    donjon[0][5] = cree_salle(False, False, True, False)   # Impasse
    
    # Ligne 1
    donjon[1][0] = cree_salle(True, False, True, False)    # Couloir vertical
    donjon[1][1] = cree_salle(True, True, False, False)    # L
    donjon[1][2] = cree_salle(False, False, True, True)    # L
    donjon[1][3] = cree_salle(True, True, False, False)    # L (dragon!)
    donjon[1][4] = cree_salle(True, False, False, True)    # L
    donjon[1][5] = cree_salle(True, False, True, False)    # Couloir
    
    # Ligne 2
    donjon[2][0] = cree_salle(True, True, False, False)    # L
    donjon[2][1] = cree_salle(False, True, False, True)    # Couloir
    donjon[2][2] = cree_salle(False, False, True, False)      # Carrefour +
    donjon[2][3] = cree_salle(False, False, True, True)    # L
    donjon[2][4] = cree_salle(False, True, False, False)   # Mur
    donjon[2][5] = cree_salle(True, False, True, False)    # Couloir
    
    # Ligne 3
    donjon[3][0] = cree_salle(False, True, True, False)    # L
    donjon[3][1] = cree_salle(False, False, False, True)   # Impasse
    donjon[3][2] = cree_salle(False, False, True, False)     # T (dragon!)
    donjon[3][3] = cree_salle(True, False, False, True)    # L
    donjon[3][4] = cree_salle(False, True, True, True)     # T
    donjon[3][5] = cree_salle(True, False, False, True)    # L
    
    # Ligne 4
    donjon[4][0] = cree_salle(True, True, False, False)    # L
    donjon[4][1] = cree_salle(False, True, True, True)     # T
    donjon[4][2] = cree_salle(True, False, False, True)    # L
    donjon[4][3] = cree_salle(False, True, True, False)    # L (dragon!)
    donjon[4][4] = cree_salle(True, False, False, True)    # L
    donjon[4][5] = cree_salle(False, False, True, False)   # Impasse
    
    # Ligne 5
    donjon[5][0] = cree_salle(False, True, False, False)   # Mur
    donjon[5][1] = cree_salle(True, True, False, True)     # T
    donjon[5][2] = cree_salle(True, False, False, True)    # Couloir
    donjon[5][3] = cree_salle(True, True, False, True)     # T
    donjon[5][4] = cree_salle(False, True, False, False)    # Couloir
    donjon[5][5] = cree_salle(True, False, False, True)    # Arrivée (dragon!)
    
    # Aventurier en haut à gauche
    aventurier = cree_aventurier(0, 0)
    
    # 4 dragons bien placés
    dragons = []
    dragons.append(cree_dragon(5, 0, 1))  # Dragon niveau 1
    dragons.append(cree_dragon(4, 5, 2))  # Dragon niveau 2
    dragons.append(cree_dragon(2, 3, 3))  # Dragon niveau 3
    dragons.append(cree_dragon(2, 4, 4))  # Dragon niveau 4
    
    return (donjon, aventurier, dragons)

def deplace_dragons_aleatoire(dragons, donjon, aventurier):
    """
    Déplace chaque dragon aléatoirement vers une case adjacente connectée.
    
    :param dragons: liste des dragons
    :param donjon: la grille
    :param aventurier: l'aventurier
    :return: True si l'aventurier survit, False s'il meurt
    """
    import random
    
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    
    # Parcourir chaque dragon
    for dragon in dragons:
        position_dragon = dragon[0]
        ligne_dragon, col_dragon = position_dragon
        
        # Trouver toutes les directions possibles
        directions_possibles = []
        
        # Haut
        if ligne_dragon > 0 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon - 1, col_dragon):
            directions_possibles.append((ligne_dragon - 1, col_dragon))
        
        # Bas
        if ligne_dragon < nb_lignes - 1 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon + 1, col_dragon):
            directions_possibles.append((ligne_dragon + 1, col_dragon))
        
        # Gauche
        if col_dragon > 0 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon, col_dragon - 1):
            directions_possibles.append((ligne_dragon, col_dragon - 1))
        
        # Droite
        if col_dragon < nb_colonnes - 1 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon, col_dragon + 1):
            directions_possibles.append((ligne_dragon, col_dragon + 1))
        
        # Si le dragon peut bouger
        if len(directions_possibles) > 0:
            # Choisir une direction aléatoire
            nouvelle_position = random.choice(directions_possibles)
            dragon[0] = nouvelle_position
            
            # Vérifier si le dragon rencontre l'aventurier
            pos_aventurier = aventurier[0]
            if nouvelle_position == pos_aventurier:
                # Combat !
                resultat = combat(aventurier, dragon, dragons)
                if not resultat:
                    return False  # Aventurier mort
    
    return True  # Aventurier survit

if __name__ == "__main__":
    # Test 1-3 : Créer et pivoter une salle
    salle = cree_salle(True, False, True, False)
    print("Salle de départ :", salle)
    
    salle_pivotee = pivote_salle(salle)
    print("Après 1 pivot :", salle_pivotee)
    
    salle2 = pivote_salle(salle_pivotee)
    print("Après 2 pivots :", salle2)
    
    salle3 = pivote_salle(salle2)
    print("Après 3 pivots :", salle3)
    
    salle4 = pivote_salle(salle3)
    print("Après 4 pivots :", salle4)
    
    if salle == salle4:
        print("✅ Parfait ! La salle est revenue à sa position initiale !")
    
    # Test 4 : Créer un petit donjon 2x3
    print("\n=== Test du donjon ===")
    donjon = cree_donjon(2, 3)
    print("Donjon 2 lignes x 3 colonnes :")
    for i in range(len(donjon)):
        print(f"Ligne {i} : {donjon[i]}")
    
    # Test 5 : Créer les personnages
    print("\n=== Test des personnages ===")
    aventurier = cree_aventurier(0, 0)
    print("Aventurier :", aventurier)
    print("Position aventurier :", aventurier[0])
    print("Niveau aventurier :", aventurier[1])
    
    dragons = []
    dragons.append(cree_dragon(1, 1, 2))
    dragons.append(cree_dragon(0, 2, 3))
    print("\nListe des dragons :", dragons)
    print("Premier dragon :", dragons[0])
    
    # Test 6 : Connexion entre salles
    print("\n=== Test des connexions ===")
    donjon = cree_donjon(2, 2)
    
    print("(0,0) et (0,1) connectées ?", salles_connectees(donjon, 0, 0, 0, 1))
    print("(0,0) et (1,0) connectées ?", salles_connectees(donjon, 0, 0, 1, 0))
    
    donjon[0][0] = cree_salle(False, False, True, True)
    print("\nAprès modification de (0,0) :")
    print("(0,0) et (0,1) connectées ?", salles_connectees(donjon, 0, 0, 0, 1))
    print("(0,0) et (1,0) connectées ?", salles_connectees(donjon, 0, 0, 1, 0))
    
    # Test 7 : Trouver un dragon
    print("\n=== Test de recherche de dragon ===")
    dragons = []
    dragons.append(cree_dragon(1, 1, 2))
    dragons.append(cree_dragon(0, 2, 3))
    dragons.append(cree_dragon(1, 0, 1))
    
    print("Liste des dragons :", dragons)
    
    dragon_trouve = trouve_dragon(dragons, 1, 1)
    print("\nDragon en (1,1) ?", dragon_trouve)
    if dragon_trouve:
        print("  → Niveau du dragon :", dragon_trouve[1])
    
    dragon_absent = trouve_dragon(dragons, 0, 0)
    print("\nDragon en (0,0) ?", dragon_absent)
    
    # Test 8 : Déplacer l'aventurier
    print("\n=== Test de déplacement ===")
    aventurier = cree_aventurier(0, 0)
    print("Position initiale :", aventurier[0])
    
    deplace_aventurier(aventurier, 1, 2)
    print("Après déplacement en (1,2) :", aventurier[0])
    
    deplace_aventurier(aventurier, 0, 1)
    print("Après déplacement en (0,1) :", aventurier[0])

    # Test 9 : Combat
    print("\n=== Test de combat ===")
    
    # Cas 1 : Aventurier gagne (niveaux égaux)
    aventurier = cree_aventurier(0, 0, 2)
    dragons = [cree_dragon(1, 1, 2), cree_dragon(0, 2, 3)]
    dragon = dragons[0]
    
    print("Avant combat :")
    print("  Aventurier niveau :", aventurier[1])
    print("  Dragon niveau :", dragon[1])
    print("  Nombre de dragons :", len(dragons))
    
    resultat = combat(aventurier, dragon, dragons)
    print("\nAprès combat :")
    print("  Aventurier a gagné ?", resultat)
    print("  Aventurier niveau :", aventurier[1])
    print("  Nombre de dragons :", len(dragons))
    
    # Cas 2 : Aventurier perd (dragon plus fort)
    print("\n--- Combat perdu ---")
    aventurier2 = cree_aventurier(0, 0, 1)
    dragons2 = [cree_dragon(1, 1, 5)]
    dragon2 = dragons2[0]
    
    print("Avant combat :")
    print("  Aventurier niveau :", aventurier2[1])
    print("  Dragon niveau :", dragon2[1])
    
    resultat2 = combat(aventurier2, dragon2, dragons2)
    print("\nAprès combat :")
    print("  Aventurier a gagné ?", resultat2)
    print("  Aventurier niveau :", aventurier2[1])

    # Test 10 : Pivoter une salle dans le donjon
    print("\n=== Test pivot dans donjon ===")
    donjon = cree_donjon(2, 2)
    donjon[0][0] = cree_salle(True, False, True, False)
    
    print("Salle avant pivot :", donjon[0][0])
    pivote_salle_donjon(donjon, 0, 0)
    print("Salle après pivot :", donjon[0][0])
    
    # Test 11 : Vérifier victoire
    print("\n=== Test de victoire ===")
    dragons = [cree_dragon(1, 1, 2), cree_dragon(0, 2, 3)]
    print("Dragons restants :", len(dragons))
    print("Tous morts ?", tous_dragons_morts(dragons))
    
    dragons = []
    print("\nAprès avoir tout tué :")
    print("Dragons restants :", len(dragons))
    print("Tous morts ?", tous_dragons_morts(dragons))

def deplace_dragons_aleatoire(dragons, donjon, aventurier):
    """
    Déplace chaque dragon aléatoirement vers une case adjacente connectée.
    
    :param dragons: liste des dragons
    :param donjon: la grille
    :param aventurier: l'aventurier
    :return: True si l'aventurier survit, False s'il meurt
    """
    import random
    
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    
    # Parcourir chaque dragon
    for dragon in dragons:
        position_dragon = dragon[0]
        ligne_dragon, col_dragon = position_dragon
        
        # Trouver toutes les directions possibles
        directions_possibles = []
        
        # Haut
        if ligne_dragon > 0 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon - 1, col_dragon):
            directions_possibles.append((ligne_dragon - 1, col_dragon))
        
        # Bas
        if ligne_dragon < nb_lignes - 1 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon + 1, col_dragon):
            directions_possibles.append((ligne_dragon + 1, col_dragon))
        
        # Gauche
        if col_dragon > 0 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon, col_dragon - 1):
            directions_possibles.append((ligne_dragon, col_dragon - 1))
        
        # Droite
        if col_dragon < nb_colonnes - 1 and salles_connectees(donjon, ligne_dragon, col_dragon, ligne_dragon, col_dragon + 1):
            directions_possibles.append((ligne_dragon, col_dragon + 1))
        
        # Si le dragon peut bouger
        if len(directions_possibles) > 0:
            # Choisir une direction aléatoire
            nouvelle_position = random.choice(directions_possibles)
            dragon[0] = nouvelle_position
            
            # Vérifier si le dragon rencontre l'aventurier
            pos_aventurier = aventurier[0]
            if nouvelle_position == pos_aventurier:
                # Combat !
                resultat = combat(aventurier, dragon, dragons)
                if not resultat:
                    return False  # Aventurier mort
    
    return True  # Aventurier survit