import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

class FenêtreAnimations:
    '''Cette classe correspond à la fenêtre de droite que l'utilisateur va voir en ouvrant l'interface. 
    Cette fenêtre va être divisée en 2 sous-fenêtres afin d'offrir la possibilité d'afficher 2 graphiques simultanément. Ces fenêtres vont permettre d'afficher des graphiques (la réponse à l'échelon
    des trois thermistances et l'énergie thermique interne de la plaque) et des animations (carte thermique 2D et 3D dans la plaque).
    Cette classe va également gérer toutes les fonctionnalités offertes à l'utilisateur en lien avec les graphiques et les animations.
    '''

    def __init__(self, fenêtre_main, controlleur):
        self.fenêtre_main = fenêtre_main             # Cette instance correspond à la fenêtre de droite de l'interface
        self.controlleur = controlleur               # Cette instance va permettre de contrôler la simulation en y stockant les informations, paramètres...

        self.fenêtre = ttk.PanedWindow(fenêtre_main, orient=tk.VERTICAL)  # Ici on divise verticalement la fenêtre principale en 2
        self.fenêtre.pack(fill=tk.BOTH, expand=True)                      # On empile les 2 sous-fenêtres l'une sur l'autre

        # Division de la fenêtre
        self.fenêtre_top = ttk.Frame(self.fenêtre)                      # Sous-fenêtre du dessus                      
        self.fenêtre.add(self.fenêtre_top, weight=50)                   # Qui va initialement correspondre à 50% en poids de la fenêtre initiale

        self.fenêtre_bottom = ttk.Frame(self.fenêtre)                   # Sous-fenêtre du dessous
        self.fenêtre.add(self.fenêtre_bottom, weight=50)

        # Initialiser les références des barres de couleur
        self.bc_carte_2D_top = None
        self.bc_carte_3D_top = None
        self.bc_carte_2D_bottom = None
        self.bc_carte_3D_bottom = None
        
        # Objets pour les animations
        self.animation1 = None
        self.animation2 = None
        
        # Créer tous les graphiques possibles
        self.créer_graphiques()
        
        # Initialiser les graphiques selon les sélections par défaut
        self.initialiser_graphique()

    def créer_graphiques(self):
        '''
        Fonction qui va créer la mise en forme de tous les graphiques (graphiques vides) 
        '''
        # Figures, graphiques et animations qui seront affichés dans la sous-fenêtre du dessus

        # Figure pour la carte 2D thermique
        self.fig_carte_2D_top = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_2D_top = self.fig_carte_2D_top.add_subplot(111)
        self.canvas_carte_2D_top = FigureCanvasTkAgg(self.fig_carte_2D_top, master=self.fenêtre_top)
        
        # Figure pour la carte 3D thermique
        self.fig_carte_3D_top = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_3D_top = self.fig_carte_3D_top.add_subplot(111, projection='3d')
        self.canvas_carte_3D_top = FigureCanvasTkAgg(self.fig_carte_3D_top, master=self.fenêtre_top)
        
        # Figure pour le graphique d'évolution des températures
        self.fig_temp_top = Figure(figsize=(6, 5), dpi=100)
        self.ax_temp_top = self.fig_temp_top.add_subplot(111)
        self.ax_temp_top.set_xlabel("Temps (s)")
        self.ax_temp_top.set_ylabel("Température (°C)")
        self.ax_temp_top.set_title("Évolution des températures")
        self.ax_temp_top.grid(True)
        self.canvas_temp_top = FigureCanvasTkAgg(self.fig_temp_top, master=self.fenêtre_top)
        
        # Figure pour le graphique d'énergie
        self.fig_energie_top = Figure(figsize=(6, 5), dpi=100)
        self.ax_energie_top = self.fig_energie_top.add_subplot(111)
        self.ax_energie_top.set_xlabel("Temps (s)")
        self.ax_energie_top.set_ylabel("Énergie interne (J)")
        self.ax_energie_top.set_title("Évolution de l'énergie thermique interne")
        self.ax_energie_top.grid(True)
        self.canvas_energie_top = FigureCanvasTkAgg(self.fig_energie_top, master=self.fenêtre_top)
        
        # Même chose pour la sous-fenêtre du bas
        self.fig_carte_2D_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_2D_bottom = self.fig_carte_2D_bottom.add_subplot(111)
        self.canvas_carte_2D_bottom = FigureCanvasTkAgg(self.fig_carte_2D_bottom, master=self.fenêtre_bottom)
        
        self.fig_carte_3D_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_3D_bottom = self.fig_carte_3D_bottom.add_subplot(111, projection='3d')
        self.canvas_carte_3D_bottom = FigureCanvasTkAgg(self.fig_carte_3D_bottom, master=self.fenêtre_bottom)
        
        self.fig_temp_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_temp_bottom = self.fig_temp_bottom.add_subplot(111)
        self.ax_temp_bottom.set_xlabel("Temps (s)")
        self.ax_temp_bottom.set_ylabel("Température (°C)")
        self.ax_temp_bottom.set_title("Évolution des températures")
        self.ax_temp_bottom.grid(True)
        self.canvas_temp_bottom = FigureCanvasTkAgg(self.fig_temp_bottom, master=self.fenêtre_bottom)
        
        self.fig_energie_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_energie_bottom = self.fig_energie_bottom.add_subplot(111)
        self.ax_energie_bottom.set_xlabel("Temps (s)")
        self.ax_energie_bottom.set_ylabel("Énergie interne (J)")
        self.ax_energie_bottom.set_title("Évolution de l'énergie thermique interne")
        self.ax_energie_bottom.grid(True)
        self.canvas_energie_bottom = FigureCanvasTkAgg(self.fig_energie_bottom, master=self.fenêtre_bottom)
    
    def initialiser_graphique(self):
        '''
        Nettoie les fenêtres et affiche les graphiques sélectionnés par l'utilisateur
        '''
        # Nettoyer les widgets existants dans les sous-fenêtres
        for widget in self.fenêtre_top.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.pack_forget()
        
        for widget in self.fenêtre_bottom.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.pack_forget()
        
        # Afficher les graphiques sélectionnés
        self.graphique_selection(self.controlleur.graphique_top_select.get(), self.fenêtre_top, top=True)
        self.graphique_selection(self.controlleur.graphique_bottom_selcet.get(), self.fenêtre_bottom, top=False)

    def graphique_selection(self, type_graphique, fenêtre_parent, top=True):
        '''
        Affiche le graphique sélectionné dans la fenêtre parent
        '''
        if top:
            canvas_carte_2D = self.canvas_carte_2D_top
            canvas_carte_3D = self.canvas_carte_3D_top
            canvas_temp = self.canvas_temp_top
            canvas_energie = self.canvas_energie_top
        else:
            canvas_carte_2D = self.canvas_carte_2D_bottom
            canvas_carte_3D = self.canvas_carte_3D_bottom
            canvas_temp = self.canvas_temp_bottom
            canvas_energie = self.canvas_energie_bottom
        
        if type_graphique == "Carte Thermique 2D":
            canvas_carte_2D.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas_carte_2D, fenêtre_parent)
            toolbar.update()
            toolbar.pack(fill=tk.X)
        elif type_graphique == "Carte Thermique 3D":
            canvas_carte_3D.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas_carte_3D, fenêtre_parent)
            toolbar.update()
            toolbar.pack(fill=tk.X)
        elif type_graphique == "Évolution Température":
            canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas_temp, fenêtre_parent)
            toolbar.update()
            toolbar.pack(fill=tk.X)
        elif type_graphique == "Énergie Interne":
            canvas_energie.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas_energie, fenêtre_parent)
            toolbar.update()
            toolbar.pack(fill=tk.X)
    
    def reset_graphiques(self):
        '''
        Réinitialise les graphiques actuellement sélectionnés
        '''
        self.stop_animations()

        graph_configs = {
            "Carte Thermique 2D": {
                "top": (self.ax_carte_2D_top, self.canvas_carte_2D_top, "bc_carte_2D_top"),
                "bottom": (self.ax_carte_2D_bottom, self.canvas_carte_2D_bottom, "bc_carte_2D_bottom")
            },
            "Carte Thermique 3D": {
                "top": (self.ax_carte_3D_top, self.canvas_carte_3D_top, "bc_carte_3D_top"),
                "bottom": (self.ax_carte_3D_bottom, self.canvas_carte_3D_bottom, "bc_carte_3D_bottom")
            },
            "Évolution Température": {
                "top": (self.ax_temp_top, self.canvas_temp_top, None),
                "bottom": (self.ax_temp_bottom, self.canvas_temp_bottom, None)
            },
            "Énergie Interne": {
                "top": (self.ax_energie_top, self.canvas_energie_top, None),
                "bottom": (self.ax_energie_bottom, self.canvas_energie_bottom, None)
            }
        }

        chart1 = self.controlleur.graphique_top_select.get()
        chart2 = self.controlleur.graphique_bottom_selcet.get()

        if chart1 in graph_configs:
            ax, canvas, cb_attr = graph_configs[chart1]["top"]
            if cb_attr:
                if cb_attr == "bc_carte_2D_top":
                    if self.bc_carte_2D_top is not None:
                        try:
                            self.bc_carte_2D_top.remove()
                        except:
                            pass
                        self.bc_carte_2D_top = None
                elif cb_attr == "bc_carte_3D_top":
                    if self.bc_carte_3D_top is not None:
                        try:
                            # Pour les colorbar 3D, ne pas utiliser remove()
                            self.bc_carte_3D_top = None
                        except:
                            pass
            ax.clear()
            if chart1 == "Évolution Température":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Température (°C)")
                ax.set_title("Évolution des températures")
                ax.grid(True)
            elif chart1 == "Énergie Interne":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Énergie interne (J)")
                ax.set_title("Évolution de l'énergie thermique interne")
                ax.grid(True)
            canvas.draw()

        if chart2 in graph_configs:
            ax, canvas, cb_attr = graph_configs[chart2]["bottom"]
            if cb_attr:
                if cb_attr == "bc_carte_2D_bottom":
                    if self.bc_carte_2D_bottom is not None:
                        try:
                            self.bc_carte_2D_bottom.remove()
                        except:
                            pass
                        self.bc_carte_2D_bottom = None
                elif cb_attr == "bc_carte_3D_bottom":
                    if self.bc_carte_3D_bottom is not None:
                        try:
                            # Pour les colorbar 3D, ne pas utiliser remove()
                            self.bc_carte_3D_bottom = None
                        except:
                            pass
            ax.clear()
            if chart2 == "Évolution Température":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Température (°C)")
                ax.set_title("Évolution des températures")
                ax.grid(True)
            elif chart2 == "Énergie Interne":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Énergie interne (J)")
                ax.set_title("Évolution de l'énergie thermique interne")
                ax.grid(True)
            canvas.draw()
    
    def update_graph_temp(self, top=True):
        '''
        Met à jour le graphique d'évolution des températures
        '''
        if not self.controlleur.temp_therm_1:
            return
        
        if top:
            ax = self.ax_temp_top
            canvas = self.canvas_temp_top
        else:
            ax = self.ax_temp_bottom
            canvas = self.canvas_temp_bottom
            
        ax.clear()
        step = max(1, len(self.controlleur.temp_therm_1) // 1000)
        times = [i * 0.001 for i in range(0, len(self.controlleur.temp_therm_1), step)]
        temp1 = self.controlleur.temp_therm_1[::step]
        temp2 = self.controlleur.temp_therm_2[::step]
        temp_laser = self.controlleur.temp_therm_laser[::step]
        
        ax.plot(times, temp1, 'r-', label='Thermistance 1')
        ax.plot(times, temp2, 'g--', label='Thermistance 2')
        ax.plot(times, temp_laser, 'b-.', label='Position Laser')
        
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Température (°C)")
        ax.set_title(f"Évolution des températures - Temps simulé: {self.controlleur.temps_courant:.2f} s")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    def update_graph_energie(self, top=True):
        '''
        Met à jour le graphique d'évolution de l'énergie
        '''
        if not self.controlleur.energie_list:
            return
        
        if top:
            ax = self.ax_energie_top
            canvas = self.canvas_energie_top
        else:
            ax = self.ax_energie_bottom
            canvas = self.canvas_energie_bottom
            
        ax.clear()
        step = max(1, len(self.controlleur.energie_list) // 1000)
        times = [i * 0.001 for i in range(0, len(self.controlleur.energie_list), step)]
        energy = self.controlleur.energie_list[::step]
        
        ax.plot(times, energy, 'b-')
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Énergie interne (J)")
        ax.set_title(f"Évolution de l'énergie thermique interne - Temps simulé: {self.controlleur.temps_courant:.2f} s")
        ax.grid(True)
        canvas.draw()
    
    def lancer_animations(self, T, params, chart1, chart2):
        '''
        Lance les animations dans les deux sous-fenêtres
        '''
        # Initialiser les graphiques statiques (Évolution Température et Énergie Interne)
        if chart1 == "Évolution Température":
            self.update_graph_temp(top=True)
        elif chart1 == "Énergie Interne":
            self.update_graph_energie(top=True)
            
        if chart2 == "Évolution Température":
            self.update_graph_temp(top=False)
        elif chart2 == "Énergie Interne":
            self.update_graph_energie(top=False)
        
        # Démarrer les animations pour les graphiques animés (2D et 3D)
        if chart1 == "Carte Thermique 2D":
            self.animation_2D_démarrer(T, params, top=True)
        elif chart1 == "Carte Thermique 3D":
            self.animation_3D_démarrer(T, params, top=True)
        elif chart2 == "Carte Thermique 2D":
            self.animation_2D_démarrer(T, params, top=False)
        elif chart2 == "Carte Thermique 3D":
            self.animation_3D_démarrer(T, params, top=False)
        else:
            # Si aucun graphique animé n'est sélectionné, démarrer une animation 2D invisible
            # pour faire avancer la simulation
            self.animation_2D_démarrer(T, params, top=True)
            # Cacher le graphique 2D
            self.canvas_carte_2D_top.get_tk_widget().pack_forget()
    
    def animation_démarrer(self, type_graphique, T, params, top=True):
        '''
        Démarre l'animation du type spécifié dans la sous-fenêtre spécifiée
        '''
        if type_graphique == "Carte Thermique 2D":
            self.animation_2D_démarrer(T, params, top)
        elif type_graphique == "Carte Thermique 3D":
            self.animation_3D_démarrer(T, params, top)
        elif type_graphique == "Évolution Température":
            self.update_graph_temp(top)
        elif type_graphique == "Énergie Interne":
            self.update_graph_energie(top)
    
    def pause_animations(self):
        '''
        Met en pause les animations en cours
        '''
        if hasattr(self, 'animation1') and self.animation1 and hasattr(self.animation1, 'event_source'):
            self.animation1.event_source.stop()
        if hasattr(self, 'animation2') and self.animation2 and hasattr(self.animation2, 'event_source'):
            self.animation2.event_source.stop()
    
    def poursuivre_animations(self):
        '''
        Reprend les animations mises en pause avec les paramètres mis à jour
        '''
        # Récupérer les paramètres actuels (potentiellement modifiés)
        params = self.controlleur.recup_params_sim()
        
        # Conserver la matrice de température actuelle
        current_T = self.controlleur.T
        
        # Recréer les animations avec les paramètres actuels
        chart1 = self.controlleur.graphique_top_select.get()
        chart2 = self.controlleur.graphique_bottom_selcet.get()
        
        # Nettoyer les widgets des graphiques pour éviter les superpositions
        self.clean_graph_widgets(chart1, True)  # Nettoyer graphique du haut
        self.clean_graph_widgets(chart2, False)  # Nettoyer graphique du bas
        
        # Démarrer de nouvelles animations avec les paramètres mis à jour
        self.lancer_animations(current_T, params, chart1, chart2)
    
    def clean_graph_widgets(self, type_graphique, top=True):
        '''
        Nettoie les widgets existants pour éviter les superpositions
        '''
        if top:
            if type_graphique == "Carte Thermique 2D":
                ax = self.ax_carte_2D_top
                cb_attr = 'bc_carte_2D_top'
            elif type_graphique == "Carte Thermique 3D":
                ax = self.ax_carte_3D_top
                cb_attr = 'bc_carte_3D_top'
            else:
                return  # Pas besoin de nettoyage pour les autres types de graphiques
        else:
            if type_graphique == "Carte Thermique 2D":
                ax = self.ax_carte_2D_bottom
                cb_attr = 'bc_carte_2D_bottom'
            elif type_graphique == "Carte Thermique 3D":
                ax = self.ax_carte_3D_bottom
                cb_attr = 'bc_carte_3D_bottom'
            else:
                return  # Pas besoin de nettoyage pour les autres types de graphiques
        
        # Nettoyer l'axe
        ax.clear()
        
        # Nettoyer la colorbar si elle existe
        if hasattr(self, cb_attr) and getattr(self, cb_attr) is not None:
            try:
                getattr(self, cb_attr).remove()
            except (AttributeError, ValueError, KeyError):
                pass
            setattr(self, cb_attr, None)
    
    def stop_animations(self):
        '''
        Arrête complètement les animations
        '''
        try:
            if self.animation1 is not None:
                try:
                    self.animation1.event_source.stop()
                except:
                    pass
                self.animation1 = None
        except:
            self.animation1 = None
        
        try:
            if self.animation2 is not None:
                try:
                    self.animation2.event_source.stop()
                except:
                    pass
                self.animation2 = None
        except:
            self.animation2 = None
    
    def animation_2D_démarrer(self, T, params, top=True):
        '''
        Démarre l'animation de la carte thermique 2D
        '''
        if top:
            fig = self.fig_carte_2D_top
            ax = self.ax_carte_2D_top
            canvas = self.canvas_carte_2D_top
            anim_attr = 'animation1'
            cb_attr = 'bc_carte_2D_top'
        else:
            fig = self.fig_carte_2D_bottom
            ax = self.ax_carte_2D_bottom
            canvas = self.canvas_carte_2D_bottom
            anim_attr = 'animation2'
            cb_attr = 'bc_carte_3D_bottom'
            
        ax.clear()
        
        # Initialisation de l'image
        temp_data = T - 273.15  # Conversion en °C
        im = ax.imshow(temp_data, cmap='hot', interpolation='nearest', origin='lower')
        
        # Création ou mise à jour de la colorbar
        if top:
            if self.bc_carte_2D_top is not None:
                try:
                    self.bc_carte_2D_top.remove()  # Supprimer l'ancienne colorbar
                except:
                    pass
            self.bc_carte_2D_top = fig.colorbar(im, ax=ax, label='Température (°C)')
        else:
            if self.bc_carte_2D_bottom is not None:
                try:
                    self.bc_carte_2D_bottom.remove()
                except:
                    pass
            self.bc_carte_2D_bottom = fig.colorbar(im, ax=ax, label='Température (°C)')
        
        ax.set_title("Simulation Thermique 2D")
        ax.set_xlabel("Position X")
        ax.set_ylabel("Position Y")
        
        # Dessiner l'actuateur et la perturbation si activés
        if self.controlleur.var_afficher_actuateur.get():
            i, j = params['pos_ac']
            nx, ny = params['nx_ac']-1, params['ny_ac']-1
            rect = plt.Rectangle((j - ny//2, i - nx//2), ny, nx, edgecolor='lime', facecolor='none', linewidth=2)
            ax.add_patch(rect)
            
        if self.controlleur.var_afficher_perturbation.get() and params['P_pert'] > 0:
            k, l = params['pos_pert']
            nx, ny = params['nx_pert']-1, params['ny_pert']-1
            rect = plt.Rectangle((l - ny//2, k - nx//2), ny, nx, edgecolor='cyan', facecolor='none', linewidth=2)
            ax.add_patch(rect)
        
        # Ajouter les points des thermistances
        ax.plot(15, 30, 'ro', markersize=5, label="Thermistance 1")
        ax.plot(60, 30, 'go', markersize=5, label="Thermistance 2")
        ax.plot(105, 30, 'bo', markersize=5, label="Position Laser")
        ax.legend(loc='upper right')
        
        canvas.draw()
        
        def update(frame):
            # Vérifier si la simulation doit s'arrêter
            if not self.controlleur.simulation_run or self.controlleur.temps_courant >= params['temps_simulation']:
                try:
                    if top:
                        self.animation1.event_source.stop()
                    else:
                        self.animation2.event_source.stop()
                except:
                    pass
                    
                if top:
                    self.controlleur.simulation_run = False
                    self.controlleur.status_var.set(f"Simulation terminée à {self.controlleur.temps_courant:.2f} s")
                    self.update_graph_temp(True)
                    self.update_graph_temp(False)
                    self.update_graph_energie(True)
                    self.update_graph_energie(False)
                return [im]
            
            # Vérifier si la simulation est en pause
            if self.controlleur.simulation_paused:
                return [im]
            
            # Mettre à jour la simulation si c'est l'animation principale
            if top:
                iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get()))
                
                for _ in range(iterations):
                    # Créer une copie des paramètres avec le temps actuel
                    params_actuels = params.copy()
                    params_actuels['current_time'] = self.controlleur.temps_courant
                    
                    # Calculer la nouvelle matrice de température
                    self.controlleur.T = self.controlleur.simulation_thermique.vector_evolution_temperature(
                        self.controlleur.T, params_actuels)
                    
                    # Enregistrer les températures aux points de mesure
                    temp1 = self.controlleur.T[30, 15] - 273.15
                    temp2 = self.controlleur.T[30, 60] - 273.15
                    temp_laser = self.controlleur.T[30, 105] - 273.15
                    
                    self.controlleur.temp_therm_1.append(temp1)
                    self.controlleur.temp_therm_2.append(temp2)
                    self.controlleur.temp_therm_laser.append(temp_laser)
                    
                    # Calculer l'énergie totale
                    E_current = params['p'] * params['cp'] * np.sum(self.controlleur.T) * params['vol']
                    self.controlleur.energie_list.append(E_current)
                    
                    # Incrémenter le temps
                    self.controlleur.temps_courant += params['dt']
                
                # Mettre à jour les autres graphiques si nécessaire
                if self.controlleur.graphique_top_select.get() == "Évolution Température":
                    self.update_graph_temp(True)
                elif self.controlleur.graphique_top_select.get() == "Énergie Interne":
                    self.update_graph_energie(True)
                
                if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                    self.update_graph_temp(False)
                elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                    self.update_graph_energie(False)
                
                # Mettre à jour le statut
                self.controlleur.status_var.set(f"Simulation en cours... Temps: {self.controlleur.temps_courant:.2f} s / {params['temps_simulation']:.2f} s")
            
            # Mettre à jour l'image avec la nouvelle matrice de température
            temp_data = self.controlleur.T - 273.15
            im.set_data(temp_data)
            
            # Mettre à jour l'échelle de couleur dynamiquement
            vmin = np.min(temp_data)
            vmax = np.max(temp_data)
            im.set_clim(vmin=vmin, vmax=vmax)
            
            # Mettre à jour le titre avec le temps actuel
            ax.set_title(f"Simulation Thermique 2D - Temps: {self.controlleur.temps_courant:.2f} s")
            
            # Redessiner le canvas
            canvas.draw_idle()
            
            return [im]
        
        # Créer l'animation
        anim = FuncAnimation(fig, update, frames=None, interval=50, blit=True, cache_frame_data=False)
        if top:
            self.animation1 = anim
        else:
            self.animation2 = anim

    def animation_3D_démarrer(self, T, params, top=True):
        '''
        Démarre l'animation de la carte thermique 3D
        '''
        if top:
            fig = self.fig_carte_3D_top
            ax = self.ax_carte_3D_top
            canvas = self.canvas_carte_3D_top
        else:
            fig = self.fig_carte_3D_bottom
            ax = self.ax_carte_3D_bottom
            canvas = self.canvas_carte_3D_bottom
            
        ax.clear()
        x = np.linspace(0, params['Lx'], params['n_x'])
        y = np.linspace(0, params['Ly'], params['n_y'])
        X, Y = np.meshgrid(x, y)
        Z = T.T - 273.15
        
        # Calculer les valeurs min et max pour l'échelle de couleur
        vmin = Z.min()
        vmax = Z.max()
        
        surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
        
        if top:
            if self.bc_carte_3D_top is None:
                self.bc_carte_3D_top = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Température (°C)')
            else:
                try:
                    self.bc_carte_3D_top.update_normal(surf)
                except:
                    self.bc_carte_3D_top = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Température (°C)')
        else:
            if self.bc_carte_3D_bottom is None:
                self.bc_carte_3D_bottom = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Température (°C)')
            else:
                try:
                    self.bc_carte_3D_bottom.update_normal(surf)
                except:
                    self.bc_carte_3D_bottom = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Température (°C)')
        
        ax.set_title("Simulation Thermique 3D")
        ax.set_xlabel("Position X (m)")
        ax.set_ylabel("Position Y (m)")
        ax.set_zlabel("Température (°C)")
        canvas.draw()
        
        def update(frame):
            if not self.controlleur.simulation_run or self.controlleur.temps_courant >= params['temps_simulation']:
                try:
                    if top:
                        self.animation1.event_source.stop()
                    else:
                        self.animation2.event_source.stop()
                except:
                    pass
                    
                if top:
                    self.controlleur.simulation_run = False
                    self.controlleur.status_var.set(f"Simulation terminée à {self.controlleur.temps_courant:.2f} s")
                    self.update_graph_temp(True)
                    self.update_graph_temp(False)
                    self.update_graph_energie(True)
                    self.update_graph_energie(False)
                return
            
            # Vérifier si la simulation est en pause
            if self.controlleur.simulation_paused:
                return
            
            if top:
                iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get()))
                
                for _ in range(iterations):
                    # Ajouter le temps actuel aux paramètres
                    params_actuels = params.copy()
                    params_actuels['current_time'] = self.controlleur.temps_courant
                    
                    # Calculer la nouvelle matrice de température
                    self.controlleur.T = self.controlleur.simulation_thermique.vector_evolution_temperature(
                        self.controlleur.T, params_actuels)
                    
                    temp1 = self.controlleur.T[30, 15] - 273.15
                    temp2 = self.controlleur.T[30, 60] - 273.15
                    temp_laser = self.controlleur.T[30, 105] - 273.15
                    
                    self.controlleur.temp_therm_1.append(temp1)
                    self.controlleur.temp_therm_2.append(temp2)
                    self.controlleur.temp_therm_laser.append(temp_laser)
                    
                    E_current = params['p'] * params['cp'] * np.sum(self.controlleur.T) * params['vol']
                    self.controlleur.energie_list.append(E_current)
                    
                    self.controlleur.temps_courant += params['dt']
                
                if self.controlleur.graphique_top_select.get() == "Évolution Température":
                    self.update_graph_temp(True)
                elif self.controlleur.graphique_top_select.get() == "Énergie Interne":
                    self.update_graph_energie(True)
                    
                if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                    self.update_graph_temp(False)
                elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                    self.update_graph_energie(False)
                
                self.controlleur.status_var.set(f"Simulation en cours... Temps: {self.controlleur.temps_courant:.2f} s / {params['temps_simulation']:.2f} s")
            
            ax.clear()
            Z = self.controlleur.T.T - 273.15
            
            # Calculer les nouvelles limites d'échelle de couleur dynamiquement
            vmin = Z.min()
            vmax = Z.max()
            
            surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
            ax.set_title(f"Simulation Thermique 3D - Temps: {self.controlleur.temps_courant:.2f} s")
            ax.set_xlabel("Position X (m)")
            ax.set_ylabel("Position Y (m)")
            ax.set_zlabel("Température (°C)")
            
            if top:
                try:
                    self.bc_carte_3D_top.update_normal(surf)
                except:
                    pass
            else:
                try:
                    self.bc_carte_3D_bottom.update_normal(surf)
                except:
                    pass
                    
            return surf
        
        # Créer l'animation
        anim = FuncAnimation(fig, update, frames=None, interval=50, blit=False, cache_frame_data=False)
        if top:
            self.animation1 = anim
        else:
            self.animation2 = anim
        canvas.draw()