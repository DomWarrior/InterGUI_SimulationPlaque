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

   
        self.fenêtre_top = ttk.Frame(self.fenêtre)                      # Sous-fenêtre du dessus                      
        self.fenêtre.add(self.fenêtre_top, weight=50)                   # Qui va initialement correspondre à 50% en poids de la fenêtre initiale

        self.fenêtre_bottom = ttk.Frame(self.fenêtre)                   # Sous-fenêtre du dessous
        self.fenêtre.add(self.fenêtre_bottom, weight=50)

        self.bc_carte_2D_top = None                                     #Instance qui va garder en mémoire la barre de couleur des graphiques. Utile pour être en mesure de réinitialiser celle-ci
        self.bc_carte_3D_top = None
        self.bc_carte_2D_bottom = None
        self.bc_carte_3D_bottom = None
        
      
        self.animation1 = None                                          #Instance qui va contenir les animations
        self.animation2 = None
        
        
        self.créer_graphiques()                                         # Créer tous les graphiques possibles
        
        self.initialiser_graphique()                                    # Initialiser les graphiques selon les sélections par défaut

    def créer_graphiques(self):
        

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
        
        for widget in self.fenêtre_top.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.pack_forget()
        
        for widget in self.fenêtre_bottom.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.pack_forget()
        

        self.graphique_selection(self.controlleur.graphique_top_select.get(), self.fenêtre_top, top=True)
        self.graphique_selection(self.controlleur.graphique_bottom_selcet.get(), self.fenêtre_bottom, top=False)

    def graphique_selection(self, type_graphique, fenêtre_parent, top=True):
    
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
                    # Nettoyer toutes les barres de couleur de la figure 3D
                    for cbar in self.fig_carte_3D_top.get_axes():
                        if cbar is not self.ax_carte_3D_top:  # Si ce n'est pas l'axe principal
                            try:
                                cbar.remove()  # Supprimer la barre de couleur
                            except:
                                pass
                    self.bc_carte_3D_top = None
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
                    # Nettoyer toutes les barres de couleur de la figure 3D
                    for cbar in self.fig_carte_3D_bottom.get_axes():
                        if cbar is not self.ax_carte_3D_bottom:  # Si ce n'est pas l'axe principal
                            try:
                                cbar.remove()  # Supprimer la barre de couleur
                            except:
                                pass
                    self.bc_carte_3D_bottom = None
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
        ax.plot(times, temp_laser, 'b-.', label='Thermistance Laser')
        
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Température (°C)")
        ax.set_title(f"Évolution des températures - Temps simulé: {self.controlleur.temps_courant:.2f} s")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    def update_graph_energie(self, top=True):

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
        Lance les animations dans les deux sous-fenêtres avec gestion de toutes les combinaisons
        '''
        try:
            conditions = []
            conditions.append(0 <= self.controlleur.var_pos_pert_x.get() <= self.controlleur.var_n_x.get())
            conditions.append(0 <= self.controlleur.var_pos_ac_x.get() <= self.controlleur.var_n_x.get())
            conditions.append(0 <= self.controlleur.var_pos_therm1x.get() <= self.controlleur.var_n_x.get())
            conditions.append(0 <= self.controlleur.var_pos_therm2x.get() <= self.controlleur.var_n_x.get())
            conditions.append(0 <= self.controlleur.var_pos_therm3x.get() <= self.controlleur.var_n_x.get())
            
            conditions.append(0 <= self.controlleur.var_pos_pert_y.get() <= self.controlleur.var_n_y.get())
            conditions.append(0 <= self.controlleur.var_pos_ac_y.get() <= self.controlleur.var_n_y.get())
            conditions.append(0 <= self.controlleur.var_pos_therm1y.get() <= self.controlleur.var_n_y.get())
            conditions.append(0 <= self.controlleur.var_pos_therm2y.get() <= self.controlleur.var_n_y.get())
            conditions.append(0 <= self.controlleur.var_pos_therm3y.get() <= self.controlleur.var_n_y.get())
        
            if all(conditions):
                
                pass
            else:
                messagebox.showinfo("Erreur de positionnement", 
                   "Certaines positions sont en dehors des limites permises.\n\n"
                   "Veuillez vérifier que toutes les coordonnées sont comprises entre 0 et les dimensions maximales du système (n_x , n_y) "
                   )
                
            


        except (AttributeError, ValueError, KeyError):
                
                pass

    
        if chart1 == "Évolution Température":
            self.update_graph_temp(top=True)
        elif chart1 == "Énergie Interne":
            self.update_graph_energie(top=True)
            
        if chart2 == "Évolution Température":
            self.update_graph_temp(top=False)
        elif chart2 == "Énergie Interne":
            self.update_graph_energie(top=False)
        
       
        has_animation_top = chart1 in ["Carte Thermique 2D", "Carte Thermique 3D"]
        has_animation_bottom = chart2 in ["Carte Thermique 2D", "Carte Thermique 3D"]
        
        if has_animation_top:
            if chart1 == "Carte Thermique 2D":
                self.animation_2D_démarrer(T, params, top=True)  
            elif chart1 == "Carte Thermique 3D":
                self.animation_3D_démarrer(T, params, top=True)  
            
            
            if has_animation_bottom:
                if chart2 == "Carte Thermique 2D":
                    
                    self.animation_2D_démarrer(T, params, top=False)  
                elif chart2 == "Carte Thermique 3D":
                    self.animation_3D_démarrer(T, params, top=False)
        
        
        elif has_animation_bottom:
            if chart2 == "Carte Thermique 2D":
               
                self.animation_2D_démarrer(T, params, top=True)
            elif chart2 == "Carte Thermique 3D":
                self.animation_3D_démarrer(T, params, top=True)
        
       
        else:
            
            self.animation_2D_démarrer(T, params, top=True)
            self.canvas_carte_2D_top.get_tk_widget().pack_forget()

        

    

    
    def pause_animations(self):
    
        if self.animation1 :
            self.animation1.event_source.stop()
        if self.animation2 :
            self.animation2.event_source.stop()
        if self.controlleur.chronometre_run:
            self.controlleur.chronometre_run = False
    
    
    def poursuivre_animations(self):
       
        params = self.controlleur.recup_params_sim()
        current_T = self.controlleur.T
        
        
        chart1 = self.controlleur.graphique_top_select.get()
        chart2 = self.controlleur.graphique_bottom_selcet.get()
        
        self.clean_graph_widgets(chart1, True)  # Nettoyer graphique du haut
        self.clean_graph_widgets(chart2, False)  # Nettoyer graphique du bas
        
        self.lancer_animations(current_T, params, chart1, chart2) #On redémarre la simulation avec les nouvelles variables et sélections
    


    def clean_graph_widgets(self, type_graphique, top=True):
        if top:
            if type_graphique == "Carte Thermique 2D":
                ax = self.ax_carte_2D_top
                cb_attr = 'bc_carte_2D_top'
            elif type_graphique == "Carte Thermique 3D":
                ax = self.ax_carte_3D_top
                cb_attr = 'bc_carte_3D_top'
            else:
                return  
        else:
            if type_graphique == "Carte Thermique 2D":
                ax = self.ax_carte_2D_bottom
                cb_attr = 'bc_carte_2D_bottom'
            elif type_graphique == "Carte Thermique 3D":
                ax = self.ax_carte_3D_bottom
                cb_attr = 'bc_carte_3D_bottom'
            else:
                return  
        
       
        ax.clear()
        
        
        colorbar = getattr(self, cb_attr, None)
        if colorbar is not None:
            try:
                colorbar.remove()  
            except (AttributeError, ValueError, KeyError):
                
                pass
            setattr(self, cb_attr, None)
    
    def stop_animations(self):
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



        pos_t1x = self.controlleur.var_pos_therm1x.get() 
        pos_t1y = self.controlleur.var_pos_therm1y.get() 
        pos_t2x =   self.controlleur.var_pos_therm2x.get() 
        pos_t2y = self.controlleur.var_pos_therm2y.get() 
        pos_t3x = self.controlleur.var_pos_therm3x.get() 
        pos_t3y = self.controlleur.var_pos_therm3y.get() 


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
            cb_attr = 'bc_carte_2D_bottom'

        
            
        ax.clear()
        
        # Initialisation de l'image
        temp_data = T   
        im = ax.imshow(temp_data, cmap='hot', interpolation='nearest', origin='lower') # Initialisation de la matrice de température (avant itération)
        
        
        for cbar in fig.get_axes():
            if cbar is not ax:  # Si ce n'est pas l'axe principal
                cbar.remove()  # Supprimer la barre de couleur

        # Position fixe pour l'axe principal
        ax.set_position([0.125, 0.1, 0.6, 0.8])

        # Créer une barre de couleur avec une position fixe
        cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])  # [x, y, width, height]
        colorbar = fig.colorbar(im, cax=cax)
        colorbar.set_label('Température (°C)')

        if top:
            self.bc_carte_2D_top = colorbar
        else:
            self.bc_carte_2D_bottom = colorbar
        
        ax.set_title("Simulation Thermique 2D")
        ax.set_xlabel("Position X")
        ax.set_ylabel("Position Y")
        ax.plot(pos_t1y, pos_t1x, 'ro', markersize=5, label="Thermistance 1")
        ax.plot(pos_t2y, pos_t2x, 'go', markersize=5, label="Thermistance 2")
        ax.plot(pos_t3y, pos_t3x, 'bo', markersize=5, label="Thermistance Laser")
        ax.legend(loc='upper right')
        
        ax.set_position([0.125, 0.1, 0.6, 0.8])


        
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
                    self.update_graph_temp(True)
                    self.update_graph_temp(False)
                    self.update_graph_energie(True)
                    self.update_graph_energie(False)
            
                # Mettre à jour l'image avec la matrice de température actuelle
                temp_data = self.controlleur.T 
                im.set_data(temp_data)
                
                # Dessiner l'actuateur et la perturbation
                if self.controlleur.var_afficher_actuateur.get():
                    i, j = params['pos_ac']
                    nx, ny = params['nx_ac'], params['ny_ac']
                    rect = plt.Rectangle((j - ny//2, i - nx//2), ny, nx, edgecolor='lime', facecolor='none', linewidth=2)
                    ax.add_patch(rect)
                    
                if self.controlleur.var_afficher_perturbation.get() and params['P_pert'] > 0:
                    k, l = params['pos_pert']
                    nx, ny = params['nx_pert'], params['ny_pert']
                    rect = plt.Rectangle((l - ny//2, k - nx//2), ny, nx, edgecolor='cyan', facecolor='none', linewidth=2)
                    ax.add_patch(rect)
                
            
                
                
                canvas.draw_idle()
                return [im]
            
            
            if self.controlleur.simulation_paused:
                return [im]
            
            
            if top:
                
                if self.controlleur.animation_on.get() == 'Activée':
                    
                    iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get()))
                   
                else:
                    iterations = self.controlleur.var_Nt

                
                
                for _ in range(iterations):
                    if self.controlleur.temps_courant >= params['temps_simulation']:
                        break
                    
                    params_actuels = params.copy()
                    params_actuels['current_time'] = self.controlleur.temps_courant
                
                    
                    self.controlleur.T = self.controlleur.simulation_thermique.vector_evolution_temperature(
                        self.controlleur.T, params_actuels)
                    
                    
                    temp1 = self.controlleur.T[pos_t1x, pos_t1y] 
                    temp2 = self.controlleur.T[pos_t2x, pos_t2y] 
                    temp_laser = self.controlleur.T[pos_t3x, pos_t3y] 
                    
                    self.controlleur.temp_therm_1.append(temp1)
                    self.controlleur.temp_therm_2.append(temp2)
                    self.controlleur.temp_therm_laser.append(temp_laser)
                    
                
                    E_current = params['p'] * params['cp'] * np.sum(self.controlleur.T) * params['vol']
                    self.controlleur.energie_list.append(E_current)
                    
                    
                    self.controlleur.temps_courant += params['dt']
                
                # Mettre à jour les autres graphiques 
                if self.controlleur.graphique_top_select.get() == "Évolution Température":
                    self.update_graph_temp(True)
                elif self.controlleur.graphique_top_select.get() == "Énergie Interne":
                    self.update_graph_energie(True)
                
                if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                    self.update_graph_temp(False)
                elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                    self.update_graph_energie(False)
                
                if self.controlleur.var_afficher_actuateur.get():
                    i, j = params['pos_ac']
                    nx, ny = params['nx_ac'], params['ny_ac']
                    rect = plt.Rectangle((j - ny//2, i - nx//2), ny, nx, edgecolor='lime', facecolor='none', linewidth=2)
                    ax.add_patch(rect)
                    
                if self.controlleur.var_afficher_perturbation.get() and params['P_pert'] > 0:
                    k, l = params['pos_pert']
                    nx, ny = params['nx_pert'], params['ny_pert']
                    rect = plt.Rectangle((l - ny//2, k - nx//2), ny, nx, edgecolor='cyan', facecolor='none', linewidth=2)
                    ax.add_patch(rect)
            
            # On remet à jour la matrice de température après les itération pour la prochaine frame
            temp_data = self.controlleur.T 
            im.set_data(temp_data)
            
            # On remet à jour l'échelle de température
            vmin = np.min(temp_data)
            vmax = np.max(temp_data)
            im.set_clim(vmin=vmin, vmax=vmax)
        
            ax.set_title(f"Simulation Thermique 2D - Temps: {self.controlleur.temps_courant:.2f} s")
            canvas.draw_idle()
            
            return [im]
        
       
        anim = FuncAnimation(fig, update, frames=None, interval=5, blit=True, cache_frame_data=False)
        if top:
            self.animation1 = anim
        else:
            self.animation2 = anim
        

    def animation_3D_démarrer(self, T, params, top=True):
        '''
        Démarre l'animation de la carte thermique 3D
        '''

        pos_t1x = self.controlleur.var_pos_therm1x.get() 
        pos_t1y = self.controlleur.var_pos_therm1y.get() 
        pos_t2x = self.controlleur.var_pos_therm2x.get() 
        pos_t2y = self.controlleur.var_pos_therm2y.get() 
        pos_t3x = self.controlleur.var_pos_therm3x.get() 
        pos_t3y = self.controlleur.var_pos_therm3y.get()

        if top:
            fig = self.fig_carte_3D_top
            ax = self.ax_carte_3D_top
            canvas = self.canvas_carte_3D_top
        else:
            fig = self.fig_carte_3D_bottom
            ax = self.ax_carte_3D_bottom
            canvas = self.canvas_carte_3D_bottom
        ax.set_position([0.125, 0.1, 0.6, 0.8])   
        ax.clear()
        x = np.linspace(0, params['Lx'], params['n_x'])
        y = np.linspace(0, params['Ly'], params['n_y'])
        X, Y = np.meshgrid(x, y)
        Z = T.T 
        
        vmin = Z.min()
        vmax = Z.max()
        
        surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
        
        
        cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])  
        colorbar = fig.colorbar(surf, cax=cax)
        colorbar.set_label('Température (°C)')

        if top:
            self.bc_carte_3D_top = colorbar
        else:
            self.bc_carte_3D_bottom = colorbar
        
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
                #iterations = max(1, self.controlleur.var_Nt)
                
                for _ in range(iterations):
                    if self.controlleur.temps_courant >= params['temps_simulation']:
                        break
                    
                    params_actuels = params.copy()
                    params_actuels['current_time'] = self.controlleur.temps_courant
                    
                    # Calculer la nouvelle matrice de température
                    self.controlleur.T = self.controlleur.simulation_thermique.vector_evolution_temperature(
                        self.controlleur.T, params_actuels)
                    
                    temp1 = self.controlleur.T[pos_t1x, pos_t1y] 
                    temp2 = self.controlleur.T[pos_t2x, pos_t2y] 
                    temp_laser = self.controlleur.T[pos_t3x, pos_t3y] 
                    
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
                
                
            ax.set_position([0.125, 0.1, 0.6, 0.8])
            ax.clear()
            Z = self.controlleur.T.T 
            
            # Calculer les nouvelles limites d'échelle de couleur dynamiquement
            vmin = Z.min()
            vmax = Z.max()
            
            surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
            ax.set_title(f"Simulation Thermique 3D - Temps: {self.controlleur.temps_courant:.2f} s")
            ax.set_xlabel("Position X (m)")
            ax.set_ylabel("Position Y (m)")
            ax.set_zlabel("Température (°C)")
            
            
            for cbar in fig.get_axes():
                if cbar is not ax:
                    cbar.remove()

            # Recréer une barre de couleur à position fixe
            cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
            colorbar = fig.colorbar(surf, cax=cax)
            colorbar.set_label('Température (°C)')

            if top:
                self.bc_carte_3D_top = colorbar
            else:
                self.bc_carte_3D_bottom = colorbar
                    
            return surf
        
        # Créer l'animation
        anim = FuncAnimation(fig, update, frames=None, interval=50, blit=False, cache_frame_data=False)
        if top:
            self.animation1 = anim
        else:
            self.animation2 = anim
        canvas.draw()