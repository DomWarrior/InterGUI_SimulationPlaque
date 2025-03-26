import json
import csv

def load_json_parameters(filename):
    """Charge des paramètres depuis un fichier JSON"""
    with open(filename, 'r') as f:
        return json.load(f)

def save_json_parameters(filename, params):
    """Sauvegarde des paramètres dans un fichier JSON"""
    with open(filename, 'w') as f:
        json.dump(params, f, indent=2)

def save_results_to_csv(filename, times, temp1, temp2, temp_laser, energy):
    """Sauvegarde les résultats dans un fichier CSV"""
    # Définition des en-têtes du fichier CSV
    fieldnames = ["Temps (s)", "Température Thermistance 1 (°C)", "Température Thermistance 2 (°C)", 
                 "Température Thermistance Laser (°C)", "Énergie Interne (J)"]

    # Écriture des données dans le fichier CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Écrire l'en-tête
        writer.writeheader()

        # Écrire les données ligne par ligne
        for time, t1, t2, tl, e in zip(times, temp1, temp2, temp_laser, energy):
            writer.writerow({
                "Temps (s)": time,
                "Température Thermistance 1 (°C)": t1,
                "Température Thermistance 2 (°C)": t2,
                "Température Thermistance Laser (°C)": tl,
                "Énergie Interne (J)": e
            })

def save_results_to_txt(filename, times, temp1, temp2, temp_laser, energy):
    """Sauvegarde les résultats dans un fichier TXT avec un format tabulaire"""
    # Définition des en-têtes
    header = (
        f"{'Temps (s)':<15}"
        f"{'Temp. Thermistance 1 (°C)':<30}"
        f"{'Temp. Thermistance 2 (°C)':<30}"
        f"{'Temp. Laser (°C)':<20}"
        f"{'Énergie Interne (J)':<20}\n"
    )
    
    # Ouverture du fichier en mode écriture
    with open(filename, mode='w') as file:
        # Écriture de l'en-tête
        file.write(header)
        
        # Écriture des données ligne par ligne
        for time, t1, t2, tl, e in zip(times, temp1, temp2, temp_laser, energy):
            line = (
                f"{round(time,6):<15}"
                f"{t1:<30}"
                f"{t2:<30}"
                f"{tl:<20}"
                f"{e:<20}\n"
            )
            file.write(line)
