
#https://docs.python.org/3/library/tkinter.messagebox.html       #Documentation pour messagox
#https://docs.python.org/3/library/tkinter.ttk.html              #Documentation pour les wigets ttk
#https://docs.python.org/3/library/tkinter.ttk.html#notebook     #Documentation pour Notebook
#https://stackoverflow.com/questions/28089942/difference-between-fill-and-expand-options-for-tkinter-pack-method     #Documentation pour la position des éléments

















import tkinter as tk                                    #Module python qu'on va utiliser pour faire l'interface graphique
from tkinter import ttk, messagebox, filedialog         # ici, ttk est pour avoir l'option de mettre des ''widgets'' qui offrent un rendu plus moderne,
                                                        #messagebox sert à pourvoir afficher des messages à l'utilisateur et filedialog permet de travailler avec des fichiers (sauvegarder , charger ..)

import matplotlib.pyplot as plt                     
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk              # FigureCanvasTkAgg permet de mettre de figure plt dans les widgets de ttk et NavigationToolbar2Tk fourni des outils pour que l'utilisateur puisse intéragir avec le canvas (zoomer, déplacer ...) 
from matplotlib.figure import Figure                                                                #classe qui permet de créer des figures

from simulation_temp import TempératurePlaque                                                       #importation de fichier contenant la modélisation de la température
from animation import FenêtreAnimations
from fonctionnalités_interface import sauvegarder_paramètres_json, charger_paramètres_json, sauvegarder_résultats_txt
import numpy as np
import time






















