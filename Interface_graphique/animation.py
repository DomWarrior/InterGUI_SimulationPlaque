import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import time

class FenêtreAnimations:
    '''
    Cette classe va gérer l'animation des graphiques de l'interface graphique (carte thermique 2D et 3D, évolution température thermistances et énergie interne).
    Elle va aussi permettre de créer les graphiques, de les mettre à jour et de gérer les animations en interaction avec le fichier interface.py.
    Aussi, elle gérer les événements de l'interface graphique liés aux graphiques (Lancer , Arrêter, Mettre sur pause , Sauvegarder , Charger ...).
    Cette classe va également gérer les chronomètres de la simulation, ainsi que les messages d'erreur. 
    '''




    def __init__(self, fenêtre_main, controlleur):

        '''
        Cette méthode va créer la sous-fenêtre de l'interface graphique qui va contenir les graphiques de la simulation thermique.
        Elle va aussi initialiser l'état de certaines variables qui seront menées à évoluer et elle va initialiser le chronomètre de la simulation.
        '''



        self.fenêtre_main = fenêtre_main                                                    # Cette instance correspond à la fenêtre de droite de l'interface. Elle hérite de l'instance self.panneau_visu de la classe FenêtreInterface de interface.py
        self.controlleur = controlleur                                                      # Cette instance va permettre de contrôler la simulation en y stockant les informations, paramètres... En réalité , celle-ci sera un objet de la classe FenêtreInterface de interface.py et va donc hériter de l'ensemble des instances de cette classe.

        self.fenêtre = ttk.PanedWindow(fenêtre_main, orient=tk.VERTICAL)                    # Ici on divise verticalement la fenêtre principale (ici, c'est la fênetre  de droite) en 2
        self.fenêtre.pack(fill=tk.BOTH, expand=True)                                        # On empile les 2 sous-fenêtres l'une sur l'autre et on les remplit en fonction de la taille de la fenêtre principale (ici, on va remplir l'ensemble de la fenêtre principale)

   
        self.fenêtre_top = ttk.Frame(self.fenêtre)                                          # Sous-fenêtre du dessus                      
        self.fenêtre.add(self.fenêtre_top, weight=50)                                       # Qui va initialement correspondre à 50% en poids de la fenêtre initiale

        self.fenêtre_bottom = ttk.Frame(self.fenêtre)                                       # Sous-fenêtre du dessous
        self.fenêtre.add(self.fenêtre_bottom, weight=50)

        self.bc_carte_2D_top = None                                                         #Instances qui vont garder en mémoire la barre de couleur des graphiques. Utile pour être en mesure de réinitialiser celles-ci.
        self.bc_carte_3D_top = None
        self.bc_carte_2D_bottom = None
        self.bc_carte_3D_bottom = None
        
      
        self.animation1 = None                                                              #Instances qui vont contenir les animations. Animation1 va correspondre à la carte thermique 2D et animation2 à la carte thermique 3D.
        self.animation2 = None

        
        self.temps_ecoule_total = 0                                                         #Instances qui vont servir pour le chronomètre de la simulation.
        self.temps_debut_chrono = 0
      
        
        
        
        self.creer_graphiques()                                                             # On fait appel à la méthode creer_graphiques() de cette classe pour créer tous les graphiques possibles lors du lancement de l'interface.
        self.initialiser_graphique()                                                        # On fait appel à la méthode initialiser_graphique() de cette classe pour initialiser les graphiques et les mettre dans la bonne sous-fenêtre (haut ou bas).




    def creer_graphiques(self):
        '''
        Cette fonction va créer la mise en forme de chacun des graphiques.
        '''


        

        # Grahique/Figure de la carte 2D thermique
        self.figure_carte_2D = Figure(figsize=(6, 5), dpi=100)                                         #Création d'une figure matplotlib.figure de (6,5) pouces avec une résolution de 100 points par pouce 
        self.ax_carte_2D = self.figure_carte_2D.add_subplot(111)                                       #Création du graphique 
        self.ax_carte_2D.set_xlabel("Position Y")                                                      #On définit les axes
        self.ax_carte_2D.set_ylabel("Position X")
        self.ax_carte_2D.set_title("Simulation Thermique 2D")  
        self.canvas_carte_2D = FigureCanvasTkAgg(self.figure_carte_2D, master=self.fenêtre_top)        #La méthode FigureCanvasTkAgg permet d'intégrer des figures Matplotlib dans l'interface. Ici, on met cet objet dans fenêtre_top, donc pour la sous-fenêtre du haut.
    

        # On refait exactement la même chose pour la carte thermique 3D 
        self.figure_carte_3D = Figure(figsize=(6, 5), dpi=100)
        self.ax_carte_3D = self.figure_carte_3D.add_subplot(111, projection='3d')                      #Ici on précise  (projection = '3d') que c'est un graphique 3D qu'on veut
        self.ax_carte_3D.set_xlabel("Position X")
        self.ax_carte_3D.set_ylabel("Position Y")
        self.ax_carte_3D.set_zlabel("Simulation Thermique 3D")
        self.canvas_carte_3D = FigureCanvasTkAgg(self.figure_carte_3D, master=self.fenêtre_top)
    
        
        #Graphique pour l'évolution de la température des thermistances
        self.figure_temperature_therm = Figure(figsize=(6, 5), dpi=100)
        self.ax_temperature_therm = self.figure_temperature_therm.add_subplot(111)
        self.ax_temperature_therm.set_xlabel("Temps (s)")
        self.ax_temperature_therm.set_ylabel("Température (°C)")
        self.ax_temperature_therm.set_title("Évolution des températures")
        self.ax_temperature_therm.grid(True)
        self.canvas_température_therm = FigureCanvasTkAgg(self.figure_temperature_therm, master=self.fenêtre_bottom)
        

        #Graphique pour l'évolution de l'énergie interne
        self.figure_energie_int = Figure(figsize=(6, 5), dpi=100)
        self.ax_energie_int = self.figure_energie_int.add_subplot(111)
        self.ax_energie_int.set_xlabel("Temps (s)")
        self.ax_energie_int.set_ylabel("Énergie interne (J)")
        self.ax_energie_int.set_title("Évolution de l'énergie thermique interne")
        self.ax_energie_int.grid(True)
        self.canvas_energie_int = FigureCanvasTkAgg(self.figure_energie_int, master=self.fenêtre_bottom)




    def initialiser_graphique(self):
        '''
        Cette fonction sert à initialiser les graphiques et à mettre les graphiques choisis aux fenêtres appropriées.
        '''

        for widget in self.fenêtre_top.winfo_children():                                         #Avant d'initialiser les graphiques, il faut s'assurer que tous les objets dans les sous-fenêtre soit vidées. Ceci est une solution fournie par Claude Sonnet/ChatGPT pour éviter un problème d'affichage de plusieurs graphiques en même temps.
                widget.pack_forget()
        
        for widget in self.fenêtre_bottom.winfo_children():
                widget.pack_forget()
        

        self.graphique_selection(self.controlleur.graphique_top_select.get(), top=True)         # Ici, on appelle la méthode graphique_selection() pour afficher le graphique sélectionné par l'utilisateur dans la sous-fenêtre du haut (top=True).   
        self.graphique_selection(self.controlleur.graphique_bottom_selcet.get(), top=False)     # ...




    def graphique_selection(self, type_graphique,top=True):

        '''
        Cette méthode va permettre de sélectionner le graphique à afficher en fonction de la sélection de l'utilisateur.Elle prendra en argument le type de graphique à afficher et la sous-fenêtre dans laquelle on veut afficher le graphique (top ou bottom).
        '''
    
        if top:
            canvas_carte_2D = self.canvas_carte_2D
            canvas_carte_3D = self.canvas_carte_3D
        else:
            canvas_temp = self.canvas_température_therm
            canvas_energie = self.canvas_energie_int
        
        
        if type_graphique == "Carte Thermique 2D":                                              # Si l'utilisateur sélectionne ce cas
            canvas_carte_2D.get_tk_widget().pack(fill=tk.BOTH, expand=True)                     # On récupère le canvas associé à cette sélection (créer par la fonction créer_graphique).Maintenant, il faut insérer cet objet dans la fenêtre et pour cela on utilise la méthode pack()
            
        elif type_graphique == "Carte Thermique 3D":
            canvas_carte_3D.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        elif type_graphique == "Évolution Température":
            canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        elif type_graphique == "Énergie Interne":
            canvas_energie.get_tk_widget().pack(fill=tk.BOTH, expand=True)




    def reset_graphiques(self):

        '''
        Cette méthode va permettre de réinitialiser les graphiques avant de relancer la simulation.
        '''
       
        self.stop_animations()                                             # On arrête les animations en cours avant de réinitialiser les graphiques.



        if self.bc_carte_2D_top is not None:                            # Ceci est une solution de Claude Sonnet/ChatGPT pour afin de régler un problème d'affichage des barres de couleurs. En effet, lorsqu'on relançais la simulation, la barre de couleur restait affichée et lorsqu'on relançait la simulation, il y avait 2 barres de couleurs qui s'affichaient. Donc ici, on s'assure de supprimer la barre de couleur avant de relancer la simulation.

            self.bc_carte_2D_top.remove()
            self.bc_carte_2D_top = None                                 # On remet de force l'état de la barre de couleur à None.
        
        self.ax_carte_2D.clear()                                        # On vide le graphique
        self.ax_carte_2D.set_xlabel("Position Y")                       # et on redéfinit les axes
        self.ax_carte_2D.set_ylabel("Position X")
        self.ax_carte_2D.set_title("Simulation Thermique 2D")
        self.canvas_carte_2D.draw()                                     # Ici, on redessine le graphique pour qu'il soit vide. La méthode draw() de FigureCanvasTkAgg permet d'afficher le graphique. En effet, tant et aussi longtemeps que n'appelle pas cette méthode, le graphique ne s'affiche pas. Les modifications sont faites en mémoire mais pas affichées sinon.




        # On fait la même chose pour la carte thermique  3D
        for barre_color in self.figure_carte_3D.get_axes():             # Solution de Claude Sonnet/ChatGPT pour régler le problème d'affichage de la barre de couleur.
            if barre_color is not self.ax_carte_3D:  
                barre_color.remove()    



        self.bc_carte_3D_top = None
        self.ax_carte_3D.clear()                                        # On vide le graphique ...
        self.ax_carte_3D.set_xlabel("Position X")
        self.ax_carte_3D.set_ylabel("Position Y")
        self.ax_carte_3D.set_zlabel("Simulation Thermique 3D")
        self.canvas_carte_3D.draw()                                     # ... et on le redessine pour qu'il soit vide.

                                                 

        # On fait la même chose que pour les cartes thermiques, mais pour les graphiques de température et d'énergie interne.                           
        self.ax_temperature_therm.clear()
        self.ax_temperature_therm.set_xlabel("Temps (s)")
        self.ax_temperature_therm.set_ylabel("Température (°C)")
        self.ax_temperature_therm.set_title("Évolution des températures")
        self.ax_temperature_therm.grid(True)
        self.canvas_température_therm.draw()
            
        self.ax_energie_int.clear()
        self.ax_energie_int.set_xlabel("Temps (s)")
        self.ax_energie_int.set_ylabel("Énergie interne (J)")
        self.ax_energie_int.set_title("Évolution de l'énergie thermique interne")
        self.ax_energie_int.grid(True)
        self.canvas_energie_int.draw()
        




    def graph_temp(self):

        '''
        Cette méthode génère et stock les données qui seront affichées dans le graphique des températures des thermistances

        '''

        if not self.controlleur.temp_therm_1:                                                           #Cette première ligne permet de s'assurer que la liste de température est vide. Si c'est le cas, on ne fait rien et on sort de la fonction.
            return
        
        
        ax = self.ax_temperature_therm                                                                  # Ces changements de variables sert uniquement à alléger le code.
        canvas = self.canvas_température_therm
            
        ax.clear()                                                                                      #On s'assure de vider le contenu du graphique avant de le remplir à nouveau
        step = max(1, len(self.controlleur.temp_therm_1) // 1000)                                       # Ici , comme le pas de temps de la simulation est très petit (0.001), alors on veut pas forcément afficher tous les points de la simulation. Ici on décide de diviser le nombre de points par 1000
        temp1 = self.controlleur.temp_therm_1[::step]                                                   # On prend 1 point à chaque saut           
        temp2 = self.controlleur.temp_therm_2[::step]
        temp_laser = self.controlleur.temp_therm_laser[::step]
        times = [i * 0.001 for i in range(0, len(self.controlleur.temp_therm_1), step)]                 # Pour avoir une correspondance entre le temps et la température, on ajuste un vecteur temps en conséquence. Ici, 0.001 est en réalité la pas de temps de la simulation (dt).Comme on ne propose pas d'ajuster le pas de temps, alors on peut se permettre de directement prendre le pas de temps de 0.001s.
        
        ax.plot(times, temp1, 'r-', label='Thermistance 1')                                             #Courbe thermistance 1
        ax.plot(times, temp2, 'g--', label='Thermistance 2')                                            #Courbe thermistance 2
        ax.plot(times, temp_laser, 'b-.', label='Thermistance 3')                                   #Courbe thermistance 3
        
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Température (°C)")
        ax.set_title(f"Évolution des températures - Temps simulé: {self.controlleur.temps_courant:.2f} s")
        ax.legend()
        ax.grid(True)
        canvas.draw()                                                                                   # On actualise le contenu de canvas (ici, self.canvas_température_therm) pour afficher le graphique avec les nouvelles données.




    def graph_energie(self):

        '''
        Cette méthode est identique à la méthode graph_temp() mais pour l'énergie interne. Le code est une quasiment une copie de la méthode graph_temp().
        '''

        if not self.controlleur.energie_list:
            return
        
        
        ax = self.ax_energie_int
        canvas = self.canvas_energie_int
            
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
        Cette méthode va lancer les animations des graphiques en fonction de la sélection de l'utilisateur.

        '''
        try: 
            # On regarde voir s'il y a des éléments positionnés en dehors de la matrice de température. 
            # De plus ,on vérifie également si les temps sont cohérents entre eux.

            pos_ac_x = self.controlleur.var_pos_ac_x.get()
            pos_ac_y = self.controlleur.var_pos_ac_y.get()
            taille_ac_x = self.controlleur.var_nx_ac.get()
            taille_ac_y = self.controlleur.var_ny_ac.get()
            
            pos_pert_x = self.controlleur.var_pos_pert_x.get()
            pos_pert_y = self.controlleur.var_pos_pert_y.get()
            taille_pert_x = self.controlleur.var_nx_pert.get()
            taille_pert_y = self.controlleur.var_ny_pert.get()
            
            n_x = self.controlleur.var_n_x.get()
            n_y = self.controlleur.var_n_y.get()
            
           
            conditions = []
            conditions2 = []

            conditions.append(0 <= self.controlleur.var_pos_pert_x.get() <= self.controlleur.var_n_x.get())          # On vérifie que la position en x (verticale) de la perturbation est bien comprise entre 0 et la taille de la matrice de température (n_x).
            conditions.append(0 <= self.controlleur.var_pos_ac_x.get() <= self.controlleur.var_n_x.get())            # ... position centre actuateur
            conditions.append(0 <= self.controlleur.var_pos_therm1x.get() <= self.controlleur.var_n_x.get())         # ... position en x thermistance 1
            conditions.append(0 <= self.controlleur.var_pos_therm2x.get() <= self.controlleur.var_n_x.get())         # ... position en x thermistance 2
            conditions.append(0 <= self.controlleur.var_pos_therm3x.get() <= self.controlleur.var_n_x.get())         # ... position en x thermistance 3
            
            conditions.append(0 <= self.controlleur.var_pos_pert_y.get() <= self.controlleur.var_n_y.get())          # On vérifie que la position en y (horizontale) de la perturbation est bien comprise entre 0 et la taille de la matrice de température (n_y).
            conditions.append(0 <= self.controlleur.var_pos_ac_y.get() <= self.controlleur.var_n_y.get())            # ... position centre actuateur
            conditions.append(0 <= self.controlleur.var_pos_therm1y.get() <= self.controlleur.var_n_y.get())         # ... position en y thermistance 1
            conditions.append(0 <= self.controlleur.var_pos_therm2y.get() <= self.controlleur.var_n_y.get())         # ... position en y thermistance 2
            conditions.append(0 <= self.controlleur.var_pos_therm3y.get() <= self.controlleur.var_n_y.get())         # ... position en y thermistance 3
            conditions.append(0 <= pos_ac_x - taille_ac_x/2 <= n_x)                                                  
            conditions.append(0 <= pos_ac_y - taille_ac_y/2 <= n_y)
            conditions.append(0 <= pos_ac_x + taille_ac_x/2 <= n_x)
            conditions.append(0 <= pos_ac_y + taille_ac_y/2 <= n_y)
            conditions.append(0 <= pos_pert_x - taille_pert_x/2 <= n_x)
            conditions.append(0 <= pos_pert_y - taille_pert_y/2 <= n_y)
            conditions.append(0 <= pos_pert_x + taille_pert_x/2 <= n_x)
            conditions.append(0 <= pos_pert_y + taille_pert_y/2 <= n_y)

            # Ici on regarde si les temps sont cohérents entre eux.
            conditions2.append(self.controlleur.var_t_ac.get() >= 0)
            conditions2.append(self.controlleur.var_t_pert.get() >= 0)
            conditions2.append(self.controlleur.var_t_ac_end.get() >= 0)
            conditions2.append(self.controlleur.var_t_pert_end.get() >= 0)
            conditions2.append(self.controlleur.var_t_ac.get() <= self.controlleur.var_temps_simulation.get())
            conditions2.append(self.controlleur.var_t_ac_end.get() <= self.controlleur.var_temps_simulation.get())
            conditions2.append(self.controlleur.var_t_pert.get() <= self.controlleur.var_temps_simulation.get())
            conditions2.append(self.controlleur.var_t_pert_end.get() <= self.controlleur.var_temps_simulation.get())
            conditions2.append(self.controlleur.var_t_ac_end.get() >= self.controlleur.var_t_ac.get())
            conditions2.append(self.controlleur.var_t_pert_end.get() >= self.controlleur.var_t_pert.get())

            if all(conditions):
                pass
            else:
                messagebox.showinfo("Erreur de positionnement", 
                   "Certaines positions sont en dehors des limites permises.\n\n"
                   "Veuillez vérifier que toutes les coordonnées sont comprises entre 0 et les dimensions maximales du système (n_x , n_y) "
                   )

                return
            if all(conditions2):
                pass
            else:
                messagebox.showinfo("Erreur de temps",
                    "Les paramètres temporels de la simulation sont incohérents.\n\n"
                    "Veuillez vérifier que tous les temps sont positifs, que les temps de début sont inférieurs aux temps de fin correspondants, et que tous les temps sont compris dans la durée totale de simulation."
                )
                return
        except (AttributeError):
                pass

        
        # Si tout est correct, on lance les simulations en fonction de la sélection de l'utilisateur.
        if graph_top == "Carte Thermique 2D":          
            self.animation_2D_démarrer(T, params, top=True)
        elif graph_top == "Carte Thermique 3D":
            self.animation_3D_démarrer(T, params, top=True)
        if graph_bottom == "Évolution Température":
            self.graph_temp()
        elif graph_bottom == "Énergie Interne":
            self.graph_energie()
            



    def pause_animations(self):
        '''
        Fonction qui va permettre de mettre sur pause la simulation et le chronomètre.
        '''
    
        if self.animation1 :
            self.animation1.event_source.stop()                                         #Ici, self.animation est un objet FuncAnimation. Celui-ci possède un méthode event_source qui est un style de timer. 
                                                                                        #C'est ce timer qui appel à répétion la fonction update de FuncAnimation. event_source possède lui même une méthode .stop() qui permet d'arrêter ce timer et donc la fonction update n'est plus appelée.
        if self.animation2 :
            self.animation2.event_source.stop()

        if self.controlleur.chronometre_run:                                            # On arrête le chronomètre de la simulation.
            self.controlleur.chronometre_run = False        




    def poursuivre_animations(self):

        '''
        Cette méthode va être appeler lorsque l'utilisateur va appuyer de nouveau sur le bouton Reprendre. Ici, on permet à l'utilisateur 
        de changer les paramètres de la simulation pendant que la simulation est sur pause.
        '''
       
        params = self.controlleur.recup_params_sim()                                                    #Avant de relancer a simulation, on s'assurer de récupérer tous les paramètres. Cela va nous permettre de récolter les paramètres potentiellement modifiés par l'utilisateur. Il est important de rappeler que cette méthode est une méthode  définie dans la classe FenetreInterface de interface.py. dont self.controlleur est un objet.
        current_T = self.controlleur.T                                                                  # On récupère la matrice de température au temps où la simulation a été mise sur pause.
        graph_top = self.controlleur.graphique_top_select.get()   
        graph_bottom = self.controlleur.graphique_bottom_selcet.get()
        
        
        self.lancer_animations(current_T, params, graph_top, graph_bottom)                              #On redémarre la simulation avec les nouvelles variables , sélections et matrice de température.




    def stop_animations(self):

        '''
        Cette méthode va gérer l'arrêt de la simulation. Elle permet de changer l'état des instances animation1 et animation2.
        '''
        
        if self.animation1 is not None:                                         #Si l'état de l'animation n'est pas None (l'animation est en cours), alors on l'arrête.
            self.animation1.event_source.stop()
            self.animation1 = None                                              #On met l'état à None pour dire que l'animation est arrêtée.
        
    
        if self.animation2 is not None:
            self.animation2.event_source.stop()
            self.animation2 = None
        

        self.temps_debut_chrono = 0                                             # On remet le chronomètre à 0.
        self.temps_ecoule_total = 0                    
        
        




    def animation_2D_démarrer(self, T, params, top=True):
        '''
        Cette méthode va gérer l'animation de la carte thermique 2D. Elle va créer une animation de la carte thermique 2D en fonction des paramètres de la simulation et de la méthode
        simulation_thermique.vector_evolution_temperature du fichier simulation_temp.py. Elle prend en argument la matrice de température T et les paramètres de la simulation.
        '''


        
        # On récupère d'abord les positions des thermistances et les temps d'application des puissances. Cela va nous servir plus tard dans le code
        pos_t1x = self.controlleur.var_pos_therm1x.get() 
        pos_t1y = self.controlleur.var_pos_therm1y.get() 
        pos_t2x = self.controlleur.var_pos_therm2x.get() 
        pos_t2y = self.controlleur.var_pos_therm2y.get() 
        pos_t3x = self.controlleur.var_pos_therm3x.get() 
        pos_t3y = self.controlleur.var_pos_therm3y.get() 
        t_ac = params.get('t_ac')
        t_ac_end = params.get('t_ac_end', params['temps_simulation'])
        t_pert = params.get('t_pert')
        t_pert_end = params.get('t_pert_end', params['temps_simulation'])



        
        # Changement de variables pour alléger le code
        fig = self.figure_carte_2D                                                                                  # Ici, rappelons que fig est un objet de la classe Figure de matplotlib.figure.
        ax = self.ax_carte_2D                                                                                       # Alors que ax est un objet de la classe Axes de matplotlib.axes.
        canvas = self.canvas_carte_2D
        
            

        
            
        ax.clear()                                                                                                  # On vide le graphique avant de le remplir à nouveau
        
        # Initialisation de l'image
        temp_data = T                                                                                               # On initialise la matrice de température avec la matrice de température mise en argument de la fonction.
        carte_2D = ax.imshow(temp_data, cmap='hot', interpolation='nearest', origin='lower')                              # Initialisation de l'image  (la matrice de température) qui sera menée à évoluer au fur et à mesure de la simulation. 
                                                                                                                    #La méthode imshow() de matplotlib.pyplot permet d'afficher une image à partir d'une matrice. 
                                                                                                                    # Ici, on utilise la carte de couleur 'hot' (rouge, jaune, orange) pour représenter la température. On utilise aussi l'option interpolation='nearest' pour éviter le flou entre les pixels 
                                                                                                                    # et origin='lower' pour que l'origine soit en bas à gauche.
        
        
        for barre_color in fig.get_axes():                                                                          # Encore une fois, solution de Claude Sonnet/ChatGPT pour éviter le problème d'affichage de la barre de couleur.           
            if barre_color is not ax:  
                barre_color.remove()  

        
        ax.set_position([0.125, 0.1, 0.6, 0.8])                                                                     # Autre solution de Claude Sonnet/ChatGPT. On fixe la position de la carte thermique 2D pour éviter qu'elle ne bouge lorsque l'on relance la simulation.

        
        cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])                                                                  # Même chose ici, on fixe la postion de la barre de couleur pour éviter qu'elle se déplace elle aussi.
        colorbar = fig.colorbar(carte_2D, cax=cax)
        colorbar.set_label('Température (°C)')

        if top:
            self.bc_carte_2D_top = colorbar
        else:
            self.bc_carte_2D_bottom = colorbar
        
        ax.set_title("Simulation Thermique 2D")                                                                     # Comme on a vidé le graphique, il faut redéfinir le cadre du graphique.
        ax.set_xlabel("Position Y")
        ax.set_ylabel("Position X")
        ax.plot(pos_t1y, pos_t1x, 'yo', markersize=5, label="Thermistance 1")                                       # Ici, on offre la possibilité à l'utilisateur d'afficher sur la carte la position des thermistance via des points de couleur.
        ax.plot(pos_t2y, pos_t2x, 'go', markersize=5, label="Thermistance 2")
        ax.plot(pos_t3y, pos_t3x, 'bo', markersize=5, label="Thermistance 3")
        ax.legend(loc='upper right')
        

        def update(frame):
            '''
            Cette méthode va mettre à jour la matrice de température et l'afficher sur le graphique. Elle est appelée à chaque itération de l'animation via la méthode event_source de FuncAnimation.
            Elle va aussi gérer l'affichage de l'actuateur et des thermistances sur le graphique.
            '''

            # On vérifie d'abord si la simulation est en cours ou si le temps de simulation est dépassé. Si c'est le cas, on arrête l'animation et on affiche la matrice de température actuelle.
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
                    self.graph_temp()
                    self.graph_energie()
            

                # On met à jour l'image avec la  matrice de température
                temp_data = self.controlleur.T 
                carte_2D.set_data(temp_data)                                                                                                       # On met à jour l'image avec la matrice de température actuelle.
                
                # On dessine l'actuateur et la perturbation
                if self.controlleur.var_afficher_actuateur.get() :                             #Si l'utilisateur a coché la case pour afficher l'actuateur.                                
                    i, j = params['pos_ac']
                    nx, ny = params['nx_ac'], params['ny_ac']
                    rectangle_actu = plt.Rectangle((j - ny/2-1, i - nx/2-1), ny+2, nx+2, edgecolor='lime', facecolor='none', linewidth=2)    # On dessine un rectangle autour de l'actuateur.
                    ax.add_patch(rectangle_actu)                                                                                             # On ajoute le rectangle au graphique. La méthode add_patch() de matplotlib.pyplot permet d'ajouter un objet graphique sur la figure/graphique.                                                                                             
                    
                if self.controlleur.var_afficher_perturbation.get():
                    k, l = params['pos_pert']
                    nx, ny = params['nx_pert'], params['ny_pert']
                    rectangle_pert = plt.Rectangle((l - ny/2-1, k - nx/2-1), ny+2, nx+2, edgecolor='purple', facecolor='none', linewidth=2)
                    ax.add_patch(rectangle_pert)
                
            
                canvas.draw_idle()                                                                                                            # La méthode draw_idle() de FigureCanvasTkAgg permet de redessiner le graphique sans bloquer l'interface graphique.   
                return [carte_2D]                                                                                                                   # On retourne l'image sous forme de matrice.           
            
            
            # Si la simulation est en pause, on ne fait rien et on retourne l'image actuelle.
            if self.controlleur.simulation_paused:
                return [carte_2D]
            
            
            # Si la simulation est en cours, alors on poursouit l'animation.
        
            if self.controlleur.animation_on.get() == 'Activé':                                                                            # Si l'utilisateur active l'animation (il veut voir l'évolution de la simulation au fur et à mesure)
                
                iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get()))                                                # On récupère à quelle vitesse il veut l'animation. Ici, à chaque Frame, le nombre d'itération par frame va dépendre de la sélection de l'utilisateur.  
                
            else:                                                                                                                           # Si l'utilisateur désactive l'animation (il ne veut pas d'animation, mais juste les résultats)
                iterations = self.controlleur.var_Nt                                                                                        # Alors ,on fait toutes les itérations de la simulation en une seule frame !                                           
                temps_debut = time.time()                                                                                                   # Note important, comme le chronomètre sera mis sur pause lors des itérations, on va devoir le remettre à jour manuellement. Donc ici, on récupère le temps de début de la simulation pour le chronomètre dans le cas où on fait toutes les itérations d'un coup.
                

            
            

            # Ceci est la boucle principale de la simulation de la carte thermique 2D. Elle va mettre à jour la matrice de température via la méthode vector_evolution_temperature de la classe SimulationThermique.
            for _ in range(iterations):
                if self.controlleur.temps_courant >= params['temps_simulation']:                                                           #On regarde si le temps de simulation est dépassé. Si c'est le cas, on arrête l'animation et on affiche la matrice de température actuelle.
                    break
                
                params_actuels = params.copy()                                                                                             #On récupère les paramètres de la simulation actuel et on fait une copie pour s'assurer de ne pas modifier les paramètres d'origine.
                params_actuels['current_time'] = self.controlleur.temps_courant                                                            # On définit une variable current_time qui va nous permettre de savoir à quel temps on est dans la simulation.
            
                
                # On entre dans la méthode vector_evolution_temperature de la classe SimulationThermique avec les paramètres actuels.
                self.controlleur.T = self.controlleur.simulation_thermique.vector_evolution_temperature(
                    self.controlleur.T, params_actuels)
                
                
                # On répère les valeurs de température aux positions d'interêt (thermistance 1, thermistance 2, thermistance 3) et on les stocke dans des listes pour pouvoir les utiliser plus tard (pour les graphiques et la sauvegarde des données).
                temp1 = self.controlleur.T[pos_t1x, pos_t1y]                                                                               # Température thermistance 1
                temp2 = self.controlleur.T[pos_t2x, pos_t2y]                                                                               # Température thermistance 2                                         
                temp_laser = self.controlleur.T[pos_t3x, pos_t3y]                                                                          # Température thermistance 3                                
                
                #Comme on veut récolter les commandes de l'actuateur et de la perturbation à chaque itération pour le fichier de sauvegarde, 
                # on va devoir vérifier si la perturbation et l'actuateur sont activés à cet instant de la simulation et si oui aller récupérer la valeur
                temps_actuel = self.controlleur.temps_courant
                if t_ac <= temps_actuel <= t_ac_end:
                    commande_actuateur = self.controlleur.var_current.get()
                else:
                    commande_actuateur = 0.0
                if t_pert <= temps_actuel <= t_pert_end:
                    commande_perturbation = self.controlleur.var_P_pert.get()
                else:
                    commande_perturbation = 0.0
                                                                                                 
                

                # On ajout ces valeurs dans les listes de la classe FenetreInterface
                self.controlleur.temp_therm_1.append(temp1)                             
                self.controlleur.temp_therm_2.append(temp2)
                self.controlleur.temp_therm_laser.append(temp_laser)
                self.controlleur.commande_ac.append(commande_actuateur)
                self.controlleur.commande_pert.append(commande_perturbation)
                
        
                # Ici, on calcul l'énergie thermique interne à chaque itération pour faire le graphique de l'énergie interne.
                E_current = params['p'] * params['vol'] * params['cp'] * np.sum(self.controlleur.T+273.15)                                 # L'énergie interne est calculée en multipliant la masse (densité*volume) par la capacité thermique (cp) et par la somme de toutes les températures de la matrice de température (T) + 273.15 (pour passer de °C à K).  Ici , on a supposé que la masse volumique , la capacité thermique et le volume sont constants dans la matrice de température.
                self.controlleur.energie_list.append(E_current)
                
                
                self.controlleur.temps_courant += params['dt']                                                                             # On met à jour le temps courant de la simulation.                                                                           
            
            if self.controlleur.animation_on.get() == 'Désactivé':                                                                        # Si l'utilisateur désactive l'animation, alors on met à jour le chronomètre de la simulation pour voir combien de temps la simulation a durée.                                
                temps_fin = time.time()
                temps_ecoule = temps_fin - temps_debut
                minutes = int(temps_ecoule // 60)
                secondes = int(temps_ecoule % 60)
                millisecondes = int((temps_ecoule % 1) * 1000)
                self.controlleur.label_chrono.config(text=f"{minutes:02d}:{secondes:02d}:{millisecondes:03d}")                             # On modifie le texte du l'instance label_chrono de la classe FenetreInterface pour afficher le temps.
                self.controlleur.temps_ecoule_total = temps_ecoule                                                                         # On met à jour le temps écoulé total de la simulation.                             
            


            
            # On met à jour les graphiquesde température et d'énergie interne. Il est important de comprendre que c'est via les animations 2D et 3D qu'on génère les données pour les graphiques de température et d'énergie interne. On doit donc mettre à jour les graphiques ici.
            
            if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                self.graph_temp()
            elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                self.graph_energie()
            

            # On dessine les rectangles après les itérations.
            if self.controlleur.var_afficher_actuateur.get():
                i, j = params['pos_ac']
                nx, ny = params['nx_ac'], params['ny_ac']
                rectangle_actu = plt.Rectangle((j - ny/2-1, i - nx/2-1), ny+2, nx+2, edgecolor='lime', facecolor='none', linewidth=2)
                ax.add_patch(rectangle_actu)
                
            if self.controlleur.var_afficher_perturbation.get():
                k, l = params['pos_pert']
                nx, ny = params['nx_pert'], params['ny_pert']
                rectangle_pert = plt.Rectangle((l - ny/2-1, k - nx/2-1), ny+2, nx+2, edgecolor='purple', facecolor='none', linewidth=2)
                ax.add_patch(rectangle_pert)
        

            # On remet à jour la matrice de température après les itération pour la prochaine frame
            temp_data = self.controlleur.T 
            carte_2D.set_data(temp_data)
            
            # On remet à jour l'échelle de température. Cela permet d'avoir une échelle de température dynamique qui évolue en fonction du minimum et du maximum de la matrice de température.
            vmin = np.min(temp_data)
            vmax = np.max(temp_data)
            carte_2D.set_clim(vmin=vmin, vmax=vmax)
        
            ax.set_title(f"Simulation Thermique 2D - Temps: {self.controlleur.temps_courant:.2f} s")
            canvas.draw_idle()                                                                                                          # On redessine le graphique dans le canvas (ici, self.canvas_carte_2D)
            
            return [carte_2D]                                                                                                                 # On retourne finalement l'image sous forme de matrice.                                          
        
     
        self.animation1 = FuncAnimation(fig, update, frames=None, interval=5, blit=True, cache_frame_data=False)                        # VIP, c'est ici que l'animation est créée. On utilise la méthode FuncAnimation de matplotlib.animation pour créer l'animation. Cette méthode prend en argument la figure qui va être amenée à évoluer, la fonction de mise à jour, le nombre de frames, l'intervalle entre chaque frame et le mode de dessin (blit=True).                                                                                                       # On insère cette animation                     
                                                                                                                                        #Le blit permet d'optimiser le rendu de l'animation en ne redessinant que les parties de l'image qui ont changé).
                                                                                                                                        # On insère cette animation dans l'instance animation1 de la classe FenetreInterface.
    



    def animation_3D_démarrer(self, T, params, top=True):
        '''
        Cette méthode va gérer l'animation de la carte thermique 3D. Elle est quasi identique à la méthode animation_2D_démarrer() mais pour la carte thermique 3D. La différence principale est que l'on utilise la méthode plot_surface() de matplotlib pour afficher la carte thermique 3D au lieu de imshow().

        '''

        pos_t1x = self.controlleur.var_pos_therm1x.get() 
        pos_t1y = self.controlleur.var_pos_therm1y.get() 
        pos_t2x = self.controlleur.var_pos_therm2x.get() 
        pos_t2y = self.controlleur.var_pos_therm2y.get() 
        pos_t3x = self.controlleur.var_pos_therm3x.get() 
        pos_t3y = self.controlleur.var_pos_therm3y.get()
        t_ac = params.get('t_ac', 0)
        t_ac_end = params.get('t_ac_end', params['temps_simulation'])
        t_pert = params.get('t_pert', 0)
        t_pert_end = params.get('t_pert_end', params['temps_simulation'])

        
        fig = self.figure_carte_3D
        ax = self.ax_carte_3D
        canvas = self.canvas_carte_3D
        
        ax.set_position([0.125, 0.1, 0.6, 0.8])   
        ax.clear()
        x = np.linspace(0, params['Lx'], params['n_x'])
        y = np.linspace(0, params['Ly'], params['n_y'])
        X, Y = np.meshgrid(x, y)
        Z = T.T 
        
        vmin = Z.min()
        vmax = Z.max()
        
        carte_3D = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)

        
        
        cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])  
        colorbar = fig.colorbar(carte_3D, cax=cax)
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
                    self.graph_temp()
                    self.graph_energie()
                return
            
            # Vérifier si la simulation est en pause
            if self.controlleur.simulation_paused:
                return
            
            if top or (not top and self.animation1 is None):
                if self.controlleur.animation_on.get() == 'Activé':
                    iterations = max(1, int(100 * self.controlleur.var_vitesse_animation.get())) 
                else:  
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

                    temps_actuel = self.controlleur.temps_courant
            
                    if t_ac <= temps_actuel <= t_ac_end:
                        commande_actuateur = self.controlleur.var_current.get()
                    else:
                        commande_actuateur = 0.0

                    if t_pert <= temps_actuel <= t_pert_end:
                        commande_perturbation = self.controlleur.var_P_pert.get()
                    else:
                        commande_perturbation = 0.0
                    
                    self.controlleur.temp_therm_1.append(temp1)
                    self.controlleur.temp_therm_2.append(temp2)
                    self.controlleur.temp_therm_laser.append(temp_laser)
                    self.controlleur.commande_ac.append(commande_actuateur)
                    self.controlleur.commande_pert.append(commande_perturbation)
                    
                    
                    E_current = params['p'] * params['cp'] * np.sum(self.controlleur.T+273.15) * params['vol']
                    self.controlleur.energie_list.append(E_current)
                    
                    self.controlleur.temps_courant += params['dt']

                if self.controlleur.animation_on.get() == 'Désactivé':
                    temps_fin = time.time()
                    temps_ecoule = temps_fin - temps_debut
                    minutes = int(temps_ecoule // 60)
                    secondes = int(temps_ecoule % 60)
                    millisecondes = int((temps_ecoule % 1) * 1000)
                    self.controlleur.label_chrono.config(text=f"{minutes:02d}:{secondes:02d}:{millisecondes:03d}")
                    self.controlleur.f_interface.update() 
                    self.controlleur.temps_ecoule_total = temps_ecoule
                    
                    ax.clear()
                    Z = self.controlleur.T.T 
                    vmin = Z.min()
                    vmax = Z.max()
                    carte_3D = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
                    ax.set_title(f"Simulation Thermique 3D - Temps: {self.controlleur.temps_courant:.2f} s")
                    ax.set_xlabel("Position X (m)")
                    ax.set_ylabel("Position Y (m)")
                    ax.set_zlabel("Température (°C)")
                    
                    for barre_color in fig.get_axes():
                        if barre_color is not ax:
                            barre_color.remove()
                            
                    cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
                    colorbar = fig.colorbar(carte_3D, cax=cax)
                    colorbar.set_label('Température (°C)')
                    
                    if top:
                        self.bc_carte_3D_top = colorbar
                    else:
                        self.bc_carte_3D_bottom = colorbar
                        
                    canvas.draw()  
                    
                
                    
                if self.controlleur.graphique_bottom_selcet.get() == "Évolution Température":
                    self.graph_temp()
                elif self.controlleur.graphique_bottom_selcet.get() == "Énergie Interne":
                    self.graph_energie()
                
                ax.set_position([0.125, 0.1, 0.6, 0.8])
                ax.clear()
                Z = self.controlleur.T.T 
                
                vmin = Z.min()
                vmax = Z.max()
                
                carte_3D = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
                ax.set_title(f"Simulation Thermique 3D - Temps: {self.controlleur.temps_courant:.2f} s")
                ax.set_xlabel("Position X (m)")
                ax.set_ylabel("Position Y (m)")
                ax.set_zlabel("Température (°C)")
            
                for barre_color in fig.get_axes():
                    if barre_color is not ax:
                        barre_color.remove()

                cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
                colorbar = fig.colorbar(carte_3D, cax=cax)
                colorbar.set_label('Température (°C)')

                if top:
                    self.bc_carte_3D_top = colorbar
                else:
                    self.bc_carte_3D_bottom = colorbar
                        
                return carte_3D
        
        self.animation2= FuncAnimation(fig, update, frames=None, interval=5, blit=False, cache_frame_data=False)
        
        
        canvas.draw()