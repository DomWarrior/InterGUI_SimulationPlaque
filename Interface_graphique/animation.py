import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox



class TempératurePlaque:
    def température_initiale(self):
        return np.ones((1,1))*300
    


class FenêtreAnimations:

    '''Cette classe  correspondre à la fênêtre de droite que l'utilisateur va voir en ouvrant l'interface. 
    Cette fenêtre va être divisé en 2 sous-fenêtres afin d'offrir la possibilité d'afficher 2 graphiques simultanément. Ces fenêtres vont permettre d'affichier des graphiques (la réponse à l'échelon
    des trois thermistances et l'énergie thermique interne de la plaque) et des animations (carte thermique 2D et 3D dans la plaque).
    Cette classe va également gérer toutes les fonctionnalités offertes à l'utilisateur en lien les graphiques et les animations
    '''

    def __init__(self, fenêtre_main, controlleur):
        self.fenêtre_main = fenêtre_main             #Cette instance correspond à la fenêtre de gauche de l'interface où est-ce que l'utilisateur va entrer les données afin de contrôleur les données. On va vouloir s'en servir pour savoir ce que l'utilisateur veut afin d'ajuster les animations/graphiques en conséquences
        self.controlleur = controlleur               #Cette instance va permettre de contrôleur la simulation en y stockant les informations , paramètres ...

        self.fenêtre = ttk.PanedWindow(fenêtre_main, orient=tk.VERTICAL)  #ici on divise verticalement la fênêtre pricipale en 2 (on va obtenir 2 sous-fenêtres)
        self.fenêtre.pack(fill=tk.BOTH,expand=True)                         # On empile les 2 sous-fenêtre l'une sur l'autre et de sorte que l'entièreté de la fenêtre_main soit recouverte


        #division de la fenêtre
        self.fenêtre_top = ttk.Frame(self.fenêtre)                      #sous-fenêtre du dessus                      
        self.fenêtre.add(self.fenêtre_top, weight=50)                   #qui va initialement correspond à 50% en poid/taille de la fenêtre initiale

        self.fenêtre_bottom = ttk.Frame(self.fenêtre)                      #sous-fenêtre du dessous
        self.fenêtre.add(self.fenêtre_bottom, weight=50)


        # Instances pour les graphiques et animations

        self.créer_graphiques() = None                                  #instances qui va s'occuper de créer tous les graphiques (la forme)
        self.initialiser_graphiques() = None                              #instances qui va initilaliser les graphiques que l'utilisateur aura sélectionnés

        self.bc_carte_2D_top = None                                     #instances qui va contenir la barre de couleur lors de l'animation de la carte thermique 2D dans la fenêtre du haut. On crée une instance pour cela car celle-ci sera amené à évoluer au cours du temps.
        self.bc_carte_3D_bottom = None                                  #barre de couleur carte thermique 3D sous-fenêtre du haut.
        self.bc_carte_2D_top = None                                     #barre de couleur carte thermique 2D sous-fenêtre du bas.
        self.bc_carte_3D_bottom = None                                  #barre de couleur carte thermique 3D sous-fenêtre du bas.


        self.animation1 = None                                          #instance qui va stocker l'animation de la sous-fenêtre du haut
        self.animation2 = None                                          #instance qui va stocker l'animation de la sous-fenêtre du bas


    def créer_graphiques(self):
        '''
        Fonction qui va créer la mise en forme de tous les graphiques (graphiques vide) 
        '''

        #Figures, graphiques et animations qui seront affichés dans la sous-fenêtre du dessus

        #Figure pour la carte 2D thermique
        self.fig_carte_2D = Figure(figsize= (6, 5), dpi=100)  #figure matplotlib de 6x5 pouces avec une résolution de 100 points par pouce pour l'animation de la carte thermique 2D
        self.ax_carte_2D = self.fig_carte_2D.add_subplot(111)  #....
        self.canvas_carte_2D = FigureCanvasTkAgg(self.fig_carte_2D, master= self.fenêtre_top)   # Ici, on intègre la figure dans un widget Tkinter afin de pouvoir l'ajouter/afficher dans l'interface Tkinter et on l'associe à la sous-figure du dessus 

        #Figure pour la carte 3D thermique
        self.fig_carte_3D = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_3D = self.fig_thermal_3d.add_subplot(111, projection='3d')
        self.canvas_carte_3D = FigureCanvasTkAgg(self.fig_carte_3D, master=self.fenêtre_top)


        #Figure pour le graphique qui contient la réponse en température des thermistances en fonction du temps
        self.fig_temp = Figure(figsize=(6, 5), dpi=100)
        self.ax_temp = self.fig_temp.add_subplot(111)
        self.ax_temp.set_xlabel("Temps (s)")
        self.ax_temp.set_ylabel("Température (°C)")
        self.ax_temp.set_title("Évolution des températures")
        self.ax_temp.grid(True)
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.fenêtre_top)

        #Figure pour le graphique qui montre l'énergie thermique interne dans la plaque en fonction du temps
        self.fig_energy = Figure(figsize=(6, 5), dpi=100)
        self.ax_energy = self.fig_energy.add_subplot(111)
        self.ax_energy.set_xlabel("Temps (s)")
        self.ax_energy.set_ylabel("Énergie interne (J)")
        self.ax_energy.set_title("Évolution de l'énergie themique interne")
        self.ax_energy.grid(True)
        self.canvas_energy = FigureCanvasTkAgg(self.fig_energy, master=self.fenêtre_top)


        #Tout ce qui a ci-dessus est pour la sous-figure du dessus. On doit refaire exactement la même chose , mais pour la sous-figure du bas
        #Figure pour la carte 2D thermique
        self.fig_carte_2D = Figure(figsize= (6, 5), dpi=100)  #figure matplotlib de 6x5 pouces avec une résolution de 100 points par pouce pour l'animation de la carte thermique 2D
        self.ax_carte_2D = self.fig_carte_2D.add_subplot(111)  #....
        self.canvas_carte_2D = FigureCanvasTkAgg(self.fig_carte_2D, master= self.fenêtre_bottom)   # Ici, on intègre la figure dans un widget Tkinter afin de pouvoir l'ajouter/afficher dans l'interface Tkinter et on l'associe à la sous-figure du dessus 

        #Figure pour la carte 3D thermique
        self.fig_carte_3D = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_3D = self.fig_thermal_3d.add_subplot(111, projection='3d')
        self.canvas_carte_3D = FigureCanvasTkAgg(self.fig_carte_3D, master=self.fenêtre_bottom)


        #Figure pour le graphique qui contient la réponse en température des thermistances en fonction du temps
        self.fig_temp = Figure(figsize=(6, 5), dpi=100)
        self.ax_temp = self.fig_temp.add_subplot(111)
        self.ax_temp.set_xlabel("Temps (s)")
        self.ax_temp.set_ylabel("Température (°C)")
        self.ax_temp.set_title("Évolution des températures")
        self.ax_temp.grid(True)
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.fenêtre_bottom)

        #Figure pour le graphique qui montre l'énergie thermique interne dans la plaque en fonction du temps
        self.fig_energy = Figure(figsize=(6, 5), dpi=100)
        self.ax_energy = self.fig_energy.add_subplot(111)
        self.ax_energy.set_xlabel("Temps (s)")
        self.ax_energy.set_ylabel("Énergie interne (J)")
        self.ax_energy.set_title("Évolution de l'énergie themique interne")
        self.ax_energy.grid(True)
        self.canvas_energy = FigureCanvasTkAgg(self.fig_energy, master=self.self.fenêtre_bottom)


        '''
        Définissons maintenant les fonctions qui permettrons de gérer les actions (contenu dans la 2e fenêtre de l'interface)de l'utilisateur en lien avec le contrôle des graphiques et animations, c'est-à-dire:
            -afficher les bons graphiques dans les bonnes sous-fenêtres
            -lancer la simulation
            -mettre la simulation sur pause
            -permettre de modifier les paramètres pendant que l'animation est sur pause et pouvoir relancer avec ces nouveaux paramètres
            -arrêter la simulation
            -réinitialiser la simulation
            -effectuer la simulation/générer les graphiques et animationw
            -

        '''
    