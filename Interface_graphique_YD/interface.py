import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

from simulation import SimulationEngine
from visualisation import VisualisationManager
from utils import load_json_parameters, save_json_parameters, save_results_to_csv




class SimulationInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulation Thermique de Plaque")
        self.master.geometry("1280x720")
        self.master.minsize(1200, 700)
        
        # Initialiser le moteur de simulation
        self.simulation_engine = SimulationEngine()
        
        # Style de l'application
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Thème plus moderne
        
        # Couleurs et style
        bg_color = "#f5f5f5"
        header_bg = "#e0e0e0"
        frame_bg = "#f0f0f0"
        
        self.style.configure('TFrame', background=frame_bg)
        self.style.configure('Header.TFrame', background=header_bg)
        self.style.configure('Header.TLabel', background=header_bg, font=('Arial', 11, 'bold'))
        self.style.configure('Section.TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background=frame_bg, font=('Arial', 9))
        self.style.configure('TButton', font=('Arial', 9))
        self.style.configure('TEntry', font=('Arial', 9))
        
        self.master.configure(bg=bg_color)
        
        # Initialiser les données de simulation
        self.init_simulation_data()
        
        # Créer les variables pour les paramètres
        self.create_variables()
        
        # Créer l'interface
        self.create_interface()
        
        # Charger les paramètres depuis le fichier JSON
        self.load_parameters("parametres_simulationYD.json")
        
    def init_simulation_data(self):
        """Initialise les variables de données pour la simulation"""
        self.compteur = 0
        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.current_time = 0
        self.frame_count = 0
        self.simulation_running = False
        self.anim1 = None
        self.anim2 = None
        self.T = None
        
    def create_variables(self):
        """Crée toutes les variables tkinter pour les paramètres"""
        # Propriétés thermiques
        self.var_k = tk.DoubleVar(value=167)
        self.var_p = tk.DoubleVar(value=2700)
        self.var_cp = tk.DoubleVar(value=900)
        self.var_T_plaque = tk.DoubleVar(value=297.47)
        
        # Dimensions plaque
        self.var_Lx = tk.DoubleVar(value=0.061)
        self.var_Ly = tk.DoubleVar(value=0.117)
        self.var_e = tk.DoubleVar(value=0.00165)
        
        # Convection
        self.var_T_air = tk.DoubleVar(value=297.47)
       # self.var_T_plaque = tk.DoubleVar(value=297.47)
        self.var_h = tk.DoubleVar(value=10)
        
        # Discrétisation
        self.var_n_x = tk.IntVar(value=61)
        self.var_n_y = tk.IntVar(value=117)
        
        # Simulation
        self.var_temps_simulation = tk.DoubleVar(value=1000)
        self.var_P_ac = tk.DoubleVar(value=1.1)
        self.var_pos_ac_x = tk.IntVar(value=30)
        self.var_pos_ac_y = tk.IntVar(value=15)
        self.var_nx_ac = tk.IntVar(value=15)
        self.var_ny_ac = tk.IntVar(value=15)
        self.var_P_pert = tk.DoubleVar(value=0)
        self.var_pos_pert_x = tk.IntVar(value=60)
        self.var_pos_pert_y = tk.IntVar(value=60)
        self.var_nx_pert = tk.IntVar(value=5)
        self.var_ny_pert = tk.IntVar(value=5)
        
        # Variables d'animation
        self.var_show_actuator = tk.BooleanVar(value=True)
        self.var_show_perturbation = tk.BooleanVar(value=True)
        self.var_temperature_min = tk.DoubleVar(value=20)
        self.var_temperature_max = tk.DoubleVar(value=30)
        self.var_speed_factor = tk.DoubleVar(value=1.0)
        
        # Variables pour les graphiques à afficher
        
        self.selected_chart1 = tk.StringVar(value="Carte Thermique 2D")
        self.selected_chart2 = tk.StringVar(value="Évolution Température")
        self.status_var = tk.StringVar(value="Prêt pour la simulation")
        
    def create_interface(self):
        """Crée l'interface utilisateur complète"""
        # Frame principal divisé en 2 parties
        main_paned = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Partie gauche : panneau de contrôle
        self.control_frame = ttk.Frame(main_paned)
        main_paned.add(self.control_frame, weight=35)
        
        # Partie droite : visualisation
        self.visualization_frame = ttk.Frame(main_paned)
        main_paned.add(self.visualization_frame, weight=65)
        
        # Construction du panneau de contrôle (gauche)
        self.create_control_panel()
        
        # Construction de la zone de visualisation (droite)
        self.vis_manager = VisualisationManager(self.visualization_frame, self)
        
        # Barre d'état
        status_bar = ttk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_control_panel(self):
        """Crée le panneau de contrôle avec onglets"""
        # Notebook pour les onglets de contrôle
        self.control_notebook = ttk.Notebook(self.control_frame)
        self.control_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Créer les onglets
        self.tab_params_physiques = ttk.Frame(self.control_notebook)
        self.tab_dimensions = ttk.Frame(self.control_notebook)
        self.tab_actuation = ttk.Frame(self.control_notebook)
        self.tab_simulation = ttk.Frame(self.control_notebook)
        
        self.control_notebook.add(self.tab_params_physiques, text="Paramètres Physiques")
        self.control_notebook.add(self.tab_dimensions, text="Dimensions")
        self.control_notebook.add(self.tab_actuation, text="Actuation")
        self.control_notebook.add(self.tab_simulation, text="Simulation")
        
        # Remplir les onglets
        self.create_params_physiques_tab()
        self.create_dimensions_tab()
        self.create_actuation_tab()
        self.create_simulation_tab()
    
    def create_params_physiques_tab(self):
        """Crée l'onglet des paramètres physiques"""
        self.create_section_header(self.tab_params_physiques, "Propriétés thermiques")
        
        # Créer un cadre pour les propriétés thermiques
        frame = ttk.Frame(self.tab_params_physiques)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Propriétés thermiques
        ttk.Label(frame, text="Conductivité thermique (k, W/mK):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_k, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Densité (ρ, kg/m³):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_p, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Capacité calorifique (cp, J/kgK):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_cp, width=10).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame, text="Température initiale de la plaque (K):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_T_plaque, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        self.create_section_header(self.tab_params_physiques, "Convection")
        
        # Créer un cadre pour la convection
        frame = ttk.Frame(self.tab_params_physiques)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Température ambiante (T_air, K):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_T_air, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Coefficient convection (h, W/m²K):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_h, width=10).grid(row=1, column=1, padx=5, pady=2)
        
    def create_dimensions_tab(self):
        """Crée l'onglet des dimensions"""
        self.create_section_header(self.tab_dimensions, "Dimensions de la plaque")
        
        frame = ttk.Frame(self.tab_dimensions)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Longueur (Lx, m):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_Lx, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Largeur (Ly, m):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_Ly, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Épaisseur (e, m):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_e, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        self.create_section_header(self.tab_dimensions, "Discrétisation")
        
        frame = ttk.Frame(self.tab_dimensions)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Nombre de points en x (n_x):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_n_x, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Nombre de points en y (n_y):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_n_y, width=10).grid(row=1, column=1, padx=5, pady=2)
        
    def create_actuation_tab(self):
        """Crée l'onglet des paramètres d'actuation"""
        self.create_section_header(self.tab_actuation, "Actuateur thermoélectrique")
        
        frame = ttk.Frame(self.tab_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Puissance (P_ac, W):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_P_ac, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position X:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_ac_x, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position Y:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_ac_y, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille X:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_nx_ac, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille Y:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_ny_ac, width=10).grid(row=4, column=1, padx=5, pady=2)
        
        self.create_section_header(self.tab_actuation, "Perturbation thermique")
        
        frame = ttk.Frame(self.tab_actuation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Puissance (P_pert, W):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_P_pert, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position X:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_pert_x, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Position Y:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_pos_pert_y, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille X:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_nx_pert, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Taille Y:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_ny_pert, width=10).grid(row=4, column=1, padx=5, pady=2)
    
    def create_simulation_tab(self):
        """Crée l'onglet des paramètres de simulation"""
        self.create_section_header(self.tab_simulation, "Paramètres de simulation")
        
        frame = ttk.Frame(self.tab_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text="Temps de simulation (s):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temps_simulation, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Vitesse de simulation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        # Créer un frame pour contenir les contrôles de vitesse
        speed_frame = ttk.Frame(frame)
        speed_frame.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

        # Entrée numérique pour le facteur de vitesse
        speed_entry = ttk.Entry(speed_frame, textvariable=self.var_speed_factor, width=5)
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
        
        ttk.Label(frame, text="Température min (°C):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temperature_min, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(frame, text="Température max (°C):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(frame, textvariable=self.var_temperature_max, width=10).grid(row=3, column=1, padx=5, pady=2)
        
        frame = ttk.Frame(self.tab_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(frame, text="Afficher l'actuateur", variable=self.var_show_actuator).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Checkbutton(frame, text="Afficher la perturbation", variable=self.var_show_perturbation).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Options d'affichage
        self.create_section_header(self.tab_simulation, "Options d'affichage")
        
        frame = ttk.Frame(self.tab_simulation)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
    
        # Créer d'abord les combobox et les garder dans des variables
        chart1_combo = ttk.Combobox(frame, textvariable=self.selected_chart1, 
                          values=["Carte Thermique 2D", "Carte Thermique 3D", "Évolution Température", "Énergie Interne"])
        chart1_combo.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        # Lier l'événement de sélection
        chart1_combo.bind("<<ComboboxSelected>>", lambda e: self.vis_manager.update_graph_display())

        chart2_combo = ttk.Combobox(frame, textvariable=self.selected_chart2, 
                          values=["Carte Thermique 2D", "Carte Thermique 3D", "Évolution Température", "Énergie Interne"])
        chart2_combo.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky=tk.W+tk.E)
        # Lier l'événement de sélection
        chart2_combo.bind("<<ComboboxSelected>>", lambda e: self.vis_manager.update_graph_display())
        
        # Boutons d'exécution
        self.create_section_header(self.tab_simulation, "Contrôles de simulation")
        
        btn_frame = ttk.Frame(self.tab_simulation)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Lancer la simulation", command=self.start_simulation).grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Arrêter la simulation", command=self.stop_simulation).grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(btn_frame, text="Charger Paramètres", command=self.load_parameters_dialog).grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Sauvegarder Paramètres", command=self.save_parameters_dialog).grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(btn_frame, text="Sauvegarder Résultats", command=self.save_results).grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(btn_frame, text="Réinitialiser", command=self.reset_simulation).grid(
            row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
            


    def create_section_header(self, parent, text):
        """Crée un en-tête de section avec style"""
        frame = ttk.Frame(parent, style='Header.TFrame')
        frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(frame, text=text, style='Header.TLabel').pack(anchor=tk.W, padx=5, pady=3)
    
    def load_parameters(self, filename=None):
        """Charge les paramètres à partir d'un fichier JSON"""
        try:
            if not filename:
                return
            
            params = load_json_parameters(filename)
                
            # Mettre à jour les variables avec les paramètres chargés
            # Propriétés thermiques
            self.var_k.set(params["proprietes_thermiques"]["k"])
            self.var_p.set(params["proprietes_thermiques"]["p"])
            self.var_cp.set(params["proprietes_thermiques"]["cp"])
            self.var_T_plaque.set(params["proprietes_thermiques"]["T_plaque"])

            
            # Dimensions plaque
            self.var_Lx.set(params["dimensions_plaque"]["Lx"])
            self.var_Ly.set(params["dimensions_plaque"]["Ly"])
            self.var_e.set(params["dimensions_plaque"]["e"])
            
            # Convection
            self.var_T_air.set(params["convection"]["T_air"])
            self.var_h.set(params["convection"]["h"])
        
            
            # Discrétisation
            self.var_n_x.set(params["discretisation"]["n_x"])
            self.var_n_y.set(params["discretisation"]["n_y"])
            
            # Simulation
            self.var_temps_simulation.set(params["simulation"]["temps_simulation"])
            self.var_P_ac.set(params["simulation"]["P_ac"])
            self.var_pos_ac_x.set(params["simulation"]["pos_ac"][0])
            self.var_pos_ac_y.set(params["simulation"]["pos_ac"][1])
            self.var_nx_ac.set(params["simulation"]["nx_ac"])
            self.var_ny_ac.set(params["simulation"]["ny_ac"])
            self.var_P_pert.set(params["simulation"]["P_pert"])
            self.var_pos_pert_x.set(params["simulation"]["pos_pert"][0])
            self.var_pos_pert_y.set(params["simulation"]["pos_pert"][1])
            self.var_nx_pert.set(params["simulation"]["nx_pert"])
            self.var_ny_pert.set(params["simulation"]["ny_pert"])
            
            self.status_var.set(f"Paramètres chargés depuis {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les paramètres: {str(e)}")
    
    def load_parameters_dialog(self):
        """Ouvre une boîte de dialogue pour charger les paramètres"""
        filename = filedialog.askopenfilename(
            title="Charger les paramètres",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.load_parameters(filename)
    
    def save_parameters_dialog(self):
        """Ouvre une boîte de dialogue pour sauvegarder les paramètres"""
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder les paramètres",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
            defaultextension=".json"
        )
        if filename:
            self.save_parameters(filename)
    
    def save_parameters(self, filename):
        """Sauvegarde les paramètres dans un fichier JSON"""
        try:
            params = {
                "proprietes_thermiques": {
                    "k": self.var_k.get(),
                    "p": self.var_p.get(),
                    "cp": self.var_cp.get(),
                    "T_value": self.var_T_plaque.get()
                },
                "dimensions_plaque": {
                    "Lx": self.var_Lx.get(),
                    "Ly": self.var_Ly.get(),
                    "e": self.var_e.get()
                },
                "convection": {
                    "T_air": self.var_T_air.get(),
                    "h": self.var_h.get()
                },
                "discretisation": {
                    "n_x": self.var_n_x.get(),
                    "n_y": self.var_n_y.get()
                },
                "simulation": {
                    "temps_simulation": self.var_temps_simulation.get(),
                    "P_ac": self.var_P_ac.get(),
                    "pos_ac": [self.var_pos_ac_x.get(), self.var_pos_ac_y.get()],
                    "nx_ac": self.var_nx_ac.get(),
                    "ny_ac": self.var_ny_ac.get(),
                    "P_pert": self.var_P_pert.get(),
                    "pos_pert": [self.var_pos_pert_x.get(), self.var_pos_pert_y.get()],
                    "nx_pert": self.var_nx_pert.get(),
                    "ny_pert": self.var_ny_pert.get()
                }
            }
            
            save_json_parameters(filename, params)
                
            self.status_var.set(f"Paramètres sauvegardés dans {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les paramètres: {str(e)}")
    
    def get_simulation_parameters(self):
        """Récupère tous les paramètres nécessaires à la simulation"""
        # Récupérer les paramètres des variables tkinter
        k = self.var_k.get()
        p = self.var_p.get()
        cp = self.var_cp.get()
        T_plaque = self.var_T_plaque.get()
        
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
        
        # Calcul des paramètres dérivés
        dx = Lx / n_x
        dy = Ly / n_y
        dz = e
        vol = dx * dy * e
        
        a = k / (cp * p)
        dt = 0.001  # Pas de temps fixe pour la simulation
        Nt = int(temps_simulation / dt)
        
        # Vérifier la stabilité numérique
        stability = (a * dt) / min(dx**2, dy**2)
        if stability >= 0.5:
            messagebox.showwarning(
                "Avertissement de stabilité", 
                f"Le critère de stabilité est de {stability:.4f}, ce qui est supérieur à 0.5. "
                "La simulation pourrait être instable. Considérez réduire le pas de temps ou augmenter la discrétisation."
            )
        
        return {
            'k': k, 'p': p, 'cp': cp,
            'Lx': Lx, 'Ly': Ly, 'e': e,
            'T_air': T_air, 'h': h,
            'T_plaque':T_plaque,
            'n_x': n_x, 'n_y': n_y,
            'temps_simulation': temps_simulation,
            'P_ac': P_ac, 'pos_ac': pos_ac, 'nx_ac': nx_ac, 'ny_ac': ny_ac,
            'P_pert': P_pert, 'pos_pert': pos_pert, 'nx_pert': nx_pert, 'ny_pert': ny_pert,
            'dx': dx, 'dy': dy, 'dz': dz, 'vol': vol,
            'a': a, 'dt': dt, 'Nt': Nt
        }
    
    def save_results(self, filename=None):
        """Sauvegarde les résultats de la simulation dans un fichier CSV"""
        if not self.temp_therm_1:
            messagebox.showinfo("Information", "Aucune donnée de simulation à sauvegarder.")
            return
            
        if filename is None:
            filename = filedialog.asksaveasfilename(
                title="Sauvegarder les résultats",
                filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
                defaultextension=".csv"
            )
        
        if not filename:
            return
        
        try:
            save_results_to_csv(
                filename,
                [i * 0.001 for i in range(len(self.temp_therm_1))],
                self.temp_therm_1,
                self.temp_therm_2,
                self.temp_therm_laser,
                self.energie_list
            )
            
            self.status_var.set(f"Résultats sauvegardés dans {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les résultats: {str(e)}")

    def reset_simulation(self):
        """Réinitialise la simulation"""
        self.stop_simulation()
        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.current_time = 0
        self.frame_count = 0
        
        # Demander au gestionnaire de visualisation de réinitialiser les graphiques
        self.vis_manager.reset_graphs()
        
        self.status_var.set("Simulation réinitialisée")

    def start_simulation(self):
        """Démarre la simulation"""
        if self.simulation_running:
            messagebox.showinfo("Information", "Une simulation est déjà en cours.")
            return
            
        # Réinitialiser les données de simulation
        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.current_time = 0
        self.frame_count = 0
        
        # Obtenir les paramètres actuels
        params = self.get_simulation_parameters()
        
        # Initialiser la matrice de température
        self.T = np.ones((params['n_x'], params['n_y'])) * params['T_plaque']
        
        # Démarrer les animations
        self.simulation_running = True
        self.status_var.set("Simulation en cours...")
        
        # Demander au gestionnaire de visualisation de démarrer les animations
        self.vis_manager.start_animations(self.T, params, self.selected_chart1.get(), self.selected_chart2.get())

    def stop_simulation(self):
        """Arrête la simulation"""
        if not self.simulation_running:
            return
            
        # Demander au gestionnaire de visualisation d'arrêter les animations
        self.vis_manager.stop_animations()
        
        self.simulation_running = False
        self.status_var.set(f"Simulation arrêtée à {self.current_time:.2f} s")