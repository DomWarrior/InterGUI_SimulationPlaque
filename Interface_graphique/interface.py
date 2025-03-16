"""
Ce fichier contient le code de l'interface utilisateur .... fenêtre de droite...

"""







import tkinter as tk                                    #Module python qu'on va utiliser pour faire l'interface graphique
from tkinter import ttk, messagebox, filedialog         # ici, ttk est pour avoir l'option de mettre des ''widgets'' qui offrent un rendu plus moderne,
                                                        #messagebox sert à pourvoir afficher des messages à l'utilisateur et filedialog permet de travailler avec des fichiers (sauvegarder , charger ..)

import matplotlib.pyplot as plt                     
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk              # FigureCanvasTkAgg permet de mettre de figure plt dans les widgets de ttk et NavigationToolbar2Tk fourni des outils pour que l'utilisateur puisse intéragir avec le canvas (zoomer, déplacer ...) 
from matplotlib.figure import Figure                                                                #classe qui permet de créer des figures

from simulation_temp import TempératurePlaque                                                       #importation de fichier contenant la modélisation de la température
from animation import FenêtreAnimations
from fonctionnalités_interface import sauvegarder_paramètres_json, charger_paramètres_json, sauvegarder_résultats_txt


class FenêtreInterface:
    '''
    Cette classe gérer l'interface graphique avec laquelle l'utilisateur va être en mesure d'intéragir afin de contrôleur les paramètres,
    les graphiques et les animations de la simulation de la température dans la plaque....
    '''

    def __init__(self, f_interface):
        self.f_interface = f_interface      #création d'une instance qui va représenter la fenêtre principale de l'interface (widget)
        self.f_interface.titre("Simulation Thermique de la plaque")    #Titre de la fenêtre Tkinter
        self.f_interface.geometry("1280x720")      #Taille initiale de la fenêtre


        self.simulation_thermique = TempératurePlaque()   # on crée une instance qui va contenir la fonction qui modélise l'évolution de la température dans la plaque 
        
        
        self.style() = ttk.Style()                      #permet d'accéder aux thèmes disponibles et de configurer le style de la fenêtre
        self.style.theme_use('clam')                    # modèle choisi

        couleur_fond = "#f5f5f5"                        #couleur de fond de la fenêtre
        couleur_entete = "#e0e0e0"                      #couleur des en-têtes
        couleur_cadre = "#f0f0f0"                       #couleur du cadre de la fenêtre


        #configuration de l'interface

        #Ici on prédifini la couleur et le style d'écriture qui sera utiliser pour les différentes parties de l'interface.

        self.style.configure('Cadre.TFrame', background=couleur_cadre)
        self.style.configure('EnTete.TFrame', background=couleur_entete)
        self.style.configure('EnTete.Etiquette', background=couleur_entete, font=('Arial', 11, 'bold'))
        self.style.configure('Section.Etiquette', font=('Arial', 10, 'bold'))
        self.style.configure('Etiquette.TLabel', background=couleur_cadre, font=('Arial', 9))
        self.style.configure('Bouton.TButton', font=('Arial', 9))
        self.style.configure('Champ.TEntry', font=('Arial', 9))
        self.f_interface.configure(bg = couleur_fond)

    
        self.initialisation_donnees_simulation()    #instance qui va initialise les données de la simulation
        self.creer_variables()                      #instance qui va créer les variables
        self.creer_interface()                      #instance qui va créer l'interface
        self.charger_parametres("paramètres_simulation.json")  #instance qui va charger les paramètres depuis un fichier json


    def initialisation_donnees_simulation(self):
        '''
        Cette fonction va s'occuper d'initialiser les variables qui va permettre de contrôleur la simulation et de réculter les données de la simulations
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
        self.anim1 = None               # cet instance va permettre de stocker l'animation qui sera afficher dans le sous-fenêtre du haut dans la fenêtre où les animations/graphiques seront affichées
        self.anim2 = None               #même chose, mais pour celle du bas
        self.T = None                   #Matrice de la température dans la plaque

    def creer_variables(self):
        '''
        Cette fonction va créer convertir tous les paramètres initiale du simulateur en variable tkinker afin de pour être utiliser par l'interface. 
        Toutes les valeurs (value=...) ici seront les valeurs par défaut afficher lors du lancement de l'interface.
        ''' 
        # Propriétés thermiques de la plaque
        self.var_k = tk.IntVar(value=167)           #conductivité thermique du matériau
        self.var_p = tk.IntVar(value=2700)          #densité du matériau
        self.var_cp = tk.IntVar(value=900)          #capacité thermique du matériau
        self.var_T_plaque = tk.DoubleVar(value=297.47)  #température initiale de la plaque 
        
        # Dimensions plaque
        self.var_Lx = tk.DoubleVar(value=0.061)     #Largeur de la plaque (x)
        self.var_Ly = tk.DoubleVar(value=0.117)     #Longeur de la plaque (y)
        self.var_e = tk.DoubleVar(value=0.00165)    #épaisseur de la plaque
        
        # Proprités thermique de l'air ambiant
        self.var_T_air = tk.DoubleVar(value=297.47) #température de l'air
        self.var_h = tk.DoubleVar(value=10)         #coefficient de convection entre l'air et la plaque
        
        # Discrétisation
        self.var_n_x = tk.IntVar(value=61)          #pas en x
        self.var_n_y = tk.IntVar(value=117)         #pas en y
        
        # Simulation
        self.var_temps_simulation = tk.DoubleVar(value=500)    #temps total de la simulation
        self.var_P_ac = tk.DoubleVar(value=1.0)                 #Puissance électrique injecté dans l'actuateur
        self.var_t_ac = tk.DoubleVar(value=0)                   #temps à lequel on veut appliquer la puissance de l'actuateur 
        self.var_pos_ac_x = tk.IntVar(value=30)                 #position verticale du centre de l'actuateur par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_ac_y = tk.IntVar(value=15)                 #position horizontale du centre de l'actuateur par rapport au bord gauche de la plaque (vue du dessus)
        self.var_nx_ac = tk.IntVar(value=15)                    # Dimension verticale en nombre d'éléments de matrice de l'actuateur (1 élément = 1mm)
        self.var_ny_ac = tk.IntVar(value=15)                    # Dimension horizontale en nombre d'éléments de matrice de l'actuateur (1 élément = 1mm)
        self.var_P_pert = tk.DoubleVar(value=0)                 #Puissance électrique injecté dans l'actuateur
        self.var_t_pert = tk.DoubleVar(value=0)                 #temps à lequel on veut appliquer la perturbation
        self.var_pos_pert_x = tk.IntVar(value=60)               #position horizontale du centre de la perturbation par rapport au bord supérieur de la plaque (vue du dessus)
        self.var_pos_pert_y = tk.IntVar(value=60)               #position horizontale du centre de la perturbation par rapport au bord gauche de la plaque (vue du dessus)
        self.var_nx_pert = tk.IntVar(value=5)                   # Dimension verticale en nombre d'éléments de matrice de la perturbation (1 élément = 1mm)
        self.var_ny_pert = tk.IntVar(value=5)                   # Dimension verticale en nombre d'éléments de matrice de la perturbation (1 élément = 1mm)
        


        self.var_couplage = tk.DoubleVar(value=1.0)              # variable représentant le couplage thermique entre l'actuateur et la plaque


        # Autres variables 
        self.var_afficher_actuateur = tk.BooleanVar(value=True)     #variable qui va permet à l'utilisateur d'afficher oui ou non l'actuateur sur l'animation 2D
        self.var_afficher_perturbation = tk.BooleanVar(value=True)  #variable qui va permet à l'utilisateur d'afficher oui ou non la perturbation sur l'animation 2D
        self.var_temperature_min = tk.DoubleVar(value=20)
        self.var_temperature_max = tk.DoubleVar(value=40)
        self.var_vitesse_animation = tk.DoubleVar(value=1.0)        #variable qui va stocker la vitesse d'animation
        self.graphique_top_select = tk.StringVar(value="Carte Thermique 2D")    # variable qui va stocker le graphique sélectionné par l'utilisateur pour la sous-figure du dessus
        self.graphique_bottom_selcet = tk.StringVar(value="Évolution Température")  # variable qui va stocker le graphique sélectionné par l'utilisateur pour la sous-figure du dessous
        self.status_var = tk.StringVar(value="Prêt pour la simulation")


    def creer_interface(self):
        '''
        Cette fonction va créer l'entièreté de l'interface qui va contenir le panneau de contrôle et le panneau de visualisation
        '''

        fenêtre_interface = ttk.PanedWindow(self.f_interface, orient=tk.HORIZONTAL) # ici on crée la fenêtre à partir de l'instance f_interface et sera divisée en 2 horizontalement
        fenêtre_interface.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        self.panneau_controle = ttk.Frame(fenêtre_interface)      #Création du panneau de contrôle à partir de la fenêtre interface
        fenêtre_interface.add(self.panneau_controle, weight=35)  # On défini le panneau de contrôle comme étant 35% du poids/taille horizontale de la fenêtre interface 

        self.panneau_visu = ttk.Frame(fenêtre_interface)      #Création du panneau visualisation animation à partir de la fenêtre interface
        fenêtre_interface.add(self.panneau_visu, weight=65)  # On défini le panneau de contrôle comme étant 35% du poids/taille horizontale de la fenêtre interface 


        self.creer_panneau_de_controle()        # Ici on fait appel à la fonction creer_panneau_de_controle dans la classe pour créer le panneau
        self.creer_panneau_visualisation = FenêtreAnimations(self.panneau_visu, self)      #Ici on fait appel à la fonction creer_panneau_visualisation dans la classe pour créer le panneau

    def creer_panneau_de_controle(self):
        '''
        Cette fonction va créer les différentes pages ou onglets dans le panneau de contrôle. Cela va permettre de diviser et de regouper
        les paramètres communs au même endroit.
        '''
        self.pages_pc = ttk.Notebook(self.panneau_controle)     #Création d'un Notebook ttk. Fonctionnalité de Tkinter qui permet créer des pages/onglets
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


        #Maintenant on appelle les fonctions suivantes pour remplir les pages de leur contenu

        self.creation_page_parametres_physiques()
        self.creation_page_dimensions()
        self.creation_page_actuateur()
        self.creation_page_simulation()

    def creation_page_parametres_physiques(self):




        '''
        Cette fonction créer la mise en forme de la page Paramètres Physiques (encadrés pour mettre les valeurs, boutons, ...)
        '''






        self.creation_frame(self.page_params_physiques, "Propriétés thermiques de la plaque") #création d'une en-tête dans la page params_physique



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

        self.creation_frame(self.page_actuation, "Actuateur thermoélectrique")
        
        frame = ttk.Frame(self.page_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Puissance de l'actuateur (W):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_P_ac, width=10).grid(row=0, column=1, padx=5, pady=2)

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

    def creation_page_simulation(self):
        '''
        .....

        '''

        self.creation_frame(self.page_simulation, "Paramètres de simulation")
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Temps de simulation (s):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temps_simulation, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Vitesse de simulation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)





        # à revoir pour cea
        

        # Créer un frame pour contenir les contrôles de vitesse
        speed_frame = ttk.Frame(frame)
        speed_frame.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        # Entrée numérique pour le facteur de vitesse
        speed_entry = ttk.Entry(speed_frame, textvariable=self.var_vitesse_animation, width=5)
        speed_entry.pack(side=tk.LEFT, padx=2)

        # Label pour indiquer l'unité
        ttk.Label(speed_frame, text="x").pack(side=tk.LEFT)

        # Boutons prédéfinis pour les vitesses courantes
        speeds_frame = ttk.Frame(frame)
        speeds_frame.grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)

        for speed in [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]:
            btn = ttk.Button(speeds_frame, text=f"{speed}x", 
                    command=lambda s=speed: self.var_speed_factor.set(s), 
                    width=4)
            btn.pack(side=tk.LEFT, padx=2)




        #À revoir pour cela aussi 
        
        ttk.Label(frame, text="Température min (°C):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temperature_min, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Température max (°C):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temperature_max, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)







        #Ici, au lieu de créer des frames (widgets) on crée des boutons avec lesquels l'utilisateur peut intéragir avec.


        
        ttk.Checkbutton(frame, text="Afficher l'actuateur", variable=self.var_afficher_actuateur).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Checkbutton(frame, text="Afficher la perturbation", variable=self.var_afficher_perturbation).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Options d'affichage
        self.creation_frame(self.page_simulation, "Options d'affichage")
        
        frame = ttk.Frame(self.page_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
    
        
        selection_graphiques_1 = ttk.Combobox(frame, textvariable=self.selected_chart1, 
                          values=["Carte Thermique 2D", "Carte Thermique 3D", "Évolution Température", "Énergie Interne"])
        selection_graphiques_1.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        

        selection_graphiques_1.bind("<<ComboboxSelected>>", lambda e: self.vis_manager.update_graph_display())          #Enregistrement de la sélection de l'utilisateur 

        selection_graphiques_2 = ttk.Combobox(frame, textvariable=self.selected_chart2, 
                          values=["Carte Thermique 2D", "Carte Thermique 3D", "Évolution Température", "Énergie Interne"])
        selection_graphiques_2.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        # Lier l'événement de sélection
        selection_graphiques_2.bind("<<ComboboxSelected>>", lambda e: self.vis_manager.update_graph_display())
        
        # Boutons d'exécution
        self.create_section_header(self.tab_simulation, "Contrôles de simulation")
        
        btn_frame = ttk.Frame(self.tab_simulation)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Lancer la simulation", command=self.start_simulation).grid(row=0, column=0, padx=5, pady=5,sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Pause/Reprendre", command=self.pause_simulation).grid(row=0, column=1, padx=5, pady=5,sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Arrêter la simulation", command=self.stop_simulation).grid(row=0, column=2, padx=5, pady=5,sticky=tk.W+tk.E)
        
        ttk.Button(btn_frame, text="Charger Paramètres", command=self.load_parameters_dialog).grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Sauvegarder Paramètres", command=self.save_parameters_dialog).grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(btn_frame, text="Sauvegarder Résultats", command=self.save_results).grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Réinitialiser", command=self.reset_simulation).grid(
            row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
            





    def creation_frame(self, page, text):

        '''
        Cette fonction, lorsqu'elle sera appelée, va générer une en-tête (frame) dans la  page d'intérêt où les widgets pourront y être inséré
        '''

        frame = ttk.Frame(page, style='EnTete.TFrame')
        frame.pack(fill=tk.X, pady=(5,0))
        ttk.Label(frame, text=text, style='EnTete.Etiquette').pack(anchor=tk.W, padx=5, pady=3)


        pass

    def lancer_simulation(self):
        pass

    def pause_simulation(self):
        pass

    def stop_simulation(self):
        pass

    def reset_simulation(self):
        pass

    def sauvegarde_paramètres(self, ficher=None):
        pass

    def sauvegarder_resultats(self, fichier=None):
        pass