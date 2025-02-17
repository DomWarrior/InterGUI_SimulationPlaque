import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import json
import tkinter
import csv


from Données_test_5 import Laser, T2, Actu, temps



# Charger les paramètres de simulation
with open('parametres_simulationYD.json', 'r') as f:
    params = json.load(f)

# Propriétés thermiques et physiques
k = params["proprietes_thermiques"]["k"]
p = params["proprietes_thermiques"]["p"]
cp = params["proprietes_thermiques"]["cp"]
Lx = params["dimensions_plaque"]["Lx"]
Ly = params["dimensions_plaque"]["Ly"]
e = params["dimensions_plaque"]["e"]

# Discrétisation
n_x = params["discretisation"]["n_x"]
n_y = params["discretisation"]["n_y"]
dx = Lx / n_x
dy = Ly / n_y
dz = e
vol = dx * dy * e

# Simulation
temps_simulation = len(temps[273:])*0.15
a = k / (cp * p)
dt = 0.001
Nt = int(temps_simulation / dt)

print(temps_simulation)
print(Nt)

# Paramètres actuateur
pos_ac = tuple(params["simulation"]["pos_ac"])
nx_ac = params["simulation"]["nx_ac"]
ny_ac = params["simulation"]["ny_ac"]
h = params["convection"]["h"]

