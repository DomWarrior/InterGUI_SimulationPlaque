
#https://docs.python.org/3/library/tkinter.messagebox.html       #Documentation pour messagox
#https://docs.python.org/3/library/tkinter.ttk.html              #Documentation pour les wigets ttk
#https://docs.python.org/3/library/tkinter.ttk.html#notebook     #Documentation pour Notebook
#https://stackoverflow.com/questions/28089942/difference-between-fill-and-expand-options-for-tkinter-pack-method     #Documentation pour la position des éléments
















import tkinter as tk                                                                                                        #Importation de la bibliothèque tkinter qui va permettre de créer l'interface graphique       
from tkinter import ttk, messagebox, filedialog                                                                             #Importation de la bibliothèque ttk qui va permettre de créer des widgets tkinter plus avancés (ttk = themed tk)         
                                                       

import matplotlib.pyplot as plt                     
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg                                                             # FigureCanvasTkAgg est une classe qui permet d'intégrer des graphiques matplotlib dans une interface Tkinter        
from matplotlib.figure import Figure                                                                

from simulation_temp import TempératurePlaque                                                                               #Importation de la classe TempératurePlaque qui va permettre de modéliser l'évolution de la température dans la plaque (fichier simulation_temp.py)                   
from animation import FenêtreAnimations                                                                                     #Importation de la classe FenêtreAnimations qui va permettre de créer les animations 2D et 3D (fichier animation.py)
from fonctionnalités_interface import sauvegarder_paramètres_json, charger_paramètres_json, sauvegarder_résultats_txt       #Importation des fonctions dans fonctionnalités_interface.py qui va permettre de sauvegarder et charger les paramètres de la simulation et les résultats de la simulation dans un fichier texte ou json
import numpy as np
import time



