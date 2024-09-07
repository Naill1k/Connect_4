from settings import *

VIDE = '.'  # Symbôle d'une case vide
JOUEURS = ('O', 'X')  # Symbôles des 2 joueurs

profondeur_max = 6  # La profondeur de recherche (automatiquement ajustée)
tableau_de_jeu = [ [VIDE for j in range(NOMBRE_DE_COLONNES)] for i in range(NOMBRE_DE_LIGNES)]
nb_vus = 0    # Nombre de positions parcourues (pour savoir quand augmenter la profondeur)


def ordre_col() :
    '''
    Renvoie l'ordre dans lequel les colonnes seront parcourues par l'ordi : du milieu vers l'extérieur
    '''
    milieu = (NOMBRE_DE_COLONNES-1)//2
    L = [milieu]
    for i in range(1,NOMBRE_DE_COLONNES) :  # On sortira toujours de la boucle avant la fin
        
        if milieu+i < NOMBRE_DE_COLONNES :
            L.append(milieu + i)
        else :
            break
        
        if milieu-i >= 0 :
            L.append(milieu - i)
        else :
            break
    return L            
    
ORDRE = ordre_col()  # Ordre dans lequel on parcours les colonnes


def joueur_gagnant(t):
    """
    Renvoie le symbole du joueur gagnant ou '' s'il n'y a pas de gagnant pour la partie qui est dans le tableau
    """
    # Détection sur lignes
    for ligne in t :
        for c in range(NOMBRE_DE_COLONNES-3) :

            if ligne[c] == ligne[c+1] == ligne[c+2] == ligne[c+3] != VIDE :
                return ligne[c]

    # Détection sur colonnes
    for l in range(NOMBRE_DE_LIGNES-3) :
        for c in range(NOMBRE_DE_COLONNES) :

            if t[l][c] == t[l+1][c] == t[l+2][c] == t[l+3][c] != VIDE :
                return t[l][c]

    # Détection sur les diagonales
    for l in range(NOMBRE_DE_LIGNES-3) :
        for c in range(NOMBRE_DE_COLONNES-3) :

            if t[l][c] == t[l+1][c+1] == t[l+2][c+2] == t[l+3][c+3] != VIDE :
                return t[l][c]

            if t[-l-1][c] == t[-l-2][c+1] == t[-l-3][c+2] == t[-l-4][c+3] != VIDE :
                return t[-l-1][c]

    return ''



def colonne_jouable(t, i):
    '''
    Renvoie un booléen qui est True si la colonne est jouable (lève une exception si la colonne n'existe pas)
    '''
    if i is None :
        raise TypeError('Le n° de colonne est None !')
    if i<0 or i>NOMBRE_DE_COLONNES :
        raise ValueError('Numéro de colonne invalide')    # On vérifie que le numéro de colonne est valide

    else :
        return t[0][i] == VIDE


def encore_au_moins_une_colonne_jouable(t):
    '''
    Renvoie un booléen qui est True si il y a encore au moins une colonne jouable pour la partie qui est dans le tableau
    '''
    for i in range(NOMBRE_DE_COLONNES) :    # On parcourt toutes les colonnes
        if colonne_jouable(t, i) :    # On regarde si au moins une colonne est libre
            return True
    return False


def liste_des_colonnes_jouables(t):
    '''
    Renvoie une liste contenant les numéros des colonnes qui sont jouables
    '''
    colonnes = []    # Liste contenant les numéros des colonnes jouables
    for i in ORDRE :
        if colonne_jouable(t, i):    # Si une colonne est jouable,
            colonnes.append(i)       # On l'ajoute à la liste
    return colonnes





def il_y_a_un_gagnant(t):
    '''
    Renvoie un booléen qui est vrai s'il y a un gagnant pour la partie qui est dans le tableau
    '''
    return joueur_gagnant(t) != ''


def partie_terminee(t):
    '''
    Renvoie un booléen qui est True si la partie qui est dans le tableau est terminée
    '''
    return il_y_a_un_gagnant(t) or not encore_au_moins_une_colonne_jouable(t)


