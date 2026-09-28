import fltk
import modele
import time
import tkinter as tk

DOSSIER_IMAGES = "salles_donjon/"



# Constantes pour l'affichage
HAUTEUR_AIDE = 100  # Hauteur de la zone d'aide en bas
LARGEUR_FENETRE = 850
HAUTEUR_FENETRE = 850

def calcule_taille_salle(donjon):
    """
    Calcule la taille optimale d'une salle pour remplir au maximum l'espace disponible.
    En tenant compte de la zone d'aide en bas.
    """
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    
    # Calculer la taille maximale possible pour remplir l'écran
    taille_max_largeur = LARGEUR_FENETRE // nb_colonnes
    taille_max_hauteur = (HAUTEUR_FENETRE - HAUTEUR_AIDE) // nb_lignes
    
    # Prendre la plus petite des deux pour que tout rentre
    return min(taille_max_largeur, taille_max_hauteur)

def dessine_donjon(donjon):
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    
    # Calculer la taille optimale des salles pour ce donjon
    taille_salle = calcule_taille_salle(donjon)
    
    # Calculer la taille totale du donjon
    largeur_donjon = nb_colonnes * taille_salle
    hauteur_donjon = nb_lignes * taille_salle
    
    # Centrer le donjon horizontalement et verticalement (en tenant compte de l'aide)
    offset_x = (LARGEUR_FENETRE - largeur_donjon) // 2
    offset_y = (HAUTEUR_FENETRE - HAUTEUR_AIDE - hauteur_donjon) // 2

    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            x = offset_x + j * taille_salle
            y = offset_y + i * taille_salle
            dessine_salle(x, y, donjon[i][j], taille_salle)

def chemin_image_salle(salle):
    haut, droite, bas, gauche = salle
    return f"{DOSSIER_IMAGES}salle_{int(haut)}{int(droite)}{int(bas)}{int(gauche)}.png"

def code_salle(salle):
    haut, droite, bas, gauche = salle
    return f"{int(haut)}{int(droite)}{int(bas)}{int(gauche)}"

from fltk import image

def calcule_offset(donjon):
    """
    Calcule les offsets pour centrer le donjon.
    Retourne aussi la taille des salles pour ce donjon.
    """
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    taille_salle = calcule_taille_salle(donjon)
    largeur_donjon = nb_colonnes * taille_salle
    hauteur_donjon = nb_lignes * taille_salle
    offset_x = (LARGEUR_FENETRE - largeur_donjon) // 2
    offset_y = (HAUTEUR_FENETRE - HAUTEUR_AIDE - hauteur_donjon) // 2
    return offset_x, offset_y, taille_salle

def dessine_salle(x, y, salle, taille_salle):
    img = chemin_image_salle(salle)
    # Affiche l'image en haut à gauche
    image(x, y, img, largeur=taille_salle, hauteur=taille_salle, ancrage="nw")



def dessine_aventurier(aventurier, donjon):
    position = aventurier[0]
    niveau = aventurier[1]
    ligne, colonne = position
    
    offset_x, offset_y, taille_salle = calcule_offset(donjon)
    x = offset_x + colonne * taille_salle + taille_salle // 2
    y = offset_y + ligne * taille_salle + taille_salle // 2

    # Afficher l'image de l'aventurier (proportionnelle à la taille de la salle)
    chemin = DOSSIER_IMAGES + "aventurier.png"
    taille_av = int(taille_salle * 0.65)  # 65% de la taille de la salle
    image(x, y, chemin, largeur=taille_av, hauteur=taille_av, ancrage="center")

    # Afficher le niveau par-dessus
    offset_niveau = int(taille_salle * 0.25)
    rayon_cercle = max(10, int(taille_salle * 0.07))
    fltk.cercle(x, y - offset_niveau, rayon_cercle, couleur="white", remplissage="white")
    fltk.texte(x, y - offset_niveau, str(niveau), ancrage="center", couleur="black", taille=max(12, int(taille_salle * 0.14)))

    