class FenêtreInterface:
    '''
    Cette classe va créer l'interface graphique de la simulation thermique de la plaque.
    Elle va contenir les différentes pages et onglets qui vont permettre de modifier les paramètres de la simulation, de lancer la simulation et de visualiser les résultats.
    '''



    def __init__(self, f_interface):
        '''
        Initialisation de la classe FênetreInterface. C'est ici qu'on crée les instances utiles pour gérer l'interface graphique et la simulation thermique de la plaque.
        '''


        self.f_interface = f_interface                                                  #création d'une instance qui va représenter la fenêtre principal de l'interface graphique (Tkinter)
        self.f_interface.title("Simulation Thermique de la plaque")                     #Titre de la fenêtre Tkinter                                                        
        self.f_interface.geometry("1280x800")                                           #Taille initiale de la fenêtre lorsque l'utilisateur va lancer l'interface


        self.simulation_thermique = TempératurePlaque()                                 # on crée une instance qui va contenir la fonction qui modélise l'évolution de la température dans la plaque présent dans le fichier simulation.py 
        
        
        self.style = ttk.Style()                                                        #permet d'accéder aux thèmes disponibles et qui va permettre de configurer le style de la fenêtre
        self.style.theme_use('clam')                                                    # thème choisi

        couleur_fond = "#f5f5f5"                                                        #couleur de fond de la fenêtre  "#f5f5f5"       #
        couleur_entete = "#e0e0e0"                                                      #couleur des en-têtes
        couleur_cadre = "#e0e0e0"                                                       #couleur du cadre de la fenêtre


        

        #Ici on prédifini la couleur et le style d'écriture qui sera utiliser pour les différentes parties (widgets) de l'interface (page,onglet,calligraphie, ...).

        self.style.configure('Cadre.TFrame', background=couleur_cadre)
        self.style.configure('EnTete.TFrame', background=couleur_entete)
        self.style.configure('EnTete.TLabel', background=couleur_entete, font=('Arial', 11, 'bold'))
        self.style.configure('Section.TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('Etiquette.TLabel', background=couleur_cadre, font=('Arial', 9))
        self.style.configure('Bouton.TButton', font=('Arial', 9))
        self.style.configure('Champ.TEntry', font=('Arial', 9))
        self.f_interface.configure(bg=couleur_fond)                                                                     


    
        self.initialisation_donnees_simulation()                                          #instance qui va initialise les données de la simulation
        self.creer_variables()                                                            #instance qui va créer toutes les variables
        self.creer_interface()                                                            #instance qui va créer l'interface

        self.temps_debut_chrono = None                                                    # Instance rajouté pour gérer le chronomètre de la simulation
        self.temps_ecoule_total = 0
        self.chronometre_run = False



    def initialisation_donnees_simulation(self):
        '''
        Cette méthode va s'occuper d'initialiser les variables qui va permettre de contrôleur la simulation et de récolter les données de la simulation
        '''
        self.commande_ac = []                                               #Va stocker les valeurs du courant injecté dans l'actuateur au cours du temps
        self.commande_pert = []                                             #Va stocker les valeurs de la puissance de la perturbation au cours du temps               
        self.compteur = 0                                                   #va servir pour le nombre d'itération 
        self.temp_therm_1 = []                                              #liste qui va contenir les températures au cours du temps de la thermistance 1
        self.temp_therm_2 = []                                              #liste qui va contenir les températures au cours du temps de la thermistance 2 
        self.temp_therm_laser = []                                          #liste qui va contenir les températures au cours du temps  de la thermistance où centre de la plaque
        self.energie_list = []                                              #liste qui va contenir l'énergie thermique interne dans la plaque au cours du temps
        self.temps_courant = 0                                              #va servir pour compter le temps écouler depuis le début de la simulation afin de pouvoir mettre l'option d'appliquer la puissance à un instant t>0 durant la simulation
        self.compter_frame = 0                                              #va servir pour compter le nombre de frame lors des animations
        self.simulation_run = False                                         #permet de savoir si la simulation est en cours ou non
        self.simulation_paused = False                                      #permet de avoir si la simulation est en pause où non
        self.anim1 = None                                                   # cet instance va permettre de stocker l'animation qui sera afficher dans le sous-fenêtre du haut du panneau de visualisation 
        self.anim2 = None                                                   #même chose, mais pour celle du bas
        self.T = None                                                       #Matrice de la température dans la plaque




    def creer_variables(self):
        '''
        Cette fonction va créer et convertir tous les paramètres initiale du simulateur en variable tkinker afin de pourvoir les utiliser par l'interface Tkinter. 
        Toutes les valeurs (value=...) ici seront les valeurs par défaut affichées lors du lancement de l'interface.
        ''' 
        # Propriétés thermiques de la plaque
        self.var_k = tk.IntVar(value=167)                                   #conductivité thermique du matériau (W/mK)
        self.var_p = tk.IntVar(value=2700)                                  #densité du matériau (kg/m³)
        self.var_cp = tk.IntVar(value=900)                                  #capacité thermique du matériau (J/kgK)
        self.var_T_plaque = tk.DoubleVar(value=25)                          #température initiale de la plaque (C)
        
        
        # Dimensions de la plaque
        self.var_Lx = tk.DoubleVar(value=0.061)                             #Largeur de la plaque x (m)
        self.var_Ly = tk.DoubleVar(value=0.117)                             #Longueur de la plaque y (m)
        self.var_e = tk.DoubleVar(value=0.00165)                            #épaisseur de la plaque (m)
        
        # Proprités thermique de l'air ambiant
        self.var_T_air = tk.DoubleVar(value=25)                             #température de l'air ambiant (C)
        self.var_h = tk.DoubleVar(value=12.2)                               #coefficient de convection entre l'air et la plaque (W/m²K)
        
        # Discrétisation de la matrice
        self.var_n_x = tk.IntVar(value=61)                                  #Nombre d'éléments de la matrice en x 
        self.var_n_y = tk.IntVar(value=117)                                 #Nombre d'éléments de la matrice en y
        
        # Variables pour la simulation
        self.var_current = tk.DoubleVar(value=0.5)                          #Courant injecté dans l'actuateur (A)
        self.var_temps_simulation = tk.DoubleVar(value=500)                 #temps total de la simulation (s)
        self.var_t_ac = tk.DoubleVar(value=0)                               #temps à lequel on veut appliquer le courant dans l'actuateur (s) 
        self.var_pos_ac_x = tk.IntVar(value=30)                             #position verticale du centre de l'actuateur par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_ac_y = tk.IntVar(value=15)                             #position horizontale du centre de l'actuateur par rapport au bord gauche de la plaque (vue du dessus)
        self.var_nx_ac = tk.IntVar(value=15)                                # Dimension verticale en nombre d'éléments de matrice de l'actuateur 
        self.var_ny_ac = tk.IntVar(value=15)                                # Dimension horizontale en nombre d'éléments de matrice de l'actuateur 
        self.var_P_pert = tk.DoubleVar(value=0)                             #Puissance thermique de la perturbation
        self.var_t_pert = tk.DoubleVar(value=0)                             #temps à lequel on veut appliquer la perturbation
        self.var_pos_pert_x = tk.IntVar(value=30)                           #position horizontale du centre de la perturbation par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_pert_y = tk.IntVar(value=35)                           #position horizontale du centre de la perturbation par rapport au bord gauche de la plaque (vue du dessus)
        self.var_nx_pert = tk.IntVar(value=3)                               # Dimension verticale en nombre d'éléments de matrice de la perturbation (1 élément = 1mm)
        self.var_ny_pert = tk.IntVar(value=6)                               # Dimension verticale en nombre d'éléments de matrice de la perturbation (1 élément = 1mm)
        self.var_pos_therm1x = tk.IntVar(value=30)                          #position verticale de la thermistance 1 par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_therm1y = tk.IntVar(value=15)                          #position  horizontale de la thermistance 1 par rapport au bord gauche de la plaque (vue du dessus)
        self.var_pos_therm2x = tk.IntVar(value=30)                          #....
        self.var_pos_therm2y = tk.IntVar(value=60)                          #....
        self.var_pos_therm3x = tk.IntVar(value=30)                          #....
        self.var_pos_therm3y = tk.IntVar(value=105)                         #.... 

        self.var_couplage = tk.DoubleVar(value=1.3)                         # variable représentant le couplage thermique entre l'actuateur et la plaque (W/A)


        # Autres variables qui ont été ajouté au fur et à mesure du développement de l'interface

        self.var_afficher_actuateur = tk.BooleanVar(value=True)                         #variable qui va permet à l'utilisateur d'afficher oui ou non l'actuateur sur l'animation 2D
        self.var_afficher_perturbation = tk.BooleanVar(value=True)                      #variable qui va permet à l'utilisateur d'afficher oui ou non la perturbation sur l'animation 2D
        self.var_vitesse_animation = tk.DoubleVar(value=10.0)                           #variable qui va stocker la vitesse d'animation
        self.graphique_top_select = tk.StringVar(value="Carte Thermique 2D")            # variable qui va stocker le graphique sélectionné par l'utilisateur pour la sous-figure du dessus. Par défaut, ça va être le graphique 2D
        self.var_chronometre = tk.DoubleVar(value = 0.0)
        self.chronometre_run = tk.BooleanVar(value=True) 
        self.graphique_bottom_selcet = tk.StringVar(value="Évolution Température")      # variable qui va stocker le graphique sélectionné par l'utilisateur pour la sous-figure du dessous. Par defaut, ¸ça va être l'évolution de la température
        self.animation_on = tk.StringVar(value="Activé")                               # variable qui va permet à l'utilisateur d'activer ou non les animations
        self.var_Nt = int(self.var_temps_simulation.get()/0.001)                        #variable qui va stocker le nombre d'itération de la simulation. C'est-à-dire le nombre de fois qu'on va devoir calculer la température dans la plaque. Ici, 0.001 est le pas de temps de la simulation.
        
        self.var_vitesse = tk.Scale(self.f_interface, orient='horizontal', from_=0, to=10, 
                           label="Vitesse", command=lambda val: self.var_vitesse_animation.set(float(val)/10))




    def creer_interface(self):
        '''
        Cette fonction va créer l'entièreté de l'interface qui va contenir le panneau de contrôle et le panneau de visualisation. Le panneau de contrôle est celui qui va permettre
        de modifier les paramètres de la simulation et le panneau de visualisation est celui qui va permettre de visualiser les résultats (animations, graphiques)
        '''

        fenêtre_interface = ttk.PanedWindow(self.f_interface, orient=tk.HORIZONTAL)                                         # Ici on crée la fenêtre principale et PanedWindow est utilisé pour engendrer une fenêtre avec plusieurs panneaux. 
        fenêtre_interface.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)                                                   # On fait en sorte que la fenêtre s'étende dans les 2 directions et cela sur toute la place disponible. padx et pady permettent d'avoir un petit espace entre la fenêtre et le bord de l'écran.


        self.panneau_controle = ttk.Frame(fenêtre_interface)                                                                #Création du panneau de contrôle à partir de la fenêtre interface
        fenêtre_interface.add(self.panneau_controle, weight=30)                                                             # On défini le panneau de contrôle comme étant 30% du poids/taille horizontale de la fenêtre interface.

        self.panneau_visu = ttk.Frame(fenêtre_interface)                                                                    #Création du panneau visualisation des animations à partir de la fenêtre interface
        fenêtre_interface.add(self.panneau_visu, weight=70)                                                                 # On défini le panneau de contrôle comme étant 70% du poids/taille horizontale de la fenêtre interface 


        self.creer_panneau_de_controle()                                                                                    # Ici on fait appel à la fonction creer_panneau_de_controle définie plus loin dans la classe pour créer le panneau de contrôle
        self.panneau_visualisation = FenêtreAnimations(self.panneau_visu, self)                                             # Ici on défini le panneau de visualisation comme un objet appartenant à la Classe FenêtreAnimation du fichier animation.py.




    def creer_panneau_de_controle(self):
        '''
        Cette méthode va créer les différentes pages/onglets du panneau de contrôle.
        '''



        self.pages_pc = ttk.Notebook(self.panneau_controle)                         #Création d'un Notebook ttk. Fonctionnalité de Tkinter qui permet créer des pages/onglets dans une seule fenêtre. On va donc pouvoir naviguer entre les différentes pages de la fenêtre de contrôle.
        self.pages_pc.pack(fill=tk.BOTH, expand=True)                               #Ici on fait en sorte que le Notebook s'étend dans la fenêtre panneau_contrôle dans les 2 directions (BOTH) et cela sur toute la place diponible (expand= True)
        

        self.page_params_physiques = ttk.Frame(self.pages_pc)                       #Instance qui va contenir la page Paramètre physique 
        self.page_dimensions = ttk.Frame(self.pages_pc)                             #Instance qui va contenir la page Paramètre Dimentions 
        self.page_actuation = ttk.Frame(self.pages_pc)                              #Instance qui va contenir la page Paramètre Actuation
        self.page_simulation = ttk.Frame(self.pages_pc)                             #Instance qui va contenir la page Paramètre Simulation 


        #Ajoute des précédentes pages dans le Notebook self.pages_pc

        self.pages_pc.add(self.page_params_physiques, text="Paramètres Physique")  # Le titre de la page sera Paramètres Physique
        self.pages_pc.add(self.page_dimensions, text="Dimensions")  
        self.pages_pc.add(self.page_actuation, text="Actuation")  
        self.pages_pc.add(self.page_simulation, text="Simulation")  


        #Maintenant on appelle les fonctions suivantes définies plus loin dans la classe  pour remplir les pages par leur contenu respectif.

        self.creation_page_parametres_physiques()
        self.creation_page_dimensions()
        self.creation_page_actuateur()
        self.creation_page_simulation()




    def creation_page_parametres_physiques(self):
        '''
        Cette méthode crée la mise en forme de la page Paramètres Physiques (encadrés pour mettre les valeurs, boutons, ...)
        '''


        self.creation_frame(self.page_params_physiques, "Propriétés thermiques de la plaque")                                   #création d'une en-tête dans la page params_physique. 
                                                                                                                                #Ici on fait appel à une autre fonction définie plus loin qui s'occupe de créer l'en-tête et de le remplir avec les widgets tkinter.



        #Création d'une frame (cadre) dans la page params_physique.
        frame = ttk.Frame(self.page_params_physiques)
        frame.pack(fill=tk.X, padx=10, pady=5)                                                                                  #le contenu de l'onglet_1 s'étendera sur toute la largeur en X et chaque widget sera séparé par 10 pixels en X et 5 pixels en Y.



        #Création des widgets dans la frame (cadre) de la page params_physique.
        ttk.Label(frame, text="Conductivité thermique (k, W/mK):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)           #.grid() permet de placer le widget dans la frame (cadre) de la page params_physique. row et column définissent la position du widget dans la grille. sticky permet de définir l'alignement du widget (ici à gauche (W=West)). padx et pady permettent de définir l'espacement entre les widgets.
        ttk.Entry(frame, textvariable=self.var_k, width=10).grid(row=0, column=1, padx=5, pady=2)                               #ttk.Entry() permet de créer un champ de texte dans lequel l'utilisateur peut entrer une valeur. textvariable permet de lier le champ de texte à une variable tkinter (ici self.var_k). 
        
        ttk.Label(frame, text="Densité (ρ, kg/m³):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_p, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Capacité calorifique (cp, J/kgK):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_cp, width=10).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Température initiale de la plaque (C):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_T_plaque, width=10).grid(row=3, column=1, padx=5, pady=2)




        #Le processus est répété pour les autres onglets de la page

        self.creation_frame(self.page_params_physiques, "Convection") 

        frame = ttk.Frame(self.page_params_physiques)
        frame.pack(fill=tk.X, padx=10, pady=5)  

        ttk.Label(frame, text="Température ambiante (C):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_T_air, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Coefficient convection (h, W/m²K):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_h, width=10).grid(row=1, column=1, padx=5, pady=2)




    def creation_page_dimensions(self):
        '''
        Cette méthode créer la mise en forme de la page Dimensions. Le processus est identique à celui de la méthode précédente
        '''


        self.creation_frame(self.page_dimensions, "Dimensions de la plaque")
        
        frame = ttk.Frame(self.page_dimensions)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Largeur (Lx, m):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_Lx, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Longueur (Ly, m):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_Ly, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Épaisseur (e, m):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_e, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        self.creation_frame(self.page_dimensions, "Discrétisation de la plaque")
        
        frame = ttk.Frame(self.page_dimensions)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Nombre d'éléments en x (n_x):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_n_x, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Nombre d'éléments en y (n_y):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_n_y, width=10).grid(row=1, column=1, padx=5, pady=2)




    def creation_page_actuateur(self):
        '''
        Page actuateur

        '''

        self.creation_frame(self.page_actuation, "Actuateur thermoélectrique")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Courant injecté dans l'actuateur (A):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_current, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Moment d'allumage de la perturbation (s) :").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_t_ac, width=10).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Couplage thermique ((W/A)):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_couplage, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position du centre en X:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_ac_x, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position du centre en Y:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_ac_y, width=10).grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille de l'actuateur en x :").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_nx_ac, width=10).grid(row=5, column=1, padx=5, pady=2)
    
        ttk.Label(frame, text="Taille de l'actuateur en Y :").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_ny_ac, width=10).grid(row=6, column=1, padx=5, pady=2)
        
        self.creation_frame(self.page_actuation, "Perturbation thermique")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Puissance (W):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_P_pert, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Moment d'allumage de la perturbation  (s):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_t_pert, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position de la perturbation en X:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_pert_x, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position de la perturbation Y:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_pert_y, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille de la perturbation en X:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_nx_pert, width=10).grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille de la perturbation en Y:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_ny_pert, width=10).grid(row=5, column=1, padx=5, pady=2)

        self.creation_frame(self.page_actuation, "Position des thermistances")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Position en X thermistance 1 :").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm1x, width=10).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(frame, text="Position en Y thermistance 1 :").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm1y, width=10).grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(frame, text="Position en X thermistance 2 :").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm2x, width=10).grid(row=2, column=3, padx=5, pady=2)
        
        ttk.Label(frame, text="Position en Y thermistance 2 :").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm2y, width=10).grid(row=3, column=3, padx=5, pady=2)
        
        ttk.Label(frame, text="Position en X thermistance 3 :").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm3x, width=10).grid(row=4, column=3, padx=5, pady=2)
        
        ttk.Label(frame, text="Position en Y thermistance 3 :").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm3y, width=10).grid(row=5, column=3, padx=5, pady=2)




    def creation_page_simulation(self):
        '''
        .....

        '''

        self.creation_frame(self.page_simulation, "Paramètres temporels de la simulation")
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Temps de simulation (s):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temps_simulation, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Vitesse d'animation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        # De la ligne 421 à 442, ces lignes de code ont été générées automatiquement par l'IA (Claude Sonnet) afin de relier le choix de bouton à la variable vitesse d'animation.
        speed_frame = ttk.Frame(frame)
        speed_frame.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        
        speed_entry = ttk.Entry(speed_frame, textvariable=self.var_vitesse_animation, width=5)
        speed_entry.pack(side=tk.LEFT, padx=2)

        speeds_frame = ttk.Frame(frame)
        speeds_frame.grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)


        for indice, speed in enumerate([1, 10, 50]):
            if indice == 0:
                btn = ttk.Button(speeds_frame, text=f"Lente", 
                        command=lambda s=speed: self.var_vitesse_animation.set(s), 
                        width=8)
                btn.pack(side=tk.LEFT, padx=2)
            elif indice == 1:
                btn = ttk.Button(speeds_frame, text=f"Normale", 
                        command=lambda s=speed: self.var_vitesse_animation.set(s), 
                        width=8)
                btn.pack(side=tk.LEFT, padx=2)
            elif indice == 2:
                btn = ttk.Button(speeds_frame, text=f"Rapide", 
                        command=lambda s=speed: self.var_vitesse_animation.set(s), 
                        width=8)
                btn.pack(side=tk.LEFT, padx=2)

        

    



        # Options d'affichage Graphique du haut
        self.creation_frame(self.page_simulation, "Options d'affichage")       

        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(frame, text="Afficher l'actuateur", variable=self.var_afficher_actuateur).grid(                     #Checkbutton est un autre widget tkinter qui permet d'enregistrer une valeur booléenne (True ou False) dans une variable tkinter.
            row=0, column=0, sticky=tk.W, padx=5, pady=2)                                                       
        ttk.Checkbutton(frame, text="Afficher la perturbation", variable=self.var_afficher_perturbation).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2)        
    
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Activation des animations:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)                               
        animation = ttk.Combobox(frame, textvariable=self.animation_on, values=["Activé", "Désactivé"])                   # Combobox est un widget tkinter qui permet de choisir une option parmi une liste de choix. Ici, on a le choix entre "Activée" et "Désactivé". Cela signifie que si l'utilisateur sélectionne "Activée", l'animation sera activée et si il sélectionne "Désactivé", l'animation sera désactivée.
        animation.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        animation.bind("<<ComboboxSelected>>", lambda e: self.animation_on)                                                 #On enregistre la sélection de l'utilisateur et on l'associe à la variable animation_on.

        ttk.Label(frame, text="Graphique supérieur:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        selection_graphiques_1 = ttk.Combobox(frame, textvariable=self.graphique_top_select,                                 #Création d'un widget qui va proposer un liste de choix que l'utilisateur pourra sélectionner
                          values=["Carte Thermique 2D", "Carte Thermique 3D"])
        
        selection_graphiques_1.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)                    #sticky est similaire à fill mais pour l'attribut grid au lieu de fill pour pack . tk.W+Tk.E signifie qu'on va étendre la texte sur toute la cellule  
        selection_graphiques_1.bind("<<ComboboxSelected>>", lambda e: self.panneau_visualisation.initialiser_graphique())          #Enregistrement de la sélection de l'utilisateur et où on va appeler la fonction (update_graph_display()) de la classe parent afin d'associer les graphiques sélectionnés 

        ttk.Label(frame, text="Graphique inférieur:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)                       
        selection_graphiques_2 = ttk.Combobox(frame, textvariable=self.graphique_bottom_selcet, 
                          values=["Évolution Température", "Énergie Interne"])
        selection_graphiques_2.grid(row=3, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        selection_graphiques_2.bind("<<ComboboxSelected>>", lambda e: self.panneau_visualisation.initialiser_graphique())





        
        # Création des différents boutons présents dans la page page_simulation qui va permettre de gérer les animations dans le panneau de visualisation (fichier visualisation.py)
        self.creation_frame(self.page_simulation, "Contrôles de simulation")
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame, text="Lancer la simulation", command=self.lancer_simulation).grid(row=0, column=0, padx=5, pady=5,sticky=tk.W+tk.E)
        ttk.Button(frame, text="Pause/Reprendre", command=self.pause_simulation).grid(row=0, column=1, padx=5, pady=5,sticky=tk.W+tk.E)
        ttk.Button(frame, text="Arrêter la simulation", command=self.stop_simulation).grid(row=0, column=2, padx=5, pady=5,sticky=tk.W+tk.E)
        
        ttk.Button(frame, text="Charger Paramètres", command=self.Windows_charger_params).grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(frame, text="Sauvegarder Paramètres", command=self.Windows_sauvegarder_params).grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(frame, text="Sauvegarder Résultats", command=self.sauvegarder_resultats).grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(frame, text="Réinitialiser", command=self.reset_simulation).grid(
            row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        self.creation_frame(self.page_simulation, "Chronomètre")

        chrono_frame = ttk.Frame(self.page_simulation)
        chrono_frame.pack(fill=tk.X, padx=10, pady=5)

        
        ttk.Label(chrono_frame, text="Temps écoulé:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)


        self.label_chrono = ttk.Label(chrono_frame, text="00:00:000", font=("Arial", 10, "bold"))
        self.label_chrono.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
                        



    def creation_frame(self, page, text):

        '''
        Cette méthode, lorsqu'elle sera appelée, va générer un ''onglet'' (frame) dans la  page d'intérêt où les widgets pourront y être insérés.
        Elle prend en entrée la page d'intérêt et le texte qui va être affiché dans l'onglet (frame). 
        '''

        frame = ttk.Frame(page, style='EnTete.TFrame')
        frame.pack(fill=tk.X, pady=(5,0))                   
        ttk.Label(frame, text=text, style='EnTete.TLabel').pack(anchor=tk.W, padx=5, pady=3)




    def recup_params_sim(self):
        '''
        Cette méthode va récupérer les variables ttk créer dans la fonction creer_variables(self) dans la de la simulation et retourner un dictionnaire qui va
        contenir toutes ces variables. Cela va permet de pourvoir facilement récupérer la valeur de cette variable.  
        '''
        k = self.var_k.get()
        p = self.var_p.get()
        cp = self.var_cp.get()
        T_plaque = self.var_T_plaque.get()

        current = self.var_current.get()
        
        Lx = self.var_Lx.get()
        Ly = self.var_Ly.get()
        e = self.var_e.get()
        
        T_air = self.var_T_air.get()
        h = self.var_h.get()
        
        n_x = self.var_n_x.get()
        n_y = self.var_n_y.get()
        
        temps_simulation = self.var_temps_simulation.get()
        pos_ac = (self.var_pos_ac_x.get(), self.var_pos_ac_y.get())
        nx_ac = self.var_nx_ac.get()
        ny_ac = self.var_ny_ac.get()
        
        P_pert = self.var_P_pert.get()
        pos_pert = (self.var_pos_pert_x.get(), self.var_pos_pert_y.get())
        nx_pert = self.var_nx_pert.get()
        ny_pert = self.var_ny_pert.get()
        couplage = self.var_couplage.get()

        pos_therm1x = self.var_pos_therm1x.get()
        pos_therm1y = self.var_pos_therm1y.get()
        pos_therm2x = self.var_pos_therm2x.get()
        pos_therm2y = self.var_pos_therm2y.get()
        pos_therm3x = self.var_pos_therm3x.get()
        pos_therm3y = self.var_pos_therm3y.get()
        



        t_ac = self.var_t_ac.get()
        t_pert = self.var_t_pert.get()
        
        # précalcul des paramètres utile pour la simulation de la température de la plaque 
        dx = Lx / n_x                                           #pas en x
        dy = Ly / n_y                                           #pas en y
        dz = e                                                  #épaisseur
        vol = dx * dy * e                           
        
        a = k / (cp * p)                                        #diffusivité thermique
        dt = 0.001                                              # Pas de temps fixe pour la simulation
        Nt = int(temps_simulation / dt)                         #nombre de points pour l'itération
        
        
        stabilité = (a * dt) / min(dx**2, dy**2)                #vérification du critère de stabilité numérique 
        if stabilité >= 0.5:                                    # On affiche un code d'erreur pour indiquer à l'utilisateur qu'en fonction des paramètres choisis, le critère de stabilité numérique n'est pas respecté  
            messagebox.showwarning(
                "Avertissement de stabilité", 
                f"Le critère de stabilité est de {stabilité:.4f}, ce qui est supérieur à 0.5. "
            )
        
        return {                                                #on retourne un dictionnaire qui va contenir toutes les variables (et leur valeur) utile pour la simulation de la tempérture dans la plaque. Cela va permettre simplement la récupération de ces variables via un appel de la fonction
            'k': k, 'p': p, 'cp': cp,
            'Lx': Lx, 'Ly': Ly, 'e': e,
            'T_air': T_air, 'h': h,
            'T_plaque':T_plaque,
            'n_x': n_x, 'n_y': n_y,
            'temps_simulation': temps_simulation,
            'I_ac': current, 'pos_ac': pos_ac, 'nx_ac': nx_ac, 'ny_ac': ny_ac,
            'P_pert': P_pert, 'pos_pert': pos_pert, 'nx_pert': nx_pert, 'ny_pert': ny_pert,
            'dx': dx, 'dy': dy, 'dz': dz, 'vol': vol,
            'a': a, 'dt': dt, 'Nt': Nt, 'couplage':couplage,
            't_ac': t_ac, 't_pert': t_pert ,
            'pos_therm1x': pos_therm1x, 'pos_therm1y': pos_therm1y,
            'pos_therm2x': pos_therm2x,'pos_therm2y': pos_therm2y,
            'pos_therm3x': pos_therm3x,'pos_therm3y': pos_therm3y,
        }




    def lancer_simulation(self):
        '''
        Cette méthode va s'occuper de lancer la simulation. Elle va d'abord vérifier si une simulation est déjà en cours , s'assurer de vider les listes 
        et récuperer les paramètres de la simulation.Ensuite , elle fait les initialisations nécessaires et appelle la fonction de la classe FenetreAnimation qui va s'occuper de lancer la simulation. 
        '''

       

        if self.simulation_run is True:
            messagebox.showinfo("Information", "Une simulation est déjà en cours.")
            return
        

        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.temps_courant = 0
        self.compter_frame = 0

        #On récupère les paramètres actuels
        params = self.recup_params_sim()

        #On initialise la matrice de températures avec les paramètres
        
        self.T = np.ones((params['n_x'], params['n_y'])) * params["T_plaque"]


        self.simulation_run = True          # On passe l'état de simulation_run de False à True pour indiquer qu'on veut commencer la simulation

        # En passant à l'état :True , on peut appeler la méthode dans le fichier animation.py qui s'occupe de lancer la simulation en mettant les paramètres.
        self.panneau_visualisation.lancer_animations(self.T, params, self.graphique_top_select.get(), self.graphique_bottom_selcet.get())
        self.démarrer_chronometre()




    def pause_simulation(self):

        '''
        Cette méthodeon permet de mettre sur pause la simulation en cours s'il y a effectivement un simulation en cours, 
        sinon elle renvoie un message d'erreur. Elle utilise les fonctions de animation.py pour effectuer les différentes opérations.

        '''

        if self.simulation_run is True:                             # Si l'animation est en cours
            if self.simulation_paused:                              # Et si l'animation est déjà sur pause (True)
                
                self.simulation_paused = False                      #Alors le prochain clic de l'utilisateur sur le bouton pause va faire poursuivre l'animation  
                self.démarrer_chronometre()
                self.panneau_visualisation.poursuivre_animations()

            else:                                                   # Sinon, on met l'animation sur pause 
                self.simulation_paused = True
                self.arrêter_chronometre()
                self.panneau_visualisation.pause_animations()
        else:
            messagebox.showinfo('Information', 'Aucune simulation en cours')




    def stop_simulation(self):
        '''
        Cette méthode permet de mettre d'arrêter la simulation en cours s'il y a effectivement un simulation en cours, 
        sinon elle renvoie un message d'erreur. Elle utilise les fonctions de animation.py pour effectuer les différentes opérations.

        '''

        if self.simulation_run is True:                             # Si l'animation est en cours
            self.panneau_visualisation.stop_animations()
            self.simulation_run = False
            self.simulation_paused = False
            self.arrêter_chronometre()
        else:
            messagebox.showinfo('Information', 'Aucune simulation en cours')




    def reset_simulation(self):
        '''
        Cette méthode s'occupe de reset les données de la simulation , mais tout en conservant les paramètres
        '''
        if self.simulation_run is True:             # Si l'animation est en cours
        
            return  messagebox.showinfo('Erreur', 'Vous devez arrêter la simulation avant de la réinitialiser')


        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.temps_courant = 0
        self.compter_frame = 0 
        params = self.recup_params_sim()
        self.T = np.ones((params['n_x'], params['n_y'])) * params["T_plaque"]

        self.simulation_paused = False                      
        self.panneau_visualisation.reset_graphiques()           #On réinitialise les graphiques
        self.réinitialiser_chronometre()



    def Windows_charger_params(self):
        '''
        cette méthode permet d'ouvrir une fenêtre dans laquelle l'utilisateur pourra sélectionner des fichers json contenant les paramètres de la simulation, similaire à 
        ce que Windows propose pour son explorateur de fichier. Ici, filedialog est un module tkinter qui permet d'ouvrir une fenêtre de dialogue pour sélectionner un fichier.
        '''
        fichier = filedialog.askopenfilename(title="Charger les paramètres", filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", ".*")]
        )

        if fichier :
            self.charger_params(fichier)




    def charger_params(self, fichier=None):        

        '''
        Lorsque cette méthode sera appelée, les paramètres de la simulations contenu dans un fichier json préalablement existant seront extraits et stockés dans les 
        variables afin d'être utilisé par la simulation
        '''
        try:
            if not fichier:
                return
            
            params = charger_paramètres_json(fichier)                       #On appelle la fonction charger_paramètres_json du fichier json.py qui va charger le fichier json et retourner un dictionnaire contenant les paramètres de la simulation.

                                                                            
                
            # Propriétés thermiques
            self.var_k.set(params["proprietes_thermiques"]["k"])
            self.var_p.set(params["proprietes_thermiques"]["p"])
            self.var_cp.set(params["proprietes_thermiques"]["cp"])
            self.var_T_plaque.set(params["proprietes_thermiques"]["T_plaque"])
            


            # Dimensions 
            self.var_Lx.set(params["dimensions_plaque"]["Lx"])
            self.var_Ly.set(params["dimensions_plaque"]["Ly"])
            self.var_e.set(params["dimensions_plaque"]["e"])
            


            # Convection
            self.var_T_air.set(params["convection"]["T_air"])
            self.var_h.set(params["convection"]["h"])
            


            # Discrétisation
            self.var_n_x.set(params["discretisation"]["n_x"])
            self.var_n_y.set(params["discretisation"]["n_y"])


            # Simulation, Actuateur et perturbation
            self.var_temps_simulation.set(params["simulation"]["temps_simulation"])
            self.var_current.set(params["simulation"]["I_ac"])
            self.var_t_ac.set(params["simulation"]["t_ac"])
            self.var_pos_ac_x.set(params["simulation"]["pos_ac"][0])
            self.var_pos_ac_y.set(params["simulation"]["pos_ac"][1])
            self.var_nx_ac.set(params["simulation"]["nx_ac"])
            self.var_ny_ac.set(params["simulation"]["ny_ac"])
            self.var_P_pert.set(params["simulation"]["P_pert"])
            self.var_t_pert.set(params["simulation"]["t_pert"])
            self.var_pos_pert_x.set(params["simulation"]["pos_pert"][0])
            self.var_pos_pert_y.set(params["simulation"]["pos_pert"][1])
            self.var_nx_pert.set(params["simulation"]["nx_pert"])
            self.var_ny_pert.set(params["simulation"]["ny_pert"])
            self.var_couplage.set(params["simulation"]["couplage"])


            #Thermistances 

            self.var_pos_therm1x.set(params["Thermistances"]["pos_therm1x"])
            self.var_pos_therm1y.set(params["Thermistances"]["pos_therm1y"])
            self.var_pos_therm2x.set(params["Thermistances"]["pos_therm2x"])
            self.var_pos_therm2y.set(params["Thermistances"]["pos_therm2y"])
            self.var_pos_therm3x.set(params["Thermistances"]["pos_therm3x"])
            self.var_pos_therm3y.set(params["Thermistances"]["pos_therm3y"])

            
            
            
        except Exception as erreur:
            messagebox.showerror("Erreur", f"Impossible de charger les paramètres: {str(erreur)}")
    



    def Windows_sauvegarder_params(self):
        '''
        cette méthode permet d'ouvrir une fenêtre dans laquelle l'utilisateur pourra sauvegarder des fichers json contenant les paramètres de la simulation.
        '''
        fichier = filedialog.asksaveasfilename(title="Sauvegarder les paramètres", filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", ".*")],
                                             defaultextension=".json",
                                             initialfile="paramètres_de_la_simulation"
        )

        if fichier :
            self.sauvegarde_params(fichier)                             # sauvegarde_params est une méthode définie plus loin dans la classe 




    def sauvegarde_params(self, ficher=None):
        '''
        Lorsque cette méthode sera appelée, elle va créer un fichier json en récupérant la valeur des paramètres de la simulation et sauvegarder le tout dans ce même fichier.
        '''

        try:
            params = {                                                              #format du fichier json
                "proprietes_thermiques": {
                    "k": self.var_k.get(),
                    "p": self.var_p.get(),
                    "cp": self.var_cp.get(),
                    "T_plaque": self.var_T_plaque.get()
                },
                "dimensions_plaque": {
                    "Lx":self.var_Lx.get(),
                    "Ly":self.var_Ly.get(),
                    "e":self.var_e.get()
                },
                "convection": {
                    "T_air": self.var_T_air.get(),
                    "h" : self.var_h.get()
                },
                "discretisation" :{
                    "n_x": self.var_n_x.get(),
                    "n_y": self.var_n_y.get()
                },
                "simulation":{
                    "temps_simulation": self.var_temps_simulation.get(),
                    "I_ac":self.var_current.get(),
                    "t_ac": self.var_t_ac.get(),
                    "pos_ac": [self.var_pos_ac_x.get(),self.var_pos_ac_y.get()],
                    "nx_ac": self.var_nx_ac.get(),
                    "ny_ac": self.var_ny_ac.get(),
                    "P_pert": self.var_P_pert.get(),
                    "t_pert": self.var_t_pert.get(),
                    "pos_pert": [self.var_pos_pert_x.get(),self.var_pos_pert_y.get()],
                    "nx_pert": self.var_nx_pert.get(),
                    "ny_pert": self.var_ny_pert.get(),
                    "couplage": self.var_couplage.get(),

                },
                "Thermistances": {
                    "pos_therm1x" : self.var_pos_therm1x.get(),
                    "pos_therm1y" : self.var_pos_therm1y.get(),
                    "pos_therm2x" : self.var_pos_therm2x.get(),
                    "pos_therm2y" : self.var_pos_therm2y.get(),
                    "pos_therm3x" : self.var_pos_therm3x.get(),
                    "pos_therm3y" : self.var_pos_therm3y.get(),

                }
            }

            sauvegarder_paramètres_json(ficher, params)               #ici on fait appel à la fonction provenant du fichier fonctionnalités_interface importé au début

        except Exception as erreur:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les paramètres : {str(erreur)}")




    def sauvegarder_resultats(self, fichier=None):
        '''
        Cette méthode s'occupe d'enregistrer les résultats (réponses en températures des thermistances) dans un fichier .txt
        '''

        #On vérifie d'abord si des données sont en stock
        if not self.temp_therm_1 :                      # Si la matrice est vide
            messagebox.showinfo("Information", "Aucune donnée de simulation en mémoire")
        
        if fichier is None:
            fichier = filedialog.asksaveasfilename(title='Sauvegarder les résultats', filetypes=[("Fichier TXT", "*.txt"), ("Tous les fichiers", "*.*")],
                                                   defaultextension=".txt",
                                                   initialfile="Données_température_thermistance")
        if not fichier:
            return
        
        try:
            sauvegarder_résultats_txt(                                          # Fonction qui provient du fichier fonctionnalités_interface.py et qui génère un fichier txt
                fichier,
                [i*0.001 for i in range(len(self.temp_therm_1))],
                self.commande_ac,
                self.commande_pert,
                self.temp_therm_1,
                self.temp_therm_2,
                self.temp_therm_laser,
                self.energie_list,

            )
        except Exception as erreur:
            messagebox.showinfo("Erreur", f"Impossible de sauvegarder: {str(erreur)}")




    def démarrer_chronometre(self):
        '''
        Méthode qui s'occupe de démarrer le chronomètre de la simulation.
        '''
        if self.temps_debut_chrono is None:                                         # Si le chronomètre est désactivé
            self.temps_debut_chrono = time.time()
            self.temps_ecoule_total = 0
        elif not self.chronometre_run:                                              # Sinon, on poursuit
            self.temps_debut_chrono = time.time() - self.temps_ecoule_total
        
        self.chronometre_run = True
        self.mettre_a_jour_chronometre()




    def arrêter_chronometre(self):
        
        if self.chronometre_run:
            self.temps_ecoule_total = time.time() - self.temps_debut_chrono
            self.chronometre_run = False




    def réinitialiser_chronometre(self):
        
        self.temps_debut_chrono = time.time()
        self.temps_ecoule_total = 0
        self.chronometre_run = False
        self.label_chrono.config(text="00:00:00")




    def mettre_a_jour_chronometre(self):
        
        if self.chronometre_run and self.simulation_run:
            temps_ecoule = time.time() - self.temps_debut_chrono
            minutes = int(temps_ecoule // 60)
            secondes = int(temps_ecoule % 60)
            millisecondes = int((temps_ecoule % 1) * 1000)
            self.label_chrono.config(text=f"{minutes:02d}:{secondes:02d}:{millisecondes:03d}")
            self.f_interface.after(1, self.mettre_a_jour_chronometre)                                   # Ici .after est une méthode de Tkinter qui appele en boucle la méthode mise en argument après 1 ms.