import numpy as np

class SimulationEngine:
    def __init__(self):
        pass
        
    def vector_evolution_temperature(self, T, params):
        """Calcule l'évolution de la température pour un pas de temps"""
        T_new = T.copy()
        
        # Extraire le temps actuel si disponible, sinon utiliser 0
        current_time = params.get('current_time', 0)
        
        # Paramètres
        t_ac = params.get('t_ac', 0)     # Temps d'activation de l'actuateur
        t_pert = params.get('t_pert', 0)  # Temps d'activation de la perturbation
        
        a = params['a']
        dt = params['dt']
        dx = params['dx']
        dy = params['dy']
        dz = params['dz']
        vol = params['vol']
        h = params['h']
        T_air = params['T_air']
        p = params['p']
        cp = params['cp']
        couplage = params['couplage']
        
        pos_ac = params['pos_ac']
        nx_ac = params['nx_ac']
        ny_ac = params['ny_ac']
        P_ac = params['P_ac']
        
        pos_pert = params['pos_pert']
        nx_pert = params['nx_pert']
        ny_pert = params['ny_pert']
        P_pert = params['P_pert']

        # Conduction éléments centraux
        T_new[1:-1, 1:-1] = T[1:-1, 1:-1] + a*dt*((T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[0:-2, 1:-1])/(dy**2) +
                                            (T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, 0:-2])/(dx**2))
        
        # Conduction bords et coins (sans changement)
        T_new[0, 1:-1] += a * dt * ((T[1, 1:-1] - T[0, 1:-1]) / dy**2 +
                                (T[0, 2:] - 2 * T[0, 1:-1] + T[0, :-2]) / dx**2)
        
        T_new[-1, 1:-1] += a * dt * ((T[-2, 1:-1] - T[-1, 1:-1]) / dy**2 +
                                (T[-1, 2:] - 2 * T[-1, 1:-1] + T[-1, :-2]) / dx**2)
        
        T_new[1:-1, 0] += a * dt * ((T[2:, 0] - 2 * T[1:-1, 0] + T[:-2, 0]) / dy**2 +
                                (T[1:-1, 1] - T[1:-1, 0]) / dx**2)
        
        T_new[1:-1, -1] += a * dt * ((T[2:, -1] - 2 * T[1:-1, -1] + T[:-2, -1]) / dy**2 +
                                (T[1:-1, -2] - T[1:-1, -1]) / dx**2)
        
        # Coins
        T_new[0, 0] += a * dt * ((T[1, 0] - T[0, 0]) / dy**2 + (T[0, 1] - T[0, 0]) / dx**2)   
        T_new[0, -1] += a * dt * ((T[1, -1] - T[0, -1]) / dy**2 + (T[0, -2] - T[0, -1]) / dx**2) 
        T_new[-1, 0] += a * dt * ((T[-2, 0] - T[-1, 0]) / dy**2 + (T[-1, 1] - T[-1, 0]) / dx**2)   
        T_new[-1, -1] += a * dt * ((T[-2, -1] - T[-1, -1]) / dy**2 + (T[-1, -2] - T[-1, -1]) / dx**2)

        # Convection
        Coeff = (h*dt)/(p*cp)
        T_new[0, :] += 1*Coeff*(T_air-T[0,:])*((dz*dx)/(vol))     # haut
        T_new[-1, :] += 1*Coeff*(T_air-T[-1,:])*((dz*dx)/(vol))   # bas
        T_new[:,0] += 1*Coeff*(T_air-T[:,0])*((dz*dy)/(vol))      # gauche
        T_new[:,-1] += 1*Coeff*(T_air-T[:,-1])*((dz*dy)/(vol))    # droite
        T_new[:,:] += 2*Coeff*(T_air-T[:,:])*((dx*dy)/vol)        # dessus/dessous

        # Actuateur - Appliquer seulement si le temps actuel >= temps d'activation
        if P_ac is not None and current_time >= t_ac:
            i, j = pos_ac
            i_min = max(0, i - nx_ac//2)
            i_max = min(T.shape[0], i + nx_ac//2+1)
            j_min = max(0, j - ny_ac//2)
            j_max = min(T.shape[1], j + ny_ac//2+1)
            
            n_elements = (i_max - i_min) * (j_max - j_min)
            if n_elements > 0:
                P_par_element = (P_ac*couplage) / n_elements
                T_new[i_min:i_max, j_min:j_max] += (P_par_element*dt)/(p*cp*vol)

        # Perturbation - Appliquer seulement si le temps actuel >= temps d'activation
        if P_pert is not None and current_time >= t_pert:
            k, l = pos_pert
            k_min = max(0, k - nx_pert//2)
            k_max = min(T.shape[0], k + nx_pert//2)
            l_min = max(0, l - ny_pert//2)
            l_max = min(T.shape[1], l + ny_pert//2)
            
            n_elements = (k_max - k_min) * (l_max - l_min)
            if n_elements > 0:
                P_par_element = P_pert / n_elements
                T_new[k_min:k_max, l_min:l_max] += (P_par_element*dt)/(p*cp*vol)

        return T_new