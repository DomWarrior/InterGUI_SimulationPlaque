import numpy as np
import matplotlib.pyplot as plt


def equProjectile(angle,G,Vinit,t):

    temps=np.linspace(0,t,1000)
    x=(Vinit*np.cos((angle*np.pi)/180))*temps
    Vy=(Vinit*np.sin((angle*np.pi)/180))
    y= (Vy*temps)-(0.5*(G*(temps**2)))

    return plt.plot(x,y), plt.show()

    
