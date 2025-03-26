import csv
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


with open('Simulation\Données Brutes\Test17.csv','r') as csv_files:
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
            Laser.append(float(i[4]))

        except: 
            pass
    csv_files.close()



plt.plot(temps[7:], Actu[7:])
plt.plot(temps[7:], T2[7:])
plt.plot(temps[7:], Laser[7:])
plt.show()