def pose_pion(tableau, numero_du_joueur, c):
    '''
    Pose un pion dans la colonne c à partir du tableau de jeu "tableau".
    Entrée : un tableau de jeu, le numéro du joueur (0 ou 1) et le numéro de la colonne
    Sortie : UN NOUVEAU TABLEAU DE JEU avec le pion posé au bon endroit
    '''
    # On commence par faire une copie du tableau
    nouveau_tableau = [[tableau[i][j] for j in range(NOMBRE_DE_COLONNES)] for i in range(NOMBRE_DE_LIGNES)]
    if c is None : print('pose_pion')
    if not colonne_jouable(nouveau_tableau, c) :
        raise ValueError('Colonne non jouable !')

    l = 0
    while l<NOMBRE_DE_LIGNES-1 and nouveau_tableau[l+1][c] == VIDE :
        l += 1
    nouveau_tableau[l][c] = JOUEURS[numero_du_joueur]
    return nouveau_tableau # on renvoie le tableau avec le pion posé




Infini = 1024    # Utilisé pour le score d'une victoire (ou une défaite) ou comme score de base
def minimax(tableau, profondeur, maximiser = True, alpha = -Infini, beta = Infini) :
    '''
    Calcule le meilleur coup estimé

    profondeur : La profondeur jusqu'à laquelle on regardera (nb de coups à l'avance)
    maximiser : Booléen, True si le joueur cherche à maximiser les points (True pour l'ordi, False pour l'humain)

    Renvoie un tuple contenant le score maximum pouvant être atteint et le numéro de la colonne à jouer (score max, colonne à jouer)
    '''
    global nb_vus
    nb_vus += 1
    
    # Si on ne va pas plus profond, la fonction renvoie l'évaluation de la position
    if profondeur == 0 or partie_terminee(tableau) :
        return (évaluer(tableau), None)    # Si None arrive au toplevel c'est que la partie est terminée


    if maximiser :  # Si c'est l'ordi qui joue il cherche donc à maximiser son score
        score_max = (-2*Infini, None)  # N'importe quel score sera inférieur
        for tab,col in liste_fils(tableau, 1) :  # Pour chacun des fils de la forme (tableau, n°colonne)
            
            score_fils = (minimax(tab, profondeur-1, False, alpha, beta)[0], col)
            if score_fils[0] > score_max[0] :
                score_max = score_fils
            
            # Elagage alpha/beta
            alpha = max(score_fils[0], alpha)
            if beta <= alpha :
                break

        return score_max  # De la forme (score max, colonne à jouer)


    else : # Sinon c'est au tour de l'humain
        score_min = (2*Infini, None)  # N'importe quel score sera supérieur
        for tab,col in liste_fils(tableau, 0) :  # Pour chacun des fils (tableau, nb colonne)
            
            score_fils = (minimax(tab, profondeur-1, True, alpha, beta)[0], col)
            if score_fils[0] < score_min[0] :
                score_min = score_fils
            
            # Elagage alpha/beta
            beta = min(score_fils[0], beta)
            if beta <= alpha :
                break

        return score_min    # De la forme (score min, colonne à jouer)




def liste_fils(tableau, joueur):
    '''
    Renvoie une liste de tuples contenant le nouveau tableau de jeu et la colonne jouée : [(tableau, colonne jouée), ...]
    
    joueur : Le numéro du joueur qui doit jouer
    '''
    fils = []
    for i in liste_des_colonnes_jouables(tableau) :
        fils.append( (pose_pion(tableau, joueur, i), i) )
    return fils



def sentinelle(t,l,c) :
    '''
    Evite les erreurs d'indices
    '''
    if l<0 or c<0 or l>=NOMBRE_DE_LIGNES or c>=NOMBRE_DE_COLONNES :
        return VIDE
    else :
        return t[l][c]