# Fonction d'évolution de la température (DOIT RESTER IDENTIQUE)
def vector_evolution_temperature(T, h, pos_ac, nx_ac, ny_ac, P_ac=None,
                               P_pert=None, pos_pert=None, nx_pert=None, ny_pert=None):
    T_new = T.copy()

    # Conduction éléments centraux
    T_new[1:-1,1:-1] = T[1:-1, 1:-1] + a*dt*((T[2:,1:-1]-2*T[1:-1, 1:-1] +T[0:-2, 1:-1])/(dy**2) +
                                           (T[1:-1,2:]-2*T[1:-1, 1:-1] +T[1:-1, 0:-2])/(dx**2))
    
    # Conduction bords et coins
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
    T_new[0, :] += 1*Coeff*(T_air-T[0,:])*((dz*dx)/(vol))     # haut   #ici, j'ai mis un coefficient 1 parce que si je veux enlever la convection juste sur 1 cote, il me suffira juste de rempacer 1 par 0
    T_new[-1, :] += 1*Coeff*(T_air-T[-1,:])*((dz*dx)/(vol))   # bas
    T_new[:,0] += 1*Coeff*(T_air-T[:,0])*((dz*dy)/(vol))      # gauche
    T_new[:,-1] += 1*Coeff*(T_air-T[:,-1])*((dz*dy)/(vol))    # droite
    T_new[:,:] += 2*Coeff*(T_air-T[:,:])*((dx*dy)/vol)      # dessus/dessous  #ici, le coefficient doit etre a 2 si on veut que les 2 surfaces soient soumises a la convection

    # Actuateur
    if P_ac is not None:
        i, j = pos_ac
        P_par_element = P_ac/(nx_ac*ny_ac)
        T_new[i-nx_ac//2:i+nx_ac//2+1, j-ny_ac//2:j+ny_ac//2+1] += (P_par_element*dt)/(p*cp*vol)

    # Perturbation
    if P_pert is not None:
        k, l = pos_pert
        P_par_element = P_pert/(nx_pert*ny_pert)
        T_new[k-nx_pert//2:k+nx_pert//2, l-ny_pert//2:l+ny_pert//2] += (P_par_element*dt)/(p*cp*vol)

    return T_new


























T_ref = round(np.mean([Actu[273]]), 4)
T_air = T_ref
T_ref = np.ones((n_x, n_y))*(T_ref)

temp_therm_1_ref, temp_therm_2_ref, temp_therm_laser_ref = Actu[273:], T2[273:], Laser[273:] 







h_values = np.arange(12,12.89,0.1)
P_values = np.arange(1.55, 1.66, 0.025)
errors = []


for h in h_values:
    for P in P_values:
        T_test = T_ref
        temp_therm_1_test, temp_therm_2_test, temp_therm_laser_test = [], [], []
        print(f'Début simulation pour ({h}:{P})')

        for _ in range(Nt):
            T_test = vector_evolution_temperature(T_test, h, pos_ac, nx_ac, ny_ac, P)
            temp_therm_1_test.append(T_test[30, 15])
            temp_therm_2_test.append(T_test[30, 60])
            temp_therm_laser_test.append(T_test[30, 105])

        
        temp_therm_1_test = temp_therm_1_test[::150]
        temp_therm_2_test = temp_therm_2_test[::150]
        temp_therm_laser_test = temp_therm_laser_test[::150]

        error = np.sum((np.array(temp_therm_1_test) - np.array(temp_therm_1_ref))**2)
        errors.append(error)
        print(errors)
        print(f'Fin simulation pour ({h}:{P}), erreur = {error}')

        times = np.array(temps[273:])  # Utiliser les temps expérimentaux

        print(len(times), len(temp_therm_1_test), len(temp_therm_1_ref))

        plt.figure(figsize=(10, 5))

        # Thermistance 1
        plt.plot(times, temp_therm_1_ref, linestyle='-', color='r', label='Réf Thermistance 1')
        plt.plot(times, temp_therm_1_test, linestyle='--', color='r', 
         label=f'Test Thermistance 1')


        # Thermistance 2
        plt.plot(times, temp_therm_2_ref, linestyle='-', color='y', label='Réf Thermistance 2')
        plt.plot(times, temp_therm_2_test, linestyle='--', color='r', 
         label=f'Test Thermistance 2 ')


        # Thermistance 3
        plt.plot(times, temp_therm_laser_ref, linestyle='-', color='k', label='Réf Thermistance Laser')
        plt.plot(times, temp_therm_laser_test, linestyle='--', color='r', 
         label=f'Test Thermistance laser')


        plt.xlabel("Temps (s)")
        plt.ylabel("Température (°C)")
        plt.title("Comparaison des températures des thermistances")
        plt.legend()
        plt.grid(True)
        plt.show()


errors = np.array(errors).reshape(len(h_values), len(P_values))

i_opt, j_opt = np.unravel_index(np.argmin(errors), errors.shape)

Hp_optimal = (h_values[i_opt], P_values[j_opt])

T_best = T_ref
temp_therm_1_best, temp_therm_2_best, temp_therm_laser_best = [], [], []

for _ in range(Nt):
    T_best = vector_evolution_temperature(T_best, Hp_optimal[0], pos_ac, nx_ac, ny_ac, Hp_optimal[1])
    temp_therm_1_best.append(T_best[30, 15])
    temp_therm_2_best.append(T_best[30, 60])
    temp_therm_laser_best.append(T_best[30, 105])
    # Sous-échantillonner la simulation pour correspondre aux données expérimentales
    

temp_therm_1_best = temp_therm_1_best[::150]
temp_therm_2_best = temp_therm_2_best[::150]
temp_therm_laser_best = temp_therm_laser_best[::150]
# Définition correcte de l'axe des temps basé sur les mesures expérimentales



times = np.array(temps[273:])  # Utiliser les temps expérimentaux

print(len(times), len(temp_therm_1_best), len(temp_therm_1_ref))

plt.figure(figsize=(10, 5))

# Thermistance 1
plt.plot(times, temp_therm_1_ref, linestyle='-', color='r', label='Réf Thermistance 1')
plt.plot(times, temp_therm_1_best, linestyle='--', color='r', 
         label=f'Test Thermistance 1 (h={Hp_optimal[0]:.2f}, P={Hp_optimal[1]:.2f})')


plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Comparaison des températures des thermistances")
plt.legend()
plt.grid(True)
plt.show()