def dessine_dragons(dragons, donjon):
    offset_x, offset_y, taille_salle = calcule_offset(donjon)
    for dragon in dragons:
        position = dragon[0]
        niveau = dragon[1]
        ligne, colonne = position

        x = offset_x + colonne * taille_salle + taille_salle // 2
        y = offset_y + ligne * taille_salle + taille_salle // 2

        chemin = DOSSIER_IMAGES + "dragon.png"

        # Image du dragon
        image(x, y, chemin, largeur=taille_salle, hauteur=taille_salle, ancrage="center")

        # Niveau au-dessus (proportionnel à la taille)
        offset_niveau = int(taille_salle * 0.28)
        rayon_cercle = max(10, int(taille_salle * 0.07))
        fltk.cercle(x, y + offset_niveau, rayon_cercle, couleur="white", remplissage="white")
        fltk.texte(x, y + offset_niveau, str(niveau), ancrage="center", couleur="black", taille=max(12, int(taille_salle * 0.14)))


def trouve_salle_cliquee(x_souris, y_souris, donjon):
    """
    Trouve quelle salle a été cliquée.
    """
    offset_x, offset_y, taille_salle = calcule_offset(donjon)
    
    # Calculer ligne et colonne à partir des pixels (en tenant compte de l'offset)
    colonne = (x_souris - offset_x) // taille_salle
    ligne = (y_souris - offset_y) // taille_salle
    
    # Vérifier que c'est dans les limites du donjon
    nb_lignes = len(donjon)
    nb_colonnes = len(donjon[0])
    
    if 0 <= ligne < nb_lignes and 0 <= colonne < nb_colonnes:
        return (ligne, colonne)
    else:
        return None

def dessine_intention(intention, donjon):
    """
    Dessine l'intention avec une ligne rouge lumineuse.
    """
    if len(intention) < 1:
        return
    
    offset_x, offset_y, taille_salle = calcule_offset(donjon)
    
    # Calculer les épaisseurs proportionnelles à la taille
    epaisseur_base = max(2, int(taille_salle * 0.05))
    
    for i in range(len(intention) - 1):
        pos1 = intention[i]
        pos2 = intention[i + 1]
        
        ligne1, col1 = pos1
        ligne2, col2 = pos2
        
        x1 = offset_x + col1 * taille_salle + taille_salle // 2
        y1 = offset_y + ligne1 * taille_salle + taille_salle // 2
        x2 = offset_x + col2 * taille_salle + taille_salle // 2
        y2 = offset_y + ligne2 * taille_salle + taille_salle // 2
        
        # Effet de lueur (ligne épaisse sombre)
        fltk.ligne(x1, y1, x2, y2, couleur='#8B0000', epaisseur=epaisseur_base + 4)
        # Ligne principale rouge vif
        fltk.ligne(x1, y1, x2, y2, couleur='#FF0000', epaisseur=epaisseur_base + 2)
        # Centre lumineux
        fltk.ligne(x1, y1, x2, y2, couleur='#FF6347', epaisseur=epaisseur_base)
    
    # Points aux extrémités
    rayon_point = max(4, int(taille_salle * 0.05))
    for i, pos in enumerate(intention):
        ligne, col = pos
        x = offset_x + col * taille_salle + taille_salle // 2
        y = offset_y + ligne * taille_salle + taille_salle // 2
        
        # Point avec effet de lueur
        fltk.cercle(x, y, rayon_point + 3, couleur='#8B0000', remplissage='#8B0000')
        fltk.cercle(x, y, rayon_point, couleur='#FF0000', remplissage='#FF0000')
        fltk.cercle(x, y, rayon_point - 3, couleur='#FF6347', remplissage='#FF6347')

