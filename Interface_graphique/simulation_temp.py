import numpy as np


'''Ce fichier contient le code qui modélise la température de la plaque.
La modélisation prendre en compte la conduction, la convection, l'actuateur thermoélectrique et  une potentielle perturbation.

Afin de faciliter l'utilisation (ultérieurement pour l'interface graphique) de la fonction qui va contenir la modélisation de la température dans la plaque, on va
créer un objet (classe) qui représente directement l'évolution de la température dans la plaque '''


class TempératurePlaque:
    def __init__(self):
        pass                #rien à initialiser 

    def vector_evolution_temperature(self,T,params):       #Ici, T correspont à la matrice de température et params est une variable , qui est en réalité un fichier 
                                                    #json) qui va contenir l'ensemble des paramètres utiles pour la modélisation et qui va falloir extraire
        T_new = T.copy()                            #On crée une copie de T afin de travailler sur une copie de T 

        temps_actuel = params.get('current_time', 0)        #variable qui a été rajouté lorsque j'ai voulu rajouter l'option d'activer l'actuateur ou la perturbation à un temps autre que t=0 pour l'interface graphique 
        t_ac = params.get('t_ac', 0)
        t_ac_end = params.get('t_ac_end')         #t_ac_end est la fin de l'activation de l'actuateur (si on veut qu'il s'arrête à un moment donné)              
        t_pert = params.get('t_pert', 0)
        t_pert_end = params.get('t_pert_end')

        #création des paramètres
        a=params['a']                               #diffusivité thermique
        dt = params['dt']                           #pas de temps (s)
        dx = params['dx']                           #résolution en x (m)
        dy = params['dy']                           #résolution en y
        dz = params['dz']                           #résolution en épaisseur
        vol = params['vol']                         #volume (m^3)
        T_air = params['T_air']                     #température de l'air
        h = params['h']                             #coefficient de convection entre l'air et la plaque
        p = params['p']                             #densité du matériaux
        cp = params['cp']                           #capacité thermique massique du matériau 
        k = params['k']                             #conductivité thermique du matériau
        couplage = params['couplage']               #couplage thermique entre l'actuateur et la plaque
        current = params['I_ac']

        pos_ac = params['pos_ac']                   #position du centre de l'actuateur sur la plaque
        nx_ac = params['nx_ac']                     #largeur de l'actuateur en x (mm)
        ny_ac = params['ny_ac']                     #largeur de l'actuateur en y (mm)
                           
        pos_pert = params['pos_pert']               #largeur de l'actuateur en x (mm)
        nx_pert = params['nx_pert']                 #largeur de la perturbation appliquée en x (mm)
        ny_pert = params['ny_pert']                 #largeur de la perturbation appliquée en y (mm)
        P_pert = params['P_pert']                   #Puissance thermique de la perturbation (W)



        #Modélisation de la conduction

        #Conduction des éléments centraux
        T_new[1:-1, 1:-1] = T[1:-1, 1:-1] + a*dt*((T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[0:-2, 1:-1])/(dy**2) +
                                            (T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, 0:-2])/(dx**2))
        
        # Conduction bords (sans les coins)
        T_new[0, 1:-1] += a * dt * ((T[1, 1:-1] - T[0, 1:-1]) / dy**2 +
                                (T[0, 2:] - 2 * T[0, 1:-1] + T[0, :-2]) / dx**2)
        
        T_new[-1, 1:-1] += a * dt * ((T[-2, 1:-1] - T[-1, 1:-1]) / dy**2 +
                                (T[-1, 2:] - 2 * T[-1, 1:-1] + T[-1, :-2]) / dx**2)
        
        T_new[1:-1, 0] += a * dt * ((T[2:, 0] - 2 * T[1:-1, 0] + T[:-2, 0]) / dy**2 +
                                (T[1:-1, 1] - T[1:-1, 0]) / dx**2)
        
        T_new[1:-1, -1] += a * dt * ((T[2:, -1] - 2 * T[1:-1, -1] + T[:-2, -1]) / dy**2 +
                                (T[1:-1, -2] - T[1:-1, -1]) / dx**2)
        
        # Conduction pour les coins
        T_new[0, 0] += a * dt * ((T[1, 0] - T[0, 0]) / dy**2 + (T[0, 1] - T[0, 0]) / dx**2)   
        T_new[0, -1] += a * dt * ((T[1, -1] - T[0, -1]) / dy**2 + (T[0, -2] - T[0, -1]) / dx**2) 
        T_new[-1, 0] += a * dt * ((T[-2, 0] - T[-1, 0]) / dy**2 + (T[-1, 1] - T[-1, 0]) / dx**2)   
        T_new[-1, -1] += a * dt * ((T[-2, -1] - T[-1, -1]) / dy**2 + (T[-1, -2] - T[-1, -1]) / dx**2)





        # Modélisation de la convection sur toutes les surfaces de la plaque

        Coeff = (h*dt)/(p*cp)
        T_new[0, :] += 1*Coeff*(T_air-T[0,:])*((dz*dx)/(vol))     # haut de la plaque (vue du dessus de la plaque)
        T_new[-1, :] += 1*Coeff*(T_air-T[-1,:])*((dz*dx)/(vol))   # bas (vue du dessus de la plaque)
        T_new[:,0] += 1*Coeff*(T_air-T[:,0])*((dz*dy)/(vol))      # gauche (vue du dessus de la plaque)
        T_new[:,-1] += 1*Coeff*(T_air-T[:,-1])*((dz*dy)/(vol))    # droite (vue du dessus de la plaque)
        T_new[:,:] += 2*Coeff*(T_air-T[:,:])*((dx*dy)/vol)        # dessus/dessous





        # Modélisation de l'actuateur comme une entrée/sortie d'énergie du système plaque
        if current is not None and t_ac < temps_actuel <= t_ac_end:       # ici on a rajouter temps_actuel afin de pouvoir activer la puissance après un temps t par rapport au début de la simulation 
            i, j = pos_ac                                   #on positionne le centre de l'actuateur sur la plaque où i est la coordonnée verticale (y) et j la coordonnée horiontale (x)
            i_min = max(0, i - nx_ac//2)
            i_max = min(T.shape[0], i + nx_ac//2+1)         #ici j'ai rajouter +1 pour prendre en compte la largeur impair de l'actuateur
            j_min = max(0, j - ny_ac//2)                    # Les min et max ici est pour empêcher de positionner le centre de l'actuateur en dehors de la matrice de température et
            j_max = min(T.shape[1], j + ny_ac//2+1)
            
            n_elements = (i_max - i_min) * (j_max - j_min)      # correspond au nombre d'éléments représentant l'actuateur donc la surperficie de celui-ci
            if n_elements > 0:
                P_par_element = (current*couplage) / n_elements
                T_new[i_min:i_max, j_min:j_max] += (P_par_element*dt)/(p*cp*vol)

        # Modélisation de l'actuateur comme une entrée/sortie d'énergie du système plaque .... même modélisation que l'actuateur
        if P_pert is not None and t_pert < temps_actuel <= t_pert_end:
            k, l = pos_pert
            k_min = max(0, k - nx_pert//2)
            k_max = min(T.shape[0], k + nx_pert//2+1)
            l_min = max(0, l - ny_pert//2)
            l_max = min(T.shape[1], l + ny_pert//2+1)
            
            n_elements = (k_max - k_min) * (l_max - l_min)
            if n_elements > 0:
                P_par_element = P_pert / n_elements
                T_new[k_min:k_max, l_min:l_max] += (P_par_element*dt)/(p*cp*vol)

        return T_new

