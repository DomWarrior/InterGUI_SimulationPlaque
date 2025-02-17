import csv
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


with open('Simulation\Données Brutes\BONtestx1.csv','r') as csv_files:
    reader = csv.reader(csv_files, delimiter=';')

    temps = []
    Actu = []
    T2 = []
    Laser = []
    

    for i in reader:
        try:
            temps.append(float(i[0]))
            Actu.append(float(i[2]))
            T2.append(float(i[3]))
            Laser.append(float(i[5]))

        except: 
            pass
    csv_files.close()



plt.plot(temps[273:], Actu[273:])
plt.plot(temps[273:], T2[273:])
plt.plot(temps[273:], Laser[273:])
plt.show()