def joue_tour_aventurier(aventurier, intention, dragons, donjon):
    """
    Fait jouer le tour de l'aventurier : il suit son intention.
    Puis les dragons se déplacent aléatoirement.
    
    :param aventurier: liste [position, niveau]
    :param intention: liste de positions à suivre
    :param dragons: liste des dragons
    :param donjon: la grille
    :return: "victoire", "defaite" ou "continue"
    """
    if len(intention) == 0:
        print("Pas d'intention définie !")
        return "continue"
    
    # ===== PHASE 1 : L'aventurier se déplace =====
    print("\n--- L'aventurier se déplace ---")
    for i in range(len(intention)):
        position_cible = intention[i]
        ligne_cible, col_cible = position_cible
        
        # Déplacer l'aventurier
        modele.deplace_aventurier(aventurier, ligne_cible, col_cible)
        print(f"Aventurier se déplace en ({ligne_cible}, {col_cible})")
        
        # Vérifier s'il y a un dragon ici
        dragon = modele.trouve_dragon(dragons, ligne_cible, col_cible)
        
        if dragon:
            print(f"Combat contre dragon niveau {dragon[1]} !")
            resultat = modele.combat(aventurier, dragon, dragons)
            
            if resultat:
                print(f"Dragon vaincu ! Aventurier niveau {aventurier[1]}")
                
                # Vérifier si tous les dragons sont morts (victoire)
                if modele.tous_dragons_morts(dragons):
                    print("🎉 VICTOIRE ! Tous les dragons sont morts !")
                    return "victoire"
            else:
                print("💀 DEFAITE ! L'aventurier est mort...")
                return "defaite"
    
    # ===== PHASE 2 : Les dragons se déplacent =====
    if len(dragons) > 0:
        print("\n--- Les dragons se déplacent ---")
        resultat_dragons = modele.deplace_dragons_aleatoire(dragons, donjon, aventurier)
        
        if not resultat_dragons:
            print("💀 DEFAITE ! Un dragon a rattrapé l'aventurier !")
            return "defaite"
        
        print("Les dragons ont bougé !")
    return "continue"


