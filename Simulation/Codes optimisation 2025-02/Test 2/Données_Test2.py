import csv
import numpy as np


with open('Simulation\Données Brutes\BONtest2.csv','r') as csv_files:
    reader = csv.reader(csv_files, delimiter=';')

    temps = []
    Actu = []
    T2 = []
    Laser = []
    

    for i in reader:
        try:
            temps.append(float(i[0]))
            Actu.append(float(i[3]))
            T2.append(float(i[4]))
            Laser.append(float(i[5]))

        except: 
            pass
    csv_files.close()

print(len(Actu))