def évaluer(tableau) :
    '''
    Renvoie le score du tableau (score ordi - score joueur)
    '''
    t = [ligne.copy() for ligne in tableau]    # On fait une copie du tableau

    score = {JOUEURS[0]:0, JOUEURS[1]:0}    # Dictionnaire contenant les scores de chaque joueur (humain et ordi)

    score[joueur_gagnant(t)] = Infini

    for l in range(NOMBRE_DE_LIGNES) :
        for c in range(NOMBRE_DE_COLONNES) :
            if t[l][c] != VIDE :
                # On incite l'ordi à jouer vers le centre
                score[t[l][c]] -= 2*( abs(l-NOMBRE_DE_LIGNES//2) + abs(c-NOMBRE_DE_COLONNES//2) )

            # Calcul du score pour les pions alignés horizontalement
                if sentinelle(t, l, c+1) == t[l][c] :    # Si 2 pions sont alignés de gauche à droite
                    if sentinelle(t, l, c+2) == t[l][c] : # Si un 3ème est aligné
                        score[t[l][c]] += 16    # On donne beaucoup de points
                        if sentinelle(t, l, c-1) != VIDE :    # Si la case deriière est occupée
                            score[t[l][c]] -= 8    # On enlève des points
                        if sentinelle(t, l, c+3) != VIDE :    # Pareil pour celle d'après
                            score[t[l][c]] -= 8    # ...

                    else :    # Si il n'y a que 2 pions alignés
                        score[t[l][c]] += 6    # Pareil qu'au-dessus
                        if sentinelle(t, l, c-1) != VIDE :
                            score[t[l][c]] -= 3
                        if sentinelle(t, l, c+2) != VIDE :
                            score[t[l][c]] -= 3


                #    Calcul du score pour les pions alignés verticalement
                if sentinelle(t, l+1, c) == t[l][c] :    # Si 2 pions sont alignés de haut en bas

                    if sentinelle(t, l+2, c) == t[l][c] : # Si un 3ème est aligné
                        score[t[l][c]] += 16    # On donne beaucoup de points
                        if sentinelle(t, l-1, c) != VIDE :    # Si la case deriière est occupée
                            score[t[l][c]] -= 8    # On enlève des points
                        if sentinelle(t, l+3, c) != VIDE :    # Pareil pour celle d'après
                            score[t[l][c]] -= 8    # ...

                    else :    # Si il n'y a que 2 pions alignés
                        score[t[l][c]] += 6    # Pareil qu'au-dessus
                        if sentinelle(t, l-1, c) != VIDE :
                            score[t[l][c]] -= 3
                        if sentinelle(t, l+2, c) != VIDE :
                            score[t[l][c]] -= 3


                #    Calcul du score pour les pions alignés en diagonal
                if sentinelle(t, l+1, c+1) == t[l][c] :    # Si 2 pions sont alignés d'en haut à gauche à en bas à droite

                    if sentinelle(t, l+2, c+2) == t[l][c] : # Si un 3ème est aligné
                        score[t[l][c]] += 16    # On donne beaucoup de points
                        if sentinelle(t, l-1, c-1) != VIDE :    # Si la case deriière est occupée
                            score[t[l][c]] -= 8    # On enlève des points
                        if sentinelle(t, l+3, c+3) != VIDE :    # Pareil pour celle d'après
                            score[t[l][c]] -= 8    # ...

                    else :    # Si il n'y a que 2 pions alignés
                        score[t[l][c]] += 6    # Pareil qu'au-dessus
                        if sentinelle(t, l-1, c-1) != VIDE :
                            score[t[l][c]] -= 3
                        if sentinelle(t, l+2, c+2) != VIDE :
                            score[t[l][c]] -= 3


            #    Calcul du score pour les pions alignés dans l'autre diagonal
            if t[l][c] != VIDE and sentinelle(t, l-1, c+1) == t[l][c] :    # Si 2 pions sont alignés d'en haut à droite à en bas à gauche(maybe🤷‍♂️)

                if sentinelle(t, l-2, c+2) == t[l][c] : # Si un 3ème est aligné
                    score[t[l][c]] += 16    # On donne beaucoup de points
                    if sentinelle(t, l+1, c-1) != VIDE :    # Si la case deriière est occupée
                        score[t[l][c]] -= 8    # On enlève des points
                    if sentinelle(t, l-3, c+3) != VIDE :    # Pareil pour celle d'après
                        score[t[l][c]] -= 8    # ...

                else :    # Si il n'y a que 2 pions alignés
                    score[t[l][c]] += 6    # Pareil qu'au-dessus
                    if sentinelle(t, l+1, c-1) != VIDE :
                        score[t[l][c]] -= 3
                    if sentinelle(t, l-2, c+2) != VIDE :
                        score[t[l][c]] -= 3


    return score[JOUEURS[1]] - score[JOUEURS[0]]


def ordi(tableau):
    global profondeur_max,nb_vus
    nb_vus = 0    # Reset du compteur
    score,colonne = minimax(tableau, profondeur_max)
    tableau = pose_pion(tableau, 1, colonne)
    
    # On adapte la profondeur de recherche en fonction
    # du nombre de positions parcourues à la dernière exécution
    if nb_vus < 25000 :
        profondeur_max += 1
    elif nb_vus > 125000 :
        profondeur_max -= 2
    elif nb_vus > 75000 :
        profondeur_max -= 1
    

    print()
    print(f'Score : {score} | Colonne jouée : {colonne} | Nb_vus : {nb_vus} | Profondeur : {profondeur_max}')
    return tableau