def affiche_menu():
    """
    Affiche un menu esthétique style donjon médiéval.
    :return: le choix du joueur (1, 2, 3) ou None si quitte
    """
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    choix = None
    
    while choix is None:
        fltk.efface_tout()
        
        # === FOND SOMBRE ===
        fltk.rectangle(0, 0, LARGEUR_FENETRE, HAUTEUR_FENETRE,
                      couleur='black', remplissage="#240101")
        
        # TITRE PRINCIPAL avec bordure
        # Ombre du titre
        fltk.texte(LARGEUR_FENETRE // 2 + 4, 84, "WALL IS YOU",
                   couleur='black', ancrage='center', taille=70)
        # Titre principal
        fltk.texte(LARGEUR_FENETRE // 2, 80, "WALL IS YOU",
                   couleur='#FF4500', ancrage='center', taille=70)
        
        # Sous-titre
        fltk.texte(LARGEUR_FENETRE // 2, 160, "Le Donjon des Dragons",
                   couleur='#FFD700', ancrage='center', taille=24)
        
        # LIGNE DÉCORATIVE
        fltk.ligne(150, 200, LARGEUR_FENETRE - 150, 200,
                  couleur='#FFD700', epaisseur=3)
        
        # TEXTE D'INSTRUCTIONS 
        fltk.texte(LARGEUR_FENETRE // 2, 240, "Choisissez votre quête :",
                   couleur='white', ancrage='center', taille=22)
        
        # BOUTON 1 : FACILE
        y1 = 300
        # Ombre
        fltk.rectangle(154, y1 + 4, 646, y1 + 74,
                      couleur='black', remplissage='black')
        # Bouton principal
        fltk.rectangle(150, y1, 650, y1 + 70,
                      couleur='#228B22', remplissage='#32CD32', epaisseur=4)
        # Icône
        fltk.cercle(200, y1 + 35, 20, couleur='white', remplissage='#90EE90')
        fltk.texte(200, y1 + 35, "1", couleur='#228B22', ancrage='center', taille=24)
        # Texte
        fltk.texte(250, y1 + 35, "Niveau 1 - Facile (4x4 - 1 Dragon)",
                   couleur='white', ancrage='w', taille=20)
        
        # BOUTON 2 : MOYEN
        y2 = 390
        fltk.rectangle(154, y2 + 4, 646, y2 + 74,
                      couleur='black', remplissage='black')
        fltk.rectangle(150, y2, 650, y2 + 70,
                      couleur='#FF8C00', remplissage='#FFA500', epaisseur=4)
        fltk.cercle(200, y2 + 35, 20, couleur='white', remplissage='#FFE4B5')
        fltk.texte(200, y2 + 35, "2", couleur='#FF8C00', ancrage='center', taille=24)
        fltk.texte(250, y2 + 35, "Niveau 2 - Moyen (5x5 - 2 Dragons)",
                   couleur='white', ancrage='w', taille=20)
        
        # === BOUTON 3 : DIFFICILE ===
        y3 = 480
        fltk.rectangle(154, y3 + 4, 646, y3 + 74,
                      couleur='black', remplissage='black')
        fltk.rectangle(150, y3, 650, y3 + 70,
                      couleur='#8B0000', remplissage='#DC143C', epaisseur=4)
        fltk.cercle(200, y3 + 35, 20, couleur='white', remplissage='#FFB6C1')
        fltk.texte(200, y3 + 35, "3", couleur='#8B0000', ancrage='center', taille=24)
        fltk.texte(250, y3 + 35, "Niveau 3 - Difficile (6x6 - 4 Dragons)",
                   couleur='white', ancrage='w', taille=20)
        
        # === INSTRUCTIONS EN BAS ===
        fltk.ligne(150, 580, LARGEUR_FENETRE - 150, 580,
                  couleur='#FFD700', epaisseur=2)
        fltk.texte(LARGEUR_FENETRE // 2, 610, "Appuyez sur 1, 2 ou 3 pour commencer",
                   couleur='#C0C0C0', ancrage='center', taille=18)
        fltk.texte(LARGEUR_FENETRE // 2, 640, "Fermez la fenêtre pour quitter",
                   couleur='#808080', ancrage='center', taille=14)
        
        # === DÉCORATION : Dragons aux coins ===
        # Dragon gauche
        fltk.cercle(50, 80, 25, couleur='#8B0000', remplissage='#DC143C')
        fltk.cercle(58, 75, 5, couleur='white', remplissage='yellow')
        fltk.cercle(42, 75, 5, couleur='white', remplissage='yellow')
        
        # Dragon droite
        fltk.cercle(LARGEUR_FENETRE - 50, 80, 25, couleur='#8B0000', remplissage='#DC143C')
        fltk.cercle(LARGEUR_FENETRE - 58, 75, 5, couleur='white', remplissage='yellow')
        fltk.cercle(LARGEUR_FENETRE - 42, 75, 5, couleur='white', remplissage='yellow')
        
        fltk.mise_a_jour()
        
        # Gérer les événements
        evenement = fltk.donne_ev()
        if evenement:
            type_ev = fltk.type_ev(evenement)
            
            if type_ev == 'Quitte':
                fltk.ferme_fenetre()
                return None
            
            elif type_ev == 'Touche':
                touche = fltk.touche(evenement)
                if touche == '1':
                    choix = 1
                elif touche == '2' :
                    choix = 2
                elif touche == '3':
                    choix = 3
    
    fltk.ferme_fenetre()
    return choix