class FenêtreInterface:
    '''
    Cette classe gérer l'interface graphique avec laquelle l'utilisateur va être en mesure d'intéragir afin de contrôleur les paramètres,
    les graphiques et les animations de la simulation de la température dans la plaque....
    '''








    def __init__(self, f_interface):
        self.f_interface = f_interface      #création d'une instance qui va représenter la fenêtre principale de l'interface (widget)
        self.f_interface.title("Simulation Thermique de la plaque")     #Titre de la fenêtre Tkinter                                                        
        self.f_interface.geometry("1280x800")      #Taille initiale de la fenêtre lorsque l'utilisateur va lancer le code


        self.simulation_thermique = TempératurePlaque()   # on crée une instance qui va contenir la fonction qui modélise l'évolution de la température dans la plaque présent dans le fichier simulation.py 
        
        
        self.style = ttk.Style()                      #permet d'accéder aux thèmes disponibles et qui va permettre de configurer le style de la fenêtre
        self.style.theme_use('clam')                    # thème choisi

        couleur_fond = "#f5f5f5"                        #couleur de fond de la fenêtre  "#f5f5f5"       #
        couleur_entete = "#e0e0e0"                      #couleur des en-têtes
        couleur_cadre = "#e0e0e0"                       #couleur du cadre de la fenêtre


        #configuration de l'interface

        #Ici on prédifini la couleur et le style d'écriture qui sera utiliser pour les différentes parties (widgets) de l'interface (page,onglet,calligraphie, ...).

        self.style.configure('Cadre.TFrame', background=couleur_cadre)
        self.style.configure('EnTete.TFrame', background=couleur_entete)
        self.style.configure('EnTete.TLabel', background=couleur_entete, font=('Arial', 11, 'bold'))
        self.style.configure('Section.TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('Etiquette.TLabel', background=couleur_cadre, font=('Arial', 9))
        self.style.configure('Bouton.TButton', font=('Arial', 9))
        self.style.configure('Champ.TEntry', font=('Arial', 9))
        self.f_interface.configure(bg=couleur_fond)


    
        self.initialisation_donnees_simulation()    #instance qui va initialise les données de la simulation
        self.creer_variables()                      #instance qui va créer les variables
        self.creer_interface()                      #instance qui va créer l'interface











    def initialisation_donnees_simulation(self):
        '''
        Cette fonction va s'occuper d'initialiser les variables qui va permettre de contrôleur la simulation et de récolter les données de la simulation
        '''
        self.compteur = 0           #va servir pour le nombre d'itération 
        self.temp_therm_1 = []      #liste qui va contenir les températures au cours du temps de la thermistance où l'actuateur
        self.temp_therm_2 = []      #liste qui va contenir les températures au cours du temps de la thermistance 2 (au centre de la plaque)
        self.temp_therm_laser = []      #liste qui va contenir les températures au cours du temps  de la thermistance où centre de la plaque
        self.energie_list = []          #liste qui va contenir l'énergie thermique interne dans la plaque au cours du temps
        self.temps_courant = 0         #va servir pour compter le temps écouler depuis le début de la simulation afin de pouvoir mettre l'option d'appliquer la puissance à un instant t>0 durant la simulation
        self.compter_frame = 0          #va servir pour compter le nombre de frame lors des animations
        self.simulation_run = False    #permet de savoir si la simulation est en cours ou non
        self.simulation_paused = False #permet de avoir si la simulation est en pause où non
        self.anim1 = None               # cet instance va permettre de stocker l'animation qui sera afficher dans le sous-fenêtre du haut du panneau de visualisation 
        self.anim2 = None               #même chose, mais pour celle du bas
        self.T = None                   #Matrice de la température dans la plaque










    def creer_variables(self):
        '''
        Cette fonction va créer et convertir tous les paramètres initiale du simulateur en variable tkinker afin de pourvoir les utiliser par l'interface Tkinter. 
        Toutes les valeurs (value=...) ici seront les valeurs par défaut affichées lors du lancement de l'interface.
        ''' 
        # Propriétés thermiques de la plaque
        self.var_k = tk.IntVar(value=167)           #conductivité thermique du matériau
        self.var_p = tk.IntVar(value=2700)          #densité du matériau
        self.var_cp = tk.IntVar(value=900)          #capacité thermique du matériau
        self.var_T_plaque = tk.DoubleVar(value=25)  #température initiale de la plaque 
        
        
        # Dimensions plaque
        self.var_Lx = tk.DoubleVar(value=0.061)     #Largeur de la plaque (x)
        self.var_Ly = tk.DoubleVar(value=0.117)     #Longueur de la plaque (y)
        self.var_e = tk.DoubleVar(value=0.00165)    #épaisseur de la plaque
        
        # Proprités thermique de l'air ambiant
        self.var_T_air = tk.DoubleVar(value=25) #température de l'air
        self.var_h = tk.DoubleVar(value=12.2)         #coefficient de convection entre l'air et la plaque
        
        # Discrétisation
        self.var_n_x = tk.IntVar(value=61)          #pas en x
        self.var_n_y = tk.IntVar(value=117)         #pas en y
        
        # Simulation
        self.var_current = tk.DoubleVar(value=1)
        self.var_temps_simulation = tk.DoubleVar(value=500)     #temps total de la simulation
        self.var_P_ac = tk.DoubleVar(value=1.0)                 #Puissance électrique injectée dans l'actuateur
        self.var_t_ac = tk.DoubleVar(value=0)                   #temps à lequel on veut appliquer la puissance de l'actuateur 
        self.var_pos_ac_x = tk.IntVar(value=30)                 #position verticale du centre de l'actuateur par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_ac_y = tk.IntVar(value=15)                 #position horizontale du centre de l'actuateur par rapport au bord gauche de la plaque (vue du dessus)
        self.var_nx_ac = tk.IntVar(value=15)                    # Dimension verticale en nombre d'éléments de matrice de l'actuateur (1 élément = 1mm)
        self.var_ny_ac = tk.IntVar(value=15)                    # Dimension horizontale en nombre d'éléments de matrice de l'actuateur (1 élément = 1mm)
        self.var_P_pert = tk.DoubleVar(value=0)                 #Puissance thermique de la perturbation
        self.var_t_pert = tk.DoubleVar(value=0)                 #temps à lequel on veut appliquer la perturbation
        self.var_pos_pert_x = tk.IntVar(value=30)               #position horizontale du centre de la perturbation par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_pert_y = tk.IntVar(value=35)               #position horizontale du centre de la perturbation par rapport au bord gauche de la plaque (vue du dessus)
        self.var_nx_pert = tk.IntVar(value=3)                   # Dimension verticale en nombre d'éléments de matrice de la perturbation (1 élément = 1mm)
        self.var_ny_pert = tk.IntVar(value=6)                   # Dimension verticale en nombre d'éléments de matrice de la perturbation (1 élément = 1mm)
        self.var_pos_therm1x = tk.IntVar(value=30)
        self.var_pos_therm1y = tk.IntVar(value=15)
        self.var_pos_therm2x = tk.IntVar(value=30)
        self.var_pos_therm2y = tk.IntVar(value=60)
        self.var_pos_therm3x = tk.IntVar(value=30)
        self.var_pos_therm3y = tk.IntVar(value=105)

        self.var_couplage = tk.DoubleVar(value=1.6)              # variable représentant le couplage thermique entre l'actuateur et la plaque


        # Autres variables 
        self.var_afficher_actuateur = tk.BooleanVar(value=True)     #variable qui va permet à l'utilisateur d'afficher oui ou non l'actuateur sur l'animation 2D
        self.var_afficher_perturbation = tk.BooleanVar(value=True)  #variable qui va permet à l'utilisateur d'afficher oui ou non la perturbation sur l'animation 2D
        self.var_vitesse_animation = tk.DoubleVar(value=1.0)        #variable qui va stocker la vitesse d'animation
        self.graphique_top_select = tk.StringVar(value="Carte Thermique 2D")    # variable qui va stocker le graphique sélectionné par l'utilisateur pour la sous-figure du dessus. Par défaut, ça va être le graphique 2D
        self.var_chronometre = tk.DoubleVar(value = 0.0)
        self.chronometre_run = tk.BooleanVar(value=True) 
        self.graphique_bottom_selcet = tk.StringVar(value="Évolution Température")  # variable qui va stocker le graphique sélectionné par l'utilisateur pour la sous-figure du dessous. Par defaut, ¸ça va être l'évolution de la température
        self.animation_on = tk.StringVar(value="Activée")
        self.var_Nt = int(self.var_temps_simulation.get()/0.001)
        self.var_vitesse = tk.Scale(self.f_interface, orient='horizontal', from_=0, to=10, 
                           label="Vitesse", command=lambda val: self.var_vitesse_animation.set(float(val)/10))








    def creer_interface(self):
        '''
        Cette fonction va créer l'entièreté de l'interface qui va contenir le panneau de contrôle et le panneau de visualisation
        '''

        fenêtre_interface = ttk.PanedWindow(self.f_interface, orient=tk.HORIZONTAL) # ici on crée la fenêtre à partir de l'instance f_interface et la division sera fait à l'horizontale
        fenêtre_interface.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)    # padx et pady défini la séparation entre le cadre de la fenêtre et le contenu


        self.panneau_controle = ttk.Frame(fenêtre_interface)      #Création du panneau de contrôle à partir de la fenêtre interface
        fenêtre_interface.add(self.panneau_controle, weight=30)  # On défini le panneau de contrôle comme étant 35% du poids/taille horizontale de la fenêtre interface. En réalité , on rajoute une fenêtre par dessus fenêtre_interface

        self.panneau_visu = ttk.Frame(fenêtre_interface)      #Création du panneau visualisation des animations à partir de la fenêtre interface
        fenêtre_interface.add(self.panneau_visu, weight=70)  # On défini le panneau de contrôle comme étant 65% du poids/taille horizontale de la fenêtre interface 


        self.creer_panneau_de_controle()        # Ici on fait appel à la fonction creer_panneau_de_controle définie plus loin dans la classe pour créer le panneau de contrôle
        self.panneau_visualisation = FenêtreAnimations(self.panneau_visu, self)      #Ici on défini le panneau de visualisation comme un objet appartenant à la Classe FenêtreAnimation









    def creer_panneau_de_controle(self):
        '''
        Cette fonction va créer les différentes pages et onglets dans le panneau de contrôle. Cela va permettre de diviser et de regouper
        les paramètres communs au même endroit.
        '''
        self.pages_pc = ttk.Notebook(self.panneau_controle)     #Création d'un Notebook ttk. Fonctionnalité de Tkinter qui permet créer des pages/onglets dans une seule fenêtre
        self.pages_pc.pack(fill=tk.BOTH, expand=True)           #Ici on fait en sorte que le Notebook s'étend dans la fenêtre panneau_contrôle dans les 2 directions (BOTH) et cela sur toute la place diponible (expand= True)
        

        self.page_params_physiques = ttk.Frame(self.pages_pc)       #Instance qui va contenir la page Paramètre physique 
        self.page_dimensions = ttk.Frame(self.pages_pc)       #Instance qui va contenir la page Paramètre Dimentions 
        self.page_actuation = ttk.Frame(self.pages_pc)       #Instance qui va contenir la page Paramètre Actuation
        self.page_simulation = ttk.Frame(self.pages_pc)       #Instance qui va contenir la page Paramètre Simulation 

        #Ajoute des précédentes pages dans le Notebook self.pages_pc

        self.pages_pc.add(self.page_params_physiques, text="Paramètres Physique")  # Le titre de la page sera Paramètres Physique
        self.pages_pc.add(self.page_dimensions, text="Dimensions")  
        self.pages_pc.add(self.page_actuation, text="Actuation")  
        self.pages_pc.add(self.page_simulation, text="Simulation")  


        #Maintenant on appelle les fonctions suivantes définies plus loin dans la classe  pour remplir les pages de leur contenu

        self.creation_page_parametres_physiques()
        self.creation_page_dimensions()
        self.creation_page_actuateur()
        self.creation_page_simulation()









    def creation_page_parametres_physiques(self):
        '''
        Cette fonction crée la mise en forme de la page Paramètres Physiques (encadrés pour mettre les valeurs, boutons, ...)
        '''


        self.creation_frame(self.page_params_physiques, "Propriétés thermiques de la plaque") #création d'une en-tête dans la page params_physique. 
                                                                                                #Ici on fait appel à une autre fonction définie plus loin qui s'occupe de créer des widgets (objet qui peut contenir des éléments d'interface graphique)



        #Création d'une instance qui va contenir le contenu de l'en-tête, c'est-à-dire contenir les différents widget tkinter
        frame = ttk.Frame(self.page_params_physiques)
        frame.pack(fill=tk.X, padx=10, pady=5)  #le contenu de l'onglet_1 s'étendera sur toute la largeur en X et chaque widget sera séparé l'un de l'autre



        #Création des widgets dans l'en-tête
        ttk.Label(frame, text="Conductivité thermique (k, W/mK):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_k, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Densité (ρ, kg/m³):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_p, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Capacité calorifique (cp, J/kgK):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_cp, width=10).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Température initiale de la plaque (K):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_T_plaque, width=10).grid(row=3, column=1, padx=5, pady=2)




        #Le processus est répété pour les autres onglets de la page




        self.creation_frame(self.page_params_physiques, "Convection") 

        frame = ttk.Frame(self.page_params_physiques)
        frame.pack(fill=tk.X, padx=10, pady=5)  

        ttk.Label(frame, text="Température ambiante (K):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_T_air, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Coefficient convection (h, W/m²K):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_h, width=10).grid(row=1, column=1, padx=5, pady=2)









    
    def creation_page_dimensions(self):
        '''
        Cette fonction créer la mise en forme de la page Dimensions. Le processus est identique à celui de la fonction précédente
        '''


        self.creation_frame(self.page_dimensions, "Dimensions de la plaque")
        
        frame = ttk.Frame(self.page_dimensions)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Longueur (Lx, m):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_Lx, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Largeur (Ly, m):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_Ly, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Épaisseur (e, m):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_e, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        self.creation_frame(self.page_dimensions, "Discrétisation")
        
        frame = ttk.Frame(self.page_dimensions)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Nombre de points en x (n_x):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_n_x, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Nombre de points en y (n_y):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_n_y, width=10).grid(row=1, column=1, padx=5, pady=2)











    def creation_page_actuateur(self):
        '''
        ......

        '''

        self.creation_frame(self.page_actuation, "Actuateur thermoélectrique et Thermistances")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Courant de l'actuateur (A):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_current, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Appliquer la puissance au temps (s) :").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_t_ac, width=10).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Couplage thermique :").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_couplage, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position X:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_ac_x, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position Y:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_ac_y, width=10).grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille X:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_nx_ac, width=10).grid(row=5, column=1, padx=5, pady=2)
    
        ttk.Label(frame, text="Taille Y:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_ny_ac, width=10).grid(row=6, column=1, padx=5, pady=2)
        
        self.creation_frame(self.page_actuation, "Perturbation thermique")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Puissance (W):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_P_pert, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Appliquer la perturbation au temps (s):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_t_pert, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position X:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_pert_x, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position Y:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_pert_y, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille X:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_nx_pert, width=10).grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille Y:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_ny_pert, width=10).grid(row=5, column=1, padx=5, pady=2)

        self.creation_frame(self.page_actuation, "Position thermistances")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Position x thermistance 1 :").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm1x, width=10).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Position y thermistance 1 :").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm1y, width=10).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Position x thermistance 2 :").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm2x, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position y thermistance 2 :").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm2y, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position x thermistance 3 :").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm3x, width=10).grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position y thermistance 3 :").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_therm3y, width=10).grid(row=5, column=1, padx=5, pady=2)












    def creation_page_simulation(self):
        '''
        .....

        '''

        self.creation_frame(self.page_simulation, "Paramètres de simulation")
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Temps de simulation (s):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temps_simulation, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Vitesse d'animation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        

        
        speed_frame = ttk.Frame(frame)
        speed_frame.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        
        speed_entry = ttk.Entry(speed_frame, textvariable=self.var_vitesse_animation, width=5)
        speed_entry.pack(side=tk.LEFT, padx=2)

        

        # Boutons prédéfinis pour les vitesses courantes
        speeds_frame = ttk.Frame(frame)
        speeds_frame.grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)


        for indice, speed in enumerate([1, 10, 100]):
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

        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)

        #Ici, au lieu de créer des frames (widgets) on crée des boutons avec lesquels l'utilisateur peut intéragir avec.


        
        ttk.Checkbutton(frame, text="Afficher l'actuateur", variable=self.var_afficher_actuateur).grid(             #Si l'utilisateur coche ce boutton, alors la variable va être True et False dans le cas contraire
            row=0, column=0, sticky=tk.W, padx=5, pady=2)                                                       
        ttk.Checkbutton(frame, text="Afficher la perturbation", variable=self.var_afficher_perturbation).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2)
        





        # Options d'affichage Graphique 1
        self.creation_frame(self.page_simulation, "Options d'affichage")            #On crée une nouvelle  onglet    
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        animation = ttk.Combobox(frame, textvariable=self.animation_on, values=["Activée", "Désactivée"])
        animation.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        animation.bind("<<ComboboxSelected>>", lambda e: self.animation_on)  

    
        selection_graphiques_1 = ttk.Combobox(frame, textvariable=self.graphique_top_select,                                 #Création d'un widget qui va proposer un liste de choix que l'utilisateur pourra sélectionner
                          values=["Carte Thermique 2D", "Carte Thermique 3D", "Évolution Température", "Énergie Interne"])
        selection_graphiques_1.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)                    #sticky est similaire à fill mais pour l'attribut grid au lieu de fill pour pack . tk.W+Tk.E signifie qu'on va étendre la texte sur toute la cellule  
        

        selection_graphiques_1.bind("<<ComboboxSelected>>", lambda e: self.panneau_visualisation.initialiser_graphique())          #Enregistrement de la sélection de l'utilisateur et où on va appeler 
                                                                                                                                        #la fonction (update_graph_display()) de la classe parent afin d'associer les graphiques sélectionnés 
                                                                                                                                        # au bon endroit dans le fenêtre de droite de l'interface(ici, ce sera dans la sous-fenêtre du haut)




        # Option affichage Graphique 2
        selection_graphiques_2 = ttk.Combobox(frame, textvariable=self.graphique_bottom_selcet, 
                          values=["Carte Thermique 2D", "Carte Thermique 3D", "Évolution Température", "Énergie Interne"])
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
        
       
            










    def creation_frame(self, page, text):

        '''
        Cette fonction, lorsqu'elle sera appelée, va générer un ''onglet'' (frame) dans la  page d'intérêt où les widgets pourront y être inséré
        '''

        frame = ttk.Frame(page, style='EnTete.TFrame')
        frame.pack(fill=tk.X, pady=(5,0))                   
        ttk.Label(frame, text=text, style='EnTete.TLabel').pack(anchor=tk.W, padx=5, pady=3)







 
    

    def recup_params_sim(self):
        '''
        Cette fonction va récupérer les variables ttk créer dans la fonction creer_variables(self) dans la de la simulation et retourner un dictionnaire qui va
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
        P_ac = self.var_P_ac.get()
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
        
        # Calcul des paramètres utile pour la simulation de la température de la plaque 
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
        
        return {                                                #on retourne un dictionnaire qui va contenir toutes les variables (et leur valeur) utile pour la simulation de la tempérture dans la plaque
            'k': k, 'p': p, 'cp': cp,
            'Lx': Lx, 'Ly': Ly, 'e': e,
            'T_air': T_air, 'h': h,
            'T_plaque':T_plaque,
            'n_x': n_x, 'n_y': n_y,
            'temps_simulation': temps_simulation,
            'P_ac': P_ac, 'pos_ac': pos_ac, 'nx_ac': nx_ac, 'ny_ac': ny_ac,
            'P_pert': P_pert, 'pos_pert': pos_pert, 'nx_pert': nx_pert, 'ny_pert': ny_pert,
            'dx': dx, 'dy': dy, 'dz': dz, 'vol': vol,
            'a': a, 'dt': dt, 'Nt': Nt, 'couplage':couplage,
            't_ac': t_ac, 't_pert': t_pert ,
            'pos_therm1x': pos_therm1x, 'pos_therm1y': pos_therm1y,
            'pos_therm2x': pos_therm2x,'pos_therm2y': pos_therm2y,
            'pos_therm3x': pos_therm3x,'pos_therm3y': pos_therm3y,
            'I_ac': current
        }
        









    def lancer_simulation(self):
        '''
        Cette fonction va s'occuper de démarrer la simulation 
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

        #On initialise la matrice de températures
        
        self.T = np.ones((params['n_x'], params['n_y'])) * params["T_plaque"]


        self.simulation_run = True          # On passe l'état de simulation_run de False à True pour indiquer qu'on veut commencer la simulation

        # En passant à l'état :True , on peut appeler la fonction dans le fichier animation.py qui s'occupe de lancer la simulation en mettant les paramètres.
        self.panneau_visualisation.lancer_animations(self.T, params, self.graphique_top_select.get(), self.graphique_bottom_selcet.get())
        #self.graphique_top_select.get() et self.graphique_bottom_selcet.get()










    def pause_simulation(self):
        '''
        Cette fonction permet de mettre sur pause la simulation en cours s'il y a effectivement un simulation en cours, 
        sinon elle renvoie un message d'erreur. Elle utilise les fonctions de animation.py pour effectuer les différentes opérations.

        '''

        if self.simulation_run is True:                             # Si l'animation est en cours
            if self.simulation_paused:                              # Et si l'animation est déjà sur pause (True)
                self.simulation_paused = False                      #Alors le prochain clic de l'utilisateur sur le bouton pause va faire poursuivre l'animation  
                self.panneau_visualisation.poursuivre_animations()

            else:                                                   # Sinon, on met l'animation sur pause 
                self.simulation_paused = True
                self.panneau_visualisation.pause_animations()
        else:
            messagebox.showinfo('Information', 'Aucune simulation en cours')










    def stop_simulation(self):
        '''
        Cette fonction permet de mettre d'arrêter la simulation en cours s'il y a effectivement un simulation en cours, 
        sinon elle renvoie un message d'erreur. Elle utilise les fonctions de animation.py pour effectuer les différentes opérations.

        '''

        if self.simulation_run is True:                             # Si l'animation est en cours
            self.panneau_visualisation.stop_animations()

            self.simulation_run = False
            self.simulation_paused = False
        else:
            messagebox.showinfo('Information', 'Aucune simulation en cours')












    def reset_simulation(self):
        '''
        Cette fonction s'occupe de reset les données de la simulation , mais tout en conservant les paramètres
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

       








    def Windows_charger_params(self):
        '''
        cette fonction permet d'ouvrir une fenêtre dans laquelle l'utilisateur pourra sélectionner des fichers json contenant les paramètres de la simulation, similaire à 
        ce que Windows propose pour son explorateur de fichier
        '''
        fichier = filedialog.askopenfilename(title="Charger les paramètres", filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", ".*")]
        )

        if fichier :
            self.charger_params(fichier)










    def charger_params(self, fichier=None):        

        '''
        Lorsque cette fonction sera appelée, les paramètres de la simulations contenu dans un fichier json préalablement existant seront extraits et stockés dans les 
        variables afin d'être utilisé par la simulation
        '''
        try:
            if not fichier:
                return
            
            params = charger_paramètres_json(fichier)
                
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
            self.var_P_ac.set(params["simulation"]["P_ac"])
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
        cette fonction permet d'ouvrir une fenêtre dans laquelle l'utilisateur pourra sauvegarder des fichers json contenant les paramètres de la simulation.
        '''
        fichier = filedialog.asksaveasfilename(title="Sauvegarder les paramètres", filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", ".*")],
                                             defaultextension=".json",
                                             initialfile="paramètres_de_la_simulation"
        )

        if fichier :
            self.sauvegarde_params(fichier)










    def sauvegarde_params(self, ficher=None):
        '''
        Lorsque cette fonction sera appelée, elle va créer un fichier json en récupérant la valeur des paramètres de la simulation et sauvegarder le tout dans ce même fichier.
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
                    "P_ac": self.var_P_ac.get(),
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
        Cette fonction s'occupe d'enregistrer les résultats (réponses en températures des thermistances) dans un fichier .txt
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
            sauvegarder_résultats_txt(
                fichier,
                [i*0.001 for i in range(len(self.temp_therm_1))],
                self.temp_therm_1,
                self.temp_therm_2,
                self.temp_therm_laser,
                self.energie_list,

            )
        except Exception as erreur:
            messagebox.showinfo("Erreur", f"Impossible de sauvegarder: {str(erreur)}")

        