'''
Ce fichier contient les fonctions permettant d'intégrer les fonctionnalités suivantes dans l'interface utilisateur:

-charger les paramètres d'une simulation à partir d'un fichier json
-sauvegarder les paramètres de simulation dans un fichier json
-sauvegarder les réponses en température des différentes thermistances dans un fichier txt
'''

import json


def charger_paramètres_json(fichier): # Fonction qui va permettre de lire un fichier json et de le charger
    with open(fichier, 'r') as f:
        return json.load(f)
    #code d'erreur à rajouter si le fichier n'est pas un json


def sauvegarder_paramètres_json(fichier, params): #Fonction qui va permettre d'écire dans un fichier json et de sauvegarder les paramètres
    with open(fichier, 'w') as f:
        json.dump(params, f, indent=2)


def sauvegarder_résultats_txt(fichier,times,commande_actuateur, commande_perturbation, temp1, temp2, temp_laser, energy): #Fonction qui va enregistrer les résultats des températures aux différents points d'intérêts en fonction du temps dans un fichier txt
    ET_tableau = (                                         #création de l'en-tête du tableau
        f"{'Temps (s)':<15}"
        f"{'Courant actuateur':<20}"
        f"{'Puissance perturbation':<30}"
        f"{'Temp. Thermistance 1 (°C)':<30}"
        f"{'Temp. Thermistance 2 (°C)':<30}"
        f"{'Temp. Thermistance 3 (°C)':<30}"
        f"{'Énergie Interne (J)':<20}\n"
    )

    with open (fichier, mode='w') as file:    #écriture du fichier 
        file.write(ET_tableau)                 #on commence par écrire l'en-tête

        for time,courant,puissance, t1, t2, tl, e in zip(times,commande_actuateur, commande_perturbation, temp1, temp2, temp_laser, energy):  # Ensuite on boucle sur les éléments des listes (times, temps 1...) et on rajoute/écrit ligne par ligne
            line = (
                f"{round(time,6):<15}"
                f"{round(courant,6):<20}"
                f"{round(puissance,6):<30}"
                f"{round(t1,6):<30}"
                f"{round(t2,6):<30}"
                f"{round(tl,6):<30}"
                f"{round(e,6):<20}\n"
            )
            file.write(line)