def dessine_aide():
    """
    Affiche l'aide des touches en bas de l'écran.
    """
    y_base = HAUTEUR_FENETRE - 100
    
    # Fond
    fltk.rectangle(0, y_base, LARGEUR_FENETRE, HAUTEUR_FENETRE,
                   couleur='black', remplissage='lightblue', epaisseur=2)
    
    # Titre
    fltk.texte(LARGEUR_FENETRE // 2, y_base + 15, "COMMANDES",
               couleur='black', ancrage='center', taille=16)
    
    # Instructions ligne 1
    texte1 = "ClicGauche : Pivoter salle  |  Shift+ClicDroit : Tracer chemin (depuis aventurier)"
    fltk.texte(LARGEUR_FENETRE // 2, y_base + 40,
               texte1, couleur='black', ancrage='center', taille=11)
    
    # Instructions ligne 2
    texte2 = "ESPACE : Jouer tour  |  Z : Annuler dernier point  |  C : Effacer chemin"
    fltk.texte(LARGEUR_FENETRE // 2, y_base + 60,
               texte2, couleur='black', ancrage='center', taille=11)
    
    # Instructions ligne 3
    texte3 = "R : Recommencer donjon  |  ESC : Quitter"
    fltk.texte(LARGEUR_FENETRE // 2, y_base + 80,
               texte3, couleur='black', ancrage='center', taille=11)




