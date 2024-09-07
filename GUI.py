import tkinter as tk

from settings import *
from game_engine import *


COULEURS = {0 : 'red', 1 : 'yellow', JOUEURS[0] : 'rouges', JOUEURS[1] : 'jaunes'}
fin_partie = False

root = tk.Tk()
root.title('Puissance 4')
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.quit())
Dessin = tk.Canvas(root, bg='black')

Largeur = root.winfo_screenwidth()
Hauteur = Dessin.winfo_screenheight()

Dessin.pack(fill=tk.BOTH, expand=True)


class Etat() :
    def __init__(self) :
        self.arrière_plan = 'black'
        self.couleur = 'blue'
        self.NB_LIGNES = NOMBRE_DE_LIGNES
        self.NB_COL = NOMBRE_DE_COLONNES
        self.largeur_case = Largeur/self.NB_COL
        self.hauteur_case = Hauteur/(self.NB_LIGNES +1)
        self.taille_rond = 4*self.hauteur_case/5
        
        self.affichage()


    def affichage(self) :
        global fin_partie
        Dessin.delete('all')

        Dessin.create_rectangle(0,0, Largeur,Hauteur,fill=self.arrière_plan)
        Dessin.create_rectangle(0,self.hauteur_case,Largeur,Hauteur,fill=self.couleur)
        for l in range(self.NB_LIGNES) :
            for c in range(self.NB_COL) :
                forme = tableau_de_jeu[l][c]
                
                if   forme == '.' : couleur = self.arrière_plan
                elif forme == 'O' : couleur = 'red'
                elif forme == 'X' : couleur = 'yellow'
                
                x = c*self.largeur_case + self.largeur_case/2
                y = (l+1)*self.hauteur_case + self.hauteur_case/2
                disque(x, y, self.taille_rond, couleur)
        
        if partie_terminee(tableau_de_jeu) :
            fin_partie = True
            if joueur_gagnant(tableau_de_jeu) == '' :
                t = 'Partie nulle'
            else :
                t = f'Gagnant : {COULEURS[joueur_gagnant(tableau_de_jeu)]}'
                
            Dessin.create_text(int(Largeur/2),int(état.hauteur_case/2),text=t,fill='white',font=('',42))
        
        
    def afficher_jeton(self,event) :
        Dessin.create_rectangle(0,0, Largeur,self.hauteur_case, fill=self.arrière_plan)
        self.affichage()
        x = event.x//self.largeur_case * self.largeur_case + self.largeur_case/2
        y = self.hauteur_case/2
        disque(x, y, self.taille_rond, COULEURS[tour])


def disque(x,y,r,coul) :
    Dessin.create_oval(x-r/2,y-r/2, x+r/2,y+r/2, fill=coul, outline='')



def clic(event) :
    '''
    Fonction appelée à chaque clic de souris
    '''
    global tour, tableau_de_jeu
    if not fin_partie :
        if  not (tour == 1 and NB_JOUEURS == 1) :  # Si ce n'est pas à l'ordi de jouer (on ne peut pas jouer pour elle en cliquant)
            colonne = int(event.x//état.largeur_case)  # On récupèr ele numéro de la colonne cliquée
            if colonne_jouable(tableau_de_jeu, colonne) :  # Si la colonne est jouable (pas pleine
                tableau_de_jeu = pose_pion(tableau_de_jeu, tour, colonne)  # On pose le jeton dans la colonne
                tour = abs(tour-1)  # On change le tour de jeu
                état.affichage()  # Et on affiche à l'écran le nouveau tableau de jeu
                
                

état = Etat()

root.bind('<Motion>', état.afficher_jeton)
root.bind('<Button-1>',clic)


def tick() :
    global tableau_de_jeu, tour
    if tour == 1 : # Tour du second joueur / de l'ordi
        if NB_JOUEURS == 1 and not partie_terminee(tableau_de_jeu) : # Si c'est à l'ordi de jouer (et pas au 1er joueur)
            tableau_de_jeu = ordi(tableau_de_jeu)
            tour = 0
            état.affichage()
    
    Dessin.after(100,tick)
    

tick()
root.mainloop()