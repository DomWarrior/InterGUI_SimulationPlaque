import csv
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


with open('Simulation\Données Brutes\Test11.csv','r') as csv_files:
    reader = csv.reader(csv_files, delimiter=';')

    temps = []
    Actu = []
    T2 = []
    Laser = []
    

    for i in reader:
        try:
            temps.append(float(i[0]))
            Actu.append(float(i[2]))
            T2.append(float(i[4]))
            Laser.append(float(i[6]))

        except: 
            pass
    csv_files.close()



plt.plot(temps[4:], Actu[4:])
plt.plot(temps[4:], T2[4:])
plt.plot(temps[4:], Laser[4:])
plt.show()
