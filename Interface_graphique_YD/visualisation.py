import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk

# Classe fictive pour simuler le moteur de simulation (à remplacer par votre vraie implémentation)
class SimulationEngine:
    def initial_temperature(self):
        return np.ones((100, 100)) * 300  # Température initiale de 300 K (exemple)
    

class VisualisationManager:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.controller = controller
        
        # Diviser le panneau de visualisation en deux parties (haut/bas)
        self.vis_paned = ttk.PanedWindow(parent_frame, orient=tk.VERTICAL)
        self.vis_paned.pack(fill=tk.BOTH, expand=True)
        
        # Panneau supérieur pour le premier graphique
        self.top_graph_frame = ttk.Frame(self.vis_paned)
        self.vis_paned.add(self.top_graph_frame, weight=50)
        
        # Panneau inférieur pour le deuxième graphique
        self.bottom_graph_frame = ttk.Frame(self.vis_paned)
        self.vis_paned.add(self.bottom_graph_frame, weight=50)
        
        # Initialiser les références des barres de couleur
        self.cb_thermal_2d = None
        self.cb_thermal_3d = None
        self.cb_thermal_2d_bottom = None
        self.cb_thermal_3d_bottom = None
        
        # Créer tous les graphiques possibles
        self.create_all_graphs()
        
        # Initialiser les graphiques selon les sélections par défaut
        self.update_graph_display()
        
        # Objets pour les animations
        self.anim1 = None
        self.anim2 = None
        
    def create_all_graphs(self):
        """Crée tous les graphiques possibles (mais ne les affiche pas encore)"""
        # Figure pour la carte thermique 2D
        self.fig_thermal_2d = Figure(figsize=(6, 5), dpi=100)
        self.ax_thermal_2d = self.fig_thermal_2d.add_subplot(111)
        self.canvas_thermal_2d = FigureCanvasTkAgg(self.fig_thermal_2d, master=self.top_graph_frame)
        
        # Figure pour la carte thermique 3D
        self.fig_thermal_3d = Figure(figsize=(6, 5), dpi=100)
        self.ax_thermal_3d = self.fig_thermal_3d.add_subplot(111, projection='3d')
        self.canvas_thermal_3d = FigureCanvasTkAgg(self.fig_thermal_3d, master=self.top_graph_frame)
        
        # Figure pour le graphique de température
        self.fig_temp = Figure(figsize=(6, 5), dpi=100)
        self.ax_temp = self.fig_temp.add_subplot(111)
        self.ax_temp.set_xlabel("Temps (s)")
        self.ax_temp.set_ylabel("Température (°C)")
        self.ax_temp.set_title("Évolution des températures")
        self.ax_temp.grid(True)
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.top_graph_frame)
        
        # Figure pour le graphique d'énergie
        self.fig_energy = Figure(figsize=(6, 5), dpi=100)
        self.ax_energy = self.fig_energy.add_subplot(111)
        self.ax_energy.set_xlabel("Temps (s)")
        self.ax_energy.set_ylabel("Énergie interne (J)")
        self.ax_energy.set_title("Évolution de l'énergie interne")
        self.ax_energy.grid(True)
        self.canvas_energy = FigureCanvasTkAgg(self.fig_energy, master=self.top_graph_frame)
        
        # Faire de même pour le graphique du bas
        self.fig_thermal_2d_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_thermal_2d_bottom = self.fig_thermal_2d_bottom.add_subplot(111)
        self.canvas_thermal_2d_bottom = FigureCanvasTkAgg(self.fig_thermal_2d_bottom, master=self.bottom_graph_frame)
        
        self.fig_thermal_3d_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_thermal_3d_bottom = self.fig_thermal_3d_bottom.add_subplot(111, projection='3d')
        self.canvas_thermal_3d_bottom = FigureCanvasTkAgg(self.fig_thermal_3d_bottom, master=self.bottom_graph_frame)
        
        self.fig_temp_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_temp_bottom = self.fig_temp_bottom.add_subplot(111)
        self.ax_temp_bottom.set_xlabel("Temps (s)")
        self.ax_temp_bottom.set_ylabel("Température (°C)")
        self.ax_temp_bottom.set_title("Évolution des températures")
        self.ax_temp_bottom.grid(True)
        self.canvas_temp_bottom = FigureCanvasTkAgg(self.fig_temp_bottom, master=self.bottom_graph_frame)
        
        self.fig_energy_bottom = Figure(figsize=(6, 5), dpi=100)
        self.ax_energy_bottom = self.fig_energy_bottom.add_subplot(111)
        self.ax_energy_bottom.set_xlabel("Temps (s)")
        self.ax_energy_bottom.set_ylabel("Énergie interne (J)")
        self.ax_energy_bottom.set_title("Évolution de l'énergie interne")
        self.ax_energy_bottom.grid(True)
        self.canvas_energy_bottom = FigureCanvasTkAgg(self.fig_energy_bottom, master=self.bottom_graph_frame)
        
        # Ajouter un bouton pour mettre à jour les graphiques
        update_btn_frame = ttk.Frame(self.parent)
        update_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(update_btn_frame, text="Mettre à jour les graphiques", 
                  command=self.update_graph_display).pack(side=tk.RIGHT, padx=5, pady=5)
    
    def update_graph_display(self):
        """Met à jour les graphiques affichés selon les sélections de l'utilisateur"""
        for widget in self.top_graph_frame.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.pack_forget()
        
        for widget in self.bottom_graph_frame.winfo_children():
            if isinstance(widget, tk.Widget):
                widget.pack_forget()
        
        self.display_selected_graph(self.controller.selected_chart1.get(), self.top_graph_frame, is_top=True)
        self.display_selected_graph(self.controller.selected_chart2.get(), self.bottom_graph_frame, is_top=False)
    
    def display_selected_graph(self, chart_type, parent_frame, is_top=True):
        """Affiche le graphique sélectionné dans le cadre parent"""
        if is_top:
            thermal_2d_canvas = self.canvas_thermal_2d
            thermal_3d_canvas = self.canvas_thermal_3d
            temp_canvas = self.canvas_temp
            energy_canvas = self.canvas_energy
        else:
            thermal_2d_canvas = self.canvas_thermal_2d_bottom
            thermal_3d_canvas = self.canvas_thermal_3d_bottom
            temp_canvas = self.canvas_temp_bottom
            energy_canvas = self.canvas_energy_bottom
        
        if chart_type == "Carte Thermique 2D":
            thermal_2d_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(thermal_2d_canvas, parent_frame)
            toolbar.update()
            toolbar.pack(fill=tk.X)
        elif chart_type == "Carte Thermique 3D":
            thermal_3d_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(thermal_3d_canvas, parent_frame)
            toolbar.update()
            toolbar.pack(fill=tk.X)
        elif chart_type == "Évolution Température":
            temp_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(temp_canvas, parent_frame)
            toolbar.update()
            toolbar.pack(fill=tk.X)
        elif chart_type == "Énergie Interne":
            energy_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(energy_canvas, parent_frame)
            toolbar.update()
            toolbar.pack(fill=tk.X)
    
    def reset_graphs(self):
        """Réinitialise les graphiques actuellement sélectionnés"""
        self.stop_animations()

        graph_configs = {
            "Carte Thermique 2D": {
                "top": (self.ax_thermal_2d, self.canvas_thermal_2d, "cb_thermal_2d"),
                "bottom": (self.ax_thermal_2d_bottom, self.canvas_thermal_2d_bottom, "cb_thermal_2d_bottom")
            },
            "Carte Thermique 3D": {
                "top": (self.ax_thermal_3d, self.canvas_thermal_3d, "cb_thermal_3d"),
                "bottom": (self.ax_thermal_3d_bottom, self.canvas_thermal_3d_bottom, "cb_thermal_3d_bottom")
            },
            "Évolution Température": {
                "top": (self.ax_temp, self.canvas_temp, None),
                "bottom": (self.ax_temp_bottom, self.canvas_temp_bottom, None)
            },
            "Énergie Interne": {
                "top": (self.ax_energy, self.canvas_energy, None),
                "bottom": (self.ax_energy_bottom, self.canvas_energy_bottom, None)
            }
        }

        chart1 = self.controller.selected_chart1.get()
        chart2 = self.controller.selected_chart2.get()

        if chart1 in graph_configs:
            ax, canvas, cb_attr = graph_configs[chart1]["top"]
            if cb_attr:
                cb = getattr(self, cb_attr)
                if cb is not None:
                    try:
                        cb.remove()
                    except (KeyError, ValueError):
                        pass
                    setattr(self, cb_attr, None)
            ax.clear()
            if chart1 == "Évolution Température":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Température (°C)")
                ax.set_title("Évolution des températures")
                ax.grid(True)
            elif chart1 == "Énergie Interne":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Énergie interne (J)")
                ax.set_title("Évolution de l'énergie interne")
                ax.grid(True)
            canvas.draw()

        if chart2 in graph_configs:
            ax, canvas, cb_attr = graph_configs[chart2]["bottom"]
            if cb_attr:
                cb = getattr(self, cb_attr)
                if cb is not None:
                    try:
                        cb.remove()
                    except (KeyError, ValueError):
                        pass
                    setattr(self, cb_attr, None)
            ax.clear()
            if chart2 == "Évolution Température":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Température (°C)")
                ax.set_title("Évolution des températures")
                ax.grid(True)
            elif chart2 == "Énergie Interne":
                ax.set_xlabel("Temps (s)")
                ax.set_ylabel("Énergie interne (J)")
                ax.set_title("Évolution de l'énergie interne")
                ax.grid(True)
            canvas.draw()
    
    def update_temp_graph(self, is_top=True):
        if not self.controller.temp_therm_1:
            return
        if is_top:
            ax = self.ax_temp
            canvas = self.canvas_temp
        else:
            ax = self.ax_temp_bottom
            canvas = self.canvas_temp_bottom
            
        ax.clear()
        step = max(1, len(self.controller.temp_therm_1) // 1000)
        times = [i * 0.001 for i in range(0, len(self.controller.temp_therm_1), step)]
        temp1 = self.controller.temp_therm_1[::step]
        temp2 = self.controller.temp_therm_2[::step]
        temp_laser = self.controller.temp_therm_laser[::step]
        
        ax.plot(times, temp1, 'r-', label='Thermistance 1')
        ax.plot(times, temp2, 'g--', label='Thermistance 2')
        ax.plot(times, temp_laser, 'b-.', label='Position Laser')
        
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Température (°C)")
        ax.set_title(f"Évolution des températures - Temps simulé: {self.controller.current_time:.2f} s")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    def update_energy_graph(self, is_top=True):
        if not self.controller.energie_list:
            return
        if is_top:
            ax = self.ax_energy
            canvas = self.canvas_energy
        else:
            ax = self.ax_energy_bottom
            canvas = self.canvas_energy_bottom
            
        ax.clear()
        step = max(1, len(self.controller.energie_list) // 1000)
        times = [i * 0.001 for i in range(0, len(self.controller.energie_list), step)]
        energy = self.controller.energie_list[::step]
        
        ax.plot(times, energy, 'b-')
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Énergie interne (J)")
        ax.set_title(f"Évolution de l'énergie interne - Temps simulé: {self.controller.current_time:.2f} s")
        ax.grid(True)
        canvas.draw()
    
    def start_animations(self, T, params, chart1, chart2):
        self.start_animation(chart1, T, params, is_top=True)
        self.start_animation(chart2, T, params, is_top=False)
    
    def start_animation(self, chart_type, T, params, is_top=True):
        if chart_type == "Carte Thermique 2D":
            self.start_2d_animation(T, params, is_top)
        elif chart_type == "Carte Thermique 3D":
            self.start_3d_animation(T, params, is_top)
        elif chart_type == "Évolution Température":
            self.update_temp_graph(is_top)
        elif chart_type == "Énergie Interne":
            self.update_energy_graph(is_top)
    
    def stop_animations(self):
        if self.anim1:
            self.anim1.event_source.stop()
            self.anim1 = None
        if self.anim2:
            self.anim2.event_source.stop()
            self.anim2 = None
    
    def start_2d_animation(self, T, params, is_top=True):
        if is_top:
            fig = self.fig_thermal_2d
            ax = self.ax_thermal_2d
            canvas = self.canvas_thermal_2d
            anim_attr = 'anim1'
            cb_attr = 'cb_thermal_2d'
        else:
            fig = self.fig_thermal_2d_bottom
            ax = self.ax_thermal_2d_bottom
            canvas = self.canvas_thermal_2d_bottom
            anim_attr = 'anim2'
            cb_attr = 'cb_thermal_2d_bottom'
            
        ax.clear()
        vmin = self.controller.var_temperature_min.get()
        vmax = self.controller.var_temperature_max.get()
        
        im = ax.imshow(T - 273.15, cmap='hot', interpolation='nearest', origin='lower', vmin=vmin, vmax=vmax)
        
        if getattr(self, cb_attr) is None:
            cb = fig.colorbar(im, ax=ax, label='Température (°C)')
            setattr(self, cb_attr, cb)
        else:
            cb = getattr(self, cb_attr)
            cb.update_normal(im)
        
        ax.set_title("Simulation Thermique 2D")
        ax.set_xlabel("Position X")
        ax.set_ylabel("Position Y")
        
        if self.controller.var_show_actuator.get():
            i, j = params['pos_ac']
            nx, ny = params['nx_ac'], params['ny_ac']
            rect = plt.Rectangle((j - ny//2, i - nx//2), ny, nx, edgecolor='lime', facecolor='none', linewidth=2)
            ax.add_patch(rect)
            
        if self.controller.var_show_perturbation.get() and params['P_pert'] > 0:
            k, l = params['pos_pert']
            nx, ny = params['nx_pert'], params['ny_pert']
            rect = plt.Rectangle((l - ny//2, k - nx//2), ny, nx, edgecolor='cyan', facecolor='none', linewidth=2)
            ax.add_patch(rect)
            
        ax.plot(15, 30, 'ro', markersize=5, label="Thermistance 1")
        ax.plot(60, 30, 'go', markersize=5, label="Thermistance 2")
        ax.plot(105, 30, 'bo', markersize=5, label="Position Laser")
        ax.legend(loc='upper right')
        canvas.draw()
        
        def init():
            im.set_data(T - 273.15)
            return [im]
        
        def update(frame):
            if not self.controller.simulation_running or self.controller.current_time >= params['temps_simulation']:
                getattr(self, anim_attr).event_source.stop()
                if is_top:
                    self.controller.simulation_running = False
                    self.controller.status_var.set(f"Simulation terminée à {self.controller.current_time:.2f} s")
                    self.update_temp_graph(True)
                    self.update_temp_graph(False)
                    self.update_energy_graph(True)
                    self.update_energy_graph(False)
                return [im]
            
            if is_top:
                self.controller.frame_count += 1
                iterations = int(100 * self.controller.var_speed_factor.get())
                iterations = max(1, iterations)

                for _ in range(iterations):
                    self.controller.T = self.controller.simulation_engine.vector_evolution_temperature(
                        self.controller.T, params)
                    temp1 = self.controller.T[30, 15] - 273.15
                    temp2 = self.controller.T[30, 60] - 273.15
                    temp_laser = self.controller.T[30, 105] - 273.15
                    
                    self.controller.temp_therm_1.append(temp1)
                    self.controller.temp_therm_2.append(temp2)
                    self.controller.temp_therm_laser.append(temp_laser)
                    
                    E_current = params['p'] * params['cp'] * np.sum(self.controller.T) * params['vol']
                    self.controller.energie_list.append(E_current)
                    
                    self.controller.current_time += params['dt']
                
                if self.controller.selected_chart1.get() == "Évolution Température":
                    self.update_temp_graph(True)
                elif self.controller.selected_chart1.get() == "Énergie Interne":
                    self.update_energy_graph(True)
                    
                if self.controller.selected_chart2.get() == "Évolution Température":
                    self.update_temp_graph(False)
                elif self.controller.selected_chart2.get() == "Énergie Interne":
                    self.update_energy_graph(False)
                
                self.controller.status_var.set(f"Simulation en cours... Temps: {self.controller.current_time:.2f} s / {params['temps_simulation']:.2f} s")
            
            im.set_data(self.controller.T - 273.15)
            ax.set_title(f"Simulation Thermique 2D - Temps: {self.controller.current_time:.2f} s")
            cb.update_normal(im)
            return [im]
        
        anim = FuncAnimation(fig, update, init_func=init, frames=None, interval=50, blit=True)
        setattr(self, anim_attr, anim)
        canvas.draw()

    def start_3d_animation(self, T, params, is_top=True):
        if is_top:
            fig = self.fig_thermal_3d
            ax = self.ax_thermal_3d
            canvas = self.canvas_thermal_3d
            anim_attr = 'anim1'
            cb_attr = 'cb_thermal_3d'
        else:
            fig = self.fig_thermal_3d_bottom
            ax = self.ax_thermal_3d_bottom
            canvas = self.canvas_thermal_3d_bottom
            anim_attr = 'anim2'
            cb_attr = 'cb_thermal_3d_bottom'
            
        ax.clear()
        x = np.linspace(0, params['Lx'], params['n_x'])
        y = np.linspace(0, params['Ly'], params['n_y'])
        X, Y = np.meshgrid(x, y)
        Z = T.T - 273.15
        
        vmin = self.controller.var_temperature_min.get()
        vmax = self.controller.var_temperature_max.get()
        
        surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
        
        if getattr(self, cb_attr) is None:
            cb = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Température (°C)')
            setattr(self, cb_attr, cb)
        else:
            cb = getattr(self, cb_attr)
            cb.update_normal(surf)
        
        ax.set_title("Simulation Thermique 3D")
        ax.set_xlabel("Position X (m)")
        ax.set_ylabel("Position Y (m)")
        ax.set_zlabel("Température (°C)")
        canvas.draw()
        
        def update(frame):
            if not self.controller.simulation_running or self.controller.current_time >= params['temps_simulation']:
                getattr(self, anim_attr).event_source.stop()
                if is_top:
                    self.controller.simulation_running = False
                    self.controller.status_var.set(f"Simulation terminée à {self.controller.current_time:.2f} s")
                    self.update_temp_graph(True)
                    self.update_temp_graph(False)
                    self.update_energy_graph(True)
                    self.update_energy_graph(False)
                return
            
            if is_top:
                self.controller.frame_count += 1
                iterations = int(100 * self.controller.var_speed_factor.get())
                iterations = max(1, iterations)

                for _ in range(iterations):
                    self.controller.T = self.controller.simulation_engine.vector_evolution_temperature(
                        self.controller.T, params)
                    temp1 = self.controller.T[30, 15] - 273.15
                    temp2 = self.controller.T[30, 60] - 273.15
                    temp_laser = self.controller.T[30, 105] - 273.15
                    
                    self.controller.temp_therm_1.append(temp1)
                    self.controller.temp_therm_2.append(temp2)
                    self.controller.temp_therm_laser.append(temp_laser)
                    
                    E_current = params['p'] * params['cp'] * np.sum(self.controller.T) * params['vol']
                    self.controller.energie_list.append(E_current)
                    
                    self.controller.current_time += params['dt']
                
                if self.controller.selected_chart1.get() == "Évolution Température":
                    self.update_temp_graph(True)
                elif self.controller.selected_chart1.get() == "Énergie Interne":
                    self.update_energy_graph(True)
                    
                if self.controller.selected_chart2.get() == "Évolution Température":
                    self.update_temp_graph(False)
                elif self.controller.selected_chart2.get() == "Énergie Interne":
                    self.update_energy_graph(False)
                
                self.controller.status_var.set(f"Simulation en cours... Temps: {self.controller.current_time:.2f} s / {params['temps_simulation']:.2f} s")
            
            ax.clear()
            Z = self.controller.T.T - 273.15
            surf = ax.plot_surface(X, Y, Z, cmap='hot', vmin=vmin, vmax=vmax, rstride=2, cstride=2, linewidth=0, antialiased=False)
            ax.set_title(f"Simulation Thermique 3D - Temps: {self.controller.current_time:.2f} s")
            ax.set_xlabel("Position X (m)")
            ax.set_ylabel("Position Y (m)")
            ax.set_zlabel("Température (°C)")
            cb.update_normal(surf)
            return surf
        
        anim = FuncAnimation(fig, update, frames=None, interval=50, blit=False)
        setattr(self, anim_attr, anim)
        canvas.draw()

class SimulationInterface:
    def __init__(self, root):
        self.root = root
        self.simulation_running = False
        self.current_time = 0
        self.frame_count = 0
        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.T = None
        
        self.simulation_engine = SimulationEngine()
        self.vis_manager = VisualisationManager(self.root, self)
        
        self.selected_chart1 = tk.StringVar(value="Carte Thermique 2D")
        self.selected_chart2 = tk.StringVar(value="Évolution Température")
        self.status_var = tk.StringVar(value="Prêt")
        self.var_temperature_min = tk.DoubleVar(value=0)
        self.var_temperature_max = tk.DoubleVar(value=100)
        self.var_show_actuator = tk.BooleanVar(value=True)
        self.var_show_perturbation = tk.BooleanVar(value=True)
        self.var_speed_factor = tk.DoubleVar(value=1.0)
        
        self.create_interface()

    def create_interface(self):
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.create_control_panel()

    def create_control_panel(self):
        notebook = ttk.Notebook(self.control_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        sim_tab = ttk.Frame(notebook)
        notebook.add(sim_tab, text="Simulation")
        self.create_simulation_tab(sim_tab)

    def create_simulation_tab(self, tab):
        # Menu déroulant pour le graphique supérieur
        ttk.Label(tab, text="Graphique supérieur:").grid(row=0, column=0, padx=5, pady=5)
        chart1_menu = ttk.Combobox(tab, textvariable=self.selected_chart1, 
                                   values=["Carte Thermique 2D", "Carte Thermique 3D", 
                                           "Évolution Température", "Énergie Interne"])
        chart1_menu.grid(row=0, column=1, padx=5, pady=5)
        
        # Menu déroulant pour le graphique inférieur
        ttk.Label(tab, text="Graphique inférieur:").grid(row=1, column=0, padx=5, pady=5)
        chart2_menu = ttk.Combobox(tab, textvariable=self.selected_chart2, 
                                   values=["Carte Thermique 2D", "Carte Thermique 3D", 
                                           "Évolution Température", "Énergie Interne"])
        chart2_menu.grid(row=1, column=1, padx=5, pady=5)
        
        # Boutons de contrôle
        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Lancer la simulation", command=self.start_simulation).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Arrêter la simulation", command=self.stop_simulation).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Réinitialiser", command=self.reset_simulation).grid(row=0, column=2, padx=5)
        
        # Barre de statut
        ttk.Label(self.root, textvariable=self.status_var).pack(side=tk.BOTTOM, fill=tk.X)

    def start_simulation(self):
        if not self.simulation_running:
            self.temp_therm_1 = []
            self.temp_therm_2 = []
            self.temp_therm_laser = []
            self.energie_list = []
            self.current_time = 0
            self.frame_count = 0
            self.simulation_running = True
            
            self.T = self.simulation_engine.initial_temperature()
            params = self.get_simulation_params()
            
            chart1 = self.selected_chart1.get()
            chart2 = self.selected_chart2.get()
            self.vis_manager.start_animations(self.T, params, chart1, chart2)
            self.status_var.set("Simulation en cours...")

    def stop_simulation(self):
        self.simulation_running = False
        self.vis_manager.stop_animations()
        self.status_var.set(f"Simulation arrêtée à {self.current_time:.2f} s")

    def reset_simulation(self):
        self.stop_simulation()
        self.temp_therm_1 = []
        self.temp_therm_2 = []
        self.temp_therm_laser = []
        self.energie_list = []
        self.current_time = 0
        self.frame_count = 0
        self.vis_manager.reset_graphs()
        self.status_var.set("Simulation réinitialisée")

    def get_simulation_params(self):
        return {
            'pos_ac': (50, 50),
            'nx_ac': 10,
            'ny_ac': 10,
            'pos_pert': (20, 20),
            'nx_pert': 5,
            'ny_pert': 5,
            'P_pert': 0,
            'temps_simulation': 10.0,
            'dt': 0.001,
            'Lx': 1.0,
            'Ly': 1.0,
            'n_x': 100,
            'n_y': 100,
            'p': 1.0,
            'cp': 1.0,
            'vol': 1.0
        }

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulation Thermique")
    app = SimulationInterface(root)
    root.mainloop()