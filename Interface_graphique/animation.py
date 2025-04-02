import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import time

class FenêtreAnimations:
    '''Cette classe correspond à la fenêtre de droite que l'utilisateur va voir en ouvrant l'interface. 
    Cette fenêtre va être divisée en 2 sous-fenêtres afin d'offrir la possibilité d'afficher 2 graphiques simultanément. Ces fenêtres vont permettre d'afficher des graphiques (la réponse à l'échelon
    des trois thermistances et l'énergie thermique interne de la plaque) et des animations (carte thermique 2D et 3D dans la plaque).
    Cette classe va également gérer toutes les fonctionnalités offertes à l'utilisateur en lien avec les graphiques et les animations.
    '''




    def __init__(self, fenêtre_main, controlleur):
        self.fenêtre_main = fenêtre_main             # Cette instance correspond à la fenêtre de droite de l'interface
        self.controlleur = controlleur               # Cette instance va permettre de contrôler la simulation en y stockant les informations, paramètres... En réalité , celle-ci sera un objet de la classe FenêtreInterface de interface.py

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

        self.frame_chrono = ttk.Frame(fenêtre_main)
        self.frame_chrono.pack(side=tk.BOTTOM, pady=5)
        self.label_chrono = ttk.Label(self.frame_chrono, text="Temps écoulé: 00:00:00", font=("Arial", 10))
        self.label_chrono.pack(padx=10, pady=5)
        self.temps_ecoule_total = 0
        self.temps_debut_chrono = 0
      
        
        
        
        self.créer_graphiques()                                         # Créer tous les graphiques possibles lors du lancement de l'interface
        
        self.initialiser_graphique()                                    # Initialiser les graphiques selon les sélections par défaut




    def créer_graphiques(self):
        '''
        Cette fonction va créer la mise en forme de chacun des graphiques.
        '''


        

        # Figure de la carte 2D thermique
        self.fig_carte_2D_top = Figure(figsize=(6, 5), dpi=100)                 #Création d'une figure matplotlib.figure de (6,5) pouces avec une résolution de 100 points par pouce 
        self.ax_carte_2D_top = self.fig_carte_2D_top.add_subplot(111)           #Création du graphique 
        self.ax_carte_2D_top.set_xlabel("Position Y")                       #On définit les axes
        self.ax_carte_2D_top.set_ylabel("Position X")
        self.ax_carte_2D_top.set_title("Simulation Thermique 2D")  
        self.canvas_carte_2D_top = FigureCanvasTkAgg(self.fig_carte_2D_top, master=self.fenêtre_top)           #La méthode FigureCanvasTkAgg permet d'intégrer des figures Matplotlib dans l'interface. Ici, on met cet objet dans fenêtre_top, donc pour la sous-fenêtre du haut 
    

        # On refait exactement la même chose pour les autres cartes thermiques
        self.fig_carte_3D_top = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_3D_top = self.fig_carte_3D_top.add_subplot(111, projection='3d')          #Ici on précise que c'est un graphique 3D qu'on veut
        self.ax_carte_3D_top.set_xlabel("Position X")
        self.ax_carte_3D_top.set_ylabel("Position Y")
        self.ax_carte_3D_top.set_zlabel("Simulation Thermique 3D")
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
        Cette fonction sert à initialiser les graphiques et à mettre les graphiques choisis aux fenêtres appropriées.
        '''

        
        for widget in self.fenêtre_top.winfo_children():        #Avant d'initialiser les graphiques, il faut s'assurer que tous les objets dans la sous-fenêtre soit vidée.
                widget.pack_forget()
        
        for widget in self.fenêtre_bottom.winfo_children():
                widget.pack_forget()
        

        self.graphique_selection(self.controlleur.graphique_top_select.get(), top=True)
        self.graphique_selection(self.controlleur.graphique_bottom_selcet.get(), top=False)




    def graphique_selection(self, type_graphique,top=True):
    
        if top:
            canvas_carte_2D = self.canvas_carte_2D_top
            canvas_carte_3D = self.canvas_carte_3D_top
        else:
            canvas_temp = self.canvas_temp_bottom
            canvas_energie = self.canvas_energie_bottom
        
        
        if type_graphique == "Carte Thermique 2D":              # Si l'utilisateur sélectionne ce cas
            canvas_carte_2D.get_tk_widget().pack(fill=tk.BOTH, expand=True)     # On récupère le canvas associé à cette sélection (créer par la fonction créer_graphique).Maintenant, il faut insérer cet objet dans la fenêtre et pour cela on utilise la méthode pack()
            
        elif type_graphique == "Carte Thermique 3D":
            canvas_carte_3D.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        elif type_graphique == "Évolution Température":
            canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        elif type_graphique == "Énergie Interne":
            canvas_energie.get_tk_widget().pack(fill=tk.BOTH, expand=True)




    def reset_graphiques(self):
       
        self.stop_animations()

        
        graph_top = self.controlleur.graphique_top_select.get()
        graph_bottom = self.controlleur.graphique_bottom_selcet.get()

        
        if graph_top == "Carte Thermique 2D":
            if self.bc_carte_2D_top is not None:
                self.bc_carte_2D_top.remove()
                self.bc_carte_2D_top = None
            
            self.ax_carte_2D_top.clear()
            self.canvas_carte_2D_top.draw()
            
        elif graph_top == "Carte Thermique 3D":
    
            for barre_color in self.fig_carte_3D_top.get_axes():
                if barre_color is not self.ax_carte_3D_top:  
                    barre_color.remove()  
            self.bc_carte_3D_top = None
            
            
            self.ax_carte_3D_top.clear()
            self.canvas_carte_3D_top.draw()

    
        if graph_bottom == "Évolution Température":
            self.ax_temp_bottom.clear()
            self.ax_temp_bottom.set_xlabel("Temps (s)")
            self.ax_temp_bottom.set_ylabel("Température (°C)")
            self.ax_temp_bottom.set_title("Évolution des températures")
            self.ax_temp_bottom.grid(True)
            self.canvas_temp_bottom.draw()
            
        elif graph_bottom == "Énergie Interne":
            self.ax_energie_bottom.clear()
            self.ax_energie_bottom.set_xlabel("Temps (s)")
            self.ax_energie_bottom.set_ylabel("Énergie interne (J)")
            self.ax_energie_bottom.set_title("Évolution de l'énergie thermique interne")
            self.ax_energie_bottom.grid(True)
            self.canvas_energie_bottom.draw()




    def graph_temp(self, top=True):

        '''
        Fonction qui génère et stock les données qui seront affichées dans le graphique des températures des thermistances

        '''

        if not self.controlleur.temp_therm_1:       #Si la liste de température est vide alors on sort de la fonction
            return
        
        if top:                                     #On associe le bon graphique et canvas en fonction de la sélection up/down
            ax = self.ax_temp_top
            canvas = self.canvas_temp_top
        else:
            ax = self.ax_temp_bottom
            canvas = self.canvas_temp_bottom
            
        ax.clear()                                  #On s'assure de vider le contenu du graphique avant de le remplir à nouveau
        step = max(1, len(self.controlleur.temp_therm_1) // 1000)   # Ici , comme le pas de temps de la simulation est très petit (0.001), alors on veut pas forcément afficher tous les points de la simulation. Ici on décide de diviser le nombre de points par 1000
        temp1 = self.controlleur.temp_therm_1[::step]               # On prend 1 point à chaque saut           
        temp2 = self.controlleur.temp_therm_2[::step]
        temp_laser = self.controlleur.temp_therm_laser[::step]
        times = [i * 0.001 for i in range(0, len(self.controlleur.temp_therm_1), step)]  # Pour avoir une correspondance entre le temps et la température, on ajuster une vecteur temps en conséquence
        
        ax.plot(times, temp1, 'r-', label='Thermistance 1')                             #Courbe thermistance 1
        ax.plot(times, temp2, 'g--', label='Thermistance 2')                            #Courbe thermistance 2
        ax.plot(times, temp_laser, 'b-.', label='Thermistance Laser')                   #Courbe thermistance laser
        
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Température (°C)")
        ax.set_title(f"Évolution des températures - Temps simulé: {self.controlleur.temps_courant:.2f} s")
        ax.legend()
        ax.grid(True)
        canvas.draw()                           # On actualise le contenu de canvas




    def graph_energie(self, top=True):

        '''
        Fonction qui génère et stock les données qui seront affichées dans le graphique de l'énergie thermique interne en fonction du temps.
        Le code est quasi identique à la fonction grap_temp...
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




    def lancer_animations(self, T, params, graph_top, graph_bottom):
        '''
        Lance les animations dans les deux sous-fenêtres avec gestion de toutes les combinaisons

        '''
        try:                #Ici on vérifie si l'utilisateur n'a pas positionné les éléments en dehors de la matrice de température avant de lancer la simulation
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
        except (AttributeError):
                
                pass

        
        if graph_top == "Carte Thermique 2D":
            self.animation_2D_démarrer(T, params, top=True)
        elif graph_top == "Carte Thermique 3D":
            self.animation_3D_démarrer(T, params, top=True)
        if graph_bottom == "Évolution Température":
            self.graph_temp(top=False)
        elif graph_bottom == "Énergie Interne":
            self.graph_energie(top=False)
            



    def pause_animations(self):
        '''
        Fonction qui va permettre de mettre sur pause la simulation
        '''
    
        if self.animation1 :
            self.animation1.event_source.stop()                 #Ici, self.animation est un objet FuncAnimation. Celui-ci possède un méthode event_source qui est un style de timer. 
                                                                #C'est ce timer qui appel à répétion la fonction update de FuncAnimation. event_source possède lui même une méthode .stop() qui permet d'arrêter ce timer et donc la fonction update n'est plus appelée.
        if self.animation2 :
            self.animation2.event_source.stop()
        if self.controlleur.chronometre_run:
            self.controlleur.chronometre_run = False




    def poursuivre_animations(self):

        '''
        Cette fonction va être appeler lorsque l'utilisateur va appuyer de nouveau sur le bouton Reprendre. Ici, on permet à l'utilisateur 
        de changer les paramètres de la simulation.
        '''
       
        params = self.controlleur.recup_params_sim()            #Avant de relancer a simulation, on s'assurer de récupérer tous les paramètres. Cela va nous permettre de récolter les paramètres potentiellement modifiés par l'utilisateur.
        current_T = self.controlleur.T                          # On récupère la matrice de température au temps au la simulation a été mise sur pause.
        
        
        graph_top = self.controlleur.graphique_top_select.get()
        graph_bottom = self.controlleur.graphique_bottom_selcet.get()
        
        
        self.lancer_animations(current_T, params, graph_top, graph_bottom) #On redémarre la simulation avec les nouvelles variables , sélections




    def stop_animations(self):

        '''
        Cette fonction va gérer l'arrêt de la simulation. Elle permet de changer l'état des instances animation1 et animation2.
        '''
        try:
            if self.animation1 is not None:                 #Si l'état de l'animation n'est pas None (l'animation est en cours), alors on l'arrêt
                self.animation1.event_source.stop()
                self.animation1 = None                      #On met l'état à None pour dire que l'animation et arrêtée.
        except:                                             #Si un code d'erreur quelconque se produit, et bien on s'assure que l'état soit quand même à None
            self.animation1 = None
        
        try:
            if self.animation2 is not None:
                self.animation2.event_source.stop()
                self.animation2 = None
        except:
            self.animation2 = None
        



        self.temps_ecoule_total = 0
        self.temps_debut_chrono = 0
        self.label_chrono.config(text="Temps écoulé: 00:00:00")




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
        else:
            fig = self.fig_carte_2D_bottom
            ax = self.ax_carte_2D_bottom
            canvas = self.canvas_carte_2D_bottom
            

        
            
        ax.clear()
        
        # Initialisation de l'image
        temp_data = T   
        im = ax.imshow(temp_data, cmap='hot', interpolation='nearest', origin='lower') # Initialisation de la matrice de température (avant itération)
        
        
        for barre_color in fig.get_axes():
            if barre_color is not ax:  # Si ce n'est pas l'axe principal
                barre_color.remove()  # Supprimer la barre de couleur

        
        ax.set_position([0.125, 0.1, 0.6, 0.8])

        # Créer une barre de couleur avec une position fixe
        cax = fig.add_axes([0.85, 0.1, 0.03, 0.8]) 
        colorbar = fig.colorbar(im, cax=cax)
        colorbar.set_label('Température (°C)')

        if top:
            self.bc_carte_2D_top = colorbar
        else:
            self.bc_carte_2D_bottom = colorbar
        
        ax.set_title("Simulation Thermique 2D")
        ax.set_xlabel("Position Y")
        ax.set_ylabel("Position X")
        ax.plot(pos_t1y, pos_t1x, 'ro', markersize=5, label="Thermistance 1")
        ax.plot(pos_t2y, pos_t2x, 'go', markersize=5, label="Thermistance 2")
        ax.plot(pos_t3y, pos_t3x, 'bo', markersize=5, label="Thermistance Laser")
        ax.legend(loc='upper right')
        
        ax.set_position([0.125, 0.1, 0.6, 0.8])


        self._message_shown = True

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
                    self.graph_temp(True)
                    self.graph_temp(False)
                    self.graph_energie(True)
                    self.graph_energie(False)
            
                # On met à jour l'image avec la nouvelle matrice de température
                temp_data = self.controlleur.T 
                im.set_data(temp_data)
                
                # On dessine l'actuateur et la perturbation
                if self.controlleur.var_afficher_actuateur.get() :
                    i, j = params['pos_ac']
                    nx, ny = params['nx_ac'], params['ny_ac']
                    rect = plt.Rectangle((j - ny/2-1, i - nx/2-1), ny+2, nx+2, edgecolor='lime', facecolor='none', linewidth=2)
                    print(j - ny//2, i - nx//2)
                    print(j - ny/2, i - nx/2)
                    ax.add_patch(rect)
                    
                if self.controlleur.var_afficher_perturbation.get() and float(self.controlleur.var_P_pert.get()) > 0:
                    k, l = params['pos_pert']
                    nx, ny = params['nx_pert'], params['ny_pert']
                    rect = plt.Rectangle((l - ny/2-1, k - nx/2-1), ny+2, nx+2, edgecolor='cyan', facecolor='none', linewidth=2)
                    ax.add_patch(rect)
                
            
                
                
                canvas.draw_idle()
                return [im]
            
            
            if self.controlleur.simulation_paused:
                return [im]
            
            
            if top or (not top and self.animation1 is None):
                
                if self.controlleur.animation_on.get() == 'Activée':
                    
                    iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get()))  # À chaque Frame, le nombre d'itération par frame va dépendre de la sélection de l'utilisateur.  
                   
                else:                                                                             # Si l'utilisateur désactive l'animation (il ne veut pas d'animation, mais juste les résultats)
                    iterations = self.controlleur.var_Nt                                          # On fait toutes les itérations de la simulation en une seule frame !
                                                                       #Pour éviter que l'utilisateur pense que la simulation soit dysfonctionnelle , on lui affiche un message pour dire que la simulation est en cours
                    #messagebox.showinfo('Information', 'Simulation en cours ... Veuillez patienter')
                    temps_debut = time.time()  
                    

                
                
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
                    commande_actuateur = self.controlleur.var_current.get()
                    commande_perturbation = self.controlleur.var_P_pert.get()  
                    
                    self.controlleur.temp_therm_1.append(temp1)
                    self.controlleur.temp_therm_2.append(temp2)
                    self.controlleur.temp_therm_laser.append(temp_laser)
                    self.controlleur.commande_ac.append(commande_actuateur)
                    self.controlleur.commande_pert.append(commande_perturbation)
                    
                
                    E_current = params['p'] * params['cp'] * np.sum(self.controlleur.T+237.15) * params['vol']
                    self.controlleur.energie_list.append(E_current)
                    
                    
                    self.controlleur.temps_courant += params['dt']
                
                if self.controlleur.animation_on.get() == 'Désactivée':
                    temps_fin = time.time()
                    temps_ecoule = temps_fin - temps_debut
                    minutes = int(temps_ecoule // 60)
                    secondes = int(temps_ecoule % 60)
                    millisecondes = int((temps_ecoule % 1) * 1000)
                    self.controlleur.label_chrono.config(text=f"{minutes:02d}:{secondes:02d}:{millisecondes:03d}")
                    self.controlleur.temps_ecoule_total = temps_ecoule
                


                
                # Mettre à jour les autres graphiques 
                if self.controlleur.graphique_top_select.get() == "Évolution Température":
                    self.graph_temp(True)
                elif self.controlleur.graphique_top_select.get() == "Énergie Interne":
                    self.graph_energie(True)
                
                if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                    self.graph_temp(False)
                elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                    self.graph_energie(False)
                
                if self.controlleur.var_afficher_actuateur.get():
                    i, j = params['pos_ac']
                    nx, ny = params['nx_ac'], params['ny_ac']
                    rect = plt.Rectangle((j - ny/2-1, i - nx/2-1), ny+2, nx+2, edgecolor='lime', facecolor='none', linewidth=2)
                    ax.add_patch(rect)
                    
                if self.controlleur.var_afficher_perturbation.get() and params['P_pert'] > 0:
                    k, l = params['pos_pert']
                    nx, ny = params['nx_pert'], params['ny_pert']
                    rect = plt.Rectangle((l - ny/2-1, k - nx/2-1), ny+2, nx+2, edgecolor='cyan', facecolor='none', linewidth=2)
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
        ax.set_xlabel("Position Y (m)")
        ax.set_ylabel("Position X (m)")
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
                    self.graph_temp(True)
                    self.graph_temp(False)
                    self.graph_energie(True)
                    self.graph_energie(False)
                return
            
            # Vérifier si la simulation est en pause
            if self.controlleur.simulation_paused:
                return
            
            if top or (not top and self.animation1 is None):
                if self.controlleur.animation_on.get() == 'Activée':
                    iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get()))  # À chaque Frame, le nombre d'itération par frame va dépendre de la sélection de l'utilisateur.  
                else:  # Si l'utilisateur désactive l'animation (il ne veut pas d'animation, mais juste les résultats)
                    iterations = self.controlleur.var_Nt  
                    temps_debut = time.time()

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
                    commande_actuateur = self.controlleur.var_current.get()
                    commande_perturbation = self.controlleur.var_P_pert.get()  
                    
                    self.controlleur.temp_therm_1.append(temp1)
                    self.controlleur.temp_therm_2.append(temp2)
                    self.controlleur.temp_therm_laser.append(temp_laser)
                    self.controlleur.commande_ac.append(commande_actuateur)
                    self.controlleur.commande_pert.append(commande_perturbation)
                    
                    
                    E_current = params['p'] * params['cp'] * np.sum(self.controlleur.T+273.15) * params['vol']
                    self.controlleur.energie_list.append(E_current)
                    
                    self.controlleur.temps_courant += params['dt']

                if self.controlleur.animation_on.get() == 'Désactivée':
                    temps_fin = time.time()
                    temps_ecoule = temps_fin - temps_debut
                    minutes = int(temps_ecoule // 60)
                    secondes = int(temps_ecoule % 60)
                    millisecondes = int((temps_ecoule % 1) * 1000)
                    self.controlleur.label_chrono.config(text=f"{minutes:02d}:{secondes:02d}:{millisecondes:03d}")
                    self.controlleur.f_interface.update()  # Force la mise à jour de l'interface
                    self.controlleur.temps_ecoule_total = temps_ecoule
                    
                    # Forcer la mise à jour du graphique 3D avec le résultat final
                    ax.clear()
                    Z = self.controlleur.T.T 
                    vmin = Z.min()
                    vmax = Z.max()
                    surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
                    ax.set_title(f"Simulation Thermique 3D - Temps: {self.controlleur.temps_courant:.2f} s")
                    ax.set_xlabel("Position X (m)")
                    ax.set_ylabel("Position Y (m)")
                    ax.set_zlabel("Température (°C)")
                    
                    for barre_color in fig.get_axes():
                        if barre_color is not ax:
                            barre_color.remove()
                            
                    cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
                    colorbar = fig.colorbar(surf, cax=cax)
                    colorbar.set_label('Température (°C)')
                    
                    if top:
                        self.bc_carte_3D_top = colorbar
                    else:
                        self.bc_carte_3D_bottom = colorbar
                        
                    canvas.draw()  # Très important : force le rafraîchissement immédiat du canvas
                    
                
                if self.controlleur.graphique_top_select.get() == "Évolution Température":
                    self.graph_temp(True)
                elif self.controlleur.graphique_top_select.get() == "Énergie Interne":
                    self.graph_energie(True)
                    
                if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                    self.graph_temp(False)
                elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                    self.graph_energie(False)
                
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
            
                for barre_color in fig.get_axes():
                    if barre_color is not ax:
                        barre_color.remove()

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