def jeu():
    """
    Fonction principale du jeu avec menu.
    """
    choix = affiche_menu()
    
    if choix is None:
        print("Jeu quitté")
        return
    
    if choix == 1:
        donjon, aventurier, dragons = modele.cree_donjon_facile()
        print("Donjon facile chargé !")
    elif choix == 2:
        donjon, aventurier, dragons = modele.cree_donjon_moyen()
        print("Donjon moyen chargé !")
    elif choix == 3:
        donjon, aventurier, dragons = modele.cree_donjon_difficile()
        print("Donjon difficile chargé !")
    
    intention = []
    etat = "jeu"
    
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    
    continuer = True
    while continuer:
        fltk.efface_tout()
        
        dessine_donjon(donjon)
        dessine_dragons(dragons, donjon)
        dessine_aventurier(aventurier, donjon)
        dessine_intention(intention, donjon)
        dessine_aide()
        
        # Messages victoire/défaite
        if etat == "victoire":
            largeur_box = 650
            hauteur_box = 250
            x1 = (LARGEUR_FENETRE - largeur_box) // 2
            y1 = 150
            x2 = x1 + largeur_box
            y2 = y1 + hauteur_box
            
            fltk.rectangle(x1, y1, x2, y2, couleur='darkgreen', remplissage='lightgreen', epaisseur=20)
            fltk.texte(LARGEUR_FENETRE // 2, 220, "VICTOIRE !",
                       couleur='darkgreen', ancrage='center', taille=60)
            fltk.texte(LARGEUR_FENETRE // 2, 340, "Appuyez sur R pour recommencer",
                        couleur='black', ancrage='center', taille=18)
            fltk.texte(LARGEUR_FENETRE // 2, 370, "Fermez la fenêtre pour quitter",
                       couleur='black', ancrage='center', taille=18)
        
        elif etat == "defaite":
            largeur_box = 650
            hauteur_box = 250
            x1 = (LARGEUR_FENETRE - largeur_box) // 2
            y1 = 150
            x2 = x1 + largeur_box
            y2 = y1 + hauteur_box
            
            fltk.rectangle(x1, y1, x2, y2, couleur='darkred', remplissage='lightcoral', epaisseur=20)
            fltk.texte(LARGEUR_FENETRE // 2, 220, "DÉFAITE !",
                       couleur='darkred', ancrage='center', taille=60)
            fltk.texte(LARGEUR_FENETRE // 2, 340, "Appuyez sur R pour recommencer",
                       couleur='black', ancrage='center', taille=18)
            fltk.texte(LARGEUR_FENETRE // 2, 370, "ou ECHAP pour quitter",
                       couleur='black', ancrage='center', taille=18)
        
        fltk.mise_a_jour()
        
        evenement = fltk.donne_ev()
        if evenement:
            type_ev = fltk.type_ev(evenement)
            
            if type_ev == 'Quitte':
                fltk.ferme_fenetre()
                return
            
            # CLIC GAUCHE : Pivoter une salle
            elif type_ev == 'ClicGauche' and etat == "jeu":
                x_souris = fltk.abscisse(evenement)
                y_souris = fltk.ordonnee(evenement)
                
                salle_cliquee = trouve_salle_cliquee(x_souris, y_souris, donjon)
                
                if salle_cliquee:
                    ligne, colonne = salle_cliquee
                    modele.pivote_salle_donjon(donjon, ligne, colonne)
                    print(f"Salle ({ligne}, {colonne}) pivotée !")
            
            # CLIC DROIT : Tracer le chemin de déplacement (avec Shift)
            elif type_ev == 'ClicDroit' and etat == "jeu":
                x_souris = fltk.abscisse(evenement)
                y_souris = fltk.ordonnee(evenement)
                
                salle_cliquee = trouve_salle_cliquee(x_souris, y_souris, donjon)
                
                if salle_cliquee:
                    ligne, colonne = salle_cliquee
                    
                    # Vérifier si Shift est pressé pour ajouter au chemin
                    if fltk.touche_pressee('Shift_L') or fltk.touche_pressee('Shift_R'):
                        peut_ajouter = False
                        
                        # Premier point du chemin : doit être sur l'aventurier
                        if len(intention) == 0:
                            pos_aventurier = aventurier[0]
                            if (ligne, colonne) == pos_aventurier:
                                peut_ajouter = True
                            else:
                                print("⚠️ Le chemin doit commencer sur l'aventurier !")
                        else:
                            # Points suivants : vérifications de validité
                            derniere_pos = intention[-1]
                            ligne_prec, col_prec = derniere_pos
                            
                            if (ligne, colonne) in intention:
                                print("⚠️ Vous ne pouvez pas revenir sur le même chemin !")
                            else:
                                diff_ligne = abs(ligne - ligne_prec)
                                diff_col = abs(colonne - col_prec)
                                
                                # Vérifier adjacence
                                if (diff_ligne == 1 and diff_col == 0) or (diff_ligne == 0 and diff_col == 1):
                                    if modele.salles_connectees(donjon, ligne_prec, col_prec, ligne, colonne):
                                        peut_ajouter = True
                                    else:
                                        print("⚠️ Ces salles ne sont pas connectées !")
                                elif diff_ligne == 1 and diff_col == 1:
                                    print("⚠️ Pas de déplacement en diagonal !")
                                else:
                                    print("⚠️ La case doit être adjacente !")
                        
                        if peut_ajouter:
                            intention.append((ligne, colonne))
                            print(f"✅ Position ({ligne}, {colonne}) ajoutée")
            
            # TOUCHES CLAVIER
            elif type_ev == 'Touche':
                touche = fltk.touche(evenement)
                
                # ESPACE : Valider le déplacement
                if touche == 'space' and etat == "jeu":
                    print("\n=== Tour de l'aventurier ===")
                    resultat = joue_tour_aventurier(aventurier, intention, dragons, donjon)
                    
                    intention.clear()
                    
                    if resultat == "victoire":
                        etat = "victoire"
                    elif resultat == "defaite":
                        etat = "defaite"
                
                # Z : Annuler le dernier point
                elif (touche == 'z' or touche == 'Z') and etat == "jeu":
                    if len(intention) > 0:
                        intention.pop()
                        print(f"↩️ Dernier point annulé !")
                
                # C : Effacer tout le chemin
                elif (touche == 'c' or touche == 'C') and etat == "jeu":
                    intention.clear()
                    print("🗑️ Chemin effacé !")
                
                # R : Recommencer
                elif touche == 'r' or touche == 'R':
                    print("Redémarrage...")
                    if choix == 1:
                        donjon, aventurier, dragons = modele.cree_donjon_facile()
                    elif choix == 2:
                        donjon, aventurier, dragons = modele.cree_donjon_moyen()
                    elif choix == 3:
                        donjon, aventurier, dragons = modele.cree_donjon_difficile()
                    intention.clear()
                    etat = "jeu"
                
                # ESCAPE : Quitter
                elif touche == 'Escape':
                    print("Fermeture du jeu...")
                    fltk.ferme_fenetre()
                    return
    
    fltk.ferme_fenetre()


if __name__ == "__main__":
    